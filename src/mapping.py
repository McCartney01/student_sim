from .nano_graphrag._llm import gpt_4o_complete, llama_complete, gpt_35_complete, claude_complete

MODEL_FUNC_MAP = {
    "4o": gpt_4o_complete,
    "3.5": gpt_35_complete,
    "claude": claude_complete,
    "llama": llama_complete
}

STR_TO_MODEL_NAME_MAP = {
    "4o": "gpt-4o",
    "3.5": "gpt-3.5-turbo",
    "claude": "claude-3-5-sonnet-20240620",
    "llama": "meta-llama/Llama-3.3-70B-Instruct-Turbo"
}