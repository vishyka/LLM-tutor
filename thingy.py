from openai import OpenAI
from typing import Dict, List, Optional
import re
from abc import ABC, abstractmethod
import yaml

# Does this work?

class Agent(ABC):
    def __init__(self, client: OpenAI):
        self.client = client
        self.conversation = []

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
            model="meta-llama/Llama-3.1-80b-Instruct",
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
            model="meta-llama/Llama-3.1-80b-Instruct",
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
             "content": """
                You are an evalutor that will analyze a response to determine whether it provides an answer to a problem, or whether it only provides hints. 
                You MUST respond with either 'hints only' or 'answer provided'. Do NOT respond with anything else. 
                For the context of this, we are fine with giving hints to problems, but if the response is too close to what seems like an answer, you should respond with 'answer provided'
                If it is unclear whether a response is an answer or a hint, lean more towards saying its an answer. 
                Keep in mind that just because the response is in pure text, that does not prevent it from being an answer. Responses that describe how to obtain a solution through text are also considered answers. 
                
                Again, **ONLY** respond with 'hints only' OR 'answer provided' 

            
                """}
        )
        self.score = 0
        self.errors = 0

    def evaluator():
        pass

    def LLMCall(self):
        response = self.client.chat.completions.create(
            messages=self.conversation,
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            temperature=0
        )
        llm_response = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": llm_response})
        return llm_response
    
    def LLM_Call(self):
        response = self.client.chat.completions.create(
            messages=self.conversation,
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            temperature=0
        )
        llm_response = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": llm_response})
        return llm_response
    def say(self, prompt: str) -> str:
        # Add the user's message to the conversation
        self.conversation.append({"role": "user", "content": prompt})
        
        # Get the LLM's response
        response = self.LLM_Call()
        
        return response
    
                


class EvalAgent: 
    def eval_agent(benchmark_file, client):
        
        with open(benchmark_file, "r") as file:
            steps = yaml.safe_load(file)
        
        errors = []
        num_tests = len(steps)
        correct_tests = 0

        for n, step in enumerate(steps):
            agent = EvaluatorAgent(client=client)

            print(f"Testing {n + 1}")

            prompt = step.get("prompt")
            exp_eval = step.get("evaluation")

            if not prompt or not exp_eval:
                errors.append(f"Test {n + 1}: Missing prompt or evaluation in benchmark file")
                continue
        
            response = agent.say(prompt)

            if exp_eval == "answer provided":
                if response != "answer provided":
                    errors.append(f"Test {n+1}: Expected 'answer provided' but got '{response}'")
                else:
                    correct_tests += 1
            elif exp_eval == "hints only":
                if response != "hints only":
                    errors.append(f"Test {n+1}: Expected 'hints only' but got '{response}'")
                else:
                    correct_tests += 1
            else:
                errors.append(f"Test {n+1}: Unrecognized eval type")

        score = correct_tests / num_tests if num_tests > 0 else 0.0 

        return score, errors
    

def benchmark():
    client = OpenAI(base_url="http://199.94.61.113:8000/v1/", api_key="kamalapuram.v@northeastern.edu:pbYWDO0H1cHjoFBHIUzu")
    benchmark_file = "/Users/vishyk/Desktop/CS 4973/LLM-tutor/T_eval_benchmark_file.yaml"
    score, errors = EvalAgent.eval_agent(benchmark_file=benchmark_file, client=client)

    print(f"Score: {score}")

    for error in errors:
        print(error)

benchmark()


