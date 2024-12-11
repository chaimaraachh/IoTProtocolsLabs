# Lightweight Kubernetes K3s for IoT Edge (Raspberry)

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

