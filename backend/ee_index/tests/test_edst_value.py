import unittest
import warnings
from datetime import datetime, timedelta

import numpy as np
from get_index.edst_index import Edst


class TestEdst(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings(
            "ignore", category=RuntimeWarning, message="Mean of empty slice"
        )
        warnings.filterwarnings(
            "ignore", category=RuntimeWarning, message="All-NaN slice encountered"
        )

    station = "EUS"
    ut_datetime = datetime(2012, 4, 30)
    days = 2
