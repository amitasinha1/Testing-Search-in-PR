from github import Github
import os
import json

# Access GitHub-specific context variables
github_token = os.environ['GITHUB_TOKEN']
repository = os.environ['GITHUB_REPOSITORY']
event_path = os.environ['GITHUB_EVENT_PATH']
keywords = ["mfa_type", "password", "first_initial", "first_name", "full_name", "initials_only","last_name", "middle_name", "preferred_name", "profile_name", "chime_sign", "biometric_information", "account_balance", "bank_identification_number", "bin_number", "cardholder_name", "cav2","cvc2", "cvv2", "cid", "expiration_date", "merchant_address", "merchant_name", "merchant_url", "pan_last_4", "pin_blocks", "service_code", "vendor_id", "partner_id", "android_advertising_id", "apple_identifier_for_advertiser_id", "full_ip_address", "google_advertising_id", "imei_number", "imsi_number", "isp_provider", "mac_address", "email_address", "email_domain", "personal_website_url", "area_code", "phone_number", "academic_record", "degrees_of_schooling", "gross_income", "credit_score", "income", "drivers_license", "social_security_number", "ssn", "passport_number", "state_id", "tax_identification_number", "genetic_data", "health_info", "city", "country", "county", "address", "geo_location", "province", "state", "street", "zipcode", "age", "birth_month", "criminal_convictions", "date_of_birth", "disability_status", "ethnic_group", "gender", "nationality", "number_of_children", "pronouns", "race", "year_of_birth", "employer_name", "employment_type", "payment_reference_number", "bank_account_number", "ach_account_number", "device_id"]
keywords_found = []
print(event_path,"1 step")
# Split the repository name into owner and repo name
owner, repo_name = repository.split('/')
print(owner, repo_name,"2 step")

# Create a GitHub instance
g = Github(github_token)
print(g, "3 step")

def check_keywords_in_pr_diff(repo, pr_number, keywords):
    pr = repo.get_pull(pr_number)
    print( pr, "7 step")
    diff = pr.get_files()
    print(diff, "8 step")

    for file in diff:
        file_content = repo.get_contents(file.filename, ref=pr.head.ref).decoded_content.decode('utf-8')
        print(file_content, "9 step")
        for keyword in keywords:
            if keyword.lower() in file_content.lower():
                keywords_found.append(keyword)
    if len(keywords_found) > 0:
        raise Exception(f"PII Field(s) '{keywords_found}' found in PR #{pr_number} diff.")
            

# Load the event data from the event path
with open(event_path) as event_file:
    event_data = json.load(event_file)
    print(event_data, "4 step")
    pr_number = event_data['number']
    print(pr_number, "5 step")

# Get the GitHub repository object
repo = g.get_repo(f"{owner}/{repo_name}")
print(repo, "6 step")

check_keywords_in_pr_diff(repo, pr_number, keywords)
