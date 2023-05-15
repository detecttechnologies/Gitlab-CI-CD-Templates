import sys
import os
import yaml
import toml
import requests
import json
import base64

def get_clients():
    if CLIENTS == "all":
        ALL_CLIENTS = os.environ['ALL_CLIENTS']
        return ALL_CLIENTS.split(',')
    elif CLIENTS == "none":
        return [DEPLOY_ENVIRONMENT]
    else:
        return CLIENTS.split(',')

def get_latest_reference(repo, headers, client):
    project_id = repo['project_id']
    
    # Get branch name from client name
    if client == "dev":
        branch = "develop"
    elif client == "qa":
        branch = "test"
    else:
        branch = "main"

    response = requests.get(f"{gitlab_url}/projects/{project_id}/repository/branches/{branch}", headers=headers)
    branch_data = response.json()

    latest_state = branch_data["commit"]["id"]
    return latest_state if 'commit' in branch_data else None

def get_latest_deployment(repo, environment, headers):
    project_id = repo['project_id']
    env_name = environment['name']
    response = requests.get(f"{gitlab_url}/projects/{project_id}/deployments?environment={env_name}&status=success&order_by=finished_at&sort=desc", headers=headers)
    deployments = response.json()

    # Get the latest successful deployment
    latest_successful_deployment = deployments[0]["deployable"]["commit"]["id"] if deployments else None
    return latest_successful_deployment

def trigger_deployment(repo, deployments_to_trigger, client):
    if client not in deployments_to_trigger.keys():
        deployments_to_trigger[client] = []
    deployments_to_trigger[client].append(repo['name'])

# get variables: DEPLOY_ENVIRONMENT and CLIENTS from arguments
DEPLOY_ENVIRONMENT = sys.argv[1]
CLIENTS = sys.argv[2]
TOKEN_CONFIG = os.environ['TOKEN_CONFIG']
clients = get_clients()
print(f"Client(s) chosen to be deployed: {clients}")
gitlab_url = "https://gitlab.com/api/v4"

deployments_to_trigger = {}

# get config file for client and check latest deployments
for client in clients:
    config_file = os.environ[f'{client}_DEPLOYMENT_CONFIG']
    config = toml.loads(config_file)
    deployed_repos = config['client'][0]['repos']
    print(f"deployed_repos for {client}: {deployed_repos}")
    tokens = toml.loads(TOKEN_CONFIG)

    for deployed_repo in deployed_repos:
        for repo in tokens['repos']:
            if deployed_repo['name'] == repo['name']:
                api_token = repo['api_token']
                headers = {"Private-Token": api_token}

                response = requests.get(f"{gitlab_url}/projects/{repo['project_id']}/environments", headers=headers)
                environments = response.json()
                target_environment = None
                for env in environments:
                    if env['name'] == client:
                        target_environment = env
                        break
                if target_environment is not None:
                    latest_reference = get_latest_reference(repo, headers, client)
                    latest_deployment = get_latest_deployment(repo, target_environment, headers)
                    print(latest_reference, latest_deployment)
                    if latest_deployment is None or latest_deployment != latest_reference:
                        trigger_deployment(repo, deployments_to_trigger, client)
                    else:
                        print(f"Latest reference {latest_reference} is already deployed for {client} in {repo['name']}")
                else:
                    print(f"No environment found with the client name: {client}")
                break

print(json.dumps(deployments_to_trigger, indent=2))

# filter out deployments_to_trigger for clients with no deployments
deployments_to_trigger = {client: deployments_to_trigger[client] for client in deployments_to_trigger if len(deployments_to_trigger[client]) > 0}
deployments_to_trigger_json = json.dumps(deployments_to_trigger)
deployments_to_trigger_base64 = base64.b64encode(deployments_to_trigger_json.encode()).decode()


# create a dynamic pipeline config using pyyaml
dynamic_config = {
    'stages': ['generate','trigger'],
    'generate_client': {
        'stage': 'generate',
        'image': 'python:3.10',
        'before_script': 'pip install pyyaml toml',
        'script': f'python3 -c "$(curl -fsSL https://github.com/detecttechnologies/Gitlab-CI-CD-Templates/raw/dashboard-ci/automation/scripts/generate_pipeline.py)" {DEPLOY_ENVIRONMENT} {deployments_to_trigger_base64}',
        'artifacts': {
            'paths': [
                'trigger-msa-*.yml'
            ]
        }
    }
}

# create another job to add in dynamic_config for each client
for client in deployments_to_trigger.keys():
    dynamic_config[f'trigger_{client}'] = {
        'stage': 'trigger',
        'trigger': {
            'include': {
                'artifact': f'trigger-msa-{client}.yml',
                'job': 'generate_client'
            },
            'strategy': 'depend',   
        },
        'needs': ['generate_client'],
    }

# write the dynamic pipeline config to a file
with open('trigger-deployment.yml', 'w') as outfile:
    yaml.dump(dynamic_config, outfile, default_flow_style=False)

print(f'Generated trigger-deployment.yml for {clients} clients')