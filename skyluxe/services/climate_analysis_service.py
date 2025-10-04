"""
Climate Analysis Service
High-level business logic orchestrating data fetching and calculations
Following Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP)
"""
from typing import Dict, Any, List
import logging
from datetime import datetime

from skyluxe.interfaces.data_source import IDataSource
from skyluxe.interfaces.metric_calculator import IMetricCalculator


class ClimateAnalysisService:
    """
    Service for orchestrating climate analysis.
    Follows SRP: Only responsible for coordinating analysis workflow
    Follows DIP: Depends on abstractions (IDataSource, IMetricCalculator), not concrete implementations
    """
    
    def __init__(self, data_source: IDataSource, calculators: List[IMetricCalculator]):
        """
        Initialize the climate analysis service.
        
        Args:
            data_source: Data source implementation (following DIP)
            calculators: List of metric calculators (following DIP)
        """
        self.data_source = data_source
        self.calculators = calculators
        self.logger = logging.getLogger(__name__)
    
    def analyze_climate(self, location: Dict[str, float], date_range: Dict[str, str]) -> Dict[str, Any]:
        """
        Perform comprehensive climate analysis for a location and date range.
        
        Args:
            location: Dictionary with 'latitude' and 'longitude'
            date_range: Dictionary with 'start_date' and 'end_date'
            
        Returns:
            Dict containing analysis results
        """
        try:
            self.logger.info(f"Starting climate analysis for location {location}")
            
            # Validate inputs
            self._validate_inputs(location, date_range)
            
            # Check data source availability
            if not self.data_source.is_available():
                return {
                    'error': 'Data source is currently unavailable',
                    'location': location,
                    'date_range': date_range
                }
            
            # Fetch data from data source
            self.logger.info("Fetching weather data...")
            weather_data = self.data_source.fetch_data(location, date_range)
            
            if weather_data.empty:
                return {
                    'error': 'No weather data available for the specified location and date range',
                    'location': location,
                    'date_range': date_range
                }
            
            # Calculate metrics using all calculators
            self.logger.info("Calculating metrics...")
            analysis_results = {
                'location': location,
                'date_range': date_range,
                'data_summary': {
                    'total_days': len(weather_data),
                    'date_range': {
                        'start': weather_data['date'].min().isoformat(),
                        'end': weather_data['date'].max().isoformat()
                    }
                },
                'metrics': []
            }
            
            # Run each calculator
            for calculator in self.calculators:
                try:
                    self.logger.info(f"Running {calculator.get_metric_name()}...")
                    metric_result = calculator.calculate(weather_data)
                    analysis_results['metrics'].append(metric_result)
                except Exception as e:
                    self.logger.error(f"Error in {calculator.get_metric_name()}: {e}")
                    analysis_results['metrics'].append({
                        'metric_name': calculator.get_metric_name(),
                        'error': str(e)
                    })
            
            self.logger.info("Climate analysis completed successfully")
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"Climate analysis failed: {e}")
            return {
                'error': f'Analysis failed: {str(e)}',
                'location': location,
                'date_range': date_range
            }
    
    def get_available_metrics(self) -> List[Dict[str, str]]:
        """
        Get list of available metrics from registered calculators.
        
        Returns:
            List of metric information
        """
        return [
            {
                'name': calculator.get_metric_name(),
                'units': calculator.get_metric_units()
            }
            for calculator in self.calculators
        ]
    
    def _validate_inputs(self, location: Dict[str, float], date_range: Dict[str, str]) -> None:
        """
        Validate input parameters.
        
        Args:
            location: Location dictionary
            date_range: Date range dictionary
            
        Raises:
            ValueError: If inputs are invalid
        """
        # Validate location
        if 'latitude' not in location or 'longitude' not in location:
            raise ValueError("Location must contain 'latitude' and 'longitude'")
        
        lat, lon = location['latitude'], location['longitude']
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        # Validate date range
        if 'start_date' not in date_range or 'end_date' not in date_range:
            raise ValueError("Date range must contain 'start_date' and 'end_date'")
        
        try:
            start_date = datetime.fromisoformat(date_range['start_date'])
            end_date = datetime.fromisoformat(date_range['end_date'])
            
            if start_date >= end_date:
                raise ValueError("Start date must be before end date")
            
            # Check date range is not too large (e.g., max 1 year)
            if (end_date - start_date).days > 365:
                raise ValueError("Date range cannot exceed 1 year")
                
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError("Dates must be in ISO format (YYYY-MM-DD)")
            raise
