from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.tools.tavily_search import TavilySearchResults
import os
import gradio as gr
from typing import List

class TutorAgent:
  def __init__(self, base_url: str, api_key: str):
      self.llm = ChatOpenAI(
        openai_api_base=base_url,
        openai_api_key=api_key,
        model="meta-llama/Meta-Llama-3.1-8B-Instruct"
      )
      
      self.memory = ConversationBufferMemory()
      tavily_api_key = "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"
      os.environ["TAVILY_API_KEY"] = tavily_api_key
      self.search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
      self.tavily_tool = TavilySearchResults(api_wrapper=self.search)
      
      self.hint_level: int = 0
      self.chat_history: List = []
      
      self.hint_prompt = PromptTemplate(
        input_variables=["question", "chat_history", "hint_level"],
        template="""
        You are a supportive tutor. Consider the chat history and provide an appropriate hint:
        
        Chat History: {chat_history}
        Current Question: {question}
        
        Provide a Level {hint_level} hint (1=general concept, 2=more specific, 3=detailed guidance):
        """
      )
      
      self.search_prompt = PromptTemplate(
        input_variables=["question", "search_results", "chat_history"],
        template="""
        As a tutor, guide the student through this topic based on their previous questions:
        
        Chat History: {chat_history}
        Current Question: {question}
        Reference Material: {search_results}
        
        Provide guidance that builds understanding without giving direct solutions:
        """
      )
      
      self.hint_chain = (
        {
            "question": lambda x: x["question"],
            "chat_history": lambda x: self.get_chat_history(),
            "hint_level": lambda x: self.hint_level
        }
        | self.hint_prompt 
        | self.llm 
        | StrOutputParser()
      )
      
      self.search_chain = (
        {
          "question": lambda x: x["question"],
          "search_results": lambda x: self.tavily_tool.invoke({"query": x["question"]}),
          "chat_history": lambda x: self.get_chat_history()
        }
        | self.search_prompt 
        | self.llm 
        | StrOutputParser()
      )
      
  def get_chat_history(self):
    return "\n".join([f"{'User' if i%2==0 else 'Tutor'}: {msg}" for i, msg in enumerate(self.chat_history[-6:])])
  
  def get_next_hint_level(self):
    self.hint_level = (self.hint_level % 3) + 1
    return self.hint_level
  
  def process_message(self, message, history):
    try:
      # Update chat history
      self.chat_history.extend([message])
      
      if message.lower() == "reset":
        self.hint_level = 0
        self.chat_history = []
        response = "Hint level and chat history have been reset."
      elif any(word in message.lower() for word in ["solution", "answer", "solve"]):
        hint = self.hint_chain.invoke({"question": message})
        level = self.get_next_hint_level()
        response = f"💡 Hint Level {level}:\n\n{hint}"
      else:
        response = self.search_chain.invoke({"question": message})
      
      self.chat_history.extend([response])
      return response
    except Exception as e:
      return f"I encountered an error: {str(e)}. Could you try rephrasing your question?"
        
        
  def generate_quiz(self, message):
    pass
  
  def generate_session_summary(self, message):
    pass
  
  
# make a full stack app after
def create_gradio_interface():
    base_url = "http://199.94.61.113:8000/v1/"
    api_key = "kamalapuram.v@northeastern.edu:pbYWDO0H1cHjoFBHIUzu"
    
    tutor = TutorAgent(base_url=base_url, api_key=api_key)

    def respond(message, chat_history):
        if message.lower() == "reset":
            return "", []
        
        bot_message = tutor.process_message(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    def clear_chat():
        tutor.hint_level = 0
        tutor.chat_history = []
        return [], ""

    with gr.Blocks(title="Interactive Tutor") as demo:
        gr.Markdown("""
        # 🎓 Interactive Learning Assistant
        
        Welcome to your personal tutor! Ask questions about any topic and get guided help.
        
        - Type your question normally for guided learning
        - Type 'reset' to start over
        - If you ask for direct solutions, you'll receive progressive hints instead
        """)
        
        chatbot = gr.Chatbot(
            label="Discussion",
            height=400
        )
        
        with gr.Row():
            msg = gr.Textbox(
                label="Your Question",
                placeholder="Ask your question here...",
                lines=2,
                scale=4
            )
            submit = gr.Button("Submit", scale=1)
            
        clear = gr.Button("Clear Chat")
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        submit.click(respond, [msg, chatbot], [msg, chatbot])
        clear.click(clear_chat, None, [chatbot, msg])

    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=True)