"""Email Integration Agent Models"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, ClassVar
import os
from py_models.base import BasePyModel
from py_models.cv_analysis.model import CVData


class EmailIntegrationResult(BasePyModel):
    """Result from email integration processing"""
    
    # Class metadata
    MODULE_NAME: ClassVar[str] = "email_integration_result"
    TEST_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "tests")
    REPORT_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "reports")
    
    enhanced_cv_data: CVData = Field(description="CV data enhanced with email information")
    integration_confidence: float = Field(description="Confidence in email integration (0-1)")
    email_insights: Optional[List[str]] = Field(description="Key insights extracted from email")
    integration_notes: Optional[str] = Field(description="Notes about the integration process")
    data_conflicts: Optional[List[str]] = Field(description="Any conflicts found between CV and email data")
    new_information_added: Optional[List[str]] = Field(description="New information added from email")