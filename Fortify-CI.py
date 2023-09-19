import subprocess
import time
import re
from decouple import config

# Fetching values from .env
ssc_url = config('SSC_URL')
ssc_token = config('SSC_TOKEN')
ssc_sast_secret = config('SSC_SAST_SECRET')
ssc_appversion_id = config('SSC_APPVERSION_ID')
fortify_bug_utility_path = config('FORTIFY_UTILITY_PATH')
fortify_bug_config_file = config('FORTIFY_CONFIG_FILE')
fcli_path = config('FCLI_PATH')
scancentral_path = config('SCANCENTRAL_PATH')
ssc_username = config('SSC_USERNAME')
ssc_password = config('SSC_PASSWORD')
ssc_appname = config('SSC_APPNAME')
ssc_appversion_name = config('SSC_APPVERSION_NAME')
jira_url = config('JIRA_URL')
jira_username = config('JIRA_USERNAME')
jira_password = config('JIRA_PASSWORD')
jira_project_key = config('JIRA_PROJECT_KEY')
code_package=config('SCANCENTRAL_PACKAGE_O')
build_tool=config('SCANCENTRAL_PACKAGE_BT')
sensor_version=config('SSC_SENSOR_VERSION')
critical_issues_limit = int(config('CRITICAL_ISSUES_LIMIT'))
high_issues_limit = int(config('HIGH_ISSUES_LIMIT'))
medium_issues_limit = int(config('MEDIUM_ISSUES_LIMIT'))
low_issues_limit = int(config('LOW_ISSUES_LIMIT'))

'''
# Start by creating the package
try:
    
    subprocess.run([scancentral_path, "package", "-bt", build_tool, "-o", code_package], shell=True, check=True)
except subprocess.CalledProcessError:
    print("Package creation failed using Scancentral")
    exit(1)
'''
# Login to SSC
try:
    subprocess.run([fcli_path, "ssc", "session", "login", "--url", ssc_url, "-t", ssc_token], shell=True, check=True)
except subprocess.CalledProcessError:
    print("Failed to login to SSC using FCLI")
    exit(1)    
# Login to SC-SAST
try:
    subprocess.run([fcli_path, "sc-sast", "session", "login", "--ssc-url", ssc_url, "-c", ssc_sast_secret, "-t", ssc_token], shell=True, check=True)
except subprocess.CalledProcessError:
    print("Failed to login to Scancentral SAST using FCLI")
    exit(1)  
# Upload the Package and retrieve the job token
try:

    job_output = subprocess.check_output([fcli_path, "sc-sast", "scan", "start", "--upload", "--appversion", ssc_appversion_id, "-p", code_package, "--sensor-version", sensor_version], shell=True).decode()
except subprocess.CalledProcessError:
    print("Failed to start a SAST scan using FCLI")
    exit(1)  

# Extract the job token using regex
job_token_search = re.search(r"^\s*([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})", job_output, re.M)
job_token = job_token_search.group(1) if job_token_search else None
print("Fortify Scan Job Token:"+job_token)

#job_token= "381b4724-01de-45b2-878c-17774bd22ee6"
while True:
    # Check the status of the job
    scan_status_output = subprocess.check_output([fcli_path, "sc-sast", "scan", "status", job_token], shell=True).decode()
   
    # Extract statuses using regex
    lines = scan_status_output.strip().split("\n")

    header_line = lines[0]
    value_line = lines[1]

# Getting the start index for each column based on header positions
    scan_state_start = header_line.index("Scan state")
    ssc_upload_state_start = header_line.index("Ssc upload state")
    ssc_processing_state_start = header_line.index("Ssc processing state")

# Extracting the values using the start indices
    scan_state = value_line[scan_state_start:scan_state_start + len("Scan state")].strip()
    ssc_upload_state = value_line[ssc_upload_state_start:ssc_upload_state_start + len("Ssc upload state")].strip()
    ssc_processing_state = value_line[ssc_processing_state_start:ssc_processing_state_start + len("Ssc processing state")].strip()

    print("Scan state:", scan_state)

    if scan_state == "COMPLETED":
        print (job_token + "is processing is completed")
        break
    time.sleep(10)

# Wait an additional 30 seconds for SSC processing
print("Waiting for Fortify SSC to process the scan results")
time.sleep(30)

# Upload issues to Jira

try:

    subprocess.run(["java", "-jar",fortify_bug_utility_path, "-configFile", fortify_bug_config_file, "-SSCBaseUrl", ssc_url, "-SSCUserName", ssc_username, "-SSCPassword", ssc_password, "-SSCApplicationVersionNamePatterns", f"{ssc_appname}:{ssc_appversion_name}", "-JiraBaseUrl", jira_url, "-JiraUserName", jira_username, "-JiraPassword", jira_password, "-JiraProjectKey", jira_project_key], shell=True, check=True)
except subprocess.CalledProcessError:
    print("Failed to execute jira integration with SSC")
    exit(1) 

print("Issues have been updated to Jira Bugtracker")

# Query the application using FCLI
app_query = subprocess.check_output([fcli_path, "ssc", "appversion-vuln", "count", "--appversion", ssc_appversion_id], shell=True).decode()

# Extract issues count for each severity
critical_issues_count_search = re.search(r"Critical\s+(\d+)", app_query)
high_issues_count_search = re.search(r"High\s+(\d+)", app_query)
medium_issues_count_search = re.search(r"Medium\s+(\d+)", app_query)
low_issues_count_search = re.search(r"Low\s+(\d+)", app_query)

critical_issues_count = int(critical_issues_count_search.group(1)) if critical_issues_count_search else 0
high_issues_count = int(high_issues_count_search.group(1)) if high_issues_count_search else 0
medium_issues_count = int(medium_issues_count_search.group(1)) if medium_issues_count_search else 0
low_issues_count = int(low_issues_count_search.group(1)) if low_issues_count_search else 0

# Check against limits
if (critical_issues_count >= critical_issues_limit or
    high_issues_count >= high_issues_limit or
    medium_issues_count >= medium_issues_limit or
    low_issues_count >= low_issues_limit):
    
    print("Build failed to obtain security clearance due to exceeded issue limits.")
    print(app_query)
    exit(1)
else:
    print("Security clearance obtained successfully.")
    exit(0)

 
