"""CV Analysis Agent Models"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, ClassVar
import os
from py_models.base import BasePyModel
from py_models.cv_analysis.model import CVData


class CVAnalysisResult(BasePyModel):
    """Result from CV analysis processing"""
    
    # Class metadata
    MODULE_NAME: ClassVar[str] = "cv_analysis_result"
    TEST_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "tests")
    REPORT_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "reports")
    
    cv_data: CVData = Field(description="Extracted CV data")
    extraction_confidence: float = Field(description="Confidence in extraction accuracy (0-1)")
    processing_notes: Optional[str] = Field(description="Notes about the extraction process")
    detected_format: Optional[str] = Field(description="Detected CV format (PDF, image, etc.)")
    quality_indicators: Optional[str] = Field(description="Quality metrics for the extraction")
