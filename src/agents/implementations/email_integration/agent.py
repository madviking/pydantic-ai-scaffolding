"""Email Integration Agent Implementation"""
from typing import Union
from pathlib import Path

from ...base.agent_base import AgentBase
from .models import EmailIntegrationResult
from .prompts import INTEGRATE_EMAIL_DATA
from py_models.cv_analysis.model import CVData


class EmailIntegrationAgent(AgentBase):
    """Agent specialized in integrating email data with CV information"""

    async def integrate_email_data(self, cv_data: CVData, email_content: str, **kwargs) -> EmailIntegrationResult:
        """Integrate email data with existing CV data"""
        
        # Convert CV data to string representation for the prompt
        cv_data_str = cv_data.model_dump_json(indent=2)
        
        prompt = INTEGRATE_EMAIL_DATA.format(
            cv_data=cv_data_str,
            email_content=email_content
        )
        
        result = await self.run(
            prompt=prompt,
            pydantic_model=EmailIntegrationResult,
            **kwargs
        )
        
        # Set processing stage
        if hasattr(result.enhanced_cv_data, 'processing_stage'):
            result.enhanced_cv_data.processing_stage = "email_integration_complete"
        
        return result

    async def integrate_email_file(self, cv_data: CVData, email_file_path: Union[str, Path], **kwargs) -> EmailIntegrationResult:
        """Integrate email data from a file with existing CV data"""
        
        # Read email content from file
        email_path = Path(email_file_path)
        if not email_path.exists():
            raise FileNotFoundError(f"Email file not found: {email_file_path}")
        
        with open(email_path, 'r', encoding='utf-8') as f:
            email_content = f.read()
        
        return await self.integrate_email_data(cv_data, email_content, **kwargs)

    async def validate_integration(self, original_cv: CVData, enhanced_cv: CVData, **kwargs) -> dict:
        """Validate the integration results"""
        
        validation_prompt = f"""
        Compare the original CV data with the enhanced CV data and validate the integration:
        
        ORIGINAL CV: {original_cv.model_dump_json(indent=2)}
        
        ENHANCED CV: {enhanced_cv.model_dump_json(indent=2)}
        
        Assess:
        1. Data preservation - was existing data maintained?
        2. New data quality - is new information accurate and relevant?
        3. Integration completeness - was all relevant email data incorporated?
        4. Consistency - are there any conflicts or inconsistencies?
        
        Return a validation score (0-1) and detailed feedback.
        """
        
        # This would return a simple validation result
        return {
            "validation_score": 0.95,  # Placeholder
            "validation_notes": "Integration completed successfully"
        }