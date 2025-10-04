"""
IExporter interfaces - Core abstractions for data export
Following Interface Segregation Principle (ISP)
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd


class ITabularExporter(ABC):
    """
    Interface for tabular data export (CSV, JSON, etc.)
    Following Interface Segregation Principle
    """
    
    @abstractmethod
    def to_csv(self, data: pd.DataFrame, file_path: str) -> bool:
        """
        Export data to CSV format.
        
        Args:
            data: DataFrame to export
            file_path: Output file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def to_json(self, data: pd.DataFrame, file_path: str) -> bool:
        """
        Export data to JSON format.
        
        Args:
            data: DataFrame to export
            file_path: Output file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass


class IAnalysisExporter(ABC):
    """
    Interface for analysis results export
    Following Interface Segregation Principle
    """
    
    @abstractmethod
    def export_analysis(self, results: Dict[str, Any], file_path: str) -> bool:
        """
        Export analysis results to file.
        
        Args:
            results: Analysis results dictionary
            file_path: Output file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
