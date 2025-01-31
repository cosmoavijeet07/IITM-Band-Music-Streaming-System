# Project Setup

This guide covers the setup for the complete development environment including the Vue.js frontend, Mailhog, a Python application, and Celery with Redis as the broker.

## Prerequisites

Ensure you have npm, Python, Redis, and Go installed on your machine. Additionally, Celery requires the Redis server to function as a message broker.

## Installation Steps

First, clone the repository to your local machine and navigate into the project directory.

### Install Node Modules
```bash
npm install
```

### Run the Vue.js Development Server
```bash
npm run serve
```

### Build for Production
```bash
npm run build
```

### Lint and Fix Files
```bash
npm run lint
```

### Mailhog
Start Mailhog server (ensure you have Mailhog installed and properly configured):
```bash
~/go/bin/Mailhog
```

### Python Application
Start the Python backend application:
```bash
python3 App.py
```

### Redis Server
Start the Redis server:
```bash
redis-server
```

### Celery Worker
Start the Celery worker process:
```bash
celery -A App.celery worker -l info
```

### Celery Beat
Start the Celery beat process for periodic tasks:
```bash
celery -A App.celery beat --max-interval 1 -l info
```

## Customize Configuration
For detailed information on project configuration and additional settings, refer to the [Vue CLI Configuration Reference](https://cli.vuejs.org/config/).

## Additional Information
For more detailed information about each component, visit their respective documentation or help pages.
