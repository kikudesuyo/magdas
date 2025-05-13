from src.usecase.ee_index.constant.magdas_station import EeIndexStation


def get_meta_data(station: EeIndexStation, iaga_code, elevation):
    metadata = {
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
    return metadata
