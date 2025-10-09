"""
hello_world model type definition
"""

import os
import json
from typing import List, Optional, Dict, Any, ClassVar
from pydantic import BaseModel, Field
from datetime import date

from py_models.base import BasePyModel


class Hello_worldModel(BasePyModel):

    name: ClassVar[str] = "Hello_worldModel"

    """
    Model for extracting structured information for hello_world
    """

    # Class variables for module configuration
    MODULE_NAME: ClassVar[str] = "hello_world"
    TEST_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "tests")
    REPORT_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "reports")

    # Define model fields - REPLACE WITH YOUR SCHEMA
    message_sentiment: int = Field(..., description="How positive is this message from 1 = very negative, 10 = very positive")
    expects_response: bool = Field(..., description="Does the writer expect a response?")

class RouteStep(BasePyModel):
    name: ClassVar[str] = "RouteStep"
    street_from: ClassVar[str] = Field(..., description="Street where to turn from")
    street_to: ClassVar[str] = Field(..., description="Street where to turn to")
    city: ClassVar[str] = Field(..., description="City where this street is located")

class RouteModel(BasePyModel):
    name: ClassVar[str] = "RouteModel"
    """
    Model for extracting structured information for hello_world
    """
    # Class variables for module configuration
    MODULE_NAME: ClassVar[str] = "hello_world"
    TEST_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "tests")
    REPORT_DIR: ClassVar[str] = os.path.join(os.path.dirname(__file__), "reports")

    # Define model fields - REPLACE WITH YOUR SCHEMA
    route_estimated_time: int = Field(..., description="How many minutes it takes to walk this route")
    instructions: str = Field(..., description="Walking instructions")
    #steps: list[RouteStep] = Field(..., description="List the route steps, max 10")
