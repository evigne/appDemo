import os
import subprocess

def render_helm_chart(chart_path, output_file, values_file=None):
    # Define the Helm command
    helm_cmd = ['helm', 'template', chart_path]
    
    # Add values file if specified
    if values_file:
        helm_cmd.extend(['--values', values_file])
    
    try:
        # Execute the Helm template command
        result = subprocess.run(helm_cmd, capture_output=True, text=True, check=True)
        
        # Write the result to the specified output file
        with open(output_file, 'w') as yaml_file:
            yaml_file.write(result.stdout)
        
        print(f"Kubernetes manifest has been written to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during Helm template execution: {e}")
        print(e.stderr)

if __name__ == "__main__":
    # Example usage
    chart_path = 'path/to/your/helm/chart'  # Update with your Helm chart path
    output_file = 'output.yaml'
    values_file = 'path/to/your/values.yaml'  # Update with your values file or set to None if not needed
    
    render_helm_chart(chart_path, output_file, values_file)