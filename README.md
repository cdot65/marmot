# Marmot

![Palo Alto Networks Logo](docs/images/paloaltonetworks_logo.png)

A collection of automation demonstrations that I use for work; provides Ansible playbooks, Python scripts, and Terraform projects to automate and manage Palo Alto Networks devices.

This repository is mostly geared towards hands-on workshops where we teach the tecnology, it should not be considered a production-ready solution.

## Table of Contents

- [Marmot](#marmot)
  - [Table of Contents](#table-of-contents)
  - [Setting Up Your Environment](#setting-up-your-environment)
    - [Using VScode Dev Containers](#using-vscode-dev-containers)
    - [Creating Python Virtual Environments](#creating-python-virtual-environments)
  - [Where to Find Documentation](#where-to-find-documentation)
  - [Contributing](#contributing)
  - [Author](#author)

## Setting Up Your Environment

There are two ways to set up your environment to execute the Ansible playbooks in this repository. You can either use Invoke to build the Docker containers and access the shell of the containers, or you can create Python virtual environments and execute Ansible within the virtual environments.

### Using VScode Dev Containers

1. clone this repository to your local workstation with VScode installed
2. after installing VScode's "Dev Container's" extension, open the repository in a container with `Dev Containers: Rebuild and Reopen in Container...`

### Creating Python Virtual Environments

1. Install Python virtualenv: `pip3 install virtualenv`
2. Create a virtual environment: `virtualenv venv`
3. Activate the virtual environment:
   - For Linux/Mac: `source venv/bin/activate`
   - For Windows: `venv\Scripts\activate`
4. Install the required Python libraries: `pip3 install -r requirements.txt`

## Where to Find Documentation

Project-specific documentation can be found in the README.md files within each standalone project directory.

- `pan-os-python`, refer to [the official documentation](https://pan-os-python.readthedocs.io/)
- `Palo Alto Ansible Collection`, refer to [the official documentation](https://paloaltonetworks.github.io/pan-os-ansible/)
- `panos` Terraform provider, refer to [the official documentation](https://registry.terraform.io/providers/PaloAltoNetworks/panos/latest/docs)

## Contributing

We welcome contributions from the community. To contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them to your branch
4. Submit a pull request with a description of your changes

## Author

Calvin Remsburg @cdot65
