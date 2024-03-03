import requests
from bs4 import BeautifulSoup
import certifi
myList = []
def fetch_scholarship_links(base_url, total_pages):
    # Define headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Iterate over the range of pages
    for page in range(1, total_pages + 1):
        # Construct the URL for the current page
        page_url = f"{base_url}&curPage={page}"

        # Attempt to fetch the content of the URL
        try:
            response = requests.get(page_url, headers=headers, verify=certifi.where())

            # Check if the request was successful
            if response.status_code == 200:
                # Initialize BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all the 'a' elements with class 'detailPageLink' within the 'thAN' header
                scholarship_links = soup.select('div.notranslate.detailPageLink a')
                #print(scholarship_links)

                # Extract and print each scholarship link
                for link in scholarship_links:
                    href = link['href']
                    full_link = f"https://www.careeronestop.org{href}"
                    myList.append(full_link)
                    print(full_link)
            else:
                print(f"Failed to fetch the webpage. Status code: {response.status_code}")
                print(f"Response text: {response.text}")

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

# Base URL to scrape (without the page number)
base_url = "https://www.careeronestop.org/Toolkit/Training/find-scholarships.aspx?"

# Total number of pages to scrape
total_pages = 582  # Adjust the number based on the actual number of pages

# Call the function with the base URL and total pages
fetch_scholarship_links(base_url, total_pages)
with open('TEXT', 'w') as file:
    # Iterate over each item in the list
    for item in myList:
        # Write the item to the file followed by a newline character
        file.write(item + '\n')

