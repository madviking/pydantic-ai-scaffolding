"""CV Formatting Agent Models"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, ClassVar
import os
from py_models.base import BasePyModel
from py_models.cv_analysis.model import CVData


class FormattingResult(BasePyModel):
    """Result from CV HTML formatting processing"""
    
    # Class metadata
    MODULE_NAME: ClassVar[str] = "formatting_result"
    TEST_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "tests")
    REPORT_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "reports")
    
    formatted_cv_data: CVData = Field(description="CV data with HTML formatted descriptions")
    formatting_confidence: float = Field(description="Confidence in formatting quality (0-1)")
    fields_formatted: List[str] = Field(description="List of fields that received HTML formatting")
    formatting_notes: Optional[str] = Field(description="Notes about the formatting process")
    html_validation_passed: bool = Field(description="Whether HTML validation passed")
    formatting_improvements: Optional[List[str]] = Field(description="Formatting improvements made")