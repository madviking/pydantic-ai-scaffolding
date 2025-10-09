# CV Parsing Agentic Flow - Implementation Brief

## Overview

This document outlines the implementation of a comprehensive CV parsing agentic flow that processes CVs through a multi-stage pipeline to extract, anonymize, enhance, and format the data.

## Current State Analysis

### Existing Components
- **CVData Model**: Comprehensive Pydantic model in `src/py_models/cv_analysis/model.py` with detailed fields for CV data extraction
- **Agent Framework**: Robust agent system with base classes, registry, and workflow orchestration
- **Existing Agents**: FileProcessorAgent, TextEditorAgent, FeedbackAgent with YAML configuration
- **AiHelper Integration**: LLM provider abstraction with usage tracking and cost reporting

### Current CV Model Capabilities
- Structured data extraction (education, experience, skills, etc.)
- Technology experience mapping with proficiency levels
- Industry experience tracking
- Assessment and quality metrics
- Version control and AI enhancement fields
- HTML validation for description fields

## Proposed Agentic Flow

### Stage 1: CV Analysis Agent
**Purpose**: Extract structured data from CV using the best possible model for document analysis

**Responsibilities**:
- Parse PDF/image CVs using vision-capable models
- Extract text content and structure it according to CVData model
- Identify key sections (experience, education, skills, etc.)
- Generate initial confidence scores and quality metrics

**Model Selection**: Google Gemini 2.5 Pro (excellent for document/image analysis) with fallback to GPT-4o Vision

**Output**: Populated CVData model with raw extracted information

### Stage 2: Anonymization and Enhancement Agent  
**Purpose**: Anonymize personal information and improve content quality

**Responsibilities**:
- Replace all personal pronouns (he/she/name) with "they"
- Anonymize company names using consistent placeholder system (Company A, Company B, etc.)
- Fix spelling and grammar errors
- Improve summary and description content while avoiding adjective overuse
- Maintain technical accuracy and factual content
- Preserve quantifiable achievements and metrics
- Populate additional fields if they can be inferred (for example project specific technology list)

**Model Selection**: Claude 3.5 Sonnet (excellent for text editing and maintaining context) with fallback to GPT-4o

**Output**: Enhanced CVData model with anonymized and improved content

### Stage 3: HTML Formatting Agent
**Purpose**: Apply proper HTML formatting to description fields

**Responsibilities**:
- Format job descriptions, education descriptions, and project descriptions
- Use only allowed HTML tags: `<p>`, `<br>`, `<ul>`, `<li>`, `<strong>`, `<em>` (note: italic should be `<em>`)
- Structure content for better readability
- Maintain semantic meaning and hierarchy
- Validate HTML compliance

**Model Selection**: GPT-4o Mini (efficient for structured formatting tasks) with fallback to Claude Haiku

**Output**: Final CVData model with properly formatted HTML descriptions

### Stage 4: Quality Assurance Agent (Optional)
**Purpose**: Validate the entire pipeline output

**Responsibilities**:
- Verify anonymization completeness
- Check HTML formatting compliance
- Assess content quality and coherence
- Generate quality metrics and confidence scores
- Identify any remaining personal information

**Model Selection**: Claude 3.5 Sonnet for comprehensive analysis

## Implementation Plan

### 1. Create CV Processing Agents

#### CVAnalysisAgent (`src/agents/implementations/cv_analysis/`)
```python
class CVAnalysisAgent(AgentBase):
    async def analyze_cv(self, file_path: str, **kwargs) -> CVData:
        """Extract structured data from CV file"""
    
    async def analyze_cv_text(self, content: str, **kwargs) -> CVData:
        """Extract structured data from CV text content"""
```

#### CVAnonymizationAgent (`src/agents/implementations/cv_anonymization/`)
```python
class CVAnonymizationAgent(AgentBase):
    async def anonymize_and_enhance(self, cv_data: CVData, **kwargs) -> CVData:
        """Anonymize personal info and enhance content quality"""
```

#### CVFormattingAgent (`src/agents/implementations/cv_formatting/`)
```python
class CVFormattingAgent(AgentBase):
    async def format_html_descriptions(self, cv_data: CVData, **kwargs) -> CVData:
        """Apply HTML formatting to description fields"""
```

#### CVQualityAgent (`src/agents/implementations/cv_quality/`)
```python
class CVQualityAgent(AgentBase):
    async def validate_quality(self, cv_data: CVData, **kwargs) -> CVData:
        """Validate and assess final output quality"""
```

### 2. Create CV Processing Workflow

#### CVProcessingWorkflow (`src/agents/workflows/cv_processing_workflow.py`)
```python
class CVProcessingWorkflow(BaseWorkflow):
    async def execute(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """Execute complete CV processing pipeline"""
        
        # Stage 1: Analysis
        analysis_result = await self.agents['cv_analysis'].analyze_cv(file_path)
        
        # Stage 2: Anonymization & Enhancement  
        enhanced_result = await self.agents['cv_anonymization'].anonymize_and_enhance(analysis_result)
        
        # Stage 3: HTML Formatting
        formatted_result = await self.agents['cv_formatting'].format_html_descriptions(enhanced_result)
        
        # Stage 4: Quality Validation (optional)
        if self.get_config_value('quality_validation', True):
            final_result = await self.agents['cv_quality'].validate_quality(formatted_result)
        else:
            final_result = formatted_result
            
        return {
            'cv_data': final_result,
            'processing_report': self._generate_report()
        }
```

