"""
NASA POWER API Client
Concrete implementation of IDataSource
Following Single Responsibility Principle (SRP) and Liskov Substitution Principle (LSP)
"""
import requests
import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta
import logging

from skyluxe.interfaces.data_source import IDataSource
from skyluxe.core.config import APIConfig


class NasaPowerClient(IDataSource):
    """
    NASA POWER API client implementation.
    Follows SRP: Only responsible for fetching data from NASA POWER API
    Follows LSP: Can be substituted for any IDataSource implementation
    """
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._base_url = config.nasa_power_url
        self._timeout = config.nasa_power_timeout
        self._max_retries = config.max_retries
    
    def fetch_data(self, location: Dict[str, float], date_range: Dict[str, str]) -> pd.DataFrame:
        """
        Fetch weather data from NASA POWER API.
        
        Args:
            location: Dictionary with 'latitude' and 'longitude'
            date_range: Dictionary with 'start_date' and 'end_date'
            
        Returns:
            pandas.DataFrame: Weather data in standardized format
        """
        try:
            # Prepare API parameters
            params = self._prepare_api_params(location, date_range)
            
            # Make API request with retries
            response = self._make_request_with_retries(params)
            
            # Parse and standardize the response
            return self._parse_response(response)
            
        except Exception as e:
            self.logger.error(f"Failed to fetch data from NASA POWER: {e}")
            raise
    
    def is_available(self) -> bool:
        """
        Check if NASA POWER API is available.
        
        Returns:
            bool: True if available, False otherwise
        """
        try:
            # Simple health check with minimal parameters
            test_params = {
                'parameters': 'T2M',
                'community': 'RE',
                'longitude': 0,
                'latitude': 0,
                'start': '2023-01-01',
                'end': '2023-01-01',
                'format': 'JSON'
            }
            
            response = requests.get(
                self._base_url,
                params=test_params,
                timeout=5
            )
            return response.status_code == 200
            
        except Exception:
            return False
    
    def _prepare_api_params(self, location: Dict[str, float], date_range: Dict[str, str]) -> Dict[str, Any]:
        """Prepare parameters for NASA POWER API request"""
        return {
            'parameters': 'T2M,T2M_MAX,T2M_MIN,PRECTOT,WS2M,WS2M_MAX,WS2M_MIN,RH2M',
            'community': 'RE',
            'longitude': location['longitude'],
            'latitude': location['latitude'],
            'start': date_range['start_date'],
            'end': date_range['end_date'],
            'format': 'JSON'
        }
    
    def _make_request_with_retries(self, params: Dict[str, Any]) -> requests.Response:
        """Make API request with retry logic"""
        for attempt in range(self._max_retries):
            try:
                response = requests.get(
                    self._base_url,
                    params=params,
                    timeout=self._timeout
                )
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt == self._max_retries - 1:
                    raise
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                continue
    
    def _parse_response(self, response: requests.Response) -> pd.DataFrame:
        """Parse NASA POWER API response into standardized DataFrame"""
        data = response.json()
        
        # Extract the data array
        if 'properties' not in data or 'parameter' not in data['properties']:
            raise ValueError("Invalid response format from NASA POWER API")
        
        parameters = data['properties']['parameter']
        
        # Convert to DataFrame
        df_data = []
        for date, values in parameters.items():
            if isinstance(values, dict):
                row = {'date': date}
                row.update(values)
                df_data.append(row)
        
        df = pd.DataFrame(df_data)
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Standardize column names
        column_mapping = {
            'T2M': 'temperature_2m',
            'T2M_MAX': 'temperature_2m_max',
            'T2M_MIN': 'temperature_2m_min',
            'PRECTOT': 'precipitation',
            'WS2M': 'wind_speed_2m',
            'WS2M_MAX': 'wind_speed_2m_max',
            'WS2M_MIN': 'wind_speed_2m_min',
            'RH2M': 'relative_humidity_2m'
        }
        
        df = df.rename(columns=column_mapping)
        
        return df
