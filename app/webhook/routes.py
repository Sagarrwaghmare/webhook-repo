import datetime
from flask import Blueprint, json, request
from pymongo import MongoClient

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# --- 1. SETUP MONGODB CONNECTION ---
# Connect to local MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['git_dashboard']  # Database name
events_col = db['events']     # Collection name

def call_external_api(data):
    print(f"--> Calling External API with: {data}")

@webhook.route('/receiver', methods=["POST"])
def receiver():
    # 1. Identify the event type
    event_type = request.headers.get('X-GitHub-Event', 'unknown')
    
    try:
        # Use get_json(silent=True) to prevent crashing if headers are wrong
        payload = request.get_json(silent=True)
        
        # If payload is None, check if GitHub sent form-data instead
        if not payload:
            if request.form and 'payload' in request.form:
                payload = json.loads(request.form['payload'])
            else:
                return "Invalid Content-Type or Empty Payload.", 400

        print("\n---------------------------------")
        print(f"🔔 EVENT RECEIVED: {event_type}")

        # Initialize data object to save
        mongo_data = None

        # --- HANDLE PUSH ---
        if event_type == 'push':
            pusher = payload.get('pusher', {}).get('name', 'Unknown')
            branch = payload.get('ref', '').split('/')[-1]
            commit_hash = payload.get('after', '')

            print(f"👉 PUSH: User '{pusher}' pushed to branch '{branch}'")
            call_external_api({"event": "push", "user": pusher})

            # Prepare Data for Mongo
            mongo_data = {
                "request_id": commit_hash,
                "author": pusher,
                "action": "PUSH",
                "from_branch": branch,
                "to_branch": branch, # Pushes happen on the same branch
                "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }

        # --- HANDLE PULL REQUEST (Includes Merge) ---
        elif event_type == 'pull_request':
            action = payload.get('action')
            pr_data = payload.get('pull_request', {})
            pr_title = pr_data.get('title', 'No Title')
            is_merged = pr_data.get('merged', False)
            
            # Determine if it's a MERGE or just a PR update
            db_action = "PULL_REQUEST"
            if action == 'closed' and is_merged:
                print(f"🔀 MERGE: PR '{pr_title}' was successfully merged!")
                call_external_api({"event": "merge", "title": pr_title})
                db_action = "MERGE"
            elif action == 'opened':
                print(f"📝 PR OPENED: '{pr_title}'")
                call_external_api({"event": "pr_opened", "title": pr_title})
            else:
                print(f"ℹ️ PR ACTION: {action}")

            # Prepare Data for Mongo
            mongo_data = {
                "request_id": str(pr_data.get('id')),
                "author": pr_data.get('user', {}).get('login'),
                "action": db_action,
                "from_branch": pr_data.get('head', {}).get('ref'),
                "to_branch": pr_data.get('base', {}).get('ref'),
                "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }

        else:
            print(f"Event {event_type} received but not handled.")

        # --- SAVE TO DB ---
        if mongo_data:
            try:
                events_col.insert_one(mongo_data)
                print("✅ Successfully saved to MongoDB")
            except Exception as db_err:
                print(f"❌ Database Error: {db_err}")

        print("---------------------------------\n")
        return "Webhook received", 200

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}, 400