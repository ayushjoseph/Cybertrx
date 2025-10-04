"""
IDataSource interface - Core abstraction for data fetching
Following Dependency Inversion Principle (DIP)
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd
from datetime import datetime


class IDataSource(ABC):
    """
    Abstract base class for data sources.
    Enforces a contract that all data sources must implement.
    """
    
    @abstractmethod
    def fetch_data(self, location: Dict[str, float], date_range: Dict[str, str]) -> pd.DataFrame:
        """
        Fetch data from the data source for a given location and date range.
        
        Args:
            location: Dictionary containing 'latitude' and 'longitude'
            date_range: Dictionary containing 'start_date' and 'end_date' (ISO format)
            
        Returns:
            pandas.DataFrame: Standardized data format
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the data source is currently available.
        
        Returns:
            bool: True if available, False otherwise
        """
        pass
