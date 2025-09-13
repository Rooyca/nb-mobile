from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

load_dotenv()

OF_COURSE_THIS_IS_NOT_SAFE = os.environ.get("OF_COURSE_THIS_IS_NOT_SAFE")

FILENAME = ""

def load_notes(notebook):
    global FILENAME
    FILENAME = f"notes.{notebook}.json"
    if not os.path.exists(FILENAME):
        return None
    with open(FILENAME, "r") as f:
        return json.load(f)

def save_notes(notes, notebook):
    global FILENAME
    FILENAME = f"notes.{notebook}.json"
    with open(FILENAME, "w") as f:
        json.dump(notes, f, indent=4)

def check_auth(the_p):
    if the_p != OF_COURSE_THIS_IS_NOT_SAFE:
        return jsonify({"error": "Unauthorized "}), 401

@app.route("/notes", methods=["GET"])
def get_notes():
    the_p = request.args.get('the_p')
    check_auth(the_p)

    notebook = request.args.get('notebook')
    
    notes = load_notes(notebook)
    if notes is None:
        return jsonify({}), 200
    
    return jsonify(notes)

@app.route("/notes", methods=["DELETE"])
def delete_notes():
    the_p = request.args.get('the_p')
    check_auth(the_p)

    idd = request.args.get('id')
    if not idd:
        return jsonify({"error": "Invalid request"}), 400

    notebook = request.args.get('notebook')

    notes = load_notes(notebook)
    if notes is None:
        return jsonify({}), 200

    notes["notes"] = [note for note in notes["notes"] if note["id"] != int(idd)]
    save_notes(notes, notebook)
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    the_p = data.get("the_p") 
    check_auth(the_p)

    notebook = data.get("notebook")

    notes = load_notes(notebook)
    if notes is None:
        notes = {"notes_index": 0, "notes": []}

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
    
    save_notes(notes, notebook)
    return jsonify({"message": "Note added successfully"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
