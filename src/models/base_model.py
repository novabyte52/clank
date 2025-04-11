"""
poop
"""
from transformers import AutoModelForCausalLM
from clank.utils.tokenizer import get_tokenizer
from clank.config import app_config

class BaseModel:
    """
    poop
    """
    def __init__(self, model_path):
        self.tokenizer = get_tokenizer(app_config)
        # self.model = AutoModelForCausalLM.from_pretrained(model_path)

    def generate_response(self, prompt):
        """
        poop
        """
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.9,        # Randomness in output
            top_k=52,               # Limits to top 50 tokens for diversity
            top_p=0.85,             # Uses nucleus sampling for more natural text
            repetition_penalty=1.9,
            do_sample=True          # Enables sampling instead of deterministic output
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
