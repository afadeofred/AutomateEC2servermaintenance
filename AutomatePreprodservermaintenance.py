import boto3
import subprocess

def update_ec2_instances(instance_ids):
    """
    Update EC2 instances with the specified instance IDs.
    """
    try:
        # Connect to AWS EC2 service
        ec2_client = boto3.client('ec2')

        # Stop instances before updating
        ec2_client.stop_instances(InstanceIds=instance_ids)
        waiter = ec2_client.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=instance_ids)
        print("Instances stopped successfully.")

        # Apply updates
        apply_os_updates()

        # Start instances after updating
        ec2_client.start_instances(InstanceIds=instance_ids)
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=instance_ids)
        print("Instances started successfully.")

        print("Instance update process completed.")

    except Exception as e:
        print(f"Error updating instances: {e}")

import subprocess
import platform

def apply_os_updates():
    """
    Apply operating system updates using package manager.
    """
    os_type = platform.system()

    if os_type == "Linux":
        # Check if it's Amazon Linux
        if platform.linux_distribution()[0] == "Amazon Linux AMI":
            try:
                # Try running yum update command
                subprocess.run(['yum', 'update', '-y'], check=True)
            except subprocess.CalledProcessError:
                # If yum update fails, run apt-get update and upgrade
                print("yum update failed, running apt-get update and upgrade")
                subprocess.run(['apt-get', 'update', '-y'])
                subprocess.run(['apt-get', 'upgrade', '-y'])
        # For Ubuntu instances
        elif platform.linux_distribution()[0] == "Ubuntu":
            try:
                # Try running apt-get update and upgrade
                subprocess.run(['apt-get', 'update', '-y'], check=True)
                subprocess.run(['apt-get', 'upgrade', '-y'], check=True)
            except subprocess.CalledProcessError:
                print("apt-get update or upgrade failed")
        else:
            print("Unsupported Linux distribution")
    else:
        print("Unsupported operating system")

# Test the function
apply_os_updates()


if __name__ == "__main__":
    # List of instance IDs to update
    instance_ids = ['instance_id_1', 'instance_id_2']  # Replace these with your actual instance IDs
    
    # Call the function to update instances
    update_ec2_instances(instance_ids)
