import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.core.models import BusSchedule
from apps.accounts.models import Bus


class Command(BaseCommand):
    help = "スクールバス時刻表を取得し、データベースに保存します。"

    def handle(self, *args, **options):
        self.stdout.write("🧹 既存のバスデータを削除中...")
        BusSchedule.objects.all().delete()
        Bus.objects.all().delete()
        self.stdout.write(self.style.WARNING("🗑️ Bus および BusSchedule データを削除しました。"))

        # バス情報の基本登録（バスが存在しないと後続処理が失敗するため）
        buses = [
            Bus(name="八王子みなみ野"),
            Bus(name="八王子"),
        ]
        Bus.objects.bulk_create(buses)
        self.stdout.write("🚌 Bus データを再登録しました。")

        self.stdout.write("🚍 バス時刻表を取得中...")

        urls = self.fetch_bus_urls()

        # 平日
        rows_minami, rows_hachi = self.fetch_weekday_bus_schedules(urls)
        self.save_to_db(rows_minami, "八王子みなみ野", is_saturday=False)
        self.save_to_db(rows_hachi, "八王子", is_saturday=False)

        # 土曜日
        rows_minami, rows_hachi = self.fetch_saturday_bus_schedules(urls)
        self.save_to_db(rows_minami, "八王子みなみ野", is_saturday=True)
        self.save_to_db(rows_hachi, "八王子", is_saturday=True)

        self.stdout.write(self.style.SUCCESS("✅ バス時刻データを保存しました。"))



# =====================================================
# スクレイピング処理
# =====================================================

    def fetch_bus_urls(self):
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


    def fetch_weekday_bus_schedules(self, urls):
        """平日のバスの時刻を取得"""
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

        return rows_minami, rows_hachi


    def fetch_saturday_bus_schedules(self, urls):
        """土曜日のバスの時刻を取得"""
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

        return rows_minami, rows_hachi

# =====================================================
# DB保存処理
# =====================================================

    def str_to_time(self, s):
        """HH:MM形式の文字列をtime型に変換"""
        try:
            return datetime.strptime(s, "%H:%M").time() if s else None
        except ValueError:
            return None


    def save_to_db(self, rows, bus_name, is_saturday=False):
        """スクレイピング結果をBusScheduleに保存"""
        bus = Bus.objects.get(name=bus_name)

        for row in rows:
            # テーブル構造に合わせて調整
            station_departure = self.str_to_time(row[0]) if len(row) > 0 else None
            campus_arrival = self.str_to_time(row[1]) if len(row) > 1 else None
            campus_departure = self.str_to_time(row[2]) if len(row) > 2 else None
            note = row[-1] if len(row) >= 4 else None

            BusSchedule.objects.create(
                bus=bus,
                station_departure=station_departure,
                campus_arrival=campus_arrival,
                campus_departure=campus_departure,
                note=note,
                is_saturday=is_saturday,
            )
