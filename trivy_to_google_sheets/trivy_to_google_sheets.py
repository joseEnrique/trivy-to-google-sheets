import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime  # Import datetime to add current date

class TrivyToGoogleSheets:
    def __init__(self, image_name):
        self.image_name = image_name
        self.creds_path = os.getenv('GOOGLE_SHEETS_CREDS')
        self.spreadsheet_name = os.getenv('SPREADSHEET_NAME', 'trivy-vulnerabilities')  # Spreadsheet name
        self.worksheet_name = os.getenv('WORKSHEET_NAME', 'default-tab-name')  # Worksheet/tab name
        self.share_emails = os.getenv('SHARE_EMAILS')  # Optional

        if not self.creds_path or not self.spreadsheet_name or not self.worksheet_name:
            raise EnvironmentError("GOOGLE_SHEETS_CREDS, SPREADSHEET_NAME, and WORKSHEET_NAME environment variables must be set.")
        
        if self.share_emails:
            self.email_list = [email.strip() for email in self.share_emails.split(",")]

        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_path, self.scope)

    def run_trivy(self):
        import subprocess
        import json
        trivy_command = f"trivy image -f json {self.image_name}"
        process = subprocess.Popen(trivy_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        if process.returncode != 0:
            print(f"Error running Trivy: {err.decode()}")
            return None

        return json.loads(out.decode())

    def push_to_google_sheets(self, data):
        client = gspread.authorize(self.creds)

        # Try to open the spreadsheet, create if it doesn't exist
        try:
            spreadsheet = client.open(self.spreadsheet_name)  # Use the environment variable for spreadsheet name
        except gspread.SpreadsheetNotFound:
            print(f"Spreadsheet '{self.spreadsheet_name}' not found. Creating a new one.")
            spreadsheet_id = self.create_spreadsheet()
            spreadsheet = client.open_by_key(spreadsheet_id)
            if self.share_emails:
                self.share_spreadsheet(spreadsheet_id)

        try:
            sheet = spreadsheet.worksheet(self.worksheet_name)  # Use the environment variable for worksheet/tab name
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title=self.worksheet_name, rows="100", cols="20")

        # Prepare data with date
        headers = ["Target", "Vulnerability ID", "Pkg Name", "Installed Version", "Fixed Version", "Severity", "Description", "Date"]  # Add "Date" header
        current_date = datetime.now().strftime("%Y-%m-%d")  # Get the current date

        rows = [headers] + [
            [
                vuln.get("Target", ""),
                vuln.get("VulnerabilityID", ""),
                vuln.get("PkgName", ""),
                vuln.get("InstalledVersion", ""),
                vuln.get("FixedVersion", "N/A"),
                vuln.get("Severity", ""),
                vuln.get("Description", ""),
                current_date  # Add the current date to each row
            ] for result in data.get('Results', []) for vuln in result.get('Vulnerabilities', [])
        ]

        # Clear the existing data and insert the new data
        sheet.clear()
        for row in rows:
            sheet.append_row(row)

        print(f"Data successfully pushed to Google Sheets with the current date!")

    def create_spreadsheet(self):
        service = build('sheets', 'v4', credentials=self.creds)
        spreadsheet = {
            'properties': {
                'title': self.spreadsheet_name  # Use the environment variable for the spreadsheet name
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        return spreadsheet.get('spreadsheetId')

    def share_spreadsheet(self, spreadsheet_id):
        if self.share_emails:
            drive_service = build('drive', 'v3', credentials=self.creds)
            for email in self.email_list:
                permission = {
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': email
                }
                drive_service.permissions().create(fileId=spreadsheet_id, body=permission, fields='id').execute()
            print(f"Spreadsheet shared with: {', '.join(self.email_list)}")
        else:
            print("No emails provided to share the spreadsheet.")

    def run(self):
        trivy_data = self.run_trivy()
        if trivy_data:
            self.push_to_google_sheets(trivy_data)
        else:
            print("No data to push to Google Sheets.")

# Main function to allow execution from command line
def main():
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Trivy scan and export results to Google Sheets.")
    parser.add_argument("image_name", help="The name of the container image to scan.")
    args = parser.parse_args()

    # Run the TrivyToGoogleSheets process
    trivy_gsheet = TrivyToGoogleSheets(image_name=args.image_name)
    trivy_gsheet.run()

if __name__ == "__main__":
    main()
