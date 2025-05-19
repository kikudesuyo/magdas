import base64
from datetime import datetime

from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.factory_ee import EeFactory
from src.usecase.file_exporter.build_iaga import (
    build_iaga_data,
    build_iaga_meta_data,
    save_as_iaga,
)
from src.usecase.file_exporter.remove_files import TMP_DIR_PATH, remove_tmp_files
from src.usecase.file_exporter.zip_create import create_zip_buffer
from src.utils.path import generate_parent_abs_path


def export_ee_as_iaga_zip(
    station: EeIndexStation, start_ut: datetime, end_ut: datetime
):
    """
    Generate and download EE index data for a given station and time period.

    Args:
        station: The station to get data for
        start_ut: Start datetime
        end_ut: End datetime

    Returns:
        Base64 encoded zip file containing the data
    """
    period = Period(start_ut, end_ut)
    params = StationParams(station, period)

    factory = EeFactory()
    er = factory.create_er(params)
    edst = factory.create_edst(period)
    euel = factory.create_euel(params)
    er_values = er.calc_er()
    edst_values = edst.compute_smoothed_edst()
    euel_values = euel.calc_euel()

    iaga_meta_data = build_iaga_meta_data(
        station,
        "EEI",
        8888.88,
    )
    iaga_data = build_iaga_data(
        start_ut,
        end_ut,
        edst_values,
        er_values,
        euel_values,
    )
    save_as_iaga(
        iaga_meta_data, iaga_data, generate_parent_abs_path("/tmp/iaga_format.txt")
    )

    dir_path = generate_parent_abs_path(TMP_DIR_PATH)
    zip_buffer = create_zip_buffer(dir_path)
    zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")
    remove_tmp_files()

    return zip_base64
