
---

# Git Event Webhook Dashboard

This project is a Flask-based web application that listens to GitHub webhook events for **Pushes**, **Pull Requests**, and **Merges**. It saves these events to a MongoDB database and displays them on a live-updating dashboard.

## Features

-   Receives and processes webhook data from GitHub.
-   Saves structured event data to a MongoDB collection with schema validation.
-   Provides a clean, real-time dashboard that polls for new events every 15 seconds.
-   Organized into a scalable Flask application structure using Blueprints.

***

## 1. Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Python 3.x**
*   **Pip** and **Virtualenv**
*   **MongoDB Community Server**: Download and install from the [official website](https://www.mongodb.com/try/download/community). Ensure the MongoDB service is running in the background.
*   **Ngrok**: Download from the [official website](https://ngrok.com/download) to expose your local server to the internet.

***

## 2. Local Setup

*   ### Clone the Repository
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

*   ### Create and Activate a Virtual Environment
    ```bash
    # Install virtualenv package if you don't have it
    pip install virtualenv

    # Create the virtual env
    virtualenv venv

    # Activate the virtual env
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

*   ### Install Requirements
    First, ensure you have a `requirements.txt` file. If not, create one with the following content:
    ```
    Flask
    pymongo
    flask-cors
    ```
    Then, install the packages:
    ```bash
    pip install -r requirements.txt
    ```

*   ### Initialize the Database
    This one-time script will create the `git_dashboard` database and the `events` collection with the required schema validation rules.
    ```bash
    python db_setup.py
    ```
    You should see a success message. You can verify the collection was created using **MongoDB Compass**.

***

## 3. Configuration (Ngrok & GitHub)

For GitHub to send events to your local machine, you need to create a secure tunnel using Ngrok.

*   ### Start Ngrok
    In a **new terminal window**, run the following command to expose your local port 5000.
    ```bash
    ngrok http 5000
    ```
    Ngrok will display a public URL (e.g., `https://random-string.ngrok-free.app`). **Copy the HTTPS URL.**

*   ### Configure the GitHub Webhook
    1.  Go to your GitHub repository and navigate to **Settings** > **Webhooks**.
    2.  Click **Add webhook**.
    3.  **Payload URL**: Paste your HTTPS Ngrok URL and append the endpoint path: `/webhook/receiver`.
        *   Example: `https://your-ngrok-url.ngrok-free.app/webhook/receiver`
    4.  **Content type**: Set this to **`application/json`**. This is critical.
    5.  **Which events would you like to trigger this webhook?**: Select **"Let me select individual events"**.
        *   Check **Pushes**.
        *   Check **Pull requests**.
    6.  Click **Add webhook**.

***

## 4. Running the Application

Make sure you have three processes running:
1.  The MongoDB service (usually in the background).
2.  The Ngrok tunnel (in its own terminal).
3.  The Flask application.

*   ### Run the Flask App
    In the terminal with your virtual environment activated, run:
    ```bash
    python run.py
    ```

*   ### View the Dashboard
    Open your web browser and go to:
    ```
    http://127.0.0.1:5000/
    ```

The dashboard will load, and as you push, create pull requests, or merge branches in your configured GitHub repository, new entries will appear automatically.

## Endpoints

*   `GET http://127.0.0.1:5000/`
    *   The main dashboard UI for viewing events.

*   `POST http://127.0.0.1:5000/webhook/receiver`
    *   The webhook receiver endpoint that GitHub sends data to.

*   `GET http://127.0.0.1:5000/api/events`
    *   The internal API that the frontend uses to fetch the latest event data from the database.