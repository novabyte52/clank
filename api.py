from transformers import pipeline, GPTNeoForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify

app = Flask(__name__)

model_name = "EleutherAI/gpt-neo-2.7B"  # Example model
model = GPTNeoForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

@app.route("/generate", methods=["POST"])
def generate_text():
    """
    handle request for generating text with clank

    data:
        response (string): the users response to the assistant, prompted or not.

    returns:
        string: clanks response to the user.
    """
    data = request.json  # Get the JSON payload
    input_text = data.get("text", "")  # Extract the input text
    if not input_text:
        return jsonify({"error": "No input text provided"}), 400

    # Tokenize input text
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate text
    outputs = model.generate(inputs["input_ids"], max_length=50, do_sample=True)

    # Decode the generated output and convert to string
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Return the generated text as JSON
    return jsonify({"generated_text": generated_text})


if __name__ == "__main__":
    app.run(debug=True)
