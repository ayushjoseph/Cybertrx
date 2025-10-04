"""
Skyluxe Main Application
Entry point with dependency injection setup
Following Dependency Inversion Principle (DIP)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from skyluxe.core.container import DIContainer
from skyluxe.core.config import ConfigManager
from skyluxe.api.analysis import router as analysis_router
from skyluxe.clients.nasa_power_client import NasaPowerClient
from skyluxe.calculators.temperature_calculator import TemperatureCalculator
from skyluxe.calculators.precipitation_calculator import PrecipitationCalculator
from skyluxe.services.climate_analysis_service import ClimateAnalysisService


# Global DI container
container = DIContainer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Sets up dependency injection on startup.
    """
    # Setup dependency injection
    setup_dependency_injection()
    yield
    # Cleanup (if needed)
    pass


def setup_dependency_injection():
    """
    Configure dependency injection container.
    This is where we wire up all our dependencies following DIP.
    """
    # Get configuration
    config_manager = ConfigManager()
    config = config_manager.get_config()
    
    # Register data source
    nasa_client = NasaPowerClient(config.api)
    container.register_singleton(NasaPowerClient, nasa_client)
    
    # Register calculators
    temp_calculator = TemperatureCalculator()
    precip_calculator = PrecipitationCalculator()
    container.register_singleton(TemperatureCalculator, temp_calculator)
    container.register_singleton(PrecipitationCalculator, precip_calculator)
    
    # Register service with dependencies
    def create_analysis_service():
        data_source = container.get(NasaPowerClient)
        calculators = [
            container.get(TemperatureCalculator),
            container.get(PrecipitationCalculator)
        ]
        return ClimateAnalysisService(data_source, calculators)
    
    container.register_factory(ClimateAnalysisService, create_analysis_service)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    # Get configuration
    config_manager = ConfigManager()
    config = config_manager.get_config()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO if not config.debug else logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create FastAPI app
    app = FastAPI(
        title="Skyluxe Climate Analysis API",
        description="A SOLID-compliant climate analysis platform",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(analysis_router)
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Skyluxe Climate Analysis API",
            "version": "1.0.0",
            "docs": "/docs"
        }
    
    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    config_manager = ConfigManager()
    config = config_manager.get_config()
    
    uvicorn.run(
        "skyluxe.main:app",
        host=config.host,
        port=config.port,
        reload=config.debug
    )
