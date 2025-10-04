"""
Dependency Injection Container
Following Dependency Inversion Principle (DIP)
"""
from typing import Dict, Any, List, Type
from skyluxe.interfaces.data_source import IDataSource
from skyluxe.interfaces.metric_calculator import IMetricCalculator
from skyluxe.interfaces.exporter import ITabularExporter, IAnalysisExporter


class DIContainer:
    """
    Simple Dependency Injection container for managing dependencies.
    Enforces Dependency Inversion Principle by managing concrete implementations.
    """
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, callable] = {}
    
    def register_singleton(self, interface: Type, implementation: Any):
        """
        Register a singleton service.
        
        Args:
            interface: The interface/abstract class
            implementation: The concrete implementation
        """
        key = interface.__name__
        self._services[key] = implementation
    
    def register_factory(self, interface: Type, factory: callable):
        """
        Register a factory function for creating instances.
        
        Args:
            interface: The interface/abstract class
            factory: Function that creates the instance
        """
        key = interface.__name__
        self._factories[key] = factory
    
    def get(self, interface: Type) -> Any:
        """
        Get an instance of the requested interface.
        
        Args:
            interface: The interface/abstract class
            
        Returns:
            Instance of the concrete implementation
        """
        key = interface.__name__
        
        if key in self._services:
            return self._services[key]
        
        if key in self._factories:
            return self._factories[key]()
        
        raise ValueError(f"No registration found for {interface.__name__}")
    
    def get_all(self, interface: Type) -> List[Any]:
        """
        Get all registered instances of an interface.
        Useful for getting all metric calculators.
        
        Args:
            interface: The interface/abstract class
            
        Returns:
            List of instances
        """
        key = interface.__name__
        if key in self._services:
            return [self._services[key]]
        return []
