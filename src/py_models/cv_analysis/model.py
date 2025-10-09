from pydantic import BaseModel, Field, constr, field_validator
from typing import Optional, List, Dict, Union, ClassVar, Any
from datetime import datetime, date
from enum import Enum
import os

from py_models.base import BasePyModel


class ProficiencyLevel(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"


class VersionStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    ARCHIVED = "archived"


class Language(BaseModel):
    Language: str = Field(description="The language name in English, e.g., 'English', 'Spanish'")
    Level: Optional[str] = Field(description="Proficiency level from 1-5, where 5 is native/bilingual proficiency")


class Education(BaseModel):
    Degree: Optional[str] = Field(description="Full name of the degree, e.g., 'Master of Science'")
    Majors: Optional[str] = Field(description="Main field of study or specialization")
    School: Optional[str] = Field(description="Full name of the educational institution")
    SchoolType: Optional[str] = Field(description="Type of institution: University, College, etc.")
    StartTime: Optional[str] = Field(description="Start date of education in YYYY-MM format")
    EndTime: Optional[str] = Field(description="End date of education in YYYY-MM format")
    Description: Optional[str] = Field(description="Additional details about the education")
    Location: Optional[str] = Field(description="City and country of the institution")
    Achievements: Optional[List[str]] = Field(description="Notable academic achievements or awards")


class Certificate(BaseModel):
    Title: str = Field(description="Name of the certification or qualification")
    Date: Optional[str] = Field(description="Date of certification in YYYY-MM-DD format")
    Issuer: Optional[str] = Field(description="Organization that issued the certificate")
    ValidUntil: Optional[str] = Field(description="Expiration date if applicable")
    CredentialID: Optional[str] = Field(description="Unique identifier for the certification")
    CredentialURL: Optional[str] = Field(description="Verification URL if available")


class TechnologyExperience(BaseModel):
    name: str = Field(description="Name of the technology, framework, or tool")
    proficiency: Optional[ProficiencyLevel] = Field(description="Current proficiency level: junior, mid, or senior")
    years_of_experience: Optional[float] = Field(description="Total years of experience with this technology")
    last_used: Optional[str] = Field(description="Most recent date this technology was used professionally")
    primary_skill: Optional[bool] = Field(description="Whether this is a primary/core skill")
    versions: Optional[List[str]] = Field(description="Specific versions or variants used")
    context: Optional[str] = Field(description="Main context of usage: backend, frontend, devops, etc.")
    projects: Optional[List[str]] = Field(description="Projects where this technology was used")


class Position(BaseModel):
    Title: str = Field(description="Job title in the organization")
    Current: Optional[str] = Field(description="Whether this is the current position (1 for current)")
    EndDate: Optional[str] = Field(description="End date in YYYY-MM-DD format or empty if current")
    StartDate: Optional[str] = Field(description="Start date in YYYY-MM-DD format")
    Description: Optional[str] = Field(description="Role description with allowed HTML tags only")
    Company: Optional[str] = Field(description="Name of the employer or organization")
    Location: Optional[str] = Field(description="Work location and remote/hybrid status")
    Technologies: Optional[List[str]] = Field(description="Technologies and tools used in this role")
    TeamSize: Optional[int] = Field(description="Size of the immediate team")
    Achievements: Optional[List[str]] = Field(description="Key achievements and contributions")
    ProjectType: Optional[str] = Field(description="Type: greenfield, maintenance, migration")
    Industry: Optional[str] = Field(description="Industry sector of the organization")
    ResponsibilityLevel: Optional[str] = Field(description="Level of responsibility in the role")
    RemoteWork: Optional[bool] = Field(description="Whether the position was remote")


class Project(BaseModel):
    Title: str = Field(description="Name of the project")
    Description: Optional[str] = Field(description="Project description with allowed HTML tags")
    Technologies: Optional[List[str]] = Field(description="Technologies and tools used")
    Role: Optional[str] = Field(description="Role or responsibility in the project")
    TeamSize: Optional[int] = Field(description="Number of team members")
    StartDate: Optional[str] = Field(description="Project start date in YYYY-MM-DD format")
    EndDate: Optional[str] = Field(description="Project end date in YYYY-MM-DD format")
    Achievements: Optional[List[str]] = Field(description="Measurable achievements and outcomes")
    Industry: Optional[str] = Field(description="Industry sector of the project")
    ProjectType: Optional[str] = Field(description="Type: greenfield, maintenance, migration")
    Scale: Optional[str] = Field(description="Project scale: startup, enterprise, etc.")
    Challenges: Optional[List[str]] = Field(description="Major challenges overcome")


class IndustryExperience(BaseModel):
    name: str = Field(description="Name of the industry sector")
    total_years: Optional[float] = Field(description="Total years of experience in this industry")
    last_exposure: Optional[str] = Field(description="Most recent exposure to this industry")
    expertise_level: Optional[str] = Field(description="Level of expertise in this industry")
    projects: Optional[List[str]] = Field(description="Projects in this industry")
    key_achievements: Optional[List[str]] = Field(description="Notable achievements in this industry")


class Assessment(BaseModel):
    score: Optional[int] = Field(description="Assessment score (typically 0-100)")
    date: Optional[str] = Field(description="Date of assessment")
    assessor: Optional[str] = Field(description="Person or system that performed the assessment")
    comments: Optional[str] = Field(description="Assessment comments or feedback")
    category: Optional[str] = Field(description="Assessment category or type")
    verification_method: Optional[str] = Field(description="How the assessment was verified")


class Question(BaseModel):
    question: str = Field(description="The question text")
    answer: Optional[str] = Field(description="The provided answer")
    category: Optional[str] = Field(description="Question category or topic")
    context: Optional[str] = Field(description="Context in which the question was asked")
    source: Optional[str] = Field(description="Source of the question")
    confidence_score: Optional[float] = Field(description="Confidence in the answer (0-1)")


class CVData(BasePyModel):
    # Class metadata
    MODULE_NAME: ClassVar[str] = "cv_analysis"
    TEST_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "tests")
    REPORT_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "reports")
    
    # Basic Information
    candidate_name: Optional[str] = Field(description="Full name of the candidate")
    email: Optional[str] = Field(description="Primary email address")
    title: Optional[str] = Field(description="Professional title")
    current_job_title: Optional[str] = Field(description="Current job title")
    current_employer: Optional[str] = Field(description="Current employer name")
    experience_in_years: Optional[str] = Field(description="Total years of professional experience")
    seniority: Optional[str] = Field(description="Overall seniority level")

    # Structured Data
    summary: Optional[str] = Field(description="Professional summary with allowed HTML tags")
    languages: Optional[List[Language]] = Field(description="Language proficiencies")
    education: Optional[List[Education]] = Field(description="Educational background")
    certificates: Optional[List[Certificate]] = Field(description="Professional certifications")
    positions: Optional[List[Position]] = Field(description="Work experience")
    projects: Optional[List[Project]] = Field(description="Notable projects")
    technologies: Optional[List[TechnologyExperience]] = Field(description="Technical skills")
    industries: Optional[List[IndustryExperience]] = Field(description="Industry experience")

    # Assessment and Analysis
    questions: Optional[List[Question]] = Field(description="Q&A about experience")
    technical_assessment: Optional[List[Assessment]] = Field(description="Technical skill assessments")
    soft_skills_assessment: Optional[List[Assessment]] = Field(description="Soft skills assessments")

    # AI Enhancement
    ai_summary: Optional[str] = Field(description="AI-generated professional summary")
    ai_enhancement_topics: Optional[List[str]] = Field(description="Areas enhanced by AI")
    ai_suggestions: Optional[List[str]] = Field(description="AI-generated improvement suggestions")
    skill_gaps: Optional[List[str]] = Field(description="Identified skill gaps")

    # Version Control
    version_status: Optional[VersionStatus] = Field(description="Current version status")
    revision_number: Optional[int] = Field(description="Version number")
    version_comments: Optional[str] = Field(description="Version change comments")
    tags: Optional[List[str]] = Field(description="Version tags or categories")

    # Quality Metrics
    quality_manual: Optional[int] = Field(description="Manual quality score (0-100)")
    quality_automated: Optional[int] = Field(description="Automated quality score (0-100)")
    quality_metrics: Optional[List[float]] = Field(description="Detailed quality metrics")
    
    # Processing Tracking Fields
    processing_stage: Optional[str] = Field(description="Current processing stage")
    anonymization_applied: Optional[bool] = Field(description="Whether anonymization was applied")
    html_formatting_applied: Optional[bool] = Field(description="Whether HTML formatting was applied")
    company_mapping: Optional[Dict[str, str]] = Field(description="Original to anonymized company name mapping")
    quality_validation_score: Optional[float] = Field(description="Final quality validation score")

    @field_validator('summary')
    def validate_html(cls, v):
        if v:
            # Basic HTML validation for allowed tags
            allowed_tags = ['<ul>', '</ul>', '<li>', '</li>', '<br>', '<p>', '</p>', '<strong>', '</strong>', '<em>', '</em>']
            # Could implement more sophisticated validation here if needed
        return v


class CVEnrichmentRequest(BaseModel):
    cv_data: CVData = Field(description="CV data to be enriched")
    focus_areas: Optional[List[str]] = Field(description="Areas to focus enrichment on")
    enhancement_type: Optional[str] = Field(description="Type of enrichment requested")
    context: Optional[Dict[str, str]] = Field(description="Additional context for enrichment")


class CVAnalysisRequest(BaseModel):
    cv_data: CVData = Field(description="CV data to analyze")
    analysis_type: str = Field(description="Type of analysis to perform")
    criteria: Optional[Dict[str, str]] = Field(description="Analysis criteria")


class ProjectRequirementMatch(BaseModel):
    cv_data: CVData = Field(description="CV to match against requirements")
    project_requirements: Dict[str, str] = Field(description="Project requirements to match")
    matching_criteria: Optional[Dict[str, float]] = Field(description="Matching criteria weights")
