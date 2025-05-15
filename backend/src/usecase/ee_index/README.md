# EE-Index Module

## Overview

This module contains the core functionality for calculating and working with EE-index data, which includes ER, EDst, and EUEL. These indices are essential for the application's functionality.

## Components

- **HComponent**: Handles the raw H-component data retrieval and processing
- **Er**: Calculates the ER index based on H-component data
- **Edst**: Calculates the EDst index using data from multiple stations
- **Euel**: Calculates the EUEL index using ER and EDst data

## Factory Pattern Implementation

The `EeFactory` class implements a factory pattern with caching to efficiently create and manage instances of the above components. This approach offers several benefits:

1. **Centralized Creation**: All component instances are created through a single factory, providing a clean API.
2. **Dependency Management**: The factory handles the dependencies between components (e.g., Er depends on HComponent).
3. **Caching**: Instances are cached to avoid redundant calculations, improving performance.
4. **Reduced Coupling**: Client code doesn't need to know how to create these components or manage their dependencies.

### Usage Example

```python
from src.domain.station_params import Period, StationParams
from src.domain.magdas_station import EeIndexStation
from src.usecase.ee_index.factory_ee import EeFactory

# Create a factory instance
factory = EeFactory()

# Define parameters
start_date = datetime(2023, 1, 1, 0, 0)
end_date = datetime(2023, 1, 2, 23, 59)
period = Period(start_date, end_date)
station = EeIndexStation.ANC
params = StationParams(station, period)

# Get components
er = factory.create_er(params)
edst = factory.create_edst(period)
euel = factory.create_euel(params)

# Calculate values
er_values = er.calc_er()
edst_values = edst.compute_smoothed_edst()
euel_values = euel.calc_euel()
```

## Design Considerations

1. **Caching Strategy**: The factory uses both an internal dictionary cache and Python's `lru_cache` decorator to optimize performance.
2. **Cache Keys**: Cache keys are created using station and time period information to uniquely identify each component.
3. **Cache Clearing**: A `clear_cache` method is provided to manually clear the cache when needed.
4. **Type Hints**: Type hints are used throughout to improve code readability and enable better IDE support.

## Future Improvements

1. **Interfaces**: Consider defining interfaces for each component to further reduce coupling.
2. **Dependency Injection**: Consider using a more sophisticated dependency injection framework for larger applications.
3. **Async Support**: Add support for asynchronous data retrieval and processing.
4. **Monitoring**: Add instrumentation to monitor cache hit rates and performance.