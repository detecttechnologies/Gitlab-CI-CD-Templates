import sys
import yaml
import toml
import os

DEPLOY_ENVIRONMENT = sys.argv[1]
deployments_to_trigger = sys.argv[2]
print(f"deployments_to_trigger: {deployments_to_trigger}")

# Set the BRANCH variable based on DEPLOY_ENVIRONMENT
if DEPLOY_ENVIRONMENT == 'dev':
    branch = 'develop'
elif DEPLOY_ENVIRONMENT == 'qa':
    branch = 'test'
else:
    branch = 'main'

# Loop through each client
for client, repos_to_trigger in deployments_to_trigger.items():
    print(f"client: {client}")
    # Get the config file for the client
    config_content = os.environ[f'{client}_DEPLOYMENT_CONFIG']

    # Read the config content using toml
    config = toml.loads(config_content)

    dynamic_config = {
        'stages': ['trigger'],
        'trigger_repos': {
            'stage': 'trigger',
            'trigger': {
                'project': '$PREFIX/$PROJECTS',
                'branch': '$BRANCH',
                'strategy': 'depend'
            },
            'parallel': {
                'matrix': []
            },
            'variables': {
                'ENVIRONMENT': client,
                'DEPLOY_ENVIRONMENT': DEPLOY_ENVIRONMENT,
                'DEPLOY_CONFIG': config_content,
                'BRANCH': branch
            },
        }
    }

    # Loop through each repository
    for repo in config["client"][0]["repos"]:
        repo_name = repo["name"]
        # Check if the latest tag is already deployed for the repo
        # Use a custom script to check the latest deployed tag
        if repo_name in repos_to_trigger:
            dynamic_config["trigger_repos"]["parallel"]["matrix"].append({
                "PROJECTS": repo_name,
                "PREFIX": 'DetectTechnologies/Software/WebApps/T-PULSE/web/tpulse-msa/tpulse-msa-{}'.format(repo["type"]),
            })

    # Save the dynamic configuration to a file with a unique name for each client
    with open(f'trigger-msa-{client}.yml', 'w') as f:
        yaml.dump(dynamic_config, f)

    print(f'Generated trigger-msa-{client}.yml for {client} client')