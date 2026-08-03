import sympy as sp
import re
from tree_sitter_languages import get_language
from tree_sitter import Parser

class UniversalASTOptimizer:
    def __init__(self):
        self.parsers = {}
        for lang in ["cpp", "javascript", "python", "rust"]:
            try:
                language_obj = get_language(lang)
                parser = Parser(language_obj)
                self.parsers[lang] = parser
            except Exception as e:
                print(f"[AST Warning] Could not load parser for {lang}: {e}")

    def _normalize_lang(self, lang: str) -> str:
        lang = str(lang).lower().strip()
        mapping = {
            "c++": "cpp", "cpp": "cpp",
            "js": "javascript", "javascript": "javascript",
            "py": "python", "python": "python",
            "rs": "rust", "rust": "rust"
        }
        return mapping.get(lang, lang)

    def optimize(self, code_str: str, lang: str) -> tuple[str, list]:
        lang_key = self._normalize_lang(lang)

        # التحقق من سلامة البناء الشجري (AST Syntax Check)
        if lang_key in self.parsers:
            try:
                parser = self.parsers[lang_key]
                tree = parser.parse(bytes(code_str, "utf8"))
                if tree.root_node.has_error:
                    return code_str, ["خطأ في بناء الكود (Syntax Error) بالنسبة للغة المحددة."]
            except Exception as e:
                print(f"[AST Parse Error]: {e}")

        optimized_code, changes = self._optimize_loop_expression(code_str, lang_key)
        return optimized_code, changes

    def _optimize_loop_expression(self, code_str: str, lang_key: str) -> tuple[str, list]:
        changes = []

        # 1. مطابقة Python: range(n) أو range(start, end)
        py_range_n_pattern = r'for\s+(\w+)\s+in\s+range\(\s*(\w+|\d+)\s*\):\s*\n?\s*(\w+)\s*\+=\s*(.*)'
        py_range_se_pattern = r'for\s+(\w+)\s+in\s+range\(\s*(\d+)\s*,\s*(\w+|\d+)(?:\s*\+\s*1)?\s*\):\s*\n?\s*(\w+)\s*\+=\s*(.*)'

        # 2. مطابقة C++ / JS / Rust
        cpp_js_pattern = r'for\s*\(\s*(?:let|var|int)?\s*(\w+)\s*=\s*(\d+);\s*\1\s*(<=|<)\s*(\w+|\d+);\s*\1\+\+\s*\)\s*\{\s*(\w+)\s*\+=\s*(.*?);?\s*\}'

        match = None
        is_python = (lang_key == "python")

        if is_python:
            match_n = re.search(py_range_n_pattern, code_str)
            match_se = re.search(py_range_se_pattern, code_str)
            
            if match_n:
                var_i, n_str, target_var, expr_str = match_n.groups()
                start_val = 0
                n_sym = sp.Symbol(n_str, integer=True)
                upper_bound = n_sym - 1  # range(n) تعني من 0 إلى n-1
                match = match_n
            elif match_se:
                var_i, start_str, n_str, target_var, expr_str = match_se.groups()
                start_val = int(start_str)
                n_sym = sp.Symbol(n_str, integer=True)
                upper_bound = n_sym
                match = match_se
        else:
            match = re.search(cpp_js_pattern, code_str, re.DOTALL)
            if match:
                var_i, start_str, op, n_str, target_var, expr_str = match.groups()
                start_val = int(start_str)
                n_sym = sp.Symbol(n_str, integer=True)
                upper_bound = n_sym if op == '<=' else n_sym - 1

        if match:
            try:
                i = sp.Symbol(var_i, integer=True)
                clean_expr = expr_str.strip().rstrip(';').replace('^', '**')
                sympy_expr = sp.sympify(clean_expr)

                # التجميع الرمزي ∑
                sum_result = sp.summation(sympy_expr, (i, start_val, upper_bound))
                simplified = sp.factor(sp.simplify(sum_result))

                formatted_math = str(simplified)

                if lang_key == "python":
                    replacement = f"{target_var} = {formatted_math}"
                elif lang_key in ["javascript", "js"]:
                    replacement = f"{target_var} += Math.floor({formatted_math});"
                else:
                    replacement = f"{target_var} += ({formatted_math});"

                optimized_code = code_str.replace(match.group(0), replacement)
                changes.append(f"تم اختزال الحلقة إلى معادلة مغلقة O(1): `{replacement}`")
                return optimized_code, changes

            except Exception as e:
                print(f"[SymPy Processing Error]: {e}")

        return code_str, ["الكود مدخل بصيغة مغلقة ومسرّع مسبقاً O(1)، أو لا يحتوي على حلقة تكرار قابلة للاختزال."]