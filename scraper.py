import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re
import os

URL = "https://www.ejobs.ro/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_job_count():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Find the element containing the text
        # We look for a wider container (div, span, p) that holds this text
        target_element = soup.find(lambda tag: tag.name in ["span", "div", "p", "h1", "h2"] and "locuri de muncă disponibile" in tag.text)
        
        if target_element:
            # Get all text from that element
            text = target_element.text.strip()
            
            # 2. THE FIX: Strict Regex
            # We look for digits ([\d\.]+) that are immediately followed by "\s*locuri de muncă"
            # \s* means "any amount of whitespace"
            match = re.search(r'([\d\.]+)\s*locuri de muncă', text)
            
            if match:
                # Extract the number part (Group 1)
                number_str = match.group(1).replace('.', '')
                return int(number_str)
            else:
                print(f"Found text but no matching number pattern. Text was: '{text[:100]}...'")
                return None
        
        print("Could not find the text 'locuri de muncă disponibile' on the page.")
        return None

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def save_to_csv(job_count):
    filename = 'ejobs_data.csv'
    today = datetime.now().strftime('%Y-%m-%d')
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Available Jobs'])
        writer.writerow([today, job_count])
    print(f"Success! Saved: {today} - {job_count} jobs")

if __name__ == "__main__":
    count = get_job_count()
    if count:
        save_to_csv(count)
