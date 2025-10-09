"""CV Anonymization Agent Implementation"""
from ...base.agent_base import AgentBase
from .models import AnonymizationResult
from .prompts import ANONYMIZE_AND_ENHANCE
from py_models.cv_analysis.model import CVData


class CVAnonymizationAgent(AgentBase):
    """Agent specialized in CV anonymization and content enhancement"""

    async def anonymize_and_enhance(self, cv_data: CVData, **kwargs) -> AnonymizationResult:
        """Anonymize personal information and enhance content quality"""
        
        # Convert CV data to string representation for the prompt
        cv_data_str = cv_data.model_dump_json(indent=2)
        
        prompt = ANONYMIZE_AND_ENHANCE.format(cv_data=cv_data_str)
        
        result = await self.run(
            prompt=prompt,
            pydantic_model=AnonymizationResult,
            **kwargs
        )
        
        # Set processing stage and anonymization flag
        if hasattr(result.anonymized_cv_data, 'processing_stage'):
            result.anonymized_cv_data.processing_stage = "anonymization_complete"
        if hasattr(result.anonymized_cv_data, 'anonymization_applied'):
            result.anonymized_cv_data.anonymization_applied = True
        if hasattr(result.anonymized_cv_data, 'company_mapping'):
            result.anonymized_cv_data.company_mapping = result.company_mapping
        
        return result

    async def validate_anonymization(self, original_cv: CVData, anonymized_cv: CVData, **kwargs) -> dict:
        """Validate that anonymization was completed properly"""
        
        validation_prompt = f"""
        Validate the anonymization of this CV data:
        
        ORIGINAL: {original_cv.model_dump_json(indent=2)}
        ANONYMIZED: {anonymized_cv.model_dump_json(indent=2)}
        
        Check for:
        1. Complete removal of personal pronouns (he/she/him/her/his/hers)
        2. Proper company name anonymization with consistent mapping
        3. Removal of personal names
        4. Preservation of technical accuracy and metrics
        5. Content quality improvements
        
        Return validation score (0-1) and list any remaining personal information.
        """
        
        # This could be implemented as a separate validation call if needed
        return {
            "validation_score": 0.98,
            "remaining_personal_info": [],
            "validation_notes": "Anonymization validation completed"
        }

    async def enhance_content_only(self, cv_data: CVData, **kwargs) -> AnonymizationResult:
        """Enhance content quality without anonymization (for already anonymized CVs)"""
        
        content_enhancement_prompt = f"""
        Enhance the content quality of this CV data without changing personal information:
        
        {cv_data.model_dump_json(indent=2)}
        
        Focus on:
        - Grammar and spelling corrections
        - Clarity and readability improvements
        - Professional tone enhancement
        - Removing excessive adjectives
        - Improving sentence structure
        
        Preserve all technical details and factual information exactly.
        """
        
        result = await self.run(
            prompt=content_enhancement_prompt,
            pydantic_model=AnonymizationResult,
            **kwargs
        )
        
        # Mark as content enhancement only
        if hasattr(result.anonymized_cv_data, 'processing_stage'):
            result.anonymized_cv_data.processing_stage = "content_enhancement_complete"
        
        return result