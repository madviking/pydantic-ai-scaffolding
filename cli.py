"""
Testing suite for the AIHelper class.
"""
import argparse
import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path

from agents.example_usage import main_agent_example
from agents.process_cv import process_cv_command
from ai_helper import AiHelper
from helpers.cli_helper_functions import flag_non_working_models, flag_file_capable_models
from helpers.llm_info_provider import LLMInfoProvider
from helpers.usage_tracker import UsageTracker, format_usage_data
from helpers.test_helpers_utils import test_hello_world, test_weather, test_file_analysis


# check command line flags
parser = argparse.ArgumentParser()
parser.add_argument('--update_non_working', nargs='*', help='Updates non-working models in the config file')
parser.add_argument('--test_file_capability', nargs='*', help='Test file capability and update file_capable_models in config')
parser.add_argument('--simple_test', nargs='*', help='Run a simple test case without tool calling')
parser.add_argument('--test_tools', nargs='*', help='Run a test case with tool calling')
parser.add_argument('--test_file', nargs='*', help='Run a test case with file analysis')
parser.add_argument('--test_agent', nargs='*', help='Run a test case with agent functionality')
parser.add_argument('--prices', nargs='*', help='Outputs price information for LLM models')
parser.add_argument('--prices_save', nargs='*', help='Saves price information for LLM models')
parser.add_argument('--custom', nargs='*', help='Run your custom code')
parser.add_argument('--usage', nargs='*', help='Print the usage report')
parser.add_argument('--usage_save', nargs='*', help='Save the sousage report')
parser.add_argument('--test_fallback', nargs='*', help='Test fallback functionality with invalid model')
parser.add_argument('--process_cv', nargs='*', help='Process CV with agentic workflow. Usage: --process_cv <cv_file_path> [email_file_path]')
parser.add_argument('--vv', action='store_true', help='Enable verbose debug logging to logs/forensics.log')
args = parser.parse_args()

# Setup forensics logging if --vv flag is present
if args.vv:
    # Ensure logs directory exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Setup forensics logger
    forensics_logger = logging.getLogger('forensics')
    forensics_logger.setLevel(logging.DEBUG)
    
    # Create file handler
    forensics_handler = logging.FileHandler('logs/forensics.log')
    forensics_handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    forensics_handler.setFormatter(formatter)
    
    # Add handler to logger
    forensics_logger.addHandler(forensics_handler)
    
    # Also setup console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    forensics_logger.addHandler(console_handler)
    
    forensics_logger.info("Forensics logging enabled - detailed debug information will be logged to logs/forensics.log")
    
    # Set debug flag globally for agents
    os.environ['AI_HELPER_DEBUG'] = 'true'

if args.update_non_working is not None:
    # if the flag is set, we will update the non-working models in the config file
    print("Updating non-working models in the config file...")
    flag_non_working_models()

if args.test_file_capability is not None:
    # if the flag is set, we will test file capability and update file_capable_models in the config file
    print("Testing file capability and updating file_capable_models in the config file...")
    flag_file_capable_models()

if args.simple_test is not None:
    ## test case with tool calling
    result, report = test_hello_world(model_name='google/gemini-2.5-pro-preview')
    print(result.model_dump_json(indent=4))
    print(report.model_dump_json(indent=4))

if args.test_tools is not None:
    if 'all' in args.test_tools:
        info = LLMInfoProvider()
        for model in info.get_models():
            result, report = test_hello_world(model_name=model)
            print(f"Model: {model}")
            print(result.model_dump_json(indent=4))
            print(report.model_dump_json(indent=4))
    else:
        result, report = test_weather()
        print(result.model_dump_json(indent=4))
        print(report.model_dump_json(indent=4))

if args.test_file is not None:
    if 'all' in args.test_file:
        info = LLMInfoProvider()
        for model in info.get_models():
            result, report = test_file_analysis(model_name=model)
            print(result.model_dump_json(indent=4))
            print(report.model_dump_json(indent=4))
    else:
        result, report = test_file_analysis()
        print(result.model_dump_json(indent=4))
        print(report.model_dump_json(indent=4))

if args.test_agent is not None:
    asyncio.run(main_agent_example())

if args.usage is not None:
    usage_tracker = UsageTracker()
    summary = usage_tracker.get_usage_summary()
    print(format_usage_data(summary))

if args.usage_save is not None:
    usage_tracker = UsageTracker()
    summary = usage_tracker.get_usage_summary()
    # Save the usage data to a file
    file = 'usage_report.txt'
    with open(file, 'w') as f:
        f.write(format_usage_data(summary))

if args.prices is not None:
    # if the flag is set, we will update the prices for the models
    print("Updating prices for the models...")
    info_provider = LLMInfoProvider()
    print(info_provider.format_price_list())

if args.prices_save is not None:
    # if the flag is set, we will update the prices for the models
    print("Updating prices for the models...")
    info_provider = LLMInfoProvider()
    file = 'llm_prices.txt'
    with open(file, 'w') as f:
        f.write(info_provider.format_price_list())

if args.test_fallback is not None:
    # Test fallback functionality
    print("Testing fallback functionality...")
    from py_models.hello_world.model import Hello_worldModel
    
    ai_helper = AiHelper()
    
    try:
        result, report = ai_helper.get_result(
            prompt='Say hello world!',
            pydantic_model=Hello_worldModel,
            llm_model_name='invalid/non-existent-model',
            provider='invalid_provider'
        )
        print("✅ Fallback test successful!")
        print(f"Final model used: {report.model_name}")
        print(f"Fallback was used: {getattr(report, 'fallback_used', 'N/A')}")
        print(f"Attempted models: {getattr(report, 'attempted_models', 'N/A')}")
        print(f"Result: {result.model_dump_json(indent=2)}")
        
    except Exception as e:
        print(f"❌ Fallback test failed: {str(e)}")

if args.process_cv is not None:
    asyncio.run(process_cv_command(args.process_cv))

if args.custom is not None:
    pass
