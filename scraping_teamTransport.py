import re
import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_team_transport(year):
    url = f"https://hotwheels.fandom.com/wiki/{year}_Car_Culture:_Team_Transport"
    print(f"🌐 Scraping {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = []
    tables = soup.find_all('table', class_='wikitable')
    line_type = "Team Transport"

    for table in tables:
        series_heading = table.find_previous(['h2', 'h3'])
        series = series_heading.text.strip().replace("[edit]", "").strip() if series_heading else 'Unknown'

        trs = table.find_all('tr')
        i = 1  # Skip header

        while i < len(trs):
            tr = trs[i]
            cols = tr.find_all('td')

            try:
                # Check if this row has rowspan=2 for toy_num (case with 2 models)
                if len(cols) >= 8 and cols[0].has_attr("rowspan") and cols[0]["rowspan"] == "2":
                    toy_num = cols[0].text.strip()
                    series_num = cols[1].text.strip()
                    model1 = cols[2].text.strip()

                    img_tag = cols[7].find('img')
                    photo_url = ''
                    if img_tag:
                        photo_url = img_tag.get('data-src') or img_tag.get('src') or ''

                    # Row berikutnya: model ke-2
                    next_tr = trs[i + 1]
                    next_cols = next_tr.find_all('td')
                    model2 = next_cols[0].text.strip() if len(next_cols) > 0 else ''

                    # Tambahkan dua baris
                    rows.append([toy_num, model1, series, series_num, photo_url, line_type, year])
                    rows.append([toy_num, model2, series, series_num, photo_url, line_type, year])

                    i += 2  # Lewatin dua baris

                elif len(cols) >= 8:
                    # Fallback: baris biasa (1 model per baris)
                    toy_num = cols[0].text.strip()
                    series_num = cols[1].text.strip()
                    model_html = cols[2]
                    raw_html = model_html.decode_contents()
                    models = [BeautifulSoup(m, 'html.parser').text.strip() for m in raw_html.split('<br>')]

                    img_tag = cols[7].find('img')
                    photo_url = ''
                    if img_tag:
                        photo_url = img_tag.get('data-src') or img_tag.get('src') or ''

                    for model in models:
                        rows.append([toy_num, model, series, series_num, photo_url, line_type, year])

                    i += 1

                else:
                    i += 1  # Skip baris yang gak cocok

            except Exception as err:
                print(f"⚠️ Gagal parsing baris {i} tahun {year}: {err}")
                i += 1

    print(f"🕵️ {len(rows)} baris ditemukan untuk tahun {year}")
    return rows

# 🔁 Loop dari 2017–2025
all_rows = []
for year in range(2017, 2026):
    try:
        all_rows.extend(scrape_team_transport(year))
        time.sleep(1)
    except Exception as e:
        print(f"❌ Gagal scraping {year}: {e}")

# 💾 Simpan ke CSV
with open('hotwheels_Team_Transport.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['toy_num', 'model', 'series', 'series_num', 'photo_url', 'line_type', 'year'])
    writer.writerows(all_rows)

print("✅ Selesai! Data tersimpan di hotwheels_Team_Transport.csv")
