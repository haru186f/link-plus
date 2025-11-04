import requests
from bs4 import BeautifulSoup


def run():
    url = 'https://www.teu.ac.jp/campus/access/2025_0922bus.html'
    res = requests.get(url)
    if res.status_code != 200:
        return

    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        div = soup.find("div", class_="commonDetailBox01")
        if div is None:
            raise AttributeError

        table = div.find("table")
        if table is None:
            raise AttributeError

        rows = table.find_all("tr")
        if rows is None:
            raise AttributeError

        from_campus_lists = []
        from_station_lists = []
        for row in rows:
            tds = row.find_all("td")
            if "シャトル運行" in row.get_text():
                continue
            if len(tds) >= 2:
                from_campus_lists.append(tds[0].get_text())
                from_station_lists.append(tds[1].get_text())

        print(from_campus_lists)
        print('-----------------------------------------------------------------')
        print(from_station_lists)

    except AttributeError:
        return

run()
