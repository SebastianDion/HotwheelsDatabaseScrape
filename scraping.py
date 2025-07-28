import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_hotwheels(year):
    url = f"https://hotwheels.fandom.com/wiki/List_of_{year}_Hot_Wheels"
    print(f"🌐 Scraping {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = []
    tables = soup.find_all('table', class_='wikitable')

    for table in tables:
        for tr in table.find_all('tr')[1:]:  # Skip header
            cols = tr.find_all('td')
            if len(cols) >= 6:
                toy_num = cols[0].text.strip()
                col_num = cols[1].text.strip()
                model = cols[2].text.strip()
                series = cols[3].text.strip()
                series_num = cols[4].text.strip()
                img_tag = cols[5].find('img')
                photo_url = ''
                if img_tag:
                    photo_url = img_tag.get('data-src') or img_tag.get('src') or ''

                
                rows.append([
                    toy_num,
                    col_num,
                    model,
                    series,
                    series_num,
                    photo_url,
                    year
                ])
    
    print(f"🕵️ {len(rows)} baris ditemukan untuk tahun {year}")
    return rows

# Change range year sesuai kebutuhan
all_rows = []

for year in range(2020, 2026):
    try:
        all_rows.extend(scrape_hotwheels(year))
        time.sleep(1)
    except Exception as e:
        print(f"❌ Gagal scraping {year}: {e}")

# Simpan ke CSV
with open('hotwheels_2020_2025.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['toy_num', 'col_num', 'model', 'series', 'series_num', 'photo_url', 'year'])
    writer.writerows(all_rows)

print("✅ Selesai! Data tersimpan di hotwheels_2020_2025.csv")
