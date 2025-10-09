"""CV Processing Workflow Implementation - Refactored"""
from typing import Dict, Any, Optional, Union
from pathlib import Path

from .base_workflow import BaseWorkflow
from py_models.cv_analysis.model import CVData


class CVProcessingWorkflow(BaseWorkflow):
    """Complete CV processing pipeline with analysis, email integration, anonymization, formatting, and quality assurance"""

    def __init__(self, ai_helper, workflow_name: str = "cv_processing"):
        super().__init__(ai_helper, workflow_name)
        self._initialize_agents()

    async def execute(self, cv_file_path: Union[str, Path], email_file_path: Optional[Union[str, Path]] = None, **kwargs) -> Dict[str, Any]:
        """Execute complete CV processing pipeline"""
        self._log(f"Starting CV processing workflow for file: {cv_file_path}", level='info')

        try:
            # Stage 1: CV Analysis
            current_cv_data = await self._execute_stage('analysis', 'cv_analysis', 'analyze_cv', cv_file_path, **kwargs)

            # Stage 2: Email Integration (optional)
            if email_file_path and Path(email_file_path).exists():
                current_cv_data = await self._execute_stage('email_integration', 'email_integration', 'integrate_email_file', current_cv_data, email_file_path, **kwargs)
            else:
                print("Stage 2: Skipping email integration (no email file provided)")
                self.processing_report['warnings'].append('No email file provided for integration')

            # Stage 3: Anonymization & Enhancement
            current_cv_data = await self._execute_stage('anonymization', 'cv_anonymization', 'anonymize_and_enhance', current_cv_data, **kwargs)

            # Stage 4: HTML Formatting
            current_cv_data = await self._execute_stage('formatting', 'cv_formatting', 'format_html_descriptions', current_cv_data, **kwargs)

            # Stage 5: Quality Assurance (if enabled)
            quality_result = None
            if self.get_config_value('quality_validation', True):
                quality_result = await self._execute_stage('quality_validation', 'cv_quality', 'validate_quality', current_cv_data, return_full_result=True, **kwargs)
                current_cv_data = quality_result.validated_cv_data
                self.processing_report['quality_metrics'] = quality_result.quality_metrics.model_dump()

                if not quality_result.validation_passed:
                    self.processing_report['errors'].append('Quality validation failed')
                    self.processing_report['quality_issues'] = quality_result.quality_issues
            else:
                print("Stage 5: Skipping quality validation (disabled in config)")

            # Generate quality-specific report data
            quality_data = {
                'quality_validation': {
                    'validation_passed': quality_result.validation_passed,
                    'quality_metrics': quality_result.quality_metrics.model_dump(),
                    'quality_issues': quality_result.quality_issues,
                    'recommendations': quality_result.recommendations,
                    'personal_info_detected': quality_result.personal_info_detected,
                    'html_validation_errors': quality_result.html_validation_errors
                } if quality_result else None
            }

            return {
                'cv_data': current_cv_data,
                'processing_report': self._generate_report(quality_data),
                'success': True,
                'stages_completed': self.processing_report['stages_completed']
            }

        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            self.processing_report['errors'].append(error_msg)
            self._log(error_msg, level='error')

            return {
                'cv_data': None,
                'processing_report': self._generate_report(),
                'success': False,
                'error': str(e)
            }

    async def execute_partial(self, cv_data: CVData, start_stage: str = 'anonymization', **kwargs) -> Dict[str, Any]:
        """Execute partial workflow starting from a specific stage"""
        current_cv_data = cv_data
        stage_map = {
            'anonymization': ('cv_anonymization', 'anonymize_and_enhance'),
            'formatting': ('cv_formatting', 'format_html_descriptions'),
            'quality': ('cv_quality', 'validate_quality')
        }

        try:
            stages_to_run = list(stage_map.keys())[list(stage_map.keys()).index(start_stage):]

            for stage in stages_to_run:
                agent_name, method_name = stage_map[stage]
                stage_name = 'quality_validation' if stage == 'quality' else stage
                current_cv_data = await self._execute_stage(stage_name, agent_name, method_name, current_cv_data, **kwargs)

            return {
                'cv_data': current_cv_data,
                'processing_report': self._generate_report(),
                'success': True,
                'stages_completed': self.processing_report['stages_completed']
            }

        except Exception as e:
            self.processing_report['errors'].append(f"Partial workflow execution failed: {str(e)}")
            return {
                'cv_data': current_cv_data, 
                'processing_report': self._generate_report(), 
                'success': False, 
                'error': str(e)
            }

    async def validate_prerequisites(self, cv_file_path: Union[str, Path], email_file_path: Optional[Union[str, Path]] = None, **kwargs) -> Dict[str, Any]:
        """Validate that all prerequisites are met for workflow execution"""
        validation_result = await super().validate_prerequisites(**kwargs)

        # Check files exist
        if not Path(cv_file_path).exists():
            validation_result['valid'] = False
            validation_result['errors'].append(f"CV file not found: {cv_file_path}")

        if email_file_path and not Path(email_file_path).exists():
            validation_result['warnings'].append(f"Email file not found: {email_file_path}")

        # Check CV-specific required agents
        required_agents = ['cv_analysis', 'cv_anonymization', 'cv_formatting']
        if self.get_config_value('quality_validation', True):
            required_agents.append('cv_quality')

        for agent_name in required_agents:
            if agent_name not in self.agents:
                validation_result['valid'] = False
                validation_result['errors'].append(f"Required agent not available: {agent_name}")

        return validation_result
