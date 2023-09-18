**# FortifyCI with Jira Intrgation
A unified script that Integrate Fortify SAST with remote scanning for all CIs with Jira Integration. 

**Prerequisites**
1. Install Scancentral client and export to the environment path
2. Install FCLI and export to the environment path 
3. Install FortifyBugtrackerutility 
4. Install Python 3
5. Install PIP
6. Install Python package python-decouple
**Configuration**
1. Create a .env file in the same directory as your script.
2. Add all necessary configurations to the .env file. For example:
SSC_URL=your_ssc_url
SSC_TOKEN=your_ssc_token
...

Running the Script
Navigate to the directory containing the script.
Run the script using Python
python your_script_name.py


Certainly! Here's the README.md content for your script:

markdown
Copy code
# FortifyCI with Jira Integration

A unified script that integrates Fortify SAST with remote scanning for all CIs and provides Jira Integration.

## Prerequisites

Before you can run the script, ensure you have the following prerequisites set up:

1. **Scancentral Client**: Install the Scancentral client and ensure it's added to your environment path.
2. **FCLI**: Install the Fortify Command Line Interface (FCLI) and ensure it's added to your environment path.
3. **FortifyBugtrackerutility**: Install the Fortify Bug Tracker Utility.
4. **Python**: Ensure you have Python 3 installed.
5. **PIP**: Ensure you have PIP installed.
6. **Python Decouple**: Install the `python-decouple` package using PIP:
   pip install python-decouple
   
**Configuration**
Create a .env file in the same directory as your script.
Add all necessary configurations to the .env file. For example:
makefile
Copy code
SSC_URL=your_ssc_url
SSC_TOKEN=your_ssc_token
...

**Running the Script**
Navigate to the directory containing the script.
Run the script using Python:
bash
Copy code
python your_script_name.py

**Understanding the Script**
The script performs the following steps:
Fetches configuration values from the .env file.
Creates a package using Scancentral.
Logs in to SSC and SC-SAST.
Starts a SAST scan using FCLI and retrieves the job token.
Monitors the scan status until completion.
Waits for Fortify SSC to process the scan results.
Uploads issues to Jira.
Queries the application using FCLI to get the count of issues based on severity.
Check the issue counts against predefined limits to determine if the build obtains security clearance.

**Troubleshooting**
Ensure all prerequisites are correctly installed and paths are set.
Ensure the .env file contains all the necessary configurations and is located in the same directory as the script.
Check the error messages printed by the script for more specific troubleshooting steps.
**
