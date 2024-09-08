import json
import os
import autogen
from autogen import AssistantAgent, UserProxyAgent, register_function
import tools
from llm import llm_config

def create_work_item(context: str):

    workitem_assistant = AssistantAgent(
        "assistant",
        llm_config=llm_config,
        system_message="""You are an Azure DevOps Work Item automation assistant, 
        you can help me create Task/Bug work items. 
        You use the az command to implement this function.
        Each time you will receive a new task description, 
        you create a work item based on the description.""",
    )

    workitem_user_proxy = UserProxyAgent(
        "user_proxy",
        code_execution_config={
            "executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")
        },
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: msg["content"] and ("exit" in msg["content"].lower() or "exiting" in msg["content"].lower()),
    )

    register_function(
        tools.get_all_pbi,
        caller=workitem_assistant,  # The assistant agent can suggest calls to the calculator.
        executor=workitem_user_proxy,  # The user proxy agent can execute the calculator calls.
        name="get_all_pbi",  # By default, the function name is used as the tool name.
        description="Get All PBI Work Items",  # A description of the tool.
    )

    register_function(
        tools.create_pbi,
        caller=workitem_assistant,  # The assistant agent can suggest calls to the calculator.
        executor=workitem_user_proxy,  # The user proxy agent can execute the calculator calls.
        name="create_pbi",  # By default, the function name is used as the tool name.
        description="Create PBI Work Items",  # A description of the tool.
    )

    register_function(
        tools.create_task,
        caller=workitem_assistant,  # The assistant agent can suggest calls to the calculator.
        executor=workitem_user_proxy,  # The user proxy agent can execute the calculator calls.
        name="create_task",  # By default, the function name is used as the tool name.
        description="Create Task Work Items",  # A description of the tool.
    )

    work_item_prefix = ""
    pbi_parent_dict = os.getenv("DEVOPS_PBI_PARENT")
    if pbi_parent_dict:
        pbi_parent_dict = json.loads(pbi_parent_dict)
        work_item_prefix = ' or '.join([f'"[{x}]"' for x in pbi_parent_dict.keys()])

    workitem_user_proxy.initiate_chat(
        workitem_assistant,
        message=f"""
    You will follow the steps below one by one:

    1. Parse the context: {context} to get the work item title and description.
    2. Get All PBI Work Items Information
    3. According to the description and all the PBI queried, if there is a work item that can be used as a parent, 
    use this PBI work item as a parent. If not, create a new PBI work item as a parent.
    {('New PBI work item title should include the prefix ' + work_item_prefix + '.') if work_item_prefix else ''}
    You can only be judged based on semantics. 
    PBI should be a large work item, so the PBI should contain and relate the information of the work item to be created.
    For example:
        1. PBI: [PythonNotebook][Release] Regular releases.  Task: [PythonNotebook]Release Python Notebook 08-08.
        2. PBI: [PythonNotebook] Runtime reliability improvement. Task: [PythonNotebook][Reliability] Fix GJS request runtime timeout when OOM
    4. Create a new Task work item with the title and description parsed from the context.
    5. Return content format: "Exit! Work Item Created: {{work item title}} {{work item url}}, {{new/existing}} parent work item: {{parent work item title}} {{parent work item url}}".
    """,
    )
    print("Work Item Created: ", workitem_user_proxy.last_message())
    return workitem_user_proxy.last_message().get("content", "")


if __name__ == "__main__":
    import sys
    context = sys.argv[1]
    create_work_item(context)
