import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re
import os

# 1. Setup the target URL and headers (to look like a real browser)
URL = "https://www.ejobs.ro/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_job_count():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status() # Check for connection errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Find the element containing the specific text
        # We look for any HTML tag that contains the text "locuri de muncă disponibile"
        target_element = soup.find(lambda tag: tag.name == "span" and "locuri de muncă disponibile" in tag.text)
        
        if not target_element:
            # Fallback: try finding it in a div if span fails
            target_element = soup.find(lambda tag: tag.name == "div" and "locuri de muncă disponibile" in tag.text)

        if target_element:
            text = target_element.text.strip()
            # 3. Extract just the numbers (e.g., "10.318" -> 10318)
            # We look for digits, possibly separated by dots
            match = re.search(r'([\d\.]+)', text)
            if match:
                # Remove the dot to make it a pure integer
                number_str = match.group(1).replace('.', '')
                return int(number_str)
        
        print("Could not find the specific text on the page.")
        return None

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def save_to_csv(job_count):
    filename = 'ejobs_data.csv'
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Check if file exists to write headers
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Available Jobs'])
        
        writer.writerow([today, job_count])
    print(f"Saved: {today} - {job_count} jobs")

if __name__ == "__main__":
    count = get_job_count()
    if count:
        save_to_csv(count)
