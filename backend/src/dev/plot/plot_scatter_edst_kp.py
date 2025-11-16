"""Kp指数とEDSTの散布図を作成
目的:
特異型EEJの傾向を把握する
"""

from datetime import datetime

import matplotlib.pyplot as plt
from src.dev.plot.config import PlotConfig
from src.domain.region import Region
from src.domain.station_params import Period
from src.service.ee_index.calc_edst import Edst
from src.service.kp import Kp
from src.service.peculiar_eej import PeculiarEejService

peculiar_eej_service = PeculiarEejService()
sudden_eej_data = peculiar_eej_service.get_by_region_and_type(
    Region.SOUTH_AMERICA, type="突発型"
)

sudden_kp_edst = []  # (kp, edst)
for sudden_eej in sudden_eej_data:
    ut_period = Period(
        start=datetime(
            sudden_eej.date.year, sudden_eej.date.month, sudden_eej.date.day, 0, 0
        ),
        end=datetime(
            sudden_eej.date.year, sudden_eej.date.month, sudden_eej.date.day, 23, 59
        ),
    )

    kp_val = Kp().get_max_of_day(ut_period)
    edst_val = Edst(ut_period).get_min_edst()
    sudden_kp_edst.append((kp_val, edst_val))


undeveloped_eej_data = peculiar_eej_service.get_by_region_and_type(
    Region.SOUTH_AMERICA, type="未発達型"
)

undevelop_kp_edst = []  # (kp, edst)
for undeveloped_eej in undeveloped_eej_data:
    ut_period = Period(
        start=datetime(
            undeveloped_eej.date.year,
            undeveloped_eej.date.month,
            undeveloped_eej.date.day,
            0,
            0,
        ),
        end=datetime(
            undeveloped_eej.date.year,
            undeveloped_eej.date.month,
            undeveloped_eej.date.day,
            23,
            59,
        ),
    )

    kp_val = Kp().get_max_of_day(ut_period)
    edst_val = Edst(ut_period).get_min_edst()
    undevelop_kp_edst.append((kp_val, edst_val))


sudden_kp, sudden_edst = zip(*sudden_kp_edst)
undevelop_kp, undevelop_edst = zip(*undevelop_kp_edst)


PlotConfig.rcparams()
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(
    sudden_kp,
    sudden_edst,
    color="red",
    label="突発型",
    alpha=0.7,
    edgecolors="w",
    s=100,
)
ax.scatter(
    undevelop_kp,
    undevelop_edst,
    color="blue",
    label="未発達型",
    alpha=0.7,
    edgecolors="w",
    s=100,
)
ax.set_xlabel("Kp index", fontsize=14)
ax.set_ylabel("EDst (nT)", fontsize=14)
ax.axhline(0, color="gray", linestyle="--", linewidth=1)
ax.axvline(0, color="gray", linestyle="--", linewidth=1)
ax.legend(fontsize=12)

ax.grid(True, linestyle="--", alpha=0.5)
fig.tight_layout()
plt.show()
