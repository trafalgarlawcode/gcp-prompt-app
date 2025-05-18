from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.get_json()
    message = data.get('message', '')
    return jsonify({"reply": f"You said: {message}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
