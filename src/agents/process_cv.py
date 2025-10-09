"""
Testing suite for the AIHelper class.
"""
import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path

from agents.example_usage import main_agent_example
from ai_helper import AiHelper
from helpers.cli_helper_functions import flag_non_working_models, flag_file_capable_models
from helpers.llm_info_provider import LLMInfoProvider
from usage_tracking.tracker import UsageTracker, format_usage_data
from helpers.test_helpers_utils import test_hello_world, test_weather, test_file_analysis


async def process_cv_command(cv_args):
    """
    Process CV using the agentic workflow and save results to JSON

    Args:
        cv_args: List of arguments [cv_file_path, email_file_path (optional)]
    """
    # Import here to avoid circular import issues
    from agents.workflows.cv_processing_workflow import CVProcessingWorkflow

    if not cv_args or len(cv_args) == 0:
        print("❌ Error: CV file path is required")
        print("Usage: --process_cv <cv_file_path> [email_file_path]")
        return

    cv_file_path = cv_args[0]
    email_file_path = cv_args[1] if len(cv_args) > 1 else None

    # Validate file paths
    if not Path(cv_file_path).exists():
        print(f"❌ Error: CV file not found: {cv_file_path}")
        return

    if email_file_path and not Path(email_file_path).exists():
        print(f"⚠️  Warning: Email file not found: {email_file_path}")
        print("Proceeding without email integration...")
        email_file_path = None

    print("🚀 Starting CV Processing Workflow...")
    print(f"📄 CV File: {cv_file_path}")
    if email_file_path:
        print(f"📧 Email File: {email_file_path}")
    print("-" * 50)

    try:
        # Initialize AI Helper and workflow
        ai_helper_instance = AiHelper()
        workflow = CVProcessingWorkflow(ai_helper_instance)

        # Validate prerequisites
        validation_result = await workflow.validate_prerequisites(cv_file_path, email_file_path)
        if not validation_result['valid']:
            print("❌ Prerequisites validation failed:")
            for error in validation_result['errors']:
                print(f"  • {error}")
            return

        if validation_result['warnings']:
            print("⚠️  Warnings:")
            for warning in validation_result['warnings']:
                print(f"  • {warning}")

        # Execute the workflow
        processing_result = await workflow.execute(cv_file_path, email_file_path)

        if processing_result['success']:
            print("✅ CV Processing completed successfully!")
            print(f"📊 Stages completed: {', '.join(processing_result['stages_completed'])}")

            # Generate output filename
            cv_filename = Path(cv_file_path).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"processed_cv_{cv_filename}_{timestamp}.json"
            output_path = Path("output") / output_filename

            # Create output directory if it doesn't exist
            output_path.parent.mkdir(exist_ok=True)

            # Prepare data for saving
            output_data = {
                "processing_metadata": {
                    "input_cv_file": str(cv_file_path),
                    "input_email_file": str(email_file_path) if email_file_path else None,
                    "processing_timestamp": datetime.now().isoformat(),
                    "workflow_version": "1.0",
                    "stages_completed": processing_result['stages_completed']
                },
                "cv_data": processing_result['cv_data'].model_dump() if processing_result['cv_data'] else None,
                "processing_report": processing_result['processing_report']
            }

            # Save to JSON file
            with open(output_path, 'w', encoding='utf-8') as output_file:
                json.dump(output_data, output_file, indent=2, ensure_ascii=False, default=str)

            print(f"💾 Results saved to: {output_path}")

            # Display quality metrics if available
            if 'quality_validation' in processing_result['processing_report']:
                quality_metrics = processing_result['processing_report']['quality_validation']['quality_metrics']
                print("\n📈 Quality Metrics:")
                print(f"  • Overall Quality: {quality_metrics.get('overall_quality', 'N/A'):.2f}")
                print(f"  • Anonymization: {quality_metrics.get('anonymization_score', 'N/A'):.2f}")
                print(f"  • Content Quality: {quality_metrics.get('content_quality', 'N/A'):.2f}")
                print(f"  • HTML Formatting: {quality_metrics.get('html_formatting_score', 'N/A'):.2f}")

                validation_passed = processing_result['processing_report']['quality_validation']['validation_passed']
                if validation_passed:
                    print("✅ Quality validation: PASSED")
                else:
                    print("❌ Quality validation: FAILED")
                    issues = processing_result['processing_report']['quality_validation']['quality_issues']
                    print("Issues found:")
                    for issue in issues:
                        print(f"  • {issue}")

            # Display anonymization info
            if 'anonymization' in processing_result['processing_report']:
                company_mapping = processing_result['processing_report']['anonymization'].get('company_mapping', {})
                if company_mapping:
                    print(f"\n🏢 Company Anonymization Mapping:")
                    for original, anonymized in company_mapping.items():
                        print(f"  • {original} → {anonymized}")

        else:
            print("❌ CV Processing failed!")
            print(f"Error: {processing_result.get('error', 'Unknown error')}")

            if processing_result.get('processing_report', {}).get('errors'):
                print("Errors encountered:")
                for error in processing_result['processing_report']['errors']:
                    print(f"  • {error}")

    except Exception as processing_error:
        print(f"❌ Unexpected error during CV processing: {str(processing_error)}")
        import traceback
        traceback.print_exc()
