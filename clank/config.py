"""
Clank configuration settings
"""

GPTNEO_BASE = "EleutherAI/gpt-neo-2.7B"

app_config = {
    "base_model_path": GPTNEO_BASE,

    "tokenizer_config": {
        "return_tensors": "pt",
        "padding": True,
        "max_length": 2048,
        "truncation": True
    },

    "api_port": 5000,
    "notes_dir": "./markdown_testing",

    "db": {
        "surrealdb": {
            "host": "localhost",
            "port": 8000,
            "protocol": "ws",  # "http" or "ws"
            "namespace": "clank",
            "database": "vault",
            "username": "root",
            "password": "root",
            "rpc_path": "/rpc"
        },
        "postgres": {
            "host": "localhost",
            "port": 5432,
            "database": "clank",
            "user": "postgres",
            "password": "postgres"
        }
    }
}
