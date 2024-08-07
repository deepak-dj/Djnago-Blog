# Blog App

This is a simple Blog App that allows users to create, read, update, and delete blog posts and comments.
Also the user who created the post or comment can only have access to update and delete.

## Prerequisites

- Docker must be installed on your system. If you don't have Docker installed, you can download it from [Docker's official website](https://www.docker.com/get-started).
- Python and pip should be installed on your system.

### Installing Docker and Docker Compose in **Ubuntu**

For Ubuntu, run the following commands:

```bash
sudo apt update -y
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install docker-compose-v2 -y
sudo docker --version
```

## Getting Started

To run the application, use the following command in your terminal:

```bash
sudo docker compose up -d
```
**OR**

```bash
sudo docker-compose up -d
```

## API Documentation

Refer to the Swagger API documentation for details of API routes, request bodies, and response bodies at: [localhost](http://127.0.0.1:8000) once the application starts running.
