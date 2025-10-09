"""CV Analysis Agent Implementation"""
from typing import Optional, Union
from pathlib import Path

from ...base.agent_base import AgentBase
from .models import CVAnalysisResult
from .prompts import ANALYZE_CV_DOCUMENT, ANALYZE_CV_TEXT


class CVAnalysisAgent(AgentBase):
    """Agent specialized in CV document analysis and data extraction"""

    async def analyze_cv(self, file_path: Union[str, Path], **kwargs) -> CVAnalysisResult:
        """Extract structured data from CV file"""
        
        result = await self.run(
            prompt=ANALYZE_CV_DOCUMENT,
            pydantic_model=CVAnalysisResult,
            file_path=file_path,
            **kwargs
        )
        
        # Set processing stage
        if hasattr(result.cv_data, 'processing_stage'):
            result.cv_data.processing_stage = "analysis_complete"
        
        return result

    async def analyze_cv_text(self, content: str, **kwargs) -> CVAnalysisResult:
        """Extract structured data from CV text content"""
        
        prompt = ANALYZE_CV_TEXT.format(content=content)
        result = await self.run(
            prompt=prompt,
            pydantic_model=CVAnalysisResult,
            **kwargs
        )
        
        # Set processing stage
        if hasattr(result.cv_data, 'processing_stage'):
            result.cv_data.processing_stage = "analysis_complete"
        
        return result

    async def reanalyze_with_context(self, file_path: Union[str, Path], 
                                   context: str, **kwargs) -> CVAnalysisResult:
        """Re-analyze CV with additional context information"""
        
        enhanced_prompt = f"{ANALYZE_CV_DOCUMENT}\n\nAdditional Context:\n{context}\n\nUse this context to enhance the CV analysis and fill in any gaps in the extracted data."
        
        result = await self.run(
            prompt=enhanced_prompt,
            pydantic_model=CVAnalysisResult,
            file_path=file_path,
            **kwargs
        )
        
        if hasattr(result.cv_data, 'processing_stage'):
            result.cv_data.processing_stage = "analysis_with_context_complete"
        
        return result