from flask import Flask, render_template, request, jsonify, send_file
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_URL = os.getenv("URL")

@app.route('/manifest.json')
def serve_manifest():
    return send_file('static/manifest.json', mimetype='application/manifest+json')

@app.route('/styles.css')
def serve_styles():
    return send_file('static/styles.css', mimetype='text/css')

@app.route("/")
def index():
    return render_template("index.html", IP=API_URL)

@app.route("/view")
def view():
    return render_template("view.html", IP=API_URL)

@app.route("/add_note", methods=["POST"])
def add_note():
    content = request.form.get("content")
    expiry_time = request.form.get("expiry_time", 24)
    data = {"content": content, "expiry_time": expiry_time}
    response = requests.post(f"{API_URL}/notes", json=data)
    return response.text

@app.route("/get_notes")
def get_notes():
    response = requests.get(f"{API_URL}/notes")
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')
