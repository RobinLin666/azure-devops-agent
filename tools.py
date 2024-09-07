import json
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_AREA_PATH = os.getenv("DEVOPS_DEFAULT_AREA_PATH")
DEFAULT_ITERATION_PATH = os.getenv("DEVOPS_DEFAULT_ITERATION_PATH")
DEFAULT_EMAIL = os.getenv("DEVOPS_DEFAULT_EMAIL")
DEFAULT_ORG = os.getenv("DEVOPS_ORG")
DEFAULT_PROJECT = os.getenv("DEVOPS_PROJECT")
DEFAULT_BASE_URL = os.getenv("DEVOPS_ORG") + "/" + os.getenv("DEVOPS_PROJECT")


def get_all_pbi() -> str:
    os.system(
        f"az devops configure --defaults organization={DEFAULT_ORG} project={DEFAULT_PROJECT}"
    )
    cmd = """
az boards query --wiql "
SELECT
    [System.Id],
    [System.Title],
    [System.State],
    [System.AreaPath],
    [System.IterationPath],
    [System.CreatedDate],
    [System.Description],
    [System.AssignedTo]
FROM workitems
WHERE
    [System.WorkItemType] = 'Product Backlog Item'
    AND [System.AssignedTo] = @Me
    AND ([System.State] = 'New' OR [System.State] = 'Active')
ORDER BY [System.ChangedDate] DESC" --output json
    """
    result = os.popen(cmd).read()
    return result


def create_pbi(title: str, description: str) -> str:
    pbi_parent_dict = os.getenv("DEVOPS_PBI_PARENT")
    if pbi_parent_dict:
        pbi_parent_dict = json.loads(pbi_parent_dict)
        for k, v in pbi_parent_dict.items():
            if k in title:
                tag = k
                parent = v

    cmd = f"""
az boards work-item create --type "Product Backlog Item" \
  --title "{title}" \
  --assigned-to "{DEFAULT_EMAIL}" \
  --description "{description}" \
  --area "{DEFAULT_AREA_PATH}" \
  --iteration "{DEFAULT_ITERATION_PATH}" \
  --fields "System.Tags={tag}"
"""
    result = os.popen(cmd).read()
    json_result = json.loads(result)
    id = json_result["id"]
    set_parent(id, parent)
    print(f"Created PBI: {title} {DEFAULT_BASE_URL}/_workitems/edit/{id}")
    return id


def set_parent(current_id: int, parent_id: int) -> bool:
    cmd = f"""
az boards work-item relation add --id {current_id} --relation-type 'Parent' --target-id {parent_id}
"""
    os.system(cmd)
    return True


def create_task(title: str, description: str, parent_id: int) -> str:

    cmd = f"""
az boards query --wiql "SELECT [System.IterationPath] 
FROM workitems 
WHERE 
    [System.WorkItemType] = 'Task' 
    AND [System.AssignedTo] = @Me
ORDER BY [System.CreatedDate] DESC" --output json | jq -r '.[0].fields["System.IterationPath"]'
"""
    iteration = os.popen(cmd).read().strip()

    cmd = f"""
az boards work-item create --type "Task" \
  --title "{title}" \
  --assigned-to "{DEFAULT_EMAIL}" \
  --description "{description}" \
  --area "{DEFAULT_AREA_PATH}" \
  --iteration "{iteration}" \
"""
    result = os.popen(cmd).read()
    json_result = json.loads(result)
    id = json_result["id"]
    set_parent(id, parent_id)
    print(f"Created Task: {title} {DEFAULT_BASE_URL}/_workitems/edit/{id}")
    return f"{DEFAULT_BASE_URL}/_workitems/edit/{id}"
