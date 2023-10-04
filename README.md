# Opencord

## Table of Contents

1. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
2. [Setting Up Python Virtual Environment](#setting-up-python-virtual-environment)
3. [Running the Application](#running-the-application)
4. [Accessing Web Server](#accessing-web-server)

---

## Getting Started

### Prerequisites

- Install NPM: Download and install from [Node.js website](https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi)

### Installation

1. Open terminal or CMD in your working directory and run:
    ```bash
    npm install
    ```

2. To start the application, run:
    ```bash
    npm start
    ```

---

## Setting Up Python Virtual Environment

1. Create a Python virtual environment to ensure all modules/libraries are the same version:
    ```bash
    python -m venv /path/to/new/virtual/environment
    ```

2. **For Windows**: Activate the virtual environment:
    ```bash
    <venv>\\Scripts\\activate
    ```

   **For Mac**: Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

   *Note*: Once activated, the name of the virtual environment should appear on the far left of your terminal/cmd.

3. Install required libraries/modules:
    ```bash
    pip install -r requirements.txt
    ```

   *Note*: `requirements.txt` is included in the git files.

---

## Running the Application

1. Navigate to the web server directory and run:
    ```bash
    flask --app main run
    ```

---

## Accessing Web Server

- Open your web browser and go to:
    ```
    http://127.0.0.1:5000
    ```

---

