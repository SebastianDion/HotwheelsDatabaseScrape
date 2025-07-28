import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_popCulture(year):
    url = f"https://hotwheels.fandom.com/wiki/{year}_Pop_Culture"
    print(f"🌐 Scraping {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = []
    tables = soup.find_all('table', class_='wikitable')
    line_type = "Pop Culture"

    for table in tables:
        # Ambil heading (misalnya: "Marvel", "Looney Tunes", etc.)
        series_heading = table.find_previous(['h2', 'h3'])
        series = series_heading.text.strip() if series_heading else 'Unknown'

        for tr in table.find_all('tr')[1:]:  # Skip header row
            cols = tr.find_all('td')
            if len(cols) >= 8:
                toy_num = cols[0].text.strip()
                model = cols[1].text.strip()
                theme = cols[2].text.strip()

                # Foto biasanya ada di kolom ke-8 (index 7)
                img_tag = cols[7].find('img')
                photo_url = ''
                if img_tag:
                    photo_url = img_tag.get('data-src') or img_tag.get('src') or ''

                # series_num gak tersedia, jadi kasih kosong/null
                rows.append([
                    toy_num,
                    model,
                    series,
                    theme,
                    '',  # series_num kosong
                    photo_url,
                    line_type,
                    year
                ])

    print(f"🕵️ {len(rows)} baris ditemukan untuk tahun {year}")
    return rows

# ⏱ Loop multi-year
all_rows = []
for year in range(2013, 2026):
    try:
        all_rows.extend(scrape_popCulture(year))
        time.sleep(1)  # jeda biar aman dari rate-limit
    except Exception as e:
        print(f"❌ Gagal scraping {year}: {e}")

# 💾 Simpan ke CSV
with open('hotwheels_PopCulture_2013_2025.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['toy_num', 'model', 'series', 'theme', 'series_num', 'photo_url', 'line_type', 'year'])
    writer.writerows(all_rows)

print("✅ Selesai! Data tersimpan di hotwheels_PopCulture_2013_2025.csv")
