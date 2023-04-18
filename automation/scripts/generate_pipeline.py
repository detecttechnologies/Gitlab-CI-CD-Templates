import sys
import yaml
import toml
import os

DEPLOY_ENVIRONMENT = sys.argv[1]
CLIENTS = sys.argv[2]
print(CLIENTS)

# if CLIENTS is "all", then we get ALL_CLIENTS from CI/CD settings variables   
if CLIENTS == "all":    
    ALL_CLIENTS = os.environ['ALL_CLIENTS']
    clients = ALL_CLIENTS.split(',')
# if CLIENTS is "none", then we get CLIENTS from DEPLOY_ENVIRONMENT
elif CLIENTS == "none":
    clients = [DEPLOY_ENVIRONMENT]
# else CLIENTS is a comma separated list of clients
else:
    clients = CLIENTS.split(',')

# Set the BRANCH variable based on DEPLOY_ENVIRONMENT
if DEPLOY_ENVIRONMENT == 'dev':
    branch = 'develop'
elif DEPLOY_ENVIRONMENT == 'qa':
    branch = 'test'
else:
    branch = 'main'

# Loop through each client
for client in clients:
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
        
        dynamic_config["trigger_repos"]["parallel"]["matrix"].append({
            "PROJECTS": repo_name,
            "PREFIX": 'DetectTechnologies/Software/WebApps/T-PULSE/web/tpulse-msa/tpulse-msa-{}'.format(repo["type"]),
        })

    # Save the dynamic configuration to a file with a unique name for each client
    with open(f'trigger-msa-{client}.yml', 'w') as f:
        yaml.dump(dynamic_config, f)

    print(f'Generated trigger-msa-{client}.yml for {client} client')