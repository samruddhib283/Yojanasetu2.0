import requests
from bs4 import BeautifulSoup
import mysql.connector

def scrape_goi_schemes():
    url = "https://en.wikipedia.org/wiki/List_of_schemes_of_the_government_of_India"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table", {"class": "wikitable"})

    schemes = []

    for table in tables:
        rows = table.find_all("tr")[1:]  # Skip header
        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) >= 6:
                name = cols[0].text.strip()
                cs_css = cols[1].text.strip()
                ministry = cols[2].text.strip()
                launch_year = cols[3].text.strip()
                sector = cols[4].text.strip()
                summary = cols[5].text.strip()
                link_tag = cols[0].find("a")
                wiki_link = "https://en.wikipedia.org" + link_tag.get("href") if link_tag else ""

                schemes.append((name, cs_css, ministry, launch_year, sector, summary, wiki_link))

    return schemes

def save_to_db(schemes):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="student@172005",
        database="schemes"
    )
    cursor = conn.cursor()

    for scheme in schemes:
        cursor.execute("""
            INSERT INTO schemes 
            (name, cs_css, ministry, launch_year, sector, summary, wiki_link)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, scheme)

    conn.commit()
    cursor.close()
    conn.close()

# Run this to scrape and save
schemes_data = scrape_goi_schemes()
save_to_db(schemes_data)





