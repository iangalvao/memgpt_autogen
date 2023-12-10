import os
import autogen

print("AQUTOGEN::::")
print(autogen.__version__)
from memgpt.autogen.memgpt_agent import create_memgpt_autogen_agent_from_config

import openai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
openai.base_url = "https://api.openai.com/v1"
USE_MEMGPT = False

# create a config for the MemGPT AutoGen agent
config_list_memgpt = [
    {
        "model": "gpt-4",
        "context_window": 8192,
        "preset": "memgpt_chat",  # NOTE: you can change the preset here
        # OpenAI specific
        "model_endpoint_type": "openai",
        "model_endpoint": "https://api.openai.com/v1",
        "openai_key": OPENAI_API_KEY,
    },
]
llm_config_memgpt = {"config_list": config_list_memgpt, "seed": 42}

# there are some additional options to do with how you want the interface to look (more info below)
interface_kwargs = {
    "debug": False,
    "show_inner_thoughts": True,
    "show_function_outputs": False,
}

# then pass the config to the constructor
coder = create_memgpt_autogen_agent_from_config(
    "MemGPT_agent",
    llm_config=llm_config_memgpt,
    system_message=f"I'm a expert python coder and Ian's good friend and startup colegue.",
    interface_kwargs=interface_kwargs,
    default_auto_reply="...",  # NOTE: you should set this to True if you expect your MemGPT AutoGen agent to call a function other than send_message on the first turn
)


config_list = [{"model": "gpt-4"}, {"model": "gpt-4"}]

llm_config = {"config_list": config_list, "seed": 42}
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
)

# non-MemGPT PM
pm = autogen.AssistantAgent(
    name="product_manager",
    system_message="Creative in software product ideas. Product manager in Experiment Ltda. You work with Ana, a code reviewer and James, a code writter. You are responsible for their coordination.",
    human_input_mode="TERMINATE",
    llm_config=llm_config,
)

# non-MemGPT PM
if not USE_MEMGPT:
    coder = autogen.AssistantAgent(
        name="james_coder",
        system_message="Python expert and great code writter.Collegue of Ana Code Reviewer in Experiment Ltda, you tend to like her reviews, as she is a very competent professional.",
        human_input_mode="TERMINATE",
        llm_config=llm_config,
    )

code_reviewer = autogen.AssistantAgent(
    name="Ana_Code_Reviewer",
    system_message="Python expert with focus on code review. Collegue of James Coder in Experiment Ltda. You usually review his code, and likes to work with him very much.",
    human_input_mode="TERMINATE",
    llm_config=llm_config,
)


groupchat = autogen.GroupChat(
    agents=[user_proxy, coder, pm, code_reviewer], messages=[], max_round=20
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="Hi! This a test for our gaming startup Experiment Ltda. Today's challenge is to create a very simple game in pygame. The simpler the better. You can chose any game from: pong, snake, tetris or any other you would like. You should comunicate between yourselves, present yourself in the chat, and cooperate to work with maximum of 20 messages in the chat. After that the work is stopped and I will analyse the results. If you are done before that send a message with TERMINATE. The last python scripts in the chat history will be submited to avaliation (if its more than one script, i will gather the last versions of all the files before testing). Good luck for everyone!",
)
