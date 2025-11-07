import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_bus_urls():
    """バスのURLの取得"""
    base_url = "https://www.teu.ac.jp"
    url = "https://www.teu.ac.jp/campus/access/006644.html#bustimetable"

    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    uls = soup.select('ul[data-role="listview"]')

    target_ul = None
    for ul in uls:
        divider = ul.find('li', attrs={'data-role': 'list-divider'})
        if divider and "スクールバス【基本】時刻表" in divider.text:
            target_ul = ul
            break

    if not target_ul:
        print("対象のリストが見つかりません。")
        return []

    urls = [urljoin(base_url, str(a['href'])) for a in target_ul.find_all('a', href=True)]

    return urls


def fetch_weekday_bus_schedules(urls):
    url = urls[0]
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    trs_minami = soup.select("#main-wrapper > div > div > div > table:nth-child(3) > tbody > tr")
    trs_hachi = soup.select("#main-wrapper > div > div > div > table:nth-child(8) > tbody > tr")

    rows_minami = []
    for i, tr in enumerate(trs_minami):
        if i == 0:
            continue
        cells = tr.find_all(["th", "td"])
        row = [cell.get_text(strip=True) for cell in cells]
        row = [None if c == "～" else c for c in row]
        rows_minami.append(row)

    rows_hachi = []
    for i, tr in enumerate(trs_hachi):
        if i == 0:
            continue
        cells = tr.find_all(["th", "td"])
        row = [cell.get_text(strip=True) for cell in cells]
        row = [None if c == "～" else c for c in row]
        rows_hachi.append(row)

    print(rows_minami)
    print("--------------------------")
    print(rows_hachi)

    return rows_minami, rows_hachi


def fetch_saturday_bus_schedules(urls):
    url = urls[1]
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    trs_minami = soup.select("#main-wrapper > div > div > div > table:nth-child(3) > tbody > tr")
    trs_hachi = soup.select("#main-wrapper > div > div > div > table:nth-child(8) > tbody > tr")


    rows_minami = []
    for i, tr in enumerate(trs_minami):
        if i == 0:
            continue
        cells = tr.find_all(["th", "td"])
        row = [cell.get_text(strip=True) for cell in cells]
        row = [None if c == "～" else c for c in row]
        rows_minami.append(row)

    rows_hachi = []
    for i, tr in enumerate(trs_hachi):
        if i == 0:
            continue
        cells = tr.find_all(["th", "td"])
        row = [cell.get_text(strip=True) for cell in cells]
        row = [None if c == "～" else c for c in row]
        rows_hachi.append(row)

    print(rows_minami)
    print("--------------------------")
    print(rows_hachi)
    return rows_minami, rows_hachi





if __name__ == "__main__":
    urls = fetch_bus_urls()
    fetch_weekday_bus_schedules(urls)
    print("--------------------------------------------")
    fetch_saturday_bus_schedules(urls)
