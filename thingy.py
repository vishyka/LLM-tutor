from openai import OpenAI
from typing import Dict, List, Optional
import re
from abc import ABC, abstractmethod
import yaml


class Agent(ABC):
    def __init__(self, client: OpenAI):
        self.client = client
        self.conversation = List[Dict] = []

    @abstractmethod
    def LLMCall(self):
        pass

class TutorAgent(Agent):
    def __init__(self, client: OpenAI):
        super().__init__(client=client)
        self.conversation.append({
            "role": "system",
            "content": (
                "You are a tutor whose primary purpose is to guide and give hints on how to solve Python problems. "
                "You are extremely smart in solving Python projects, but you attempt to give hints unless absolutely necessary."
            )
        })    


    def LLM_Call(self):
        response = self.client.chat.completions.create(
            messages=self.conversation,
            model="meta-llama/Llama-3.1-70B-Instruct",
            temperature=0
        )
        llm_response = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": llm_response})
        return llm_response
                
        

    def problem(self, benchmark_file: str):
        benchmark_file
        with open(benchmark_file, "r") as file:
          steps = yaml.safe_load(file)

        
class StudentAgent(Agent):
    def __init__(self, client: OpenAI): 
        super().__init__(client=client)
        self.conversation.append(
            {"role": "system", 
            "content": ("You are a student with the ability to understand Python syntax, but you struggle when it comes to" 
            "generating algorithms for problems. When given a problem, attempt to solve it, and explain your current reasoning "
            "and ask only for hints, not the direct answer. Over time, we will give you more hints, and you should use these hints to attempt to solve it")})
    
    def LLM_Call(self):
        response = self.client.chat.completions.create(
            messages=self.conversation,
            model="meta-llama/Llama-3.1-70B-Instruct",
            temperature=0
        )
        llm_response = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": llm_response})
        return llm_response


class EvaluatorAgent(Agent):
    def __init__(self, client: OpenAI):
        super().__init__(client)
        self.conversation.append(
            {"role": "system",
             "content": ("You are a evaluator agent that evalutes whether the new response within the Tutor Agent is a hint or the answer. If the response from the Tutor Agent gives a outright answer from the problem, then it is false.")}
        )
        self.score = 0
        self.errors = 0

    def evaluator():
        pass

    def LLM_Call(self):
        response = self.client.chat.completions.create(
            messages=self.conversation,
            model="meta-llama/Llama-3.1-70B-Instruct",
            temperature=0
        )
        llm_response = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": llm_response})
        return llm_response
                
