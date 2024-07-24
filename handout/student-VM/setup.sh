#!/bin/bash

# ------------------------------------------------------------------------------
# Required softwares in student VM:
#   - terraform
#   - azure cli
#   - docker
#   - kubectl #TODO(@Marcus)
#   - python 3.9
# ------------------------------------------------------------------------------

setup_docker() {
    # Uninstall old versions
    for pkg in docker.io docker-doc docker-compose containerd runc; do
        sudo apt-get remove $pkg;
    done

    # set up the repository
    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get install ca-certificates curl gnupg

    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
        "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # install
    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # add user to docker group
    sudo gpasswd -a azureuser docker
    newgrp docker

    # check
    docker --version
}

# setup_terraform() {
#     sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install gnupg software-properties-common
#     wget -O- https://apt.releases.hashicorp.com/gpg | \
#         gpg --dearmor | \
#         sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

#     gpg --no-default-keyring \
#         --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
#         --fingerprint

#     echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
#         https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
#         sudo tee /etc/apt/sources.list.d/hashicorp.list

#     sudo apt update
#     sudo DEBIAN_FRONTEND=noninteractive apt-get install -y terraform

#     terraform --version
# }


setup_azure_cli() {
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
    az
}


setup_kubectl() {
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    kubectl version --client
}

setup_jq() {
    sudo apt update
    sudo apt install jq
}


# IMPORTANT TO AVOID RACE CONDITION
# See https://developer.hashicorp.com/packer/docs/debugging#issues-installing-ubuntu-packages
cloud-init status --wait

# Python3 already exists on Ubuntu VM, so we are not installing that here.
setup_docker
#setup_terraform
setup_azure_cli
setup_kubectl
setup_jq
