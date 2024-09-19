from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="trivy-to-google-sheets",  # Replace with your package name
    version="0.1.0",
    author="Quique Ruiz",
    author_email="joseenriqueruiznavarro@gmail.com",
    description="A tool to run Trivy scans and export results to Google Sheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joseEnrique/trivy-to-google-sheets",  # Replace with your GitHub URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'gspread>=5.7.1',
        'oauth2client>=4.1.3',
        'google-api-python-client>=2.92.0',
    ],
    entry_points={
        'console_scripts': [
            'trivy-to-google-sheets=trivy_to_google_sheets.trivy_to_google_sheets:main',
        ],
    },
)
