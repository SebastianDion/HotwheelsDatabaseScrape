import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_hotwheels(year):
    # Handle khusus untuk 2014/2015
    if year in (2014, 2015):
        url = "https://hotwheels.fandom.com/wiki/2014/2015_Red_Line_Club_Membership"
        year_label = "2014/2015"
    else:
        url = f"https://hotwheels.fandom.com/wiki/{year}_Red_Line_Club_Membership"
        year_label = str(year)
    
    print(f"🌐 Scraping {url}")
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = []
    tables = soup.find_all('table', class_='wikitable')
    line_type = "Red Line Club Membership"
    
    for table in tables:
        series_heading = table.find_previous(['h2', 'h3'])
        series = series_heading.text.strip() if series_heading else 'Unknown'

        headers = [th.text.strip().lower() for th in table.find_all('th')]

        for tr in table.find_all('tr')[1:]:  # Skip header
            cols = tr.find_all('td')
            if not cols:
                continue

            # Format khusus 2002 (toy#, model, color, qty, pic)
            if 'toy #' in headers or 'model name' in headers:
                if len(cols) >= 5:
                    toy_num = cols[0].text.strip()
                    model = cols[1].text.strip()
                    color = cols[2].text.strip()
                    img_tag = cols[4].find('img')
                else:
                    continue

            # Format umum (2003+)
            else:
                if len(cols) >= 6:
                    toy_num = cols[0].text.strip()
                    model = cols[1].text.strip()
                    color = cols[2].text.strip()
                    img_tag = cols[-1].find('img')  # ambil kolom terakhir (biasanya gambar)
                else:
                    continue

            # Ambil photo_url
            photo_url = ''
            if img_tag:
                photo_url = img_tag.get('data-src') or img_tag.get('src') or ''
                if photo_url.startswith('//'):
                    photo_url = 'https:' + photo_url

            rows.append([
                toy_num,
                model,
                color,
                series,
                photo_url,
                year_label,
                line_type
            ])
    
    print(f"🕵️ {len(rows)} baris ditemukan untuk tahun {year_label}")
    return rows


# Main scraping loop
all_rows = []
for year in range(2002, 2026):
    try:
        all_rows.extend(scrape_hotwheels(year))
        time.sleep(1)
    except Exception as e:
        print(f"❌ Gagal scraping {year}: {e}")

# Simpan ke CSV
filename = 'hotwheels_RLC_2002_2025.csv'
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['toy_num', 'model', 'color', 'series', 'photo_url', 'year', 'line_type'])
    writer.writerows(all_rows)

print(f"✅ Selesai! Data tersimpan di {filename}")

