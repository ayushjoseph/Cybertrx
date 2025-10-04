"""
Analysis API endpoints
Following Single Responsibility Principle (SRP)
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import logging

from skyluxe.services.climate_analysis_service import ClimateAnalysisService


# Pydantic models for request/response validation
class LocationRequest(BaseModel):
    """Location request model"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude between -90 and 90")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude between -180 and 180")


class DateRangeRequest(BaseModel):
    """Date range request model"""
    start_date: str = Field(..., description="Start date in ISO format (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date in ISO format (YYYY-MM-DD)")


class AnalysisRequest(BaseModel):
    """Complete analysis request model"""
    location: LocationRequest
    date_range: DateRangeRequest


class MetricInfo(BaseModel):
    """Metric information model"""
    name: str
    units: str


class AnalysisResponse(BaseModel):
    """Analysis response model"""
    location: Dict[str, float]
    date_range: Dict[str, str]
    data_summary: Dict[str, Any]
    metrics: List[Dict[str, Any]]


# Create router
router = APIRouter(prefix="/analysis", tags=["analysis"])
logger = logging.getLogger(__name__)


def get_analysis_service() -> ClimateAnalysisService:
    """
    Dependency injection for ClimateAnalysisService.
    Gets service from the global DI container.
    """
    from skyluxe.main import container
    return container.get(ClimateAnalysisService)


@router.post("/", response_model=AnalysisResponse)
async def analyze_climate(
    request: AnalysisRequest,
    service: ClimateAnalysisService = Depends(get_analysis_service)
) -> AnalysisResponse:
    """
    Perform climate analysis for a given location and date range.
    
    Args:
        request: Analysis request containing location and date range
        service: Injected climate analysis service
        
    Returns:
        AnalysisResponse: Climate analysis results
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        logger.info(f"Received analysis request for {request.location}")
        
        # Convert request to service format
        location = {
            'latitude': request.location.latitude,
            'longitude': request.location.longitude
        }
        date_range = {
            'start_date': request.date_range.start_date,
            'end_date': request.date_range.end_date
        }
        
        # Perform analysis
        result = service.analyze_climate(location, date_range)
        
        # Check for errors
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return AnalysisResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/metrics", response_model=List[MetricInfo])
async def get_available_metrics(
    service: ClimateAnalysisService = Depends(get_analysis_service)
) -> List[MetricInfo]:
    """
    Get list of available climate metrics.
    
    Args:
        service: Injected climate analysis service
        
    Returns:
        List[MetricInfo]: Available metrics
    """
    try:
        metrics = service.get_available_metrics()
        return [MetricInfo(**metric) for metric in metrics]
        
    except Exception as e:
        logger.error(f"Failed to get available metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict[str, str]: Health status
    """
    return {"status": "healthy", "service": "climate-analysis-api"}
