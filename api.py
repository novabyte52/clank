from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/generate", methods=["POST"])
def generate_text():
    """
    handle request for generating text with clank

    data:
        response (string): the users response to the assistant, prompted or not.

    returns:
        string: clanks response to the user.
    """
    data = request.json
    prompt = data.get("response", "Hello, I am Clank")
    generator = pipeline("text-generation", model="gpt2")
    output = generator(prompt, max_length=50)
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
