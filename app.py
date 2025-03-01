from flask import Flask, render_template, request, jsonify, send_file
import os
import requests
from pytube import YouTube

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    if "youtube.com" in url or "youtu.be" in url:
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            filepath = stream.download()

            return jsonify({"success": True, "download_link": f"/downloaded/{os.path.basename(filepath)}"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": False, "error": "Unsupported platform."})

@app.route("/downloaded/<filename>")
def serve_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
