import requests
from bs4 import BeautifulSoup
from datetime import datetime
from apps.accounts.models import Bus
from .models import BusSchedule


def fetch_and_save_bus_times():
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

        from_school = []
        to_school = []

        for row in rows:
            tds = row.find_all("td")
            if "シャトル運行" in row.get_text():
                continue
            if len(tds) >= 2:
                from_school.append(tds[0].get_text().strip())
                to_school.append(tds[1].get_text().strip())

        bus = Bus.objects.first()
        if not bus:
            return

        for time_str in to_school:
            if time_str:
                time = datetime.strptime(time_str, "%H:%M").time()
                BusSchedule.objects.get_or_create(
                    bus=bus,
                    direction="to_school",
                    departure_time=time,
                    is_weekend=False
                )

        for time_str in from_school:
            if time_str:
                time = datetime.strptime(time_str, "%H:%M").time()
                BusSchedule.objects.get_or_create(
                    bus=bus,
                    direction="from_school",
                    departure_time=time,
                    is_weekend=False
                )

    except AttributeError:
        return
