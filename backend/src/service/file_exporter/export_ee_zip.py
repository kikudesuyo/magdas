import base64
from datetime import datetime

from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.model.file import FileModel
from src.service.calc_utils.moving_avg import calc_moving_avg
from src.service.ee_index.factory_ee import EeFactory
from src.service.file_exporter.build_iaga import EeIndexIagaService, IagaValues
from src.service.file_exporter.zip_create import ZipService


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
    params = StationParam(station, period)

    factory = EeFactory()
    er = factory.create_er(params)
    edst = factory.create_edst(period)
    euel = factory.create_euel(params)

    er_values = er.calc_er()
    edst_raw = edst.calc_edst()
    edst_1h_values = calc_moving_avg(edst_raw, TimeUnit.ONE_HOUR.min, 30)
    edst_6h_values = calc_moving_avg(
        edst_raw, TimeUnit.SIX_HOURS.min, TimeUnit.THREE_HOURS.min
    )

    euel_values = euel.calc_euel()

    ee_index_iaga_service = EeIndexIagaService()
    values = IagaValues(
        edst_1h=edst_1h_values.tolist(),
        edst_6h=edst_6h_values.tolist(),
        er=er_values.tolist(),
        euel=euel_values.tolist(),
    )
    iaga_byte_file = ee_index_iaga_service.build_iaga_file(
        station, start_ut, end_ut, values
    )
    filename = f"{station.code.lower()}{start_ut.strftime('%Y%m%d')}.iaga"
    zip_service = ZipService()
    zip_buffer = zip_service.create(
        [FileModel(filename=filename, content=iaga_byte_file)]
    )
    zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")
    return zip_base64
