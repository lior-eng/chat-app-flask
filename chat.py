from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods= ["GET"])
def index_chat() -> str:
    return render_template('index.html')

@app.route("/<room>", methods= ["GET"])
def room_chat(room: str) -> str:
    return render_template('index.html')

@app.route("/api/chat/<room>", methods=["POST"])
def post_chat_message(room: str) -> tuple[str, int]:
    username = request.form.get("username")
    message = request.form.get("msg")
    
    if username and message:
        current_time: str = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        chat_line: str  = f"{current_time} {username}: {message}\n"
        
        file_path: str = f"/app/{room}_chat.txt"
        try:
            with open(file_path, "a") as chat_file:
                chat_file.write(chat_line)
        except FileNotFoundError:
            return "Room not found", 404
        
        return "", 201
    else:
        return "Invalid data", 400

@app.route("/api/chat/<room>", methods=["GET"])
def get_chat_messages(room: str) -> tuple[any, int]:
    file_path: str = f"/app/{room}_chat.txt"
    try:
        with open(file_path, "r") as chat_file:
            chat_lines: list[str] = chat_file.readlines()
            return jsonify(chat_lines), 200
    except FileNotFoundError:
        return "There are no messages yet; you can be the first one. ", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
