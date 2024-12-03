from autogen import AssistantAgent, UserProxyAgent
from autogen import ConversableAgent

def sequential_tool_handler(agent, message):
    # Implement a custom handler that processes tools one at a time
    tools = agent.tools  # Assuming the agent has a list of tools
    results = []
    for tool in tools:
        result = tool.execute()  # Process each tool sequentially
        results.append(result)
    return results

setup = {
    "config_list": [{
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "base_url": "http://199.94.61.113:8000/v1/",
        "api_key": "kamalapuram.v@northeastern.edu:pbYWDO0H1cHjoFBHIUzu"
    }],
    
}

agent_with_number = ConversableAgent(
    "agent_with_number",
    system_message="You are playing a game of guess-my-number. You have the "
    "number 53 in your mind, and I will try to guess it. "
    "If I guess too high, say 'too high', if I guess too low, say 'too low'. ",
    llm_config=setup,
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda msg: "53" in msg["content"],
    human_input_mode="NEVER",
)

human_proxy = ConversableAgent(
    "human_proxy",
    llm_config=False,
    human_input_mode="ALWAYS",
)

result = human_proxy.initiate_chat(
    agent_with_number,
    message="Let's play a number guessing game",
)