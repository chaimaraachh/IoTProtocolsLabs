![53](https://github.com/user-attachments/assets/9525e6e8-7656-479e-ba1c-1c36dd293b67)# Lightweight Kubernetes K3s for IoT Edge (Raspberry)

## Overview

This project explores the use of **K3s**, a lightweight Kubernetes distribution, to set up an efficient container orchestration platform for IoT Edge computing using Raspberry Pi. Kubernetes (K8s) is a powerful tool for container management, but its resource-intensive nature poses challenges for IoT and Edge devices. **K3s**, developed by Rancher, addresses these challenges with its minimal resource requirements and ease of deployment.

### Why K3s?

K3s is specifically designed for resource-constrained environments, offering:
- A single ~50MB binary, requiring only 512MB of RAM.
- Preconfigured and secure by default with tools like Containerd, CoreDNS, Flannel, and Traefik.
- CNCF certification, ensuring compatibility and reliability.

By utilizing **K3s**, this project demonstrates the deployment and management of a Kubernetes cluster on Raspberry Pi devices, simulating an edge computing environment.

## Objectives

1. **Set Up K3s**: Deploy K3s on two Raspberry Pi virtual machines, creating a cluster with one server and one agent.
2. **Explore K3s Features**:
   - Configure and manage cluster nodes.
   - Deploy containerized applications.
3. **Practical Applications**: Run a lightweight IoT application to simulate Edge computing.

## Tools and Technologies

- **K3s**: Lightweight Kubernetes for IoT and Edge computing.
- **Raspberry Pi OS (32-bit)**: Operating system for Raspberry Pi devices.
- **Docker**: Container runtime for application deployment.
- **Helm**: Kubernetes package manager for managing applications.

## Why IoT Edge?

IoT Edge computing enables real-time data processing closer to data sources, reducing latency and dependency on centralized cloud systems. By leveraging **K3s**, this project provides a scalable and efficient solution for deploying applications in such environments.

---


# Installation Process for K3s on Raspberry Virtual Machines

---

## 1. Installation of Two 23-bit Raspberry Virtual Machines

### Command Explanation: 
The command:
```bash
getconf LONG_BIT
```

### Explanation:
- **Purpose**: This command is used to determine whether the operating system is 32-bit or 64-bit.
- **Output**:
  
![1](https://github.com/user-attachments/assets/1ca04862-383e-4e1f-9106-9d645e868123)

---

## 2. K3s Installation on a Single Server

### Summary of the Installation Command:
The command:
```bash
curl -sfL https://get.k3s.io | sh -
```
![2](https://github.com/user-attachments/assets/9c18a369-c814-4afc-b497-fad9bd1d2f81)

### Explanation:
- **`curl`**: Downloads the installation script for K3s.
- **`-sfL`**:
  - `-s`: Runs in silent mode to suppress progress messages.
  - `-f`: Ensures silent failure for HTTP errors.
  - `-L`: Follows redirects if the URL points to another location.
- **`sh -`**: Executes the downloaded installation script directly.

---

### Steps Performed by the Script:
1. **Download and Verify**:
   - Fetches the latest stable K3s release binary.
   - Verifies the integrity of the binary file to ensure secure installation.

2. **Install K3s**:
   - Places the K3s binary in `/usr/local/bin/`.
   - Sets up additional Kubernetes tools:
     - `kubectl`: Kubernetes command-line tool.
     - `ctr` and `crictl`: Tools for container management.
   - Symlinks are created for these tools for easier access.

3. **Systemd Service Creation**:
   - Configures K3s to run as a systemd service.
   - The service file is stored in `/etc/systemd/system/k3s.service`.

4. **Environment Configuration**:
   - Creates environment files to allow advanced customization (e.g., enabling/disabling components, setting arguments).

---

# K3s Installation Verification

## b. Installation Verification

### Commands to verify the correct installation of the K3s server:
These commands help verify whether K3s is installed and running properly.
```bash
sudo systemctl status k3s  # Check the status of the K3s service
sudo kubectl get node      # List nodes in the K3s cluster
sudo kubectl get nodes -o wide  # Detailed information about nodes
```


![4](https://github.com/user-attachments/assets/2bd083d8-f767-4c5d-b5be-2beb71e4c402)



## c. Expected Results of Commands

### Command: `sudo kubectl get node`
This command shows the status of the K3s server node in the cluster. The expected result should indicate that the node is "Ready".
Expected result:

![5](https://github.com/user-attachments/assets/dc5c887e-55a9-4936-99e8-098315bd827b)


### Command: `sudo kubectl get nodes -o wide`
This command provides more detailed information about the K3s node, including IP addresses and operating system details.
Expected result:

![6](https://github.com/user-attachments/assets/a5933f4d-71b9-4ea9-8880-c453580e19ee)


## d. Commands to restart the K3s server
If the K3s service is not working correctly or you need to restart it, use these commands.
```bash
sudo systemctl restart k3s  # Restart the K3s service
sudo systemctl status k3s  # Check the status of the K3s service after restart
```



![7](https://github.com/user-attachments/assets/acf1fd30-cc4c-4701-ae1f-336ebe62f280)
---


# K3s Multi-Node Installation Guide

## 3. Installation of K3s with Multiple Agent Nodes

### a. How to Retrieve the Token (K3S_TOKEN: Environment Variable for the Token) from the Server
The token is required for agent nodes to join the K3s cluster. It can be retrieved from the server with the following command:

```bash
# On the K3s server, retrieve the token:
cat /var/lib/rancher/k3s/server/node-token
```

![8](https://github.com/user-attachments/assets/4ef76d0e-0269-4d2c-b160-1dd0aeb170ce)

### b. Commands to Configure a K3s Agent Node
To configure a K3s agent node and join it to the cluster:

```bash
# Run the following command on the agent node:
k3s agent --server https://<server-ip>:6443 --token <K3S_TOKEN>

# Example:
k3s agent --server https://192.168.58.135:6443 --token <retrieved-token>
```
![10](https://github.com/user-attachments/assets/79728e32-7b60-4e45-9647-3c5867f52090)


### c. Commands to Copy the K3s Configuration File from the Server to the Agent Node
The configuration file is located on the server at `/etc/rancher/k3s/k3s.yaml`. Use the `scp` command to copy it to the agent node:

```bash
# Copy the file from the server to the agent node:
scp root@<server-ip>:/etc/rancher/k3s/k3s.yaml ~/k3s-agent-config.yaml

# Example:
scp root@192.168.58.135:/etc/rancher/k3s/k3s.yaml ~/k3s-agent-config.yaml
```
![13](https://github.com/user-attachments/assets/30300611-6c8c-4d02-94f9-1749523f9472)

### d. Modifying the Configuration File to Contain the Server's IP Address
After copying the file, update the server IP address in the configuration file:

```bash
# Replace the default IP `127.0.0.1` with the server's actual IP:
sed -i 's/127.0.0.1/192.168.58.135/' ~/k3s-agent-config.yaml
```
![14](https://github.com/user-attachments/assets/0b7d69df-4bc9-4e06-8116-db3f141c04bf)


### e. Role of the Command: `kubectl config view`
This command is used to view the current Kubernetes configuration file (kubeconfig). It shows details about:
- Clusters
- Contexts
- Users
- Their associated credentials

It helps verify or troubleshoot Kubernetes cluster configuration.
![16](https://github.com/user-attachments/assets/684bc374-ba87-476a-a497-64cdb7746375)

### f. Role of the Command: `kubectl get nodes -o wide`
This command lists all the nodes in the Kubernetes cluster with additional information:
- Internal IP
- External IP
- Operating system
- Kernel version
- Container runtime details

It is useful for inspecting the cluster's node configurations.

### g. Role of the Command: `kubectl get pods -A`
This command displays all pods running across all namespaces. It provides:
- Pod names
- Status (e.g., Running, Pending, Failed)
- Namespaces
- Additional metadata

It is commonly used for monitoring and troubleshooting cluster workloads.
![17](https://github.com/user-attachments/assets/409599dc-dad9-4515-b39a-f8e11d64a507)
----


# Installation of Helm

## a. What is the role of Helm?

Helm is a package manager for Kubernetes, often referred to as the "Yum" or "Apt" for Kubernetes. It simplifies the deployment, upgrade, and management of applications on Kubernetes clusters by using predefined configuration templates called Helm Charts.

### Key Roles of Helm:
1. **Package Management**: Simplifies the distribution and deployment of Kubernetes applications.
2. **Configuration Management**: Allows customization of applications using a set of configurable parameters.
3. **Version Control**: Provides rollback capabilities to previous application states.
4. **Dependency Management**: Manages application dependencies for seamless deployment.

---

## b. Commands for installing Helm

To install Helm on a Raspberry Pi or any Linux-based system:

1. Download the Helm binary:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```



2. Verify the installation:
   ```bash
   helm version
   ```

This will output the version of Helm installed, confirming successful installation.
![19](https://github.com/user-attachments/assets/76617708-091a-4ba4-b835-c2926998a592)

---

## c. Purpose of the command: `helm list -n kube-system`

This command lists all the Helm releases deployed in the `kube-system` namespace.

### What it Verifies:
- Displays the names of the deployed Helm charts.
- Shows the status of each release (e.g., deployed, failed, pending).
- Indicates the revision number, which reflects the number of updates or rollbacks performed.
![20](https://github.com/user-attachments/assets/d39f3c03-e97f-4acd-87cd-7eea08e0515a)

---


## e. Explanation of the deployment of Traefik in the `kube-system` namespace

Traefik is a Kubernetes-native ingress controller and proxy server. When deployed in the `kube-system` namespace, it serves as the default ingress controller in many K3s setups.

### Significance:
1. **Traffic Management**: Traefik routes external HTTP(S) traffic to internal services in the Kubernetes cluster.
2. **Load Balancing**: Balances requests across multiple pods of a service.
3. **TLS Termination**: Handles secure connections with SSL/TLS certificates.
4. **Dynamic Configuration**: Automatically updates routes based on Kubernetes Ingress resources.
![21](https://github.com/user-attachments/assets/29c50db0-428d-45e0-9906-85ddc40ea71d)
![22](https://github.com/user-attachments/assets/dc63b7a9-476e-4f9d-b5eb-2638516cf31f)
![23](https://github.com/user-attachments/assets/d4925aee-ce8c-400a-bca0-ba59c7fb1869)

----

# Docker Installation and Python Application Deployment for Edge IoT

## 5. Docker Installation

### a. Docker Configuration Commands
To install and configure Docker on your system, use the following commands:

```bash
# Update package information
sudo apt update

# Install prerequisite packages
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable repository for Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# Add the current user to the Docker group
sudo usermod -aG docker $USER

# Verify Docker installation
docker --version
```
![29](https://github.com/user-attachments/assets/b497c482-8552-4670-8fcb-0ecd52bf201d)

### b. Purpose of the Command `sudo docker run hello-world`
This command verifies that Docker is installed and functioning correctly:
- **Pulls the "hello-world" image**: If the image is not present locally, Docker downloads it from Docker Hub.
- **Runs the image**: Executes the image in a container, displaying a confirmation message.
- **Purpose**: Tests Docker installation and configuration.
![30](https://github.com/user-attachments/assets/605f99bb-3e38-412c-8b66-41e7cbfcd06f)

---

## 6. Deploying a Python Application in Docker for Edge IoT

### Configuration and Deployment Steps
To deploy a Python-based IoT application in Docker, follow these steps:

#### Step 1: Create a Python Application
Create a simple Python application. For example, `iot_app.py`:

![32](https://github.com/user-attachments/assets/99909a6e-0a60-498b-91cc-703bdccb61e3)


#### Step 2: Write a Dockerfile
Create a `Dockerfile` to containerize the application:

![33](https://github.com/user-attachments/assets/a4f3afec-9218-4a38-b13e-09ad967d4496)


#### Step 3: Build and Run the Docker Image
```bash
# Build the Docker image
docker build -t iot-python-app .

# Run the container
docker run --name iot-app-container -d iot-python-app
```
![34](https://github.com/user-attachments/assets/21ddb3f1-f15d-4403-b024-d8fbfa18ff11)


---

# IoT Application Deployment Using Docker

This document contains the steps for setting up and deploying IoT applications in Docker using Raspberry Pi.

---

## Step 1: Setting Up the Node.js Application

1. Create a directory for your application.
   ```bash
   mkdir app-test
   cd app-test
   ```

2. Create the Node.js application file (`app.js`) with the following content:
   ```javascript
   const http = require('http');

   const server = http.createServer((req, res) => {
       res.writeHead(200, { 'Content-Type': 'text/plain' });
       res.end('Hello from app-test!');
   });

   server.listen(3000, () => {
       console.log('Server running on port 3000');
   });
   ```

![35](https://github.com/user-attachments/assets/b4e6597d-3135-44c2-a813-21877caa5c4d)

3. Create a `Dockerfile` for the Node.js application:
   ```Dockerfile
   FROM node:16-slim

   WORKDIR /app

   COPY app.js /app/app.js

   CMD ["node", "app.js"]
   ```

![36](https://github.com/user-attachments/assets/ceb8b3cb-448a-4cac-9558-ff9e700a09e2)

4. Build the Docker image:
   ```bash
   sudo docker build -t app-test .
   ```

---

![37](https://github.com/user-attachments/assets/7efcbe4b-8869-492f-b5f7-236b8275dcd0)

![39](https://github.com/user-attachments/assets/9f8befa2-d57b-4a2e-be95-10a666bcfe14)

![40](https://github.com/user-attachments/assets/d7b87736-cd55-446b-a3e3-3f7557702c19)

---

## Outputs

- **Node.js Application Output**: "Hello from app-test!" when accessed on port 3000.

---

---
## Step 2: Deploying the Application on Kubernetes

### Creating a Deployment File

1. Create a deployment file `app-test-deployment.yaml` with the following content:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: app-test
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: app-test
     template:
       metadata:
         labels:
           app: app-test
       spec:
         containers:
         - name: app-test-container
           image: chaimaraach/app-test:latest
           ports:
           - containerPort: 3000
   ```

![41](https://github.com/user-attachments/assets/b40ca3bf-ce21-4bda-9d37-2d462c1700b1)

2. Apply the deployment file to Kubernetes:
   ```bash
   kubectl apply -f app-test-deployment.yaml
   ```

![42](https://github.com/user-attachments/assets/e714f1e7-6301-4f43-a7f9-6af03a096319)

3. Verify the deployment:
   ```bash
   kubectl get deployments
   kubectl get pods
   ```

![43](https://github.com/user-attachments/assets/58eac67a-80b9-4015-ae4f-0de6292ee21f)

![44](https://github.com/user-attachments/assets/64ae63d0-b26b-46ac-bc61-53dc1bd0da2a)

4. Check the status of running pods:
   ```bash
   kubectl get pods -o wide
   ```

---

## Step 3: Exposing Kubernetes Deployment as a Service

### Steps to Expose and Verify the Service

1. Expose the deployment using a NodePort service:
   ```bash
   kubectl expose deployment app-test --type=NodePort --port=3000
   ```

![45](https://github.com/user-attachments/assets/fc8e22a9-140c-4e37-a9e1-215515cf7fb4)

2. Verify the service:
   ```bash
   kubectl get service app-test
   ```

3. Describe the service to get details:
   ```bash
   kubectl describe service app-test
   ```

4. Access the application through the service using the `<Node_IP>:<NodePort>` (e.g., `http://192.168.175.131:30343`):
   - **Using a Browser**: Visit the URL to confirm the application response.
   - **Using cURL**: Run the command:
     ```bash
     curl http://192.168.175.131:30343
     ```
   - **Using PowerShell**: Use the same URL with `curl`.

![46](https://github.com/user-attachments/assets/32b6037b-ec7b-4067-9911-977c50af13f1)

![47](https://github.com/user-attachments/assets/413e23ed-bc18-45cc-b285-1f9733ff6ef3)

![48](https://github.com/user-attachments/assets/ef106add-11b6-4c0d-8428-f3c389132683)


---

## Outputs

- **Service Description**: Detailed information about the Kubernetes service, including the NodePort.
- **Application Response**: "Hello from app-test!" message served via the browser, `curl`, or PowerShell.

---

Ensure the Kubernetes cluster has the correct configuration and the service's NodePort is accessible from your network.
## Step 4: Managing ReplicaSets and Updating Deployment

### Describing and Managing ReplicaSets

1. To describe the ReplicaSet associated with your deployment:
   ```bash
   kubectl describe replicaset -l app=app-test
   ```

![49](https://github.com/user-attachments/assets/30b2e60b-d55f-4b7a-bec7-50357b24e85c)

2. Outputs include:
   - **Pod Creation**: Shows the events where pods were created or deleted.
   - **ReplicaSet Information**: Details like labels, selectors, and replica counts.

### Updating Kubernetes Deployment

1. Edit the deployment file `app-test-deployment.yaml` to include resource requests, limits, environment variables, and probes:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: app-test
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: app-test
     template:
       metadata:
         labels:
           app: app-test
       spec:
         containers:
         - name: app-test-container
           image: chaimaraach/app-test:latest
           ports:
           - containerPort: 3000
           resources:
             requests:
               memory: "64Mi"
               cpu: "250m"
             limits:
               memory: "128Mi"
               cpu: "500m"
           livenessProbe:
             httpGet:
               path: /
               port: 3000
             initialDelaySeconds: 3
             periodSeconds: 5
           readinessProbe:
             httpGet:
               path: /
               port: 3000
             initialDelaySeconds: 3
             periodSeconds: 5
           env:
           - name: ENVIRONMENT
             value: "production"
           - name: APP_PORT
             value: "3000"
     affinity:
       nodeAffinity:
         requiredDuringSchedulingIgnoredDuringExecution:
           nodeSelectorTerms:
           - matchExpressions:
             - key: kubernetes.io/hostname
               operator: In
               values:
               - raspberry-agent
   ```

2. Apply the updated deployment file:
   ```bash
   kubectl apply -f app-test-deployment.yaml
   ```

![52](https://github.com/user-attachments/assets/2620286a-2944-4656-b53e-8bb9d8d1c0fc)

3. Verify the updated deployment:
   ```bash
   kubectl describe deployment app-test
   kubectl get pods
   ```

---

![53](https://github.com/user-attachments/assets/bf46b6a8-5835-46b7-86a3-581b9ee45ccc)

![54](https://github.com/user-attachments/assets/17e0c1ff-9409-4e50-9ea9-d79ab2ee1324)

## Outputs

- **ReplicaSets**: Shows scaling events and pod creation/deletion associated with the ReplicaSet.
- **Updated Deployment**: Reflects new configurations, such as resource limits and probes.

---


