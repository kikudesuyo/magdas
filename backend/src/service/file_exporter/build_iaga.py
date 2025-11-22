import io
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation


@dataclass
class EeIndexIagaRecord:
    date: str
    time: str
    doy: int
    edst_1h: float
    edst_6h: float
    er: float
    euel: float


class EeIndexIagaModel(BaseModel):
    iaga_meta_data: dict
    dates: List[str]
    times: List[str]
    doys: List[int]
    edst_1h: List[float]
    edst_6h: List[float]
    er: List[float]
    euel: List[float]


class EeIndexIagaService:
    def build_iaga_meta_data(
        self, station: EeIndexStation, iaga_code, elevation
    ) -> dict:
        return {
            "Format": "IAGA-2002",
            "Source of Data": "Kyushu University (KU)",
            "Station Name": f"{station.code}",
            "IAGA CODE": f"{iaga_code} (KU code)",
            "Geodetic Latitude": station.gm_lat,
            "Geodetic Longitude": station.gm_lon,
            "Elevation": elevation,
            "Reported": "EE-index",
            "Recorded data": "EE-index: EDst1h, EDst6h, ER_HUA, EUEL_HUA",
            "Digital Sampling": "1 second",
            "Data Interval Type": "Averaged 1-minute (00:30 - 01:29)",
            "Data Type": "Provisional EE-index:230202",
        }

    def build_iaga_records(
        self,
        start_ut: datetime,
        end_ut: datetime,
        edst_1h_values,
        edst_6h_values,
        er_values,
        euel_values,
    ) -> list[EeIndexIagaRecord]:
        minutes = TimeUnit.ONE_DAY.min
        days = (end_ut - start_ut).days + 1

        records = []
        idx = 0

        for day in range(days):
            base_date = start_ut + timedelta(days=day)
            doy = base_date.timetuple().tm_yday

            for m in range(minutes):
                hour = m // 60
                minute = m % 60

                time_str = f"{hour:02d}:{minute:02d}:00.000"
                date_str = base_date.strftime("%Y-%m-%d")

                records.append(
                    EeIndexIagaRecord(
                        date=date_str,
                        time=time_str,
                        doy=doy,
                        edst_1h=edst_1h_values[idx],
                        edst_6h=edst_6h_values[idx],
                        er=er_values[idx],
                        euel=euel_values[idx],
                    )
                )
                idx += 1
        return records

    def build_iaga_content(self, meta, records: list[EeIndexIagaRecord]) -> bytes:
        buf = io.StringIO()
        for k, v in meta.items():
            buf.write(f"{k:<25} {v:<40}\n")
        buf.write(
            f"{'DATE':<11}{'TIME':<13}{'DOY':<7}"
            f"{'EDst1h':<10}{'EDst6h':<10}{'ER':<10}{'EUEL':<10}\n"
        )
        for r in records:
            buf.write(
                f"{r.date:<11}{r.time:<13}{str(r.doy).zfill(3):<7}"
                f"{r.edst_1h:<10.2f}{r.edst_6h:<10.2f}{r.er:<10.2f}{r.euel:<10.2f}\n"
            )
        return buf.getvalue().encode("utf-8")
