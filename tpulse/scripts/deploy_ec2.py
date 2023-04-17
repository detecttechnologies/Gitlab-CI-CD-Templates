import os
import sys
import toml
import subprocess

# Run a shell command and return stdout and stderr as strings
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def ec2_deployment(client, repo):
    print(f"Starting EC2 deployment for client: {client['name']}")
    client_public_ip = client['ec2_public_ip']
    client_private_key = client['ec2_private_key']
    ssh_key_path = os.path.expanduser(f"~/.ssh/id_rsa_{client['name']}")

    os.makedirs(os.path.dirname(ssh_key_path), exist_ok=True)

    with open(ssh_key_path, 'w') as f:
        f.write(client_private_key.strip())
    os.chmod(ssh_key_path, 0o400)

    ec2_user = 'ubuntu'
    ci_project_dir = repo['name']
    local_project_dir = f'{ci_project_dir}/temp-worktree/dist/'
    remote_project_dir = '/home/ubuntu/pipeline_folder/dist/'

    commands = [
        f'ssh -v -i {ssh_key_path} {ec2_user}@{client_public_ip} "mkdir -p {remote_project_dir}"',
        f'rsync -zvhr -auv -e "ssh -v -i {ssh_key_path}" {local_project_dir} {ec2_user}@{client_public_ip}:{remote_project_dir}',
        f'ssh -v -i {ssh_key_path} {ec2_user}@{client_public_ip} "sudo cp -R {remote_project_dir}* /var/www/html/dist"',
    ]

    for cmd in commands:
        stdout, stderr = run_command(cmd)
        if stderr:
            print(f"Error executing command: {cmd}\n{stderr}")
        else:
            print(f"Command executed successfully: {cmd}\n{stdout}")


# The main function that orchestrates the entire deployment process
def main(config_toml_path):
    config = toml.loads(config_toml_path)
    
    client = config['client'][0]
    repos = client['repos']
    current_repo = os.environ['CI_PROJECT_NAME']
    for repo in repos:
        if repo['name'] == current_repo:
            ec2_deployment(client, repo)
if __name__ == "__main__":
    config_toml_path = sys.argv[1]
    main(config_toml_path)
