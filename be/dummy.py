import click
import yaml

def generate_docker_compose(service_name, image, ports=None, environment=None, volumes=None, output='docker-compose.yml'):
    """Generate a Docker Compose YAML file."""
    compose_dict = {
        'version': '3',
        'services': {
            service_name: {
                'image': image
            }
        }
    }

    # Add optional fields if provided
    if ports:
        compose_dict['services'][service_name]['ports'] = ports
    if environment:
        compose_dict['services'][service_name]['environment'] = environment
    if volumes:
        compose_dict['services'][service_name]['volumes'] = volumes

    # Write the dictionary to a YAML file
    with open(output, 'w') as file:
        yaml.dump(compose_dict, file, default_flow_style=False)

    click.echo(f"Docker Compose file '{output}' created successfully.")

@click.command()
@click.option('--output', prompt='Output file name', default='docker-compose.yml', help='Name of the output YAML file')
def cli(output):
    """Interactive CLI to create a Docker Compose YAML file."""
    service_name = click.prompt('Service name')
    image = click.prompt('Docker image (e.g., nginx:latest)')

    ports = click.prompt('List of ports to map (comma-separated, e.g., "8080:80,443:443")', default='', show_default=False)
    ports_list = ports.split(',') if ports else None

    env_vars = click.prompt('List of environment variables (comma-separated, e.g., "VAR1=value1,VAR2=value2")', default='', show_default=False)
    env_dict = {item.split('=')[0]: item.split('=')[1] for item in env_vars.split(',')} if env_vars else None

    volumes = click.prompt('List of volumes (comma-separated, e.g., "./data:/data,./log:/var/log")', default='', show_default=False)
    volumes_list = volumes.split(',') if volumes else None

    # Generate the Docker Compose file using the collected inputs
    generate_docker_compose(
        service_name=service_name,
        image=image,
        ports=ports_list,
        environment=env_dict,
        volumes=volumes_list,
        output=output
    )

if __name__ == '__main__':
    cli()
###############

import click
import yaml

def generate_docker_compose(base_template, services, output='docker-compose.yml'):
    """Generate a Docker Compose YAML file using a base template and adding services."""
    compose_dict = base_template

    # Add each service to the `services` section of the base template
    for service in services:
        service_name, service_config = service
        compose_dict['services'][service_name] = service_config

    # Write the dictionary to a YAML file
    with open(output, 'w') as file:
        yaml.dump(compose_dict, file, default_flow_style=False)

    click.echo(f"Docker Compose file '{output}' created successfully.")

@click.command()
@click.option('--output', prompt='Output file name', default='docker-compose.yml', help='Name of the output YAML file')
def cli(output):
    """Interactive CLI to add multiple services to a base Docker Compose template."""
    # Load or define your base template
    base_template = {
        'version': '3',
        'services': {}
    }

    services = []

    while True:
        service_name = click.prompt('Service name')
        image = click.prompt('Docker image (e.g., nginx:latest)')

        ports = click.prompt('List of ports to map (comma-separated, e.g., "8080:80,443:443")', default='', show_default=False)
        ports_list = ports.split(',') if ports else None

        env_vars = click.prompt('List of environment variables (comma-separated, e.g., "VAR1=value1,VAR2=value2")', default='', show_default=False)
        env_dict = {item.split('=')[0]: item.split('=')[1] for item in env_vars.split(',')} if env_vars else None

        volumes = click.prompt('List of volumes (comma-separated, e.g., "./data:/data,./log:/var/log")', default='', show_default=False)
        volumes_list = volumes.split(',') if volumes else None

        # Prepare the configuration for the current service
        service_config = {'image': image}
        if ports_list:
            service_config['ports'] = ports_list
        if env_dict:
            service_config['environment'] = env_dict
        if volumes_list:
            service_config['volumes'] = volumes_list

        services.append((service_name, service_config))

        # Ask if another service should be added
        add_more = click.confirm('Add another service?', default=False)
        if not add_more:
            break

    # Generate the Docker Compose file with the specified services
    generate_docker_compose(base_template, services, output)

if __name__ == '__main__':
    cli()
##################################### GEM

import click
import yaml

