import subprocess

def generate_kubernetes_manifest(chart_path, output_file, values=None, values_file=None):
    """
    Generate a plain Kubernetes YAML manifest from a Helm chart and specified values.
    
    :param chart_path: Path to the Helm chart.
    :param output_file: Path to output the final Kubernetes YAML manifest.
    :param values: A dictionary containing key-value pairs for Helm values.
    :param values_file: Path to a YAML file with Helm values (overrides inline values if both are given).
    """
    # Base helm template command
    helm_cmd = ['helm', 'template', chart_path]
    
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

if __name__ == "__main__":
    # Example usage
    chart_path = 'path/to/your/helm/chart'  # Replace with the path to your Helm chart
    output_file = 'output.yaml'
    
    # Optionally, provide key-value pairs or a values file
    values = {
        'replicaCount': 2,
        'image.tag': 'v1.0.0'
    }
    values_file = 'path/to/your/values.yaml'  # Set to None if not required
    
    # Generate the Kubernetes manifest
    generate_kubernetes_manifest(chart_path, output_file, values=values, values_file=values_file)