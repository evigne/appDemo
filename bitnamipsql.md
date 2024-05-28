Sure, here is a Python program that removes a specific dependency from the `Chart.yaml` file:

```python
import yaml

def remove_dependency(chart_file, dependency_name):
    with open(chart_file, 'r') as file:
        chart_data = yaml.safe_load(file)

    # Remove the specified dependency
    if 'dependencies' in chart_data:
        chart_data['dependencies'] = [
            dep for dep in chart_data['dependencies'] 
            if dep.get('name') != dependency_name
        ]

    # Write the modified data back to the file
    with open(chart_file, 'w') as file:
        yaml.safe_dump(chart_data, file)

if __name__ == "__main__":
    chart_file = 'Chart.yaml'
    dependency_name = 'postgres'
    remove_dependency(chart_file, dependency_name)
    print(f"Dependency '{dependency_name}' removed from {chart_file}.")
```

This script will:

1. Read the `Chart.yaml` file.
2. Parse the YAML content.
3. Remove the specified dependency from the `dependencies` list.
4. Write the modified content back to the `Chart.yaml` file.

Make sure you have the PyYAML library installed. You can install it using:

```sh
pip install pyyaml
```

Run the script in the directory containing your `Chart.yaml` file. The script will remove the specified dependency and save the updated file.