
# GitHub Webhook Receiver & UI Dashboard

This is the main application repository for the Developer Assessment Task. It consists of a Flask backend that receives GitHub webhooks (Push, Pull Request, Merge), stores them in MongoDB, and a frontend UI that polls for changes in real-time.

## 📋 Project Overview

*   **Backend:** Python (Flask)
*   **Database:** MongoDB
*   **Frontend:** HTML/JS (Polls API every 15 seconds)
*   **Purpose:** To capture and display Git events from a connected repository.

## ⚙️ Prerequisites

Before running the application, ensure you have the following installed:
1.  **Python 3.x**
2.  **MongoDB** (Ensure the service is running locally on port `27017`)
3.  **Ngrok** (To expose your localhost to GitHub)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <YOUR_WEBHOOK_REPO_LINK>
cd webhook-repo
```

### 2. Set Up Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Start your local MongoDB service, then run the setup script to create the database and collection schema:
```bash
python db_setup.py
```
*This will create the `git_events` database and applies necessary schema validation.*

## 🏃‍♂️ Running the Application

### Step 1: Start the Flask Server
```bash
python run.py
```
The application will start running at `http://localhost:5000`.

### Step 2: Expose via Ngrok 
In a separate terminal window, start Ngrok to tunnel traffic to your localhost:
```bash
ngrok http 5000
```
**Copy the HTTPS URL** provided by Ngrok (e.g., `https://random-id.ngrok-free.app`). You will need this to configure the GitHub Webhook. Also make sure you have authenticated in ngrok before running the above command.

### Step 3: Access the Dashboard
Open your browser and navigate to `http://localhost:5000`.
*   The UI polls the database every 15 seconds.
*   New events triggered in the Action Repo will appear here automatically.

## 📡 API Endpoints

*   `POST /webhook/receiver`: Endpoint for GitHub to send event payloads.
*   `GET /events`: Internal API used by the UI to fetch the latest stored events.
*   `GET /`: Renders the main dashboard.

## 🧪 Testing
To test this, you must configure a webhook on a separate GitHub repository (see the `action-repo` README for details).
