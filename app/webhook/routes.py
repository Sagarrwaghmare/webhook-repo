from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# relying on local mongodb instance for storage
client = MongoClient('mongodb://localhost:27017/')
db = client['git_dashboard']
events_col = db['events']

@webhook.route('/receiver', methods=["POST"])
def receiver():
    # github sends the event type in the header, crucial for switching logic
    event_type = request.headers.get('X-GitHub-Event', 'unknown')
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"msg": "Invalid payload"}), 400

    print(f"🔔 Event Received: {event_type}")
    
    mongo_data = None
    
    # formatting time to UTC string as requested in the assignment schema
    current_time = datetime.utcnow().strftime("%d %b %Y - %I:%M %p UTC")

    try:
        if event_type == 'push':
            # parsing push metadata; 'ref' usually looks like 'refs/heads/main'
            pusher = payload.get('pusher', {}).get('name')
            branch = payload.get('ref', '').split('/')[-1]
            commit_hash = payload.get('after')

            mongo_data = {
                "request_id": commit_hash,
                "author": pusher,
                "action": "PUSH",
                "from_branch": branch, # local HEAD
                "to_branch": branch,   # remote target
                "timestamp": current_time
            }

        elif event_type == 'pull_request':
            # extracting nested pr data to keep code clean
            pr_data = payload.get('pull_request', {})
            action = payload.get('action')
            
            # handling the brownie point requirement: 
            # a merge is technically a PR with action 'closed' and merged=True
            if action == 'closed' and pr_data.get('merged'):
                event_action = "MERGE"
            else:
                event_action = "PULL_REQUEST"

            mongo_data = {
                "request_id": str(pr_data.get('id')),
                "author": pr_data.get('user', {}).get('login'),
                "action": event_action,
                "from_branch": pr_data.get('head', {}).get('ref'),
                "to_branch": pr_data.get('base', {}).get('ref'),
                "timestamp": current_time
            }

        # only insert if we successfully parsed a supported event
        if mongo_data:
            events_col.insert_one(mongo_data)
            print(f"✅ Saved {mongo_data['action']} action to DB")
            return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ignored"}), 200