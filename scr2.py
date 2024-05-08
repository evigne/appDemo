import subprocess

def helm_to_yaml(chart_path, output_file, values_file=None):
    # Start building the Helm command
    helm_cmd = ['helm', 'template', chart_path]
    
    # Include a values file if specified
    if values_file:
        helm_cmd.extend(['--values', values_file])
    
    # Run the helm command and capture the output
    result = subprocess.run(helm_cmd, capture_output=True, text=True)

    # Write the output directly to the YAML file
    with open(output_file, 'w') as yaml_file:
        yaml_file.write(result.stdout)

if __name__ == "__main__":
    # Example usage: Update paths to your specific Helm chart and values file
    chart_path = 'path/to/your/helm/chart'
    output_file = 'output.yaml'
    values_file = 'path/to/your/values.yaml'  # Set to None if no values file is needed
    
    helm_to_yaml(chart_path, output_file, values_file)