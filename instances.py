import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import re
import time

@dataclass
class Scholarship:
    organization: str
    phone_number: str
    email: str
    level_of_study: str
    award_type: str
    purpose: str
    focus: str
    GPA: float
    qualifications: str
    criteria: str
    duration: str
    to_apply: str
    more_information: str
    deadline: str = None

def fetch_scholarship_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 202:
            # Retry with exponential backoff
            max_retries = 5
            retry_delay = 1
            for retry_count in range(max_retries):
                print(f"Received status code 202. Retrying (attempt {retry_count + 1})...")
                time.sleep(retry_delay)
                response = requests.get(url, headers=headers)
                if response.status_code != 202:
                    break
                retry_delay *= 2  # Exponential backoff

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract scholarship information from the HTML
            organization_tag = soup.find("td", string="Organization")
            organization = organization_tag.find_next_sibling("td").text.strip() if organization_tag else None
            phone_number_tag = soup.find("td", string="Phone Number")
            phone_number = phone_number_tag.find_next_sibling("td").text.strip() if phone_number_tag else None
            email_tag = soup.find("td", string="Emails")
            email = email_tag.find_next_sibling("td").text.strip() if email_tag and email_tag.find_next_sibling("td") else None
            level_of_study_tag = soup.find("td", string="Level of Study")
            level_of_study = level_of_study_tag.find_next_sibling("td").text.strip() if level_of_study_tag else None
            award_type_tag = soup.find("td", string="Award Type")
            award_type = award_type_tag.find_next_sibling("td").text.strip() if award_type_tag else None
            purpose_tag = soup.find("td", string="Purpose")
            purpose = purpose_tag.find_next_sibling("td").text.strip() if purpose_tag else None
            focus_tag = soup.find("td", string="Focus")
            focus = focus_tag.find_next_sibling("td").text.strip() if focus_tag else None
            qualifications_tag = soup.find("td", string="Qualifications")
            qualifications = qualifications_tag.find_next_sibling("td").text.strip() if qualifications_tag else None
            # Search for GPA in qualifications and extract the number
            GPA_match = re.search(r'(\d+(\.\d+)?) GPA', qualifications) if qualifications else None
            GPA = float(GPA_match.group(1)) if GPA_match else None
            criteria_tag = soup.find("td", string="Criteria")
            criteria = criteria_tag.find_next_sibling("td").text.strip() if criteria_tag else None
            duration_tag = soup.find("td", string="Duration")
            duration = duration_tag.find_next_sibling("td").text.strip() if duration_tag else None
            to_apply_tag = soup.find("td", string="To Apply")
            to_apply = to_apply_tag.find_next_sibling("td").text.strip() if to_apply_tag else None
            more_information_tag = soup.find("td", string="For more information")
            more_information = more_information_tag.find_next_sibling("td").text.strip() if more_information_tag else None
            deadline_tag = soup.find("td", string="Deadline")
            deadline = deadline_tag.find_next_sibling("td").text.strip() if deadline_tag else None
            # Initialize Scholarship object with extracted details
            scholarship = Scholarship(organization, phone_number, email, level_of_study, award_type, purpose, focus, GPA, qualifications, criteria, duration, to_apply, more_information, deadline)
            return scholarship
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def main():
    # Read URLs from text file
    with open("text", "r") as file:
        urls = file.read().splitlines()

    # Fetch scholarship information for each URL
    scholarships = []
    for url in urls:
        scholarship_info = fetch_scholarship_info(url)
        if scholarship_info:
            scholarships.append(scholarship_info)
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print(scholarships)
        else:
            print(f"Failed to fetch scholarship information for URL: {url}")

    # Write scholarship instances to a new file
    print(scholarships)

if __name__ == "__main__":
    main()
