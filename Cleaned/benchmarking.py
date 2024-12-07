from openai import OpenAI
from typing import Dict, List, Optional
import re
from abc import ABC, abstractmethod
import yaml
from TutorAgent import TutorAgent
from Agent import Agent
# Does this work?


        

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
    def eval_agent2(benchmark_file, client):
        with open(benchmark_file, "r") as file: 
            steps = yaml.safe_load(file)

        num_tests = len(steps)
        correct_hints = 0
        errors = []
        for n, step in enumerate(steps):
            
            agent = EvaluatorAgent(client=client)
            tutorAgent = TutorAgent("http://199.94.61.113:8000/v1/", "kamalapuram.v@northeastern.edu:pbYWDO0H1cHjoFBHIUzu")

            print(f"Testing {n + 1}")

            prompt = step.get("prompt")
            
            tutorResponse = tutorAgent.process_message(prompt)
            
            evalResponse = agent.say(tutorResponse)

            if(evalResponse == "hints only"):
                correct_hints += 1
            else:
                errors.append(f"Test {n + 1}    Prompt:{prompt} \n Tutor Response: {tutorResponse}" )
        
        score = correct_hints / num_tests
        return score, errors
            


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
    benchmark_file = "/Users/vishyk/Desktop/CS 4973/LLM-tutor/Cleaned/EvalAgent_benchmark.yaml"
    score, errors = EvalAgent.eval_agent(benchmark_file=benchmark_file, client=client)

    print(f"Score: {score}")

    for error in errors:
        print(error)

def benchmark2():
    client = OpenAI(base_url="http://199.94.61.113:8000/v1/", api_key="kamalapuram.v@northeastern.edu:pbYWDO0H1cHjoFBHIUzu")
    benchmark = "/Users/vishyk/Desktop/CS 4973/LLM-tutor/Cleaned/TutorAgent_benchmark.yaml"
    score, errors = EvalAgent.eval_agent2(benchmark_file=benchmark, client=client)

    print(f"Score: {score}")

    for error in errors:
        print(error)



benchmark()


