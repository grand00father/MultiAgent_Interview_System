import json

def to_json(text):
    text = text.strip()
    if "```json" in text:
        parts = text.split("```json")
        if len(parts) > 1:
            json_part = parts[1].split("```")[0].strip()
            if json_part.startswith("{") and json_part.endswith("}"):
                return json.loads(json_part)
                
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end <= 0:
        return {}
    return json.loads(text[start:end])
