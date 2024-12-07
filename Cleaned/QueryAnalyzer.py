from openai import OpenAI
from Agent import Agent

class QueryAnalyzer(Agent):
  def __init__(self, client: OpenAI):
    super().__init__(client)
    self.conversation = []
    self.conversation.append(
      {
        "role": "system",
            "content": (
                """
                You are a query evaluator that checks the conversation message to determine what kind of question the message is and the difficulty level.
                Examples include Math, Science, History, Programming, Algorithmic and types of difficulty include 
                

                Again, **ONLY** respond with guiding hints. 
                """
            ) 
      }
    )
  
  def LLMCall(self):
    llm_response = self.client.chat.completions.create(
      messages=self.conversation,
      model="meta-llama/Meta-Llama-3.1-8B-Instruct",
      temperature=0
    )
    
    llm_response_finished = llm_response.choices[0].message.content
    self.conversation.append({"role": "assistant", "content": llm_response_finished})
    return llm_response_finished
  
  def 

    
    
  