# Base template (you can read this from a file if needed)
BASE_TEMPLATE = {
    'services': {
        'cluster': {
            'image': 'docker/tilt-ctlptl',
            'environment': ['KIND_EXPERIMENTAL_DOCKER_NETWORK=${COMPOSE_PROJECT_NAME}_default'],
            'command': "bash -c 'cat <<EOF | ctlptl apply -f - && sleep infinity\n"
                       "apiVersion: ctlptl.dev/v1alpha1\nkind: Registry\n"
                       "name: tilt-avatars-registry\n---\napiVersion: ctlptl.dev/v1alpha1\n"
                       "kind: Cluster\nproduct: kind\nname: kind-tilt-avatars\n"
                       "registry: tilt-avatars-registry\nEOF'",
            'healthcheck': {
                'test': 'kubectl get nodes',
                'interval': '1s',
                'retries': 10,
                'start_period': '20s'
            },
            'volumes': ['kubeconfig:/root/.kube', '/var/run/docker.sock:/var/run/docker.sock']
        },
        'cluster-down': {
            'image': 'docker/tilt-ctlptl',
            'command': 'ctlptl delete cluster kind-tilt-avatars --cascade=true',
            'volumes_from': ['cluster'],
            'profiles': ['cli']
        },
        'tilt-up': {
            'image': 'docker/tilt',
            'environment': ['TILT_DISABLE_ANALYTICS=1', 'TILT_HOST=0.0.0.0'],
            'command': 'tilt up',
            'ports': ['10350:10350', '5734:5734', '5735:5735'],
            'working_dir': '/app',
            'volumes_from': ['cluster'],
            'volumes': ['.:/app'],
            'depends_on': {
                'cluster': {'condition': 'service_healthy'}
            }
        },
        'ctlptl': {
            'image': 'docker/tilt-ctlptl',
            'entrypoint': 'ctlptl',
            'volumes_from': ['cluster'],
            'profiles': ['cli']
        },
        'tilt': {
            'image': 'docker/tilt',
            'entrypoint': 'docker exec -i $COMPOSE_PROJECT_NAME-tilt-up-1 tilt',
            'volumes_from': ['tilt-up'],
            'profiles': ['cli']
        }
    },
    'volumes': {
        'kubeconfig': {}
    }
}

def add_service(services):
    """Interactively add a new service to the existing services."""
    service_name = click.prompt('Service name for the new service')
    image = click.prompt('Docker image (e.g., nginx:latest)')

    ports = click.prompt('List of ports to map (comma-separated, e.g., "8080:80,443:443")', default='', show_default=False)
    ports_list = ports.split(',') if ports else None

    env_vars = click.prompt('List of environment variables (comma-separated, e.g., "VAR1=value1,VAR2=value2")', default='', show_default=False)
    env_dict = {item.split('=')[0]: item.split('=')[1] for item in env_vars.split(',')} if env_vars else None

    volumes = click.prompt('List of volumes (comma-separated, e.g., "./data:/data,./log:/var/log")', default='', show_default=False)
    volumes_list = volumes.split(',') if volumes else None

    # Prepare the new service configuration
    service_config = {'image': image}
    if ports_list:
        service_config['ports'] = ports_list
    if env_dict:
        service_config['environment'] = env_dict
    if volumes_list:
        service_config['volumes'] = volumes_list

    # Add the new service to the `services` dictionary
    services[service_name] = service_config

@click.command()
@click.option('--output', prompt='Output file name', default='docker-compose.yml', help='Name of the output YAML file')
def cli(output):
    """Interactive CLI to add new services to the existing Docker Compose template."""
    services = BASE_TEMPLATE['services']

    # Loop to allow adding multiple services
    while True:
        add_service(services)
        add_more = click.confirm('Add another service?', default=False)
        if not add_more:
            break

    # Write back the updated dictionary to the output file
    with open(output, 'w') as file:
        yaml.dump(BASE_TEMPLATE, file, default_flow_style=False)

    click.echo(f"Docker Compose file '{output}' created successfully.")

if __name__ == '__main__':
    cli()
################# WOW
import click
import yaml

def load_base_template(filename):
    """Load the base template from a YAML file."""
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def add_service(services):
    """Interactively add a new service to the existing services."""
    service_name = click.prompt('Service name for the new service')
    image = click.prompt('Docker image (e.g., nginx:latest)')

    ports = click.prompt('List of ports to map (comma-separated, e.g., "8080:80,443:443")', default='', show_default=False)
    ports_list = ports.split(',') if ports else None

    env_vars = click.prompt('List of environment variables (comma-separated, e.g., "VAR1=value1,VAR2=value2")', default='', show_default=False)
    env_dict = {item.split('=')[0]: item.split('=')[1] for item in env_vars.split(',')} if env_vars else None

    volumes = click.prompt('List of volumes (comma-separated, e.g., "./data:/data,./log:/var/log")', default='', show_default=False)
    volumes_list = volumes.split(',') if volumes else None

    # Prepare the new service configuration
    service_config = {'image': image}
    if ports_list:
        service_config['ports'] = ports_list
    if env_dict:
        service_config['environment'] = env_dict
    if volumes_list:
        service_config['volumes'] = volumes_list

    # Add the new service to the `services` dictionary
    services[service_name] = service_config

@click.command()
@click.option('--input', prompt='Input YAML file', default='docker.yaml', help='Path to the existing base YAML file')
@click.option('--output', prompt='Output YAML file', default='docker-compose.yml', help='Path to the final YAML file')
def cli(input, output):
    """Interactive CLI to add new services to the existing Docker Compose template."""
    # Load the base template from the specified file
    base_template = load_base_template(input)

    # Ensure the 'services' key exists in the base template
    if 'services' not in base_template:
        base_template['services'] = {}

    services = base_template['services']

    # Loop to allow adding multiple services
    while True:
        add_service(services)
        add_more = click.confirm('Add another service?', default=False)
        if not add_more:
            break

    # Write the updated dictionary back to the output file
    with open(output, 'w') as file:
        yaml.dump(base_template, file, default_flow_style=False)

    click.echo(f"Docker Compose file '{output}' created successfully.")

