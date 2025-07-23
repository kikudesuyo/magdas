from datetime import datetime, timedelta

from src.domain.magdas_station import EeIndexStation
from src.service.file_exporter.export_ee_zip import export_ee_as_iaga_zip


class EeIndexZipByDays:
    def __init__(self, ut_date: datetime, days: int, station: EeIndexStation):
        self.ut_date = ut_date
        self.days = days
        self.station = station

    def get_ee_as_iaga_zip(self):
        start_ut = self.ut_date.replace(hour=0, minute=0)
        end_ut = start_ut + timedelta(days=self.days - 1, hours=23, minutes=59)
        return export_ee_as_iaga_zip(self.station, start_ut, end_ut)

    def get_filename(self):
        start_date = self.ut_date.strftime("%Y-%m-%d")
        end_date = (self.ut_date + timedelta(days=self.days - 1)).strftime("%Y-%m-%d")
        return f"ee_index_{start_date}_to_{end_date}.zip"
