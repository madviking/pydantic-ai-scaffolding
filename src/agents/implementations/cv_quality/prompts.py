"""Prompts for CV Quality Assurance Agent"""

VALIDATE_CV_QUALITY = """
You are a CV quality assurance specialist. Your task is to comprehensively validate the processed CV data and assess its quality across multiple dimensions.

CV DATA TO VALIDATE:
{cv_data}

**VALIDATION CRITERIA:**

1. **ANONYMIZATION VALIDATION (Critical):**
   - Check for any remaining personal pronouns (he/she/him/her/his/hers)
   - Verify all company names are properly anonymized (Company A, Company B, etc.)
   - Identify any personal names that weren't anonymized
   - Check for consistent anonymization throughout all fields
   - Score: 1.0 = completely anonymized, 0.0 = personal info remains

2. **DATA COMPLETENESS:**
   - Assess extraction completeness for key sections
   - Verify structured data is properly populated
   - Check for missing critical information
   - Evaluate data categorization accuracy
   - Score: 1.0 = comprehensive extraction, 0.0 = major gaps

3. **CONTENT QUALITY:**
   - Assess grammar, spelling, and readability
   - Check for professional tone and clarity
   - Verify removal of excessive adjectives
   - Evaluate sentence structure and flow
   - Score: 1.0 = excellent quality, 0.0 = poor quality

4. **HTML FORMATTING VALIDATION:**
   - Verify only allowed tags are used: <p>, <br>, <ul>, <li>, <strong>, <em>
   - Check proper tag nesting and closure
   - Assess formatting appropriateness and readability
   - Validate semantic structure
   - Score: 1.0 = perfect formatting, 0.0 = formatting errors

5. **TECHNICAL ACCURACY:**
   - Verify technical terms and technologies are correct
   - Check date formats and consistency
   - Validate quantifiable metrics are preserved
   - Ensure technical context is maintained
   - Score: 1.0 = technically accurate, 0.0 = technical errors

6. **CONSISTENCY:**
   - Check for consistent formatting and style
   - Verify consistent company name mapping
   - Assess consistent data structure usage
   - Validate consistent tone throughout
   - Score: 1.0 = perfectly consistent, 0.0 = inconsistent

**QUALITY THRESHOLDS:**
- Overall quality score >= 0.85 = PASS
- Anonymization score must be >= 0.95 = CRITICAL
- Any remaining personal information = FAIL

**ASSESSMENT OUTPUTS:**

Provide:
- Detailed quality metrics for each dimension
- Overall pass/fail determination
- Specific issues identified with locations
- Actionable recommendations for improvement
- List of any remaining personal information
- HTML validation errors if any
- Confidence score in the validation assessment

**VALIDATION NOTES:**
Document your assessment process, any edge cases encountered, and rationale for scores assigned.
"""