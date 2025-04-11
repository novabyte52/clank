"""
poop
"""
from transformers import AutoTokenizer

PADDING_TOKEN = "[PAD]"

def get_tokenizer(config):
    """
    poop
    """
    tokenizer = AutoTokenizer.from_pretrained(config["base_model_path"], **config["tokenizer_config"])

    tokenizer.add_special_tokens({'eos_token': '<eos>'})
    tokenizer.pad_token_id = tokenizer.convert_tokens_to_ids(
        PADDING_TOKEN
    )  # Set the padding token ID
    tokenizer.pad_token = PADDING_TOKEN

    return tokenizer
