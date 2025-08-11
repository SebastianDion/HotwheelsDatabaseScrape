import requests
from bs4 import BeautifulSoup
import csv

URL = "https://hotwheels.fandom.com/wiki/Car_Culture_2-Packs"
print(f"🌐 Scraping {URL}")
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

rows = []

tables = soup.find_all("table", class_="wikitable")
line_type = "Car Culture 2 Pack"

for table in tables:
    # Cari series/mix
    series_heading = table.find_previous("h3")
    series = series_heading.text.strip().replace("[edit]", "").strip() if series_heading else "Unknown"

    # Cari tahun dari heading h2 sebelum series
    year_heading = series_heading.find_previous("h2") if series_heading else table.find_previous("h2")
    year = year_heading.text.strip().replace("[edit]", "").strip() if year_heading else "Unknown"

    trs = table.find_all("tr")
    i = 1  # skip header row

    while i < len(trs):
        tr = trs[i]
        cols = tr.find_all("td")

        try:
            # Cek kalau Toy # rowspan 2
            if len(cols) >= 8 and cols[0].has_attr("rowspan") and cols[0]["rowspan"] == "2":
                toy_num = cols[0].text.strip()
                theme = cols[1].text.strip()
                model1 = cols[2].text.strip()

                img_tag = cols[7].find("img")
                photo_url = ""
                if img_tag:
                    photo_url = img_tag.get("data-src") or img_tag.get("src") or ""

                # Ambil baris kedua
                next_tr = trs[i + 1]
                next_cols = next_tr.find_all("td")
                model2 = next_cols[0].text.strip()

                # Simpan dua baris
                rows.append([year, toy_num, theme, model1, series, photo_url, line_type])
                rows.append([year, toy_num, theme, model2, series, photo_url, line_type])

                i += 2

            elif len(cols) >= 8:
                # Case normal
                toy_num = cols[0].text.strip()
                theme = cols[1].text.strip()
                model = cols[2].text.strip()

                img_tag = cols[7].find("img")
                photo_url = ""
                if img_tag:
                    photo_url = img_tag.get("data-src") or img_tag.get("src") or ""

                rows.append([year, toy_num, theme, model, series, photo_url, line_type])

                i += 1
            else:
                i += 1
        except Exception as e:
            print(f"⚠️ Error parsing row {i} in series {series}: {e}")
            i += 1

print(f"✅ Ditemukan {len(rows)} baris data")

# Simpan ke CSV
with open("hotwheels_2packs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["year", "toy_num", "theme", "model", "series", "photo_url", "line_type"])
    writer.writerows(rows)

print("💾 Data tersimpan di hotwheels_2packs.csv")
