import subprocess
import json
import re
from config import MODEL, SYSTEM_PROMPT


# =========================================================
# EXTRACT JSON FROM MODEL OUTPUT
# =========================================================

def extract_json(text):
    """
    Extract the first valid JSON object from model output.
    """

    # Direct parse
    try:
        return json.loads(text)
    except:
        pass

    # Extract embedded JSON
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except:
            return None

    return None


# =========================================================
# MAIN LLM QUERY FUNCTION
# =========================================================

def query_llm(user_input):

    # Proper structured prompt
    prompt = f"""
{SYSTEM_PROMPT}

User Request:
{user_input}

Assistant:
"""

    # Run Ollama model
    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8"
    )

    # Raw output
    output = result.stdout.strip()

    # =====================================================
    # CLEAN OUTPUT
    # =====================================================

    # Remove ANSI terminal escape codes
    output = re.sub(
        r'\x1b\[[0-9;]*[a-zA-Z]',
        '',
        output
    )

    # Remove HTML/XML tags
    output = re.sub(
        r'<[^>]+>',
        '',
        output
    )

    # Remove markdown code fences
    output = re.sub(
        r'```json|```',
        '',
        output
    )

    output = output.strip()

    # =====================================================
    # TRY JSON PARSING
    # =====================================================

    parsed = extract_json(output)

    if parsed and isinstance(parsed, dict):

        msg_type = parsed.get("type", "")

        # -------------------------
        # NORMAL ANSWER
        # -------------------------
        if msg_type == "answer":

            content = parsed.get("content", "").strip()

            if content:
                return content

        # -------------------------
        # ACTION REQUEST
        # -------------------------
        if msg_type == "action":
            return parsed

    # =====================================================
    # FALLBACK SAFETY
    # =====================================================

    # If empty after cleaning
    if not output:
        return "I couldn't generate a valid response."

    return output