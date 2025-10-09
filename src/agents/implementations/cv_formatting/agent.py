"""CV Formatting Agent Implementation"""
import re
from ...base.agent_base import AgentBase
from .models import FormattingResult
from .prompts import FORMAT_HTML_DESCRIPTIONS
from py_models.cv_analysis.model import CVData


class CVFormattingAgent(AgentBase):
    """Agent specialized in HTML formatting of CV description fields"""

    async def format_html_descriptions(self, cv_data: CVData, **kwargs) -> FormattingResult:
        """Apply HTML formatting to CV description fields"""
        
        # Convert CV data to string representation for the prompt
        cv_data_str = cv_data.model_dump_json(indent=2)
        
        prompt = FORMAT_HTML_DESCRIPTIONS.format(cv_data=cv_data_str)
        
        result = await self.run(
            prompt=prompt,
            pydantic_model=FormattingResult,
            **kwargs
        )
        
        # Validate HTML formatting
        validation_result = self._validate_html_formatting(result.formatted_cv_data)
        result.html_validation_passed = validation_result['valid']
        
        # Set processing stage
        if hasattr(result.formatted_cv_data, 'processing_stage'):
            result.formatted_cv_data.processing_stage = "html_formatting_complete"
        if hasattr(result.formatted_cv_data, 'html_formatting_applied'):
            result.formatted_cv_data.html_formatting_applied = True
        
        return result

    def _validate_html_formatting(self, cv_data: CVData) -> dict:
        """Validate HTML formatting in CV description fields"""
        
        allowed_tags = ['<p>', '</p>', '<br>', '<ul>', '</ul>', '<li>', '</li>', '<strong>', '</strong>', '<em>', '</em>']
        validation_errors = []
        
        # Fields to check for HTML content
        description_fields = []
        
        # Check summary fields
        if cv_data.summary:
            description_fields.append(('summary', cv_data.summary))
        if cv_data.ai_summary:
            description_fields.append(('ai_summary', cv_data.ai_summary))
        
        # Check position descriptions
        if cv_data.positions:
            for i, position in enumerate(cv_data.positions):
                if position.Description:
                    description_fields.append((f'positions[{i}].Description', position.Description))
        
        # Check education descriptions
        if cv_data.education:
            for i, edu in enumerate(cv_data.education):
                if edu.Description:
                    description_fields.append((f'education[{i}].Description', edu.Description))
        
        # Check project descriptions
        if cv_data.projects:
            for i, project in enumerate(cv_data.projects):
                if project.Description:
                    description_fields.append((f'projects[{i}].Description', project.Description))
        
        # Validate each field
        for field_name, content in description_fields:
            if self._contains_html(content):
                field_errors = self._validate_field_html(content, allowed_tags)
                if field_errors:
                    validation_errors.extend([f"{field_name}: {error}" for error in field_errors])
        
        return {
            'valid': len(validation_errors) == 0,
            'errors': validation_errors,
            'fields_checked': len(description_fields)
        }
    
    def _contains_html(self, text: str) -> bool:
        """Check if text contains HTML tags"""
        return bool(re.search(r'<[^>]+>', text))
    
    def _validate_field_html(self, content: str, allowed_tags: list) -> list:
        """Validate HTML in a specific field"""
        errors = []
        
        # Find all HTML tags
        html_tags = re.findall(r'<[^>]+>', content)
        
        # Check for disallowed tags
        for tag in html_tags:
            if tag not in allowed_tags:
                errors.append(f"Disallowed HTML tag: {tag}")
        
        # Check for proper tag pairing (basic validation)
        tag_stack = []
        for tag in html_tags:
            if tag == '<br>':  # Self-closing tag
                continue
            elif tag.startswith('</'):  # Closing tag
                tag_name = tag[2:-1]
                if tag_stack and tag_stack[-1] == tag_name:
                    tag_stack.pop()
                else:
                    errors.append(f"Unmatched closing tag: {tag}")
            else:  # Opening tag
                tag_name = tag[1:-1]
                tag_stack.append(tag_name)
        
        # Check for unclosed tags
        if tag_stack:
            errors.append(f"Unclosed tags: {tag_stack}")
        
        return errors

    async def validate_formatting_only(self, cv_data: CVData, **kwargs) -> dict:
        """Validate existing HTML formatting without making changes"""
        
        validation_result = self._validate_html_formatting(cv_data)
        
        return {
            "validation_passed": validation_result['valid'],
            "validation_errors": validation_result['errors'],
            "fields_checked": validation_result['fields_checked'],
            "validation_notes": "HTML formatting validation completed"
        }