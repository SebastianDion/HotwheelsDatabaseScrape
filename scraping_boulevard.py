import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_boulevard(year):
    url = f"https://hotwheels.fandom.com/wiki/{year}_Hot_Wheels_Boulevard"
    print(f"🌐 Scraping {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = []
    tables = soup.find_all('table', class_='wikitable')
    line_type = "Boulevard"

    for table in tables:
        # Ambil heading sebelumnya (misal: "Japan Historics", "Euro Style", etc.)
        series_heading = table.find_previous(['h2', 'h3'])
        series = series_heading.text.strip() if series_heading else 'Unknown'

        for tr in table.find_all('tr')[1:]:  # Skip header
            cols = tr.find_all('td')

            try:
                if year >= 2020 and len(cols) >= 8:
                    toy_num = cols[0].text.strip()
                    series_num = cols[1].text.strip()
                    model = cols[2].text.strip()
                    img_tag = cols[7].find('img')
                elif year < 2020 and len(cols) >= 6:
                    toy_num = cols[0].text.strip()
                    series_num = ''
                    model = cols[1].text.strip()
                    img_tag = cols[5].find('img')
                else:
                    continue  #

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
            except Exception as e:
                print(f"⚠️ Error parsing baris: {e}")
    
    print(f"🕵️ {len(rows)} baris ditemukan untuk tahun {year}")
    return rows

# ⏱ Loop multi-year
all_rows = []
for year in range(2012, 2026):
    try:
        all_rows.extend(scrape_boulevard(year))
        time.sleep(1)  # jeda biar ga di-rate limit
    except Exception as e:
        print(f"❌ Gagal scraping {year}: {e}")

# 💾 Simpan CSV
filename = 'hotwheels_boulevard_2012_2025.csv'
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['toy_num', 'model', 'series', 'series_num', 'photo_url', 'line_type', 'year'])
    writer.writerows(all_rows)

print(f"✅ Selesai! Data tersimpan di {filename}")
