from pymongo import MongoClient

def setup_database():
    client = MongoClient('mongodb://localhost:27017/')
    db_name = 'git_dashboard'
    
    # Drop database if exists to start fresh (Optional, remove if you want to keep data)
    # client.drop_database(db_name) 
    
    db = client[db_name]

    # VALIDATION RULES (The "Schema")
    # This enforces that data MUST match your image requirements before saving.
    collection_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["request_id", "author", "action", "from_branch", "to_branch", "timestamp"],
            "properties": {
                "request_id": {
                    "bsonType": "string",
                    "description": "Commit Hash or PR ID - Required String"
                },
                "author": {
                    "bsonType": "string",
                    "description": "GitHub Username - Required String"
                },
                "action": {
                    "enum": ["PUSH", "PULL_REQUEST", "MERGE"],
                    "description": "Must be one of: PUSH, PULL_REQUEST, MERGE"
                },
                "from_branch": {
                    "bsonType": "string",
                    "description": "Source Branch - Required String"
                },
                "to_branch": {
                    "bsonType": "string",
                    "description": "Target Branch - Required String"
                },
                "timestamp": {
                    "bsonType": "string",
                    "description": "UTC Date Time String - Required String"
                }
            }
        }
    }

    try:
        db.create_collection("events", validator=collection_schema)
        print("✅ Database 'git_dashboard' and Collection 'events' created with Strict Schema.")
    except Exception as e:
        print(f"⚠️ Collection might already exist. Details: {e}")

if __name__ == "__main__":
    setup_database()