import subprocess

def generate_kubernetes_manifest(chart_path, output_file, release_name=None, values=None, values_file=None):
    """
    Generate a plain Kubernetes YAML manifest from a Helm chart and specified values,
    including a specific release name.

    :param chart_path: Path to the Helm chart.
    :param output_file: Path to output the final Kubernetes YAML manifest.
    :param release_name: The release name for the Helm deployment.
    :param values: A dictionary containing key-value pairs for Helm values.
    :param values_file: Path to a YAML file with Helm values (overrides inline values if both are given).
    """
    # Base helm template command
    helm_cmd = ['helm', 'template']
    
    # Include the release name if specified
    if release_name:
        helm_cmd.append(release_name)
    
    helm_cmd.append(chart_path)
    
    # If a values file is specified, include it
    if values_file:
        helm_cmd.extend(['--values', values_file])
    
    # If inline values are specified, append them
    if values:
        for key, value in values.items():
            helm_cmd.extend(['--set', f"{key}={value}"])

    # Execute the command and capture the output
    result = subprocess.run(helm_cmd, capture_output=True, text=True)
    
    # Write the command output directly to the YAML file
    with open(output_file, 'w') as yaml_file:
        yaml_file.write(result.stdout)

def change_image_name(values, image_name):
    """
    Update the image name in a given values dictionary.

    :param values: The values dictionary where the image name needs to be updated.
    :param image_name: The new image name to set.
    """
    # Assuming that the image name is specified in the `image.repository` field
    values['image.repository'] = image_name

if __name__ == "__main__":
    # Example usage
    chart_path = 'path/to/your/helm/chart'  # Replace with the path to your Helm chart
    output_file = 'output.yaml'
    release_name = 'my-release'  # Specify the release name

    values = {
        'replicaCount': 2,
        'image.repository': 'default-image',
        'image.tag': 'v1.0.0'
    }
    values_file = None  # Set to 'path/to/your/values.yaml' if needed

    # Change the image name to a desired one
    new_image_name = 'my-custom-image'
    change_image_name(values, new_image_name)

    # Generate the Kubernetes manifest with the specified release name
    generate_kubernetes_manifest(chart_path, output_file, release_name, values=values, values_file=values_file)