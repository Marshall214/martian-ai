import os
import re
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import login
from dotenv import load_dotenv

# Load environment variables (such as HF_TOKEN)
load_dotenv()


class LlamaHumanizer:
    """
    Singleton wrapper for the Llama 3.1 8B Instruct model.
    Loads once on first call and reuses across all subsequent requests.
    Uses NF4 4-bit quantization via bitsandbytes to fit in ~4GB VRAM.
    """
    _instance = None
    _model = None
    _tokenizer = None
    _pipeline = None

    @classmethod
    def get_pipeline(cls):
        if cls._pipeline is None:
            # --- Validate HF_TOKEN before attempting download ---
            hf_token = os.getenv("HF_TOKEN")
            if not hf_token or hf_token.strip() == "":
                raise RuntimeError(
                    "HF_TOKEN is not set. Llama 3.1 is a gated model — you must:\n"
                    "  1. Accept the license at https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct\n"
                    "  2. Create an access token at https://huggingface.co/settings/tokens\n"
                    "  3. Set HF_TOKEN=hf_your_token_here in backend/.env"
                )
            login(token=hf_token)

            print("Loading Llama 3.1 8B model in 4-bit precision...")
            model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

            # Configure 4-bit quantization to run on 4GB VRAM + 32GB RAM
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16
            )

            cls._tokenizer = AutoTokenizer.from_pretrained(model_id)
            cls._model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=bnb_config,
                device_map="auto"  # Automatically splits across GPU and CPU
            )

            cls._pipeline = pipeline(
                "text-generation",
                model=cls._model,
                tokenizer=cls._tokenizer,
            )
            print("Model loaded successfully.")
        return cls._pipeline


# --- Output sanitization patterns ---
# Llama often prepends these despite the "no preamble" instruction.
_PREAMBLE_PATTERNS = [
    re.compile(r"^(Sure[!,.]?\s*)", re.IGNORECASE),
    re.compile(r"^(Of course[!,.]?\s*)", re.IGNORECASE),
    re.compile(r"^(Here(?:'s| is) (?:the |a |my )?rewritten (?:text|version)[:\.\!\s]*)", re.IGNORECASE),
    re.compile(r"^(Here(?:'s| is) (?:the |a |my )?(?:revised|updated|new) (?:text|version)[:\.\!\s]*)", re.IGNORECASE),
    re.compile(r"^(I'?ve rewritten (?:the |your )?text[:\.\!\s]*)", re.IGNORECASE),
    re.compile(r"^(Below is (?:the |a )?rewritten (?:text|version)[:\.\!\s]*)", re.IGNORECASE),
]


def _sanitize_output(text: str) -> str:
    """Strip common Llama preamble artifacts from the generated output."""
    cleaned = text.strip()

    # Remove leading preamble patterns
    for pattern in _PREAMBLE_PATTERNS:
        cleaned = pattern.sub("", cleaned).strip()

    # Remove wrapping quotes if the model quoted the entire output
    if len(cleaned) > 2 and cleaned[0] == '"' and cleaned[-1] == '"':
        cleaned = cleaned[1:-1].strip()

    return cleaned


def rewrite_with_llama(text: str, tone: str = "casual human") -> str:
    """
    Rewrites text using Llama 3.1 8B to bypass AI detection by optimizing
    for perplexity and burstiness.

    Args:
        text: The input text to humanize.
        tone: Target tone for the rewrite (default: "casual human").

    Returns:
        The rewritten text with Llama preamble artifacts stripped.

    Raises:
        RuntimeError: If HF_TOKEN is missing or model loading fails.
    """
    pipe = LlamaHumanizer.get_pipeline()
    tokenizer = LlamaHumanizer._tokenizer

    system_prompt = f"""You are an expert human writer whose goal is to rewrite the provided text to bypass AI detection models (like ZeroGPT). 
Your rewriting MUST preserve all specific domain terminology and technical nouns completely intact. 

To bypass AI detection, you must:
1. INCREASE BURSTINESS: Vary your sentence lengths dramatically. Mix very short, punchy 3-word sentences with longer, complex 20-word sentences naturally.
2. INCREASE PERPLEXITY: Avoid standard AI phrases. Never use phrases like 'In conclusion', 'It is important to note', 'Crucial', 'Furthermore', 'Moreover', 'Delve', 'Tapestry', or 'Testament to'.
3. MATCH TONE: The requested tone is '{tone}'.

Only return the rewritten text, with absolutely no preamble, explanation, or conversational filler like 'Here is the rewritten text:'.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Rewrite this text:\n\n{text}"},
    ]

    # Scale max_new_tokens to 1.5× the input token count, capped at 2048.
    # This prevents truncation for longer inputs while staying within model limits.
    input_tokens = len(tokenizer.encode(text, add_special_tokens=False))
    max_new_tokens = min(int(input_tokens * 1.5), 2048)
    # Ensure a reasonable minimum
    max_new_tokens = max(max_new_tokens, 256)

    outputs = pipe(
        messages,
        max_new_tokens=max_new_tokens,
        temperature=0.7,   # Randomness for burstiness
        top_p=0.9,
        do_sample=True,    # Required for temperature/top_p to take effect
    )

    raw_output = outputs[0]["generated_text"][-1]["content"].strip()
    return _sanitize_output(raw_output)
