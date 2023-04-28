import sys
import os
import toml
import boto3
from jq import jq
import subprocess

# Run a shell command and return stdout and stderr as strings
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def ecs_deployment(client, repo, tag):

    # Print starting deployment message for the client
    print(f"Starting ECS deployment for client: {client['name']}")
    
    # Set AWS environment variables
    os.environ["AWS_ACCOUNT_ID"] = client["aws_account_id"]
    os.environ["AWS_DEFAULT_REGION"] = client["region"]
    os.environ["AWS_ACCESS_KEY_ID"] = client["aws_access_key_id"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = client["aws_secret_access_key"]

    # Get AWS account ID and client-specific information
    aws_account_id = boto3.client('sts').get_caller_identity()['Account']
    client_region = client['region']
    client_cluster_name = client['ecs_cluster_name']
    
    client_task_definition_name = repo['task_definition_name']
    client_service_name = repo['service_name']
    
    # Print the client's region, cluster, task definition, and service details
    print(f"Region:{client_region}, Cluster:{client_cluster_name}, Task Definition:{client_task_definition_name}, Service: {client_service_name}")
    
    # Create an ECS client using the client's region
    ecs = boto3.client('ecs', region_name=client_region)
    
    # Describe the task definition and get the container definitions
    task_definition = ecs.describe_task_definition(taskDefinition=client_task_definition_name)
    container_definitions = task_definition['taskDefinition']['containerDefinitions']
    
    # Create the image URL with the new tag
    image = f"{aws_account_id}.dkr.ecr.{client_region}.amazonaws.com/{client_service_name}:{tag}"
    
    # Update the container definition with the new image URL
    updated_container_definition = jq(f'.[0] | .image = "{image}"').transform(container_definitions)

    # Register a new task definition with the updated container definition
    new_task_definition = ecs.register_task_definition(
        family=client_task_definition_name,
        containerDefinitions=[updated_container_definition],
    )
    new_task_definition_arn = new_task_definition['taskDefinition']['taskDefinitionArn']
    
    # Update the ECS service to use the new task definition
    ecs.update_service(
        cluster=client_cluster_name,
        service=client_service_name,
        taskDefinition=new_task_definition_arn,
        forceNewDeployment=True,
    )
    
    # Print a message indicating that the service update has been initiated
    print(f"Updated ECS service. Waiting for service to become stable.")
    
    # Wait for the service to become stable
    timeout_seconds = 300
    wait_delay = 20  # Time to wait between checks, in seconds
    max_attempts = timeout_seconds // wait_delay

    ecs.get_waiter('services_stable', WaiterConfig={'Delay': wait_delay, 'MaxAttempts': max_attempts}).wait(
        cluster=client_cluster_name,
        services=[client_service_name],
    )
    
    # Print a message indicating successful deployment
    print(f"Deployment successful for client: {client['name']}")

# The main function that orchestrates the entire deployment process
def main(config_toml_path, tag):
    config = toml.loads(config_toml_path)
    
    client = config['client'][0]
    repos = client['repos']
    current_repo = os.environ['CI_PROJECT_NAME']
    for repo in repos:
        if repo['name'] == current_repo:
            ecs_deployment(client, repo, tag)

if __name__ == "__main__":
    config_toml_path = sys.argv[1]
    tag = sys.argv[2]
    main(config_toml_path, tag)
