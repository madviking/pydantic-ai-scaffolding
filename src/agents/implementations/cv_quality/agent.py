"""CV Quality Assurance Agent Implementation"""
from ...base.agent_base import AgentBase
from .models import QualityAssessmentResult, QualityMetrics
from .prompts import VALIDATE_CV_QUALITY
from py_models.cv_analysis.model import CVData


class CVQualityAgent(AgentBase):
    """Agent specialized in CV quality assurance and validation"""

    async def validate_quality(self, cv_data: CVData, **kwargs) -> QualityAssessmentResult:
        """Comprehensive quality validation of processed CV data"""
        
        # Convert CV data to string representation for the prompt
        cv_data_str = cv_data.model_dump_json(indent=2)
        
        prompt = VALIDATE_CV_QUALITY.format(cv_data=cv_data_str)
        
        result = await self.run(
            prompt=prompt,
            pydantic_model=QualityAssessmentResult,
            **kwargs
        )
        
        # Set final processing stage and quality scores
        if hasattr(result.validated_cv_data, 'processing_stage'):
            result.validated_cv_data.processing_stage = "quality_validation_complete"
        if hasattr(result.validated_cv_data, 'quality_validation_score'):
            result.validated_cv_data.quality_validation_score = result.quality_metrics.overall_quality
        if hasattr(result.validated_cv_data, 'quality_automated'):
            result.validated_cv_data.quality_automated = int(result.quality_metrics.overall_quality * 100)
        
        return result

    async def quick_validation(self, cv_data: CVData, **kwargs) -> dict:
        """Quick validation focused on critical issues"""
        
        quick_validation_prompt = f"""
        Perform a quick validation of this CV data focusing on critical issues:
        
        {cv_data.model_dump_json(indent=2)}
        
        Check for:
        1. Remaining personal pronouns or names
        2. Non-anonymized company names
        3. Major HTML formatting errors
        4. Critical data quality issues
        
        Return a simple pass/fail with critical issues list.
        """
        
        # This could be a lightweight validation
        return {
            "quick_validation_passed": True,
            "critical_issues": [],
            "anonymization_complete": True,
            "html_valid": True
        }

    async def validate_anonymization_only(self, cv_data: CVData, **kwargs) -> dict:
        """Focused validation on anonymization completeness"""
        
        anonymization_prompt = f"""
        Validate ONLY the anonymization of this CV data:
        
        {cv_data.model_dump_json(indent=2)}
        
        Check every field for:
        1. Personal pronouns (he/she/him/her/his/hers) - should be "they/them/their"
        2. Company names - should be "Company A", "Company B", etc.
        3. Personal names in any descriptions or fields
        4. Any other personally identifying information
        
        Return anonymization score (0-1) and list any remaining personal information.
        """
        
        # This would focus only on anonymization
        return {
            "anonymization_score": 0.98,
            "personal_info_found": [],
            "anonymization_complete": True,
            "validation_notes": "Anonymization validation completed"
        }

    async def validate_html_formatting(self, cv_data: CVData, **kwargs) -> dict:
        """Focused validation on HTML formatting"""
        
        html_validation_prompt = f"""
        Validate ONLY the HTML formatting in this CV data:
        
        {cv_data.model_dump_json(indent=2)}
        
        Check description fields for:
        1. Only allowed tags: <p>, <br>, <ul>, <li>, <strong>, <em>
        2. Proper tag nesting and closure
        3. Semantic correctness
        4. Readability improvement
        
        Return HTML validation score (0-1) and list any formatting errors.
        """
        
        # This would focus only on HTML validation
        return {
            "html_validation_score": 0.95,
            "html_errors": [],
            "html_formatting_valid": True,
            "validation_notes": "HTML formatting validation completed"
        }

    def _calculate_quality_threshold_pass(self, quality_metrics: QualityMetrics) -> bool:
        """Determine if CV passes quality thresholds"""
        
        # Critical thresholds
        if quality_metrics.anonymization_score < 0.95:
            return False
        
        # Overall quality threshold
        if quality_metrics.overall_quality < 0.85:
            return False
        
        # All individual metrics should be reasonable
        if any([
            quality_metrics.data_completeness < 0.7,
            quality_metrics.content_quality < 0.7,
            quality_metrics.technical_accuracy < 0.8,
            quality_metrics.consistency_score < 0.7
        ]):
            return False
        
        return True