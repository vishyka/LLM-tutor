from openai import OpenAI
from typing import Dict, List, Optional
import re
from abc import ABC, abstractmethod
import yaml

class Agent(ABC):
    def __init__(self, client: OpenAI):
        self.client = client
        self.conversation = []

    @abstractmethod
    def LLMCall(self):
        pass