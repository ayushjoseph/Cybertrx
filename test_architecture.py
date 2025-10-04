#!/usr/bin/env python3
"""
Architecture Test Script
Quick test to verify SOLID principles compliance
"""
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        # Test core imports
        from skyluxe.interfaces.data_source import IDataSource
        from skyluxe.interfaces.metric_calculator import IMetricCalculator
        from skyluxe.interfaces.exporter import ITabularExporter, IAnalysisExporter
        
        # Test concrete implementations
        from skyluxe.clients.nasa_power_client import NasaPowerClient
        from skyluxe.calculators.temperature_calculator import TemperatureCalculator
        from skyluxe.calculators.precipitation_calculator import PrecipitationCalculator
        
        # Test services
        from skyluxe.services.climate_analysis_service import ClimateAnalysisService
        
        # Test core
        from skyluxe.core.container import DIContainer
        from skyluxe.core.config import ConfigManager
        
        print("All modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"Import failed: {e}")
        return False

def test_solid_compliance():
    """Test SOLID principles compliance"""
    print("Testing SOLID principles compliance...")
    
    try:
        from skyluxe.interfaces.data_source import IDataSource
        from skyluxe.interfaces.metric_calculator import IMetricCalculator
        from skyluxe.calculators.temperature_calculator import TemperatureCalculator
        from skyluxe.calculators.precipitation_calculator import PrecipitationCalculator
        from skyluxe.core.config import ConfigManager
        from skyluxe.clients.nasa_power_client import NasaPowerClient
        
        # Test Dependency Inversion Principle
        config_manager = ConfigManager()
        config = config_manager.get_config()
        
        # Create instances
        nasa_client = NasaPowerClient(config.api)
        temp_calc = TemperatureCalculator()
        precip_calc = PrecipitationCalculator()
        
        # Test that they implement the interfaces (LSP)
        assert isinstance(nasa_client, IDataSource), "NasaPowerClient should implement IDataSource"
        assert isinstance(temp_calc, IMetricCalculator), "TemperatureCalculator should implement IMetricCalculator"
        assert isinstance(precip_calc, IMetricCalculator), "PrecipitationCalculator should implement IMetricCalculator"
        
        print("SOLID principles compliance verified")
        return True
        
    except Exception as e:
        print(f"SOLID compliance test failed: {e}")
        return False

def test_dependency_injection():
    """Test dependency injection container"""
    print("Testing dependency injection...")
    
    try:
        from skyluxe.core.container import DIContainer
        from skyluxe.core.config import ConfigManager
        from skyluxe.clients.nasa_power_client import NasaPowerClient
        from skyluxe.calculators.temperature_calculator import TemperatureCalculator
        from skyluxe.services.climate_analysis_service import ClimateAnalysisService
        
        # Create DI container
        container = DIContainer()
        
        # Register services
        config_manager = ConfigManager()
        config = config_manager.get_config()
        
        nasa_client = NasaPowerClient(config.api)
        temp_calc = TemperatureCalculator()
        
        container.register_singleton(NasaPowerClient, nasa_client)
        container.register_singleton(TemperatureCalculator, temp_calc)
        
        # Test retrieval
        retrieved_client = container.get(NasaPowerClient)
        retrieved_calc = container.get(TemperatureCalculator)
        
        assert retrieved_client is nasa_client, "Should return the same instance"
        assert retrieved_calc is temp_calc, "Should return the same instance"
        
        print("Dependency injection working correctly")
        return True
        
    except Exception as e:
        print(f"Dependency injection test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Skyluxe Architecture Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_solid_compliance,
        test_dependency_injection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Architecture is SOLID-compliant.")
        return 0
    else:
        print("Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
