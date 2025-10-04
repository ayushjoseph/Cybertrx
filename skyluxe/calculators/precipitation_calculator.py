"""
Precipitation Calculator
Concrete implementation of IMetricCalculator
Following Single Responsibility Principle (SRP) and Liskov Substitution Principle (LSP)
"""
import pandas as pd
from typing import Dict, Any
import numpy as np

from skyluxe.interfaces.metric_calculator import IMetricCalculator


class PrecipitationCalculator(IMetricCalculator):
    """
    Calculator for precipitation-related metrics.
    Follows SRP: Only responsible for precipitation calculations
    Follows LSP: Can be substituted for any IMetricCalculator implementation
    """
    
    def calculate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate precipitation metrics from weather data.
        
        Args:
            data: DataFrame with weather data
            
        Returns:
            Dict containing precipitation metrics
        """
        if 'precipitation' not in data.columns:
            return {
                'metric_name': self.get_metric_name(),
                'error': 'Precipitation data not available'
            }
        
        precip_data = data['precipitation'].dropna()
        
        if len(precip_data) == 0:
            return {
                'metric_name': self.get_metric_name(),
                'error': 'No valid precipitation data found'
            }
        
        # Calculate basic statistics
        metrics = {
            'metric_name': self.get_metric_name(),
            'units': self.get_metric_units(),
            'total_precipitation': float(precip_data.sum()),
            'mean_daily_precipitation': float(precip_data.mean()),
            'max_daily_precipitation': float(precip_data.max()),
            'precipitation_std': float(precip_data.std()),
            'data_points': len(precip_data),
            'date_range': {
                'start': data['date'].min().isoformat(),
                'end': data['date'].max().isoformat()
            }
        }
        
        # Calculate precipitation categories
        metrics.update(self._calculate_precipitation_categories(precip_data))
        
        # Calculate dry/wet periods
        metrics.update(self._calculate_dry_wet_periods(precip_data))
        
        return metrics
    
    def get_metric_name(self) -> str:
        """Get the name of the precipitation metric"""
        return "Precipitation Analysis"
    
    def get_metric_units(self) -> str:
        """Get the units for precipitation"""
        return "mm"
    
    def _calculate_precipitation_categories(self, precip_data: pd.Series) -> Dict[str, Any]:
        """Calculate precipitation category statistics"""
        # Define precipitation categories (in mm)
        categories = {
            'no_rain': precip_data == 0,
            'light_rain': (precip_data > 0) & (precip_data < 2.5),
            'moderate_rain': (precip_data >= 2.5) & (precip_data < 10),
            'heavy_rain': (precip_data >= 10) & (precip_data < 25),
            'very_heavy_rain': precip_data >= 25
        }
        
        category_stats = {}
        for category, mask in categories.items():
            count = mask.sum()
            percentage = (count / len(precip_data)) * 100
            category_stats[f'{category}_days'] = int(count)
            category_stats[f'{category}_percentage'] = round(percentage, 2)
        
        return category_stats
    
    def _calculate_dry_wet_periods(self, precip_data: pd.Series) -> Dict[str, Any]:
        """Calculate dry and wet period statistics"""
        # Define dry day as < 1mm precipitation
        dry_days = (precip_data < 1.0)
        wet_days = (precip_data >= 1.0)
        
        # Calculate consecutive dry/wet days
        dry_periods = self._find_consecutive_periods(dry_days)
        wet_periods = self._find_consecutive_periods(wet_days)
        
        return {
            'dry_days_total': int(dry_days.sum()),
            'wet_days_total': int(wet_days.sum()),
            'longest_dry_period': int(dry_periods.max()) if len(dry_periods) > 0 else 0,
            'longest_wet_period': int(wet_periods.max()) if len(wet_periods) > 0 else 0,
            'average_dry_period': float(dry_periods.mean()) if len(dry_periods) > 0 else 0,
            'average_wet_period': float(wet_periods.mean()) if len(wet_periods) > 0 else 0
        }
    
    def _find_consecutive_periods(self, condition: pd.Series) -> pd.Series:
        """Find consecutive periods where condition is True"""
        # Create groups of consecutive True values
        groups = (condition != condition.shift()).cumsum()
        periods = condition.groupby(groups).sum()
        
        # Return only periods where condition was True
        return periods[condition.groupby(groups).first()]
