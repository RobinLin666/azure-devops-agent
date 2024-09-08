# Azure DevOps Work Item Agent

## Description
This project automates the creation of Azure DevOps work items (Tasks/Bugs) using an AI assistant.

In our work, we typically need to create various work items to track our progress.
The usual hierarchy of work items is as follows: Epic -> Feature -> Product Backlog Item (PBI) -> Task/Bug.
During the progression of a Feature, additional work items may need to be added.
Generally, we need to find an existing PBI or create a new one, and then create Tasks under it.
This process can be quite cumbersome.

Therefore, the purpose of this Agent is to reduce the time spent searching for PBIs by automatically creating Tasks and associating them with existing or newly created PBIs.

The methodology is as follows:
1. Use the az tool to create and query work items.
2. Employ LLM to analyze, match, and create the necessary PBIs and Tasks.
3. Utilize the AutoGen framework to integrate the LLM and the az tool, streamlining the entire process.

## Installation
Follow these steps to set up the project and its dependencies.

```bash
# Clone the repository
git clone https://github.com/RobinLin666/azure-devops-agent.git

# Navigate to the project directory
cd azure-devops-agent

# Install dependencies
pip install -r requirements.txt

# Install Azure CLI
# Refer to: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
brew update && brew install azure-cli # macOS

# Copy the .env file
cp .env.template .env
# Update the .env file with your Azure OpenAI keys and Azure DevOps details
code .env
```

## Usage
Instructions on how to run and use the project.

```bash
# Authenticate with Azure CLI, if you haven't already
az login

# Run the script
python create_work_item.py "Create a new task for updating the project documentation."
```

## License

This project is licensed under the MIT License.
