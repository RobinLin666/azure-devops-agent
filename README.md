# Azure DevOps Work Item Automation

## Description
This project automates the creation of Azure DevOps work items (Tasks/Bugs) using an AI assistant.
The assistant interacts with the user to receive task descriptions and creates corresponding work items using the Azure CLI (`az` command).


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
# Authenticate with Azure CLI
az login

# Run the script
python create_work_item.py "Create a new task for updating the project documentation."
```

## License

This project is licensed under the MIT License.
