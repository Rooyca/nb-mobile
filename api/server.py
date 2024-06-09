from flask import Flask, request, jsonify
import json, os, sys
from datetime import datetime, timedelta
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

load_dotenv()

DATA_FILE = os.environ.get("FILENAME", "notes.json")
OF_COURSE_THIS_IS_NOT_SAFE = os.environ.get("OF_COURSE_THIS_IS_NOT_SAFE")

def load_notes():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=4)

def get_expire_after(data):
    expire_after_str = data.get("expire_after")
    if expire_after_str:
        try:
            return int(expire_after_str)
        except ValueError:
            pass
    return 1

@app.route("/notes", methods=["GET"])
def get_notes():
    the_p = request.args.get('the_p')
    if the_p != OF_COURSE_THIS_IS_NOT_SAFE:
        return jsonify({"error": "Unauthorized "}), 401
    notes = load_notes()
    save_notes(notes)
    return jsonify(notes)

@app.route("/notes", methods=["DELETE"])
def delete_notes():
    the_p = request.args.get('the_p')
    if the_p != OF_COURSE_THIS_IS_NOT_SAFE:
        return jsonify({"error": "Unauthorized "}), 401

    idd = request.args.get('id')
    if not idd:
        return jsonify({"error": "Invalid request"}), 400

    notes = load_notes()
    notes["notes"] = [note for note in notes["notes"] if note["id"] != int(idd)]
    save_notes(notes)
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    if data.get("the_p") != OF_COURSE_THIS_IS_NOT_SAFE:
        return jsonify({"error": "Unauthorized "}), 401

    notes = load_notes()
    
    # Ensure notes_index and notes keys exist
    if "notes_index" not in notes:
        notes["notes_index"] = 0
    if "notes" not in notes:
        notes["notes"] = []
    
    notes["notes_index"] += 1
    note_id = notes["notes_index"]
    tags = data.get("tags")
    if tags:
        tags = tags.replace(" ", "")
        tags = tags.split(",")
        tags = ["#"+tag for tag in tags]
    
    notes["notes"].append({
        "id": note_id,
        "content": data["content"],
        "tags": tags,
        "is_todo": data.get("is_todo", False),
        "is_bookmark": data.get("is_bookmark", False),
        "timestamp": datetime.now().strftime("%Y%m%d%H%M")
    })
    
    save_notes(notes)
    return jsonify({"message": "Note added successfully"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
