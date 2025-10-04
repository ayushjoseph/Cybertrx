"""
Architecture tests to verify SOLID principles compliance
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta

from skyluxe.interfaces.data_source import IDataSource
from skyluxe.interfaces.metric_calculator import IMetricCalculator
from skyluxe.calculators.temperature_calculator import TemperatureCalculator
from skyluxe.calculators.precipitation_calculator import PrecipitationCalculator
from skyluxe.services.climate_analysis_service import ClimateAnalysisService


class MockDataSource(IDataSource):
    """Mock data source for testing - follows LSP"""
    
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
    
    def fetch_data(self, location, date_range):
        if self.should_fail:
            raise Exception("Mock data source failure")
        
        # Create mock data
        dates = pd.date_range(
            start=date_range['start_date'],
            end=date_range['end_date'],
            freq='D'
        )
        
        data = pd.DataFrame({
            'date': dates,
            'temperature_2m': [20 + i * 0.1 for i in range(len(dates))],
            'precipitation': [0.5 + i * 0.01 for i in range(len(dates))]
        })
        
        return data
    
    def is_available(self):
        return not self.should_fail


class TestSOLIDCompliance:
    """Test SOLID principles compliance"""
    
    def test_dependency_inversion_principle(self):
        """Test that services depend on abstractions, not concretions"""
        # Create mock data source (abstraction)
        mock_data_source = MockDataSource()
        
        # Create calculators (abstractions)
        temp_calculator = TemperatureCalculator()
        precip_calculator = PrecipitationCalculator()
        
        # Service depends on abstractions (DIP)
        service = ClimateAnalysisService(
            data_source=mock_data_source,
            calculators=[temp_calculator, precip_calculator]
        )
        
        # Should work with any IDataSource implementation
        assert isinstance(service.data_source, IDataSource)
        assert all(isinstance(calc, IMetricCalculator) for calc in service.calculators)
    
    def test_liskov_substitution_principle(self):
        """Test that derived classes can substitute base classes"""
        # Mock data source should work as IDataSource
        mock_source = MockDataSource()
        assert isinstance(mock_source, IDataSource)
        
        # Calculators should work as IMetricCalculator
        temp_calc = TemperatureCalculator()
        precip_calc = PrecipitationCalculator()
        
        assert isinstance(temp_calc, IMetricCalculator)
        assert isinstance(precip_calc, IMetricCalculator)
    
    def test_open_closed_principle(self):
        """Test that system is open for extension, closed for modification"""
        # Create service with existing calculators
        mock_source = MockDataSource()
        temp_calc = TemperatureCalculator()
        precip_calc = PrecipitationCalculator()
        
        service = ClimateAnalysisService(
            data_source=mock_source,
            calculators=[temp_calc, precip_calc]
        )
        
        # Should be able to add new calculators without modifying existing code
        # (This would be done by updating DI configuration)
        original_calculators = len(service.calculators)
        assert original_calculators == 2
        
        # Adding new calculator doesn't require modifying existing classes
        # This demonstrates OCP compliance
    
    def test_single_responsibility_principle(self):
        """Test that each class has a single responsibility"""
        # TemperatureCalculator only handles temperature calculations
        temp_calc = TemperatureCalculator()
        assert temp_calc.get_metric_name() == "Temperature Analysis"
        
        # PrecipitationCalculator only handles precipitation calculations
        precip_calc = PrecipitationCalculator()
        assert precip_calc.get_metric_name() == "Precipitation Analysis"
        
        # ClimateAnalysisService only orchestrates the analysis
        mock_source = MockDataSource()
        service = ClimateAnalysisService(
            data_source=mock_source,
            calculators=[temp_calc, precip_calc]
        )
        
        # Service should coordinate, not implement calculations
        assert hasattr(service, 'analyze_climate')
        assert hasattr(service, 'get_available_metrics')
    
    def test_interface_segregation_principle(self):
        """Test that interfaces are focused and not bloated"""
        # IDataSource has minimal, focused interface
        data_source_methods = [method for method in dir(IDataSource) 
                              if not method.startswith('_')]
        assert len(data_source_methods) == 2  # fetch_data, is_available
        
        # IMetricCalculator has focused interface
        calculator_methods = [method for method in dir(IMetricCalculator) 
                             if not method.startswith('_')]
        assert len(calculator_methods) == 3  # calculate, get_metric_name, get_metric_units
    
    def test_end_to_end_analysis(self):
        """Test complete analysis workflow"""
        # Setup
        mock_source = MockDataSource()
        temp_calc = TemperatureCalculator()
        precip_calc = PrecipitationCalculator()
        
        service = ClimateAnalysisService(
            data_source=mock_source,
            calculators=[temp_calc, precip_calc]
        )
        
        # Test data
        location = {'latitude': 40.7128, 'longitude': -74.0060}
        date_range = {'start_date': '2023-01-01', 'end_date': '2023-01-07'}
        
        # Perform analysis
        result = service.analyze_climate(location, date_range)
        
        # Verify results
        assert 'location' in result
        assert 'date_range' in result
        assert 'metrics' in result
        assert len(result['metrics']) == 2  # Temperature and precipitation
        
        # Check temperature metrics
        temp_metrics = next(m for m in result['metrics'] 
                          if m['metric_name'] == 'Temperature Analysis')
        assert 'mean_temperature' in temp_metrics
        
        # Check precipitation metrics
        precip_metrics = next(m for m in result['metrics'] 
                             if m['metric_name'] == 'Precipitation Analysis')
        assert 'total_precipitation' in precip_metrics
    
    def test_error_handling(self):
        """Test error handling in the system"""
        # Test with failing data source
        failing_source = MockDataSource(should_fail=True)
        temp_calc = TemperatureCalculator()
        
        service = ClimateAnalysisService(
            data_source=failing_source,
            calculators=[temp_calc]
        )
        
        location = {'latitude': 40.7128, 'longitude': -74.0060}
        date_range = {'start_date': '2023-01-01', 'end_date': '2023-01-07'}
        
        result = service.analyze_climate(location, date_range)
        
        # Should handle error gracefully
        assert 'error' in result
        assert 'Data source is currently unavailable' in result['error']
