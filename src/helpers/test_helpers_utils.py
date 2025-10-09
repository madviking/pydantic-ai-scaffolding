from typing import Tuple, TypeVar

import pytest
from ai_helper import AiHelper
from py_models.base import LLMReport
from py_models.hello_world.model import Hello_worldModel, RouteModel
from py_models.weather.model import WeatherModel
from py_models.file_analysis.model import FileAnalysisModel

from tools.tool_date import tool_get_human_date
from tools.tool_weather import tool_get_weather

T = TypeVar('T', bound='BasePyModel')

"""
Example usages:
- basic
- with tools
- with file

Agent example is at src/agents/example_usage.py
"""

def test_hello_world(model_name: str = 'mistralai/ministral-3b', provider='open_router'):
    base = AiHelper()
    test_text = """I confirm that the NDA has been signed on both sides. My sincere apologies for the delay in following up - over the past few weeks, series of regional public holidays and an unusually high workload disrupted our regular scheduling.
                Attached to this email, you'll find a short but I believe comprehensive CV of the developer we would propose for the project. He could bring solid expertise in Odoo development, and has extensive experience in odoo migrations.
                Please feel free to reach out if you have any questions.
                """
    prompt = 'Please analyse the sentiment of this text\n Here is the text to analyse:' + test_text
    result, report = base.get_result(prompt, Hello_worldModel, llm_model_name=model_name, provider=provider)
    return result, report

def test_deterministic(model_name: str = 'anthropic/claude-sonnet-4', provider='anthropic'):
    base = AiHelper()
    prompt = """What is the best route from Potsdam to Berghain? """
    result, report = base.get_result(prompt, RouteModel, llm_model_name=model_name, provider=provider)
    return result, report

def test_weather(model_name: str = 'openai/gpt-4.1', provider='openai'):
    base = AiHelper()
    prompt = 'Please return the current weather and time in a form of a haiku. Location is Sofia, Bulgaria. Sofia needs to be used in the haiku.'
    tools = [
        tool_get_weather,
        tool_get_human_date
    ]
    result, report = base.get_result(prompt, WeatherModel, llm_model_name=model_name, provider=provider, tools=tools)
    return result, report


def test_file_analysis(model_name: str = 'openai/gpt-4o', provider='openai'):
    base = AiHelper()
    prompt = 'Please analyze this file and extract its text content and provide a summary of its main content and purpose.'
    file_path = 'tests/files/test.pdf'
    result, report = base.get_result(prompt, FileAnalysisModel, llm_model_name=model_name, provider=provider, file=file_path)
    return result, report
