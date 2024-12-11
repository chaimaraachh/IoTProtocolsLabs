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

