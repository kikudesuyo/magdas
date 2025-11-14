"""特異型EEJの月齢別発生割合をプロット"""

from collections import defaultdict
from datetime import datetime, time
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from src.dev.plot.config import PlotConfig
from src.domain.region import Region
from src.model.peculiar_eej import PeculiarEejModel
from src.service.moon_phase import get_lunar_time
from src.service.peculiar_eej import PeculiarEejService


def aggregate_peculiar_eej_ratio_by_lunar_time(
    peculiar_eej_data: List[PeculiarEejModel], bin_size: int = 1
) -> Tuple[List[int], List[float]]:
    """
    月齢ごとに件数を集計し、
    全体件数に対する割合（%）を算出して返す。
    """
    moon_age_bins: Dict[int, int] = defaultdict(int)

    for eej in peculiar_eej_data:
        dt = datetime.combine(eej.date, time.min)
        moon_age = get_lunar_time(dt)

        bin_key = round(moon_age / bin_size) * bin_size
        moon_age_bins[bin_key] += 1

    total_count = len(peculiar_eej_data)
    bins = sorted(moon_age_bins.keys())
    ratios = [(moon_age_bins[b] / total_count) * 100 for b in bins]

    return bins, ratios


def plot_peculiar_ratio(
    x: List[int], peculiar_ratio: List[float], title: str, filename: str
):
    PlotConfig.rcparams()
    plt.figure(figsize=(10, 6))
    import matplotlib.ticker as mticker

    plt.bar(
        x,
        peculiar_ratio,
        width=1,
        edgecolor="black",
    )
    plt.margins(x=0)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.xlabel("Lunar Time")
    plt.ylabel("Peculiar EEJ Ratio (%)")
    plt.grid(True)
    plt.title(title)
    plt.savefig(f"img/peculiar_eej/{filename}")
    plt.close()


if __name__ == "__main__":
    peculiar_eej_service = PeculiarEejService()
    undev_peculiar_eej_data = peculiar_eej_service.get_by_region_and_type(
        region=Region.SOUTH_AMERICA, type="未発達型"
    )
    sudden_peculiar_eej_data = peculiar_eej_service.get_by_region_and_type(
        region=Region.SOUTH_AMERICA, type="突発型"
    )

    x, y = aggregate_peculiar_eej_ratio_by_lunar_time(sudden_peculiar_eej_data)
    title = "南アメリカ地域 突発型EEJ発生割合"
    filename = "2016-2020_南アメリカ_突発型_月齢.png"
    plot_peculiar_ratio(x, y, title, filename)