### 3. Configuration Updates

Add to `src/agents/config/agents.yaml`:

```yaml
agents:
  cv_analysis:
    name: "CV Analysis Specialist"
    description: "Extracts structured data from CV documents with high accuracy"
    default_model: "google/gemini-2.5-pro-preview-03-25"
    default_provider: "google"
    fallback_model: "openai/gpt-4o"
    fallback_provider: "openai"
    capabilities:
      - document_analysis
      - vision_processing
      - structured_extraction
    system_prompt: |
      You are a CV analysis specialist. Extract comprehensive structured data from CVs.
      Focus on accuracy, completeness, and proper categorization of information.
      Handle various CV formats and layouts with precision.

  cv_anonymization:
    name: "CV Anonymization & Enhancement"
    description: "Anonymizes personal information and enhances content quality"
    default_model: "anthropic/claude-3-5-sonnet-latest"
    default_provider: "anthropic"
    fallback_model: "openai/gpt-4o"
    fallback_provider: "openai"
    capabilities:
      - text_anonymization
      - content_enhancement
      - grammar_correction
    system_prompt: |
      You are a content anonymization and enhancement specialist.
      Replace personal pronouns with 'they', anonymize companies consistently,
      fix grammar/spelling, and improve content while preserving factual accuracy.

  cv_formatting:
    name: "CV HTML Formatter"
    description: "Applies proper HTML formatting to CV description fields"
    default_model: "openai/gpt-4o-mini"
    default_provider: "openai"
    fallback_model: "anthropic/claude-3-haiku"
    fallback_provider: "anthropic"
    capabilities:
      - html_formatting
      - content_structuring
    system_prompt: |
      You are an HTML formatting specialist for CV descriptions.
      Use only allowed tags: <p>, <br>, <ul>, <li>, <strong>, <em>.
      Structure content for readability while maintaining semantic meaning.

  cv_quality:
    name: "CV Quality Assurance"
    description: "Validates CV processing quality and completeness"
    default_model: "anthropic/claude-3-5-sonnet-latest"
    default_provider: "anthropic"
    fallback_model: "openai/gpt-4o"
    fallback_provider: "openai"
    capabilities:
      - quality_assessment
      - validation
      - metrics_generation
    system_prompt: |
      You are a quality assurance specialist for CV processing.
      Verify anonymization, HTML compliance, content quality, and generate metrics.

workflows:
  cv_processing:
    description: "Complete CV processing pipeline with anonymization and formatting"
    agents:
      - cv_analysis
      - cv_anonymization
      - cv_formatting
      - cv_quality
    max_iterations: 1
    quality_threshold: 0.85
    quality_validation: true
```

### 4. Enhanced Model Specifications

Update CVData model to include:

```python
# Additional fields for tracking processing
processing_stage: Optional[str] = Field(description="Current processing stage")
anonymization_applied: Optional[bool] = Field(description="Whether anonymization was applied")
html_formatting_applied: Optional[bool] = Field(description="Whether HTML formatting was applied")
company_mapping: Optional[Dict[str, str]] = Field(description="Original to anonymized company name mapping")
quality_validation_score: Optional[float] = Field(description="Final quality validation score")
```

Make sure that all fields are marked as optional where appropriate to allow for partial processing results. 

### 5. Testing Strategy

#### Unit Tests for Each Agent
- CV extraction accuracy with sample CVs
- Anonymization completeness verification
- HTML formatting validation
- Quality metrics calculation

#### Integration Tests
- End-to-end workflow execution
- Model fallback scenarios
- Error handling and recovery
- Performance benchmarking

#### Test Data
- Sample CVs in various formats (PDF, DOCX, images)
- Expected outputs for each processing stage
- Edge cases (malformed CVs, missing sections)

## Missing Elements from Original Brief

Based on your requirements, I've identified and addressed:

1. **Model Selection Strategy**: Specified best models for each stage based on capabilities
2. **Anonymization Scope**: Extended beyond pronouns to include company names with consistent mapping
3. **HTML Tag Specification**: Clarified allowed tags (added `<em>` for italic instead of `<italic>`)
4. **Quality Assurance**: Added validation stage to ensure processing completeness
5. **Workflow Orchestration**: Structured as a proper workflow with configuration
6. **Error Handling**: Implicit through agent fallback mechanisms
7. **Performance Tracking**: Integration with existing usage tracking system

## Next Steps

1. **Review and Approve**: Validate this implementation approach
2. **Implement Agents**: Create the four specialized agents
3. **Build Workflow**: Implement the orchestrating workflow
4. **Configure Models**: Update YAML configuration
5. **Create Tests**: Develop comprehensive test suite
~~6. **Integration**: Connect with existing CLI and API interfaces~~ 

## Success Criteria

- **Accuracy**: >95% extraction accuracy for standard CV fields
- **Anonymization**: 100% removal of personal identifiers
- **Formatting**: Valid HTML in all description fields
- **Quality**: >85% quality threshold on validation metrics
- **Reliability**: Graceful fallback handling for model failures

This implementation provides a robust, scalable solution for CV processing while maintaining the flexibility and quality standards of the existing agent framework.
