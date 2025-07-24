from datetime import datetime

from src.domain.magdas_station import EeIndexStation
from src.service.file_exporter.export_ee_zip import export_ee_as_iaga_zip


class EeIndexZipByRangeUsecase:
    def __init__(self, ut_date: datetime, end_ut: datetime, station: EeIndexStation):
        self.ut_date = ut_date
        self.end_ut = end_ut
        self.station = station

    def get_ee_as_iaga_zip(self):
        start_ut = self.ut_date.replace(hour=0, minute=0)
        end_ut = self.end_ut.replace(hour=23, minute=59)
        return export_ee_as_iaga_zip(self.station, start_ut, end_ut)

    def get_filename(self):
        start_date = self.ut_date.strftime("%Y-%m-%d")
        end_date = self.end_ut.strftime("%Y-%m-%d")
        return f"ee_index_{start_date}_to_{end_date}.zip"
