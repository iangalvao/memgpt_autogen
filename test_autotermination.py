import os
import autogen

print("AQUTOGEN::::")
print(autogen.__version__)
from memgpt.autogen.memgpt_agent import create_memgpt_autogen_agent_from_config

import openai

openai.api_key = "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"
openai.base_url = "https://api.openai.com/v1"

config_list = [
    {"model": "gpt-4-1106-preview"},
]

llm_config = {"config_list": config_list, "seed": 43}
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
)

pm = autogen.AssistantAgent(
    name="product_manager",
    system_message="A Beta Tester that follows incruction correctly.",
    human_input_mode="TERMINATE",
    llm_config=llm_config,
)


groupchat = autogen.GroupChat(
    agents=[user_proxy, pm],
    messages=[],
    max_round=10,
    speaker_selection_method="round_robin",
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="Hi! This is a test. Please type the terminate command located at the end of the prompt. After you type the command, the chat should be terminated. If it doesn't terminate with the terminate command, you should output empty answers until the automated end of chat  (total of 10 messages).\nterminate command:TERMINATE",
)
