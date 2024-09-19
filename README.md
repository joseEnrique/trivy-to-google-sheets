# Trivy to Google Sheets

trivy-to-google-sheets is a Python package that automates running Trivy scans on container images and exporting the results to a Google Sheet. It also automatically shares the generated sheet with specified emails and can be used as a command-line tool.

## Features
Run a Trivy scan on a Docker container image.
- Export Trivy scan results directly to Google Sheets.
- Automatically create a new Google Sheet if it doesn't exist.
- Share the created Google Sheet with multiple users via email.
- Use the package via CLI for quick access.

## Installation

Install the package from PyPI:

```bash 
pip install trivy-to-google-sheets
```

## Usage
### Environment Variables

Before running the script or using the CLI tool, ensure the following environment variables are set:

- `GOOGLE_SHEETS_CREDS`: Path to your Google service account credentials JSON file.
- `WORKSHEET_NAME`: (Optional) Name of the Google Sheet worksheet (tab) where the data will be inserted. Default - `default-trivy-name`
- `SPREADSHEET_NAME`: (Optional) Name of the Google Sheet - Default -`trivy-vulnerabilities-spreadsheet`
- `SHARE_EMAILS`: Comma-separated list of emails to share the Google Sheet with.
  
#### Example

```bash
export GOOGLE_SHEETS_CREDS=/path/to/credentials.json
export WORKSHEET_NAME="vulnerability-scan"
export SHARE_EMAILS="email1@example.com,email2@example.com"

```

### Running the Script Programmatically

You can run the script directly in Python by initializing the `TrivyToGoogleSheets` class:

```python
from trivy_to_google_sheets import TrivyToGoogleSheets

# Initialize the process
trivy_gsheet = TrivyToGoogleSheets(image_name="your-container-image")
trivy_gsheet.run()

```
### Using as a Command-Line Tool

After installing the package, you can use the `trivy-to-google-sheets` command directly in your terminal.

```bash
trivy-to-google-sheets your-container-image
```

## Google Setup

To use this package, you need to set up the Google Sheets API and Google Drive API in your Google Cloud project. Follow the steps below to configure everything properly.

### Create a Google Cloud Project
1. Go to the Google Cloud Console.
2.  Create a new project:
    - Click on the project dropdown in the top navigation bar.
    - Click New Project.
    - Enter your Project Name and select your Billing Account (if applicable).
    - Click Create.
  
### Enable Google Sheets and Google Drive APIs

1. Enable the Google Sheets API:
    - Go to Google Sheets API Library.
    - Click Enable.
2. Enable the Google Drive API:
    - Go to Google Drive API Library.
    - Click Enable.

### Create a Service Account

1. Go to APIs & Services > Credentials in the left sidebar.
2. Click Create Credentials and choose Service Account.
3. Fill in the service account details:
    - Name: e.g., trivy-to-google-sheets-service-account.
    - Role: Choose Editor or Owner (this allows the service account to create and edit spreadsheets).
4. Click Done.
5. After creating the service account, under the Keys tab, click Add Key > Create New Key.
    - Choose JSON and download the file. This is your credentials file.


### Set the Service Account Credentials Path
Once you have the JSON file, set the path to it in your environment variables:

```bash
export GOOGLE_SHEETS_CREDS=/path/to/your/service-account-key.json
```


### Share Spreadsheet with Multiple Emails

If your script needs to share the Google Sheets with multiple people, you can set the `SHARE_EMAILS` environment variable with a comma-separated list of emails:

```bash
export SHARE_EMAILS="email1@example.com,email2@example.com"
```