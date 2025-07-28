import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_car_culture(year):
    url = f"https://hotwheels.fandom.com/wiki/{year}_Car_Culture"
    print(f"🌐 Scraping {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = []
    tables = soup.find_all('table', class_='wikitable')
    line_type = "Car Culture"

    for table in tables:
        # Ambil heading sebelumnya (misal: "Japan Historics", "Euro Style", etc.)
        series_heading = table.find_previous(['h2', 'h3'])
        series = series_heading.text.strip() if series_heading else 'Unknown'

        for tr in table.find_all('tr')[1:]:  # Skip header
            cols = tr.find_all('td')
            if len(cols) >= 8:
                toy_num = cols[0].text.strip()
                series_num = cols[1].text.strip()
                model = cols[2].text.strip()

                # Photo Carded ada di kolom ke-7 (index 7)
                img_tag = cols[7].find('img')
                photo_url = ''
                if img_tag:
                    photo_url = img_tag.get('data-src') or img_tag.get('src') or ''

                rows.append([
                    toy_num,
                    model,
                    series,
                    series_num,
                    photo_url,
                    line_type,
                    year
                ])
    
    print(f"🕵️ {len(rows)} baris ditemukan untuk tahun {year}")
    return rows

# ⏱ Loop multi-year
all_rows = []
for year in range(2016, 2026):
    try:
        all_rows.extend(scrape_car_culture(year))
        time.sleep(1)  # jeda biar ga di-rate limit
    except Exception as e:
        print(f"❌ Gagal scraping {year}: {e}")

# 💾 Simpan CSV
with open('hotwheels_car_culture_2016_2025.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['toy_num', 'model', 'series', 'series_num', 'photo_url', 'line_type', 'year'])
    writer.writerows(all_rows)

print("✅ Selesai! Data tersimpan di hotwheels_car_culture_2016_2025.csv")
