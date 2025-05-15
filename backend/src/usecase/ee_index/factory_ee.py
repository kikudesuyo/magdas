from functools import lru_cache
from typing import Dict, Tuple

from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_edst import Edst
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_euel import Euel
from src.usecase.ee_index.calc_h_component import HComponent


class EeFactory:
    """Factory for creating EE-index related components with caching.
    
    This factory implements caching to avoid redundant calculations and follows
    dependency injection principles. It serves as a central point for creating
    instances of HComponent, Er, Edst, and Euel.
    """
    
    def __init__(self):
        # Cache for instances to avoid redundant calculations
        self._h_cache: Dict[Tuple[EeIndexStation, str, str], HComponent] = {}
        self._er_cache: Dict[Tuple[EeIndexStation, str, str], Er] = {}
        self._edst_cache: Dict[Tuple[str, str], Edst] = {}
        self._euel_cache: Dict[Tuple[EeIndexStation, str, str], Euel] = {}
    
    @lru_cache(maxsize=32)
    def create_h(self, calc_params: StationParams) -> HComponent:
        """Create or retrieve a cached HComponent instance.
        
        Args:
            calc_params: Parameters for the station and time period.
            
        Returns:
            HComponent instance.
        """
        cache_key = (calc_params.station, calc_params.period.start.isoformat(), 
                     calc_params.period.end.isoformat())
        
        if cache_key not in self._h_cache:
            self._h_cache[cache_key] = HComponent(calc_params)
        
        return self._h_cache[cache_key]
    
    @lru_cache(maxsize=32)
    def create_er(self, calc_params: StationParams) -> Er:
        """Create or retrieve a cached Er instance.
        
        Args:
            calc_params: Parameters for the station and time period.
            
        Returns:
            Er instance.
        """
        cache_key = (calc_params.station, calc_params.period.start.isoformat(), 
                     calc_params.period.end.isoformat())
        
        if cache_key not in self._er_cache:
            h = self.create_h(calc_params)
            self._er_cache[cache_key] = Er(h)
        
        return self._er_cache[cache_key]
    
    @lru_cache(maxsize=32)
    def create_edst(self, period: Period) -> Edst:
        """Create or retrieve a cached Edst instance.
        
        Args:
            period: Time period for the calculation.
            
        Returns:
            Edst instance.
        """
        cache_key = (period.start.isoformat(), period.end.isoformat())
        
        if cache_key not in self._edst_cache:
            self._edst_cache[cache_key] = Edst(period)
        
        return self._edst_cache[cache_key]
    
    @lru_cache(maxsize=32)
    def create_euel(self, calc_params: StationParams) -> Euel:
        """Create or retrieve a cached Euel instance.
        
        Args:
            calc_params: Parameters for the station and time period.
            
        Returns:
            Euel instance.
        """
        cache_key = (calc_params.station, calc_params.period.start.isoformat(), 
                     calc_params.period.end.isoformat())
        
        if cache_key not in self._euel_cache:
            er = self.create_er(calc_params)
            edst = self.create_edst(calc_params.period)
            self._euel_cache[cache_key] = Euel(er, edst)
        
        return self._euel_cache[cache_key]
    
    def clear_cache(self) -> None:
        """Clear all cached instances."""
        self._h_cache.clear()
        self._er_cache.clear()
        self._edst_cache.clear()
        self._euel_cache.clear()
        # Also clear the lru_cache
        self.create_h.cache_clear()
        self.create_er.cache_clear()
        self.create_edst.cache_clear()
        self.create_euel.cache_clear()
