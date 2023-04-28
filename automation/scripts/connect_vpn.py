import base64
import os
import subprocess
import sys
import toml
import pyotp

def main():
    config_file = os.environ["VPN_CONFIG"]
    config = toml.loads(config_file)

    totp_secret = config["vpn"]["totp_secret"]
    vpn_username = config["vpn"]["username"]
    prefix = config["vpn"]["prefix"]
    config_base64 = config["vpn"]["config_base64"]
    config_filename = config["vpn"]["config_filename"]

    keyfile_base64 = config["keyfile"]["content_base64"]
    keyfile_filename = config["keyfile"]["filename"]

    ca_cert_base64 = config["ca_cert"]["content_base64"]
    ca_cert_filename = config["ca_cert"]["filename"]

    with open(f"{config_filename}", "wb") as f:
        f.write(base64.b64decode(config_base64))

    # Read the existing configuration file
    with open(f"{config_filename}", "r") as f:
        config_contents = f.readlines()

    # Add the line to ignore IPv6 route directives
    config_contents.append("pull-filter ignore \"ifconfig-ipv6\"\n")
    config_contents.append("pull-filter ignore \"route-ipv6\"\n")
    config_contents.append("redirect-gateway def1\n")
    config_contents.append("log client.log\n")

    
    # Write the updated configuration file
    with open(f"{config_filename}", "w") as f:
        f.writelines(config_contents)

    print("Updated OpenVPN configuration file")


    with open(f"{keyfile_filename}", "wb") as f:
        f.write(base64.b64decode(keyfile_base64))
    # Add this line after writing the keyfile
    
    os.chmod(f"{keyfile_filename}", 0o600)
    
    with open(f"{ca_cert_filename}", "wb") as f:
        f.write(base64.b64decode(ca_cert_base64))

    totp = pyotp.TOTP(totp_secret)
    totp_token = totp.now()
    print(f"token:{totp_token}")

    os.umask(0o077)  # Set the umask before creating the file
    with open("vpn_auth.txt", "w") as f:
        f.write(vpn_username + "\n")
        f.write(prefix + totp_token)
    os.umask(0o022)  # Reset the umask after creating the file

    print("Created VPN authentication file")
    subprocess.run(["openvpn", "--config", f"{config_filename}", "--auth-user-pass", "vpn_auth.txt", "--daemon"])

if __name__ == "__main__":
    main()
