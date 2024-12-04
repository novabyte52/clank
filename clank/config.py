"""
poop
"""
GPTNEO_BASE = "EleutherAI/gpt-neo-2.7B"

app_config = {
    "base_model_path": GPTNEO_BASE,
    # define more model paths for specialized models
    "tokenizer_config": {"return_tensors": "pt", "padding": True, "max_length": 2048, "truncation": True},
    "api_port": 5000,
}
