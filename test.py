from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, Tool
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.tools import BaseTool
from typing import Dict, List
import gradio as gr

# Initialize our LLaMA model
llm = ChatOpenAI(
    base_url="http://199.94.61.113:8000/v1/",
    api_key="kamalapuram.v@northeastern.edu:pbYWDO0H1cHjoFBHIUzu",
    model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
    temperature=0.7
)

# Create analyzer chain
analyzer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a programming problem analyzer. Analyze the query and determine:
    - Problem complexity (SIMPLE/COMPLEX)
    - Programming domain
    - Key concepts required
    - Suggested approach"""),
    ("human", "{query}")
])

analyzer_chain = LLMChain(
    llm=llm,
    prompt=analyzer_prompt,
    memory=ConversationBufferMemory(),
)

# Create tutor chain
tutor_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert programming tutor. Based on the analysis:
    {analysis}
    
    Provide a detailed solution with:
    1. Conceptual explanation
    2. Step-by-step breakdown
    3. Code examples
    4. Common pitfalls to avoid"""),
    ("human", "{query}")
])

tutor_chain = LLMChain(
    llm=llm,
    prompt=tutor_prompt,
    memory=ConversationBufferMemory(),
)

# Create solution enhancer chain
enhancer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a solution optimizer. Enhance the given solution by adding:
    1. Performance considerations
    2. Alternative approaches
    3. Best practices
    4. Additional examples
    5. Testing strategies"""),
    ("human", """Original solution: {solution}
    Please enhance this solution.""")
])

enhancer_chain = LLMChain(
    llm=llm,
    prompt=enhancer_prompt,
    memory=ConversationBufferMemory(),
)

# Create custom tools
class AnalyzerTool(BaseTool):
    name = "problem_analyzer"
    description = "Analyzes programming problems to determine complexity and approach"

    def _run(self, query: str) -> str:
        return analyzer_chain.run(query=query)

class TutorTool(BaseTool):
    name = "programming_tutor"
    description = "Provides detailed programming tutorials and solutions"

    def _run(self, query: str, analysis: str) -> str:
        return tutor_chain.run(query=query, analysis=analysis)

class EnhancerTool(BaseTool):
    name = "solution_enhancer"
    description = "Enhances and optimizes programming solutions"

    def _run(self, solution: str) -> str:
        return enhancer_chain.run(solution=solution)

# Create tools list
tools = [
    AnalyzerTool(),
    TutorTool(),
    EnhancerTool()
]

# Create main agent
class DPTutor:
    def __init__(self):
        self.tools = tools
        self.memory = ConversationBufferMemory()

    def process_query(self, query: str) -> str:
        try:
            # Step 1: Analyze the problem
            analysis = self.tools[0]._run(query)
            
            # Step 2: Generate solution
            solution = self.tools[1]._run(query, analysis)
            
            # Step 3: Enhance solution
            enhanced_solution = self.tools[2]._run(solution)
            
            return f"""
Problem Analysis:
{analysis}

Initial Solution:
{solution}

Enhanced Solution:
{enhanced_solution}
"""
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Create Gradio interface
def create_ui():
    tutor = DPTutor()
    
    def process_query(query):
        return tutor.process_query(query)
    
    interface = gr.Interface(
        fn=process_query,
        inputs=[
            gr.Textbox(
                lines=5, 
                label="Enter your programming question",
                placeholder="e.g., How do I implement fibonacci using dynamic programming?"
            )
        ],
        outputs=[
            gr.Textbox(
                lines=20, 
                label="Tutorial Response"
            )
        ],
        title="Dynamic Programming Tutor",
        description="Get expert help with programming problems and algorithms",
        examples=[
            ["How do I implement fibonacci using dynamic programming?"],
            ["Explain the knapsack problem and its solution"],
            ["How to find the longest common subsequence?"]
        ]
    )
    
    interface.launch()

if __name__ == "__main__":
    create_ui()