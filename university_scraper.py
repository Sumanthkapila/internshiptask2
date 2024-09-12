from bs4 import BeautifulSoup
import requests
import json
import os

# Function to extract information from a single university page
def extract_university_data(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract university name
    name = soup.find('h1').text.strip()

    # Extract university logo URL
    logo_url = soup.find('img', alt='University Logo')['src']

    # Extract university type
    type = soup.find('td', text='Type').find_next_sibling('td').text.strip()

    # Extract university founded year
    founded_year = soup.find('td', text='Founded').find_next_sibling('td').text.strip()

    # Extract university location
    location = {
        'country': soup.find('td', text='Country').find_next_sibling('td').text.strip(),
        'state': soup.find('td', text='State').find_next_sibling('td').text.strip(),
        'city': soup.find('td', text='City').find_next_sibling('td').text.strip(),
    }

    # Extract university contact information
    contact = {}
    for link in soup.find_all('a', href=True):
        if 'facebook' in link['href']:
            contact['facebook'] = link['href']
        elif 'twitter' in link['href']:
            contact['twitter'] = link['href']
        elif 'instagram' in link['href']:
            contact['instagram'] = link['href']
        elif 'linkedin' in link['href']:
            contact['linkedin'] = link['href']
        elif 'youtube' in link['href']:
            contact['youtube'] = link['href']

    # Extract university official website URL
    contact['official_website'] = soup.find('td', text='Website').find_next_sibling('td').find('a')['href']

    # Create dictionary with extracted data
    university_data = {
        'name': name,
        'logoSrc': logo_url,
        'type': type,
        'establishedYear': founded_year,
        'location': location,
        'contact': contact
    }

    return university_data

# Get all university URLs from the main website
main_url = "https://www.4icu.org/de/universities/"
response = requests.get(main_url)
response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')
university_urls = [a['href'] for a in soup.find_all('a', href=True) if 'university' in a['href']]

# Create a directory to store the JSON files
if not os.path.exists('university_data'):
    os.makedirs('university_data')

# Extract and save data for each university
for url in university_urls:
    university_data = extract_university_data(url)
    with open(f"university_data/{university_data['name']}.json", 'w', encoding='utf-8') as f:
        json.dump(university_data, f, indent=4)

print("Data extraction complete!")