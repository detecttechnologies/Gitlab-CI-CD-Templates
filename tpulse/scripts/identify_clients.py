import sys
import os
import yaml

# get variables: DEPLOY_ENVIRONMENT and CLIENTS from arguments 
DEPLOY_ENVIRONMENT = sys.argv[1]
CLIENTS = sys.argv[2]

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

# create a dynamic pipeline config using pyyaml
dynamic_config = {
    'stages': ['generate','trigger'],
    'generate_client': {
        'stage': 'generate',
        'image': 'python:3.10',
        'before_script': 'pip install pyyaml toml',
        'script': f'python3 -c "$(curl -fsSL https://github.com/detecttechnologies.com/Gitlab-CI-CD-Templates/raw/dashboard-ci/tpulse/scripts/generate_pipeline.py)" {DEPLOY_ENVIRONMENT} {CLIENTS}',
        'artifacts': {
            'paths': [
                'trigger-msa-*.yml'
            ]
        }
    }
}

# create another job to add in dynamic_config for each client
for client in clients:
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