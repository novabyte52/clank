class ConversationContext:
    """
    poop
    """

    def __init__(self):
        self.history = []

    def add_message(self, user_message, assistant_response):
        """
        poop
        """
        self.history.append({"user": user_message, "assistant": assistant_response})

    def get_history(self):
        """
        poop
        """
        return self.history

    def get_context(self):
        """
        poop
        """
        # Combine all previous user inputs and assistant responses into one string
        context = ""
        for message in range(len(self.history) - 3, len(self.history)):
            context += f"User: {message['user']}\nAssistant: {message['assistant']}\n"
        return context

# === old context stuff for reference === #

# from flask import jsonify, Blueprint, request, current_app
# from api.utils import create_session_id
# from api.conversation.conversation_context import ConversationContext
# from api.constants import ConfigKeys

# active_sessions = {}

# clank = Blueprint("clank", __name__)

# PREAMBLE = (
#     "You are Clank, an AI assistant. Your purpose is to assist users with helpful and relevant res"
#     "ponses. Stay polite, conversational, and focused on the user's questions or needs. Don't be a"
#     "fraid to ask for more context if needed."
# )

# @clank.route("/generate", methods=["POST"])
# def generate():
#     """
#     handle request for generating text with clank

#     data:
#         response (string): the users response to the assistant, prompted or not.

#     returns:
#         string: clanks response to the user.
#     """
#     tokenizer = current_app.config[ConfigKeys.TOKENIZER.name]
#     data = request.json  # Get the JSON payload
#     input_text = data.get("text", "")  # Extract the input text
#     session_id = data.get("session_id", None)

#     if not input_text:
#         return jsonify({"error": "No input text provided"}), 400

#     if not session_id:
#         session_id = create_session_id()
#         active_sessions[session_id] = ConversationContext()

#     context = active_sessions[session_id]

#     # Get the full conversation context
#     full_context = PREAMBLE + "\n" + context.get_context()

#     # Combine the full context with the new user message
#     model_input = full_context + f"User: {input_text}\nAssistant:"


#     # Decode the generated output and convert to string
#     generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Store user input and assistant response in context
#     context.add_message(input_text, generated_text)

#     # Return the generated text as JSON
#     return jsonify({
#         "session_id": session_id,
#         "generated_text": generated_text,
#         "history": context.history
#     })
