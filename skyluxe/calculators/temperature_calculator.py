"""
Temperature Calculator
Concrete implementation of IMetricCalculator
Following Single Responsibility Principle (SRP) and Liskov Substitution Principle (LSP)
"""
import pandas as pd
from typing import Dict, Any
import numpy as np

from skyluxe.interfaces.metric_calculator import IMetricCalculator


class TemperatureCalculator(IMetricCalculator):
    """
    Calculator for temperature-related metrics.
    Follows SRP: Only responsible for temperature calculations
    Follows LSP: Can be substituted for any IMetricCalculator implementation
    """
    
    def calculate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate temperature metrics from weather data.
        
        Args:
            data: DataFrame with weather data
            
        Returns:
            Dict containing temperature metrics
        """
        if 'temperature_2m' not in data.columns:
            return {
                'metric_name': self.get_metric_name(),
                'error': 'Temperature data not available'
            }
        
        temp_data = data['temperature_2m'].dropna()
        
        if len(temp_data) == 0:
            return {
                'metric_name': self.get_metric_name(),
                'error': 'No valid temperature data found'
            }
        
        # Calculate basic statistics
        metrics = {
            'metric_name': self.get_metric_name(),
            'units': self.get_metric_units(),
            'mean_temperature': float(temp_data.mean()),
            'max_temperature': float(temp_data.max()),
            'min_temperature': float(temp_data.min()),
            'temperature_range': float(temp_data.max() - temp_data.min()),
            'temperature_std': float(temp_data.std()),
            'data_points': len(temp_data),
            'date_range': {
                'start': data['date'].min().isoformat(),
                'end': data['date'].max().isoformat()
            }
        }
        
        # Calculate temperature categories
        metrics.update(self._calculate_temperature_categories(temp_data))
        
        return metrics
    
    def get_metric_name(self) -> str:
        """Get the name of the temperature metric"""
        return "Temperature Analysis"
    
    def get_metric_units(self) -> str:
        """Get the units for temperature"""
        return "°C"
    
    def _calculate_temperature_categories(self, temp_data: pd.Series) -> Dict[str, Any]:
        """Calculate temperature category statistics"""
        # Define temperature categories (in Celsius)
        categories = {
            'very_cold': temp_data < -10,
            'cold': (temp_data >= -10) & (temp_data < 0),
            'cool': (temp_data >= 0) & (temp_data < 10),
            'mild': (temp_data >= 10) & (temp_data < 20),
            'warm': (temp_data >= 20) & (temp_data < 30),
            'hot': (temp_data >= 30) & (temp_data < 40),
            'very_hot': temp_data >= 40
        }
        
        category_stats = {}
        for category, mask in categories.items():
            count = mask.sum()
            percentage = (count / len(temp_data)) * 100
            category_stats[f'{category}_days'] = int(count)
            category_stats[f'{category}_percentage'] = round(percentage, 2)
        
        return category_stats
