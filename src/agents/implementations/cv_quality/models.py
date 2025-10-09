"""CV Quality Assurance Agent Models"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from py_models.base import BasePyModel
from py_models.cv_analysis.model import CVData


class QualityMetrics(BaseModel):
    """Detailed quality metrics for CV processing"""
    
    data_completeness: float = Field(description="Completeness of extracted data (0-1)")
    anonymization_score: float = Field(description="Anonymization completeness score (0-1)")
    content_quality: float = Field(description="Content quality and readability score (0-1)")
    html_formatting_score: float = Field(description="HTML formatting quality score (0-1)")
    technical_accuracy: float = Field(description="Technical information accuracy score (0-1)")
    consistency_score: float = Field(description="Internal consistency score (0-1)")
    overall_quality: float = Field(description="Overall quality score (0-1)")


class QualityAssessmentResult(BasePyModel):
    """Result from CV quality assurance processing"""
    
    validated_cv_data: CVData = Field(description="Validated and potentially corrected CV data")
    quality_metrics: QualityMetrics = Field(description="Detailed quality metrics")
    validation_passed: bool = Field(description="Whether CV passed quality validation")
    quality_issues: List[str] = Field(description="List of quality issues identified")
    recommendations: List[str] = Field(description="Recommendations for improvement")
    validation_notes: Optional[str] = Field(description="Detailed validation notes")
    personal_info_detected: List[str] = Field(description="Any remaining personal information detected")
    html_validation_errors: List[str] = Field(description="HTML formatting validation errors")
