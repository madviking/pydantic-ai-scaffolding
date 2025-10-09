"""CV Anonymization Agent Models"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, ClassVar
import os
from py_models.base import BasePyModel
from py_models.cv_analysis.model import CVData


class AnonymizationResult(BasePyModel):
    """Result from CV anonymization and enhancement processing"""
    
    # Class metadata
    MODULE_NAME: ClassVar[str] = "anonymization_result"
    TEST_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "tests")
    REPORT_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "reports")
    
    anonymized_cv_data: CVData = Field(description="Anonymized and enhanced CV data")
    anonymization_confidence: float = Field(description="Confidence in anonymization completeness (0-1)")
    company_mapping: Dict[str, str] = Field(description="Mapping of original to anonymized company names")
    changes_made: List[str] = Field(description="List of changes made during processing")
    enhancement_notes: Optional[str] = Field(description="Notes about content enhancement")
    spelling_corrections: Optional[List[str]] = Field(description="Spelling corrections made")
    grammar_improvements: Optional[List[str]] = Field(description="Grammar improvements made")
    anonymization_applied: bool = Field(description="Whether anonymization was successfully applied")