if __name__ == '__main__':
    cli()
#####################
"""
In Docker Compose, the volumes_from directive specifies that a service should inherit volumes from another service or container. This is useful when services share the same data, making one service depend on another's volumes.

In your specific case, whether you need to add the new services to the volumes_from of the existing service depends on your data-sharing requirements:

Shared Data: If the new services need access to the same data as the referenced service (tilt-up), then you should include them in the volumes_from directive.
Isolated Data: If the new services have isolated or separate data needs, there's no requirement to add them to the volumes_from directive. Instead, configure individual volume mounts directly.
Here's a summary of how to approach it:

If a new service must share the same volumes as tilt-up, then:
yaml
Copy code
'tilt': {
    'image': 'docker/tilt',
    'entrypoint': 'docker exec -i $COMPOSE_PROJECT_NAME-tilt-up-1 tilt',
    'volumes_from': ['tilt-up', 'new_service_1', 'new_service_2'],  # or add other existing services
    'profiles': ['cli']
}
Be sure that the additional services are already defined and have their volumes configured correctly.
Otherwise, if your new services only require access to specific directories or files, you can add separate volumes entries in their configuration.
Remember to carefully manage dependencies between services to ensure that they start in the correct order and that the required data is available.
*/

"""

#######################

"""
version: '3.8'

services:
  # Cluster service (unchanged)
  cluster:
    image: docker/tilt-ctlptl
    environment:
      - KIND_EXPERIMENTAL_DOCKER_NETWORK=${COMPOSE_PROJECT_NAME}_default
    command: |
      bash -c 'cat <<EOF | ctlptl apply -f - && sleep infinity
      apiVersion: ctlptl.dev/v1alpha1
      kind: Registry
      name: tilt-avatars-registry
      ---
      apiVersion: ctlptl.dev/v1alpha1
      kind: Cluster
      product: kind
      name: kind-tilt-avatars
      registry: tilt-avatars-registry
      EOF'
    healthcheck:
      test: kubectl get nodes
      interval: 1s
      retries: 10
      start_period: 20s
    volumes:
      - kubeconfig:/root/.kube
      - /var/run/docker.sock:/var/run/docker.sock

  # Cluster-down service (unchanged)
  cluster-down:
    image: docker/tilt-ctlptl
    command: ctlptl delete cluster kind-tilt-avatars --cascade=true
    volumes_from:
      - cluster
    profiles:
      - cli

  # Tilt-up service (unchanged)
  tilt-up:
    image: docker/tilt
    environment:
      - TILT_DISABLE_ANALYTICS=1
      - TILT_HOST=0.0.0.0
    command: tilt up
    ports:
      - '10350:10350'
      - '5734:5734'
      - '5735:5735'
    working_dir: /app
    volumes_from:
      - cluster
    volumes:
      - .:/app
    depends_on:
      cluster:
        condition: service_healthy

  # New service B (example)
  service_b:
    image: custom/service_b:latest  # Replace with the actual image
    environment:
      - TILT_DISABLE_ANALYTICS=1
      - TILT_HOST=0.0.0.0
    command: tilt up --file /app/service_b.tiltfile  # Adjust this path accordingly
    working_dir: /app
    volumes_from:
      - cluster
    volumes:
      - .:/app  # Mount the necessary files for Tilt
    depends_on:
      - cluster

  # Existing ctlptl service (unchanged)
  ctlptl:
    image: docker/tilt-ctlptl
    entrypoint: ctlptl
    volumes_from:
      - cluster
    profiles:
      - cli

  # Existing tilt service (unchanged)
  tilt:
    image: docker/tilt
    entrypoint: docker exec -i $COMPOSE_PROJECT_NAME-tilt-up-1 tilt
    volumes_from:
      - tilt-up
    profiles:
      - cli

volumes:
  kubeconfig:
  pgdata:  # Keep or remove if not needed

"""

##########################
"""
version: '3.8'

services:
  # Existing Tilt-Up service
  tilt-up:
    image: docker/tilt
    environment:
      - TILT_DISABLE_ANALYTICS=1
      - TILT_HOST=0.0.0.0
    command: tilt up
    ports:
      - '10350:10350'
      - '5734:5734'
      - '5735:5735'
    working_dir: /app
    volumes_from:
      - cluster
    volumes:
      - .:/app
    depends_on:
      cluster:
        condition: service_healthy

  # New Service B
  service_b:
    image: custom/service_b:latest  # Replace with the actual image
    environment:
      - TILT_DISABLE_ANALYTICS=1
      - TILT_HOST=0.0.0.0
    command: tilt up --file /app/service_b.tiltfile  # Adjust path if necessary
    working_dir: /app
    volumes_from:
      - cluster
    volumes:
      - .:/app  # Adjust this path as needed
    depends_on:
      - cluster

  # Tilt command service
  tilt:
    image: docker/tilt
    entrypoint: docker exec -i $COMPOSE_PROJECT_NAME-tilt-up-1 tilt
    volumes_from:
      - tilt-up
      - service_b  # Both tilt-up and service_b for shared access
    profiles:
      - cli

"""