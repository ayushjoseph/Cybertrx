"""
IMetricCalculator interface - Core abstraction for metric calculations
Following Dependency Inversion Principle (DIP)
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd


class IMetricCalculator(ABC):
    """
    Abstract base class for metric calculators.
    Enforces a contract that all calculators must implement.
    """
    
    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate metrics from the provided data.
        
        Args:
            data: Standardized pandas DataFrame from data source
            
        Returns:
            Dict containing calculated metrics and metadata
        """
        pass
    
    @abstractmethod
    def get_metric_name(self) -> str:
        """
        Get the name of the metric this calculator produces.
        
        Returns:
            str: Human-readable metric name
        """
        pass
    
    @abstractmethod
    def get_metric_units(self) -> str:
        """
        Get the units for the metric this calculator produces.
        
        Returns:
            str: Units string (e.g., "°C", "mm", "m/s")
        """
        pass
