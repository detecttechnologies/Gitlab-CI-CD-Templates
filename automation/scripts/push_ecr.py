import os
import sys
import toml
import subprocess

# Run a shell command and return stdout and stderr as strings
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def ecr_push(client, repo, tag):

    # Set AWS environment variables
    os.environ["AWS_ACCOUNT_ID"] = client["aws_account_id"]
    os.environ["AWS_DEFAULT_REGION"] = client["region"]
    os.environ["AWS_ACCESS_KEY_ID"] = client["aws_access_key_id"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = client["aws_secret_access_key"]

    
    ecr_repository = f"{client['aws_account_id']}.dkr.ecr.{client['region']}.amazonaws.com/{repo['name']}"
    
    ci_registry_user = os.environ['CI_REGISTRY_USER']
    ci_registry_password = os.environ['CI_REGISTRY_PASSWORD']
    ci_registry = os.environ['CI_REGISTRY']
    ci_registry_image = os.environ['CI_REGISTRY_IMAGE']
    
    local_image = f"{ci_registry_image}:{tag}"
    remote_image = f"{ecr_repository}:{tag}"
    
    print(f"Pushing Docker image {local_image} to ECR repository {remote_image}")

    # Define the list of commands to be executed in sequence
    commands = [
        f"docker login -u {ci_registry_user} -p {ci_registry_password} {ci_registry}",
        f"docker pull {local_image}",
        f"docker tag {local_image} {remote_image}",
        f"aws ecr get-login-password --region {client['region']} | docker login --username AWS --password-stdin {ecr_repository}",
        f"docker push {remote_image}",
    ]

    # Execute the commands and handle errors
    for command in commands:
        stdout, stderr = run_command(command)
        if stderr:
            print(f"Error executing command: {command}\n{stderr}")
        else:
            print(f"Command executed successfully: {command}\n{stdout}")

    print(f"Image pushed to ECR: {remote_image}")

# The main function that orchestrates the entire deployment process
def main(config_toml_path, tag):
    config = toml.loads(config_toml_path)
    client = config['client'][0]
    repos = client['repos']
    current_repo = os.environ['CI_PROJECT_NAME']
    for repo in repos:
        if repo['name'] == current_repo:
            ecr_push(client, repo, tag)

if __name__ == "__main__":
    config_toml_path = sys.argv[1]
    tag = sys.argv[2]
    main(config_toml_path, tag)