import json
import requests


class LocalOllamaOptimizer:

    def __init__(
        self,
        model_name: str = "llama3.1",
        base_url: str = "http://localhost:11434",
    ):
        self.model_name = model_name
        self.base_url = f"{base_url}/api/generate"

    def optimize_code(self, original_code: str, language: str) -> dict:
        # بناء الـ Prompt باستخدام التنسيق العادي لمنع تداخل الأقواس المزدوجة
        prompt = (
            "[ROLE] You are an Expert Code Optimizer.\n"
            f"[TASK] Refactor and heavily optimize the provided {language} code.\n\n"
            "[CRITICAL RULES]:\n"
            '1. OUTPUT FORMAT: Return ONLY valid JSON with keys "optimized_code" and "explanation".\n'
            "2. NO EXECUTION / RAW CODE ONLY: Do NOT calculate hardcoded results. Return fully executable SOURCE CODE text only.\n"
            "3. PRESERVE FUNCTION SIGNATURE: You MUST keep the function definition, function name, parameters, and return types intact. Never return a bare statement.\n"
            "4. MATHEMATICAL FORMULAS: Convert loops to O(1) math formulas or functional pipelines where applicable, but ALWAYS write them as valid executable code.\n\n"
            "[EXAMPLE JAVASCRIPT]:\n"
            "Input:\n"
            "function processData(arr) {\n"
            "  let sum = 0;\n"
            "  for (let i = 0; i < arr.length; i++) { sum += arr[i]; }\n"
            "  return sum;\n"
            "}\n"
            'Output JSON "optimized_code":\n'
            '"function processData(arr) { return arr.reduce((a, b) => a + b, 0); }"\n\n'
            f"[CODE TO OPTIMIZE]:\n```{language}\n{original_code}\n```"
        )

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        try:
            response = requests.post(self.base_url, json=payload, timeout=120)
            if response.status_code == 200:
                data = response.json()
                result_json = json.loads(data.get("response", "{}"))

                opt_code = result_json.get("optimized_code", "").strip()
                expl = result_json.get(
                    "explanation", "تم تبسيط الكود بنجاح."
                )

                if opt_code:
                    return {
                        "success": True,
                        "optimized_code": opt_code,
                        "math_explanation": expl,
                    }
        except Exception as e:
            print(f"[Ollama Error]: {e}")

        return {"success": False, "error": "Ollama Timeout or Error"}