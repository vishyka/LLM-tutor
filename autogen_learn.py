from autogen import AssistantAgent, UserProxyAgent
from autogen import ConversableAgent

setup = { "config_list": [{ "model": "meta-llama/Meta-Llama-3.1-8B-Instruct", "base_url":"http://199.94.61.113:8000/v1/", "api_key": "kamalapuram.v@northeastern.edu:pbYWDO0H1cHjoFBHIUzu"}], "cache": None}


agent_with_number = ConversableAgent(
    "agent_with_number",
    system_message="You are playing a game of guess-my-number. You have the "
    "number 53 in your mind, and I will try to guess it. "
    "If I guess too high, say 'too high', if I guess too low, say 'too low'. ",
    llm_config=setup,
    ##max_consecutive_auto_reply=1,
    is_termination_msg=lambda msg: "53" in msg["content"],  # terminate if the number is guessed by the other agent
    human_input_mode="NEVER",  # never ask for human input
)

human_proxy = ConversableAgent(
    "human_proxy",
    llm_config=False,  # no LLM used for human proxy
    human_input_mode="ALWAYS",  # always ask for human input
)

# Start a chat with the agent with number with an initial guess.
result = human_proxy.initiate_chat(
    agent_with_number,  # this is the same agent with the number as before
    message="Help me solve my problem",
)


