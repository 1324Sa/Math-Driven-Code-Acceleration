import re
import ast
import time

class MultiLanguageOptimizer:

    @staticmethod
    def normalize_language(lang: str) -> str:
        lang = str(lang).lower().strip()
        if lang in ["c++", "cpp", "cplusplus"]:
            return "cpp"
        elif lang in ["javascript", "js"]:
            return "js"
        elif lang in ["rust", "rs"]:
            return "rust"
        elif lang in ["python", "py"]:
            return "python"
        return lang

    @staticmethod
    def optimize_python(code_str: str) -> tuple[str, list]:
        changes = []
        try:
            tree = ast.parse(code_str)
            class PythonTransformer(ast.NodeTransformer):
                def visit_For(self, node):
                    self.generic_visit(node)
                    if isinstance(node.iter, ast.Call) and getattr(node.iter.func, 'id', '') == 'range':
                        limit_arg = node.iter.args[0]
                        loop_var = node.target.id if isinstance(node.target, ast.Name) else None

                        if len(node.body) == 1 and isinstance(node.body[0], ast.AugAssign):
                            aug = node.body[0]
                            if isinstance(aug.op, ast.Add):
                                val = aug.value
                                if isinstance(val, ast.Name) and val.id == loop_var:
                                    changes.append("Python: تحويل حلقة range إلى O(1)")
                                    return ast.AugAssign(
                                        target=aug.target,
                                        op=ast.Add(),
                                        value=ast.BinOp(
                                            left=ast.BinOp(
                                                left=limit_arg, 
                                                op=ast.Mult(), 
                                                right=ast.BinOp(left=limit_arg, op=ast.Sub(), right=ast.Constant(value=1))
                                            ),
                                            op=ast.FloorDiv(),
                                            right=ast.Constant(value=2)
                                        )
                                    )
                    return node

            transformer = PythonTransformer()
            new_tree = transformer.visit(tree)
            ast.fix_missing_locations(new_tree)
            return ast.unparse(new_tree), changes
        except Exception:
            return code_str, []

    @staticmethod
    def optimize_js(code_str: str) -> tuple[str, list]:
        changes = []
        optimized = code_str

        # مطابقة حلقة for(let i=0; i<n; i++) أو i=1; i<=n
        pattern_nat = r'for\s*\(\s*(?:let|var)\s+(\w+)\s*=\s*(0|1)\s*;\s*\1\s*(<|<=)\s*(\w+|\d+)\s*;\s*\1\+\+\s*\)\s*\{\s*(\w+)\s*\+=\s*\1\s*;\s*\}'
        
        match = re.search(pattern_nat, code_str, re.MULTILINE)
        if match:
            var_i, start, op, limit, var_total = match.groups()
            
            if limit.isdigit():
                n = int(limit)
                calc_val = (n * (n + 1)) // 2 if op == "<=" or start == "1" else (n * (n - 1)) // 2
                replacement = f"{var_total} += {calc_val};"
            else:
                if op == "<=":
                    replacement = f"{var_total} += ({limit} * ({limit} + 1)) / 2;"
                else:
                    replacement = f"{var_total} += ({limit} * ({limit} - 1)) / 2;"
            
            optimized = re.sub(pattern_nat, replacement, code_str)
            changes.append("JS: استبدال الحلقة بحساب مباشر O(1)")

        return optimized, changes

    @staticmethod
    def optimize_rust(code_str: str) -> tuple[str, list]:
        changes = []
        optimized = code_str

        # مطابقة for i in 0..n { total += i; }
        pattern_nat = r'for\s+(\w+)\s+in\s+0\.\.(\w+|\d+)\s*\{\s*(\w+)\s*\+=\s*\1\s*;\s*\}'
        match = re.search(pattern_nat, code_str, re.MULTILINE)
        if match:
            var_i, limit, var_total = match.groups()
            if limit.isdigit():
                n = int(limit)
                calc_val = (n * (n - 1)) // 2
                replacement = f"{var_total} += {calc_val};"
            else:
                replacement = f"{var_total} += {limit} * ({limit} - 1) / 2;"
            
            optimized = re.sub(pattern_nat, replacement, code_str)
            changes.append("Rust: تبسيط نطاق 0..n إلى قانون O(1)")

        return optimized, changes

    @staticmethod
    def optimize_cpp(code_str: str) -> tuple[str, list]:
        changes = []
        optimized = code_str

        pattern_nat = r'for\s*\(\s*(?:int|long|long\s+long|size_t)\s+(\w+)\s*=\s*0\s*;\s*\1\s*<\s*(\w+|\d+)\s*;\s*\1\+\+\s*\)\s*\{\s*(\w+)\s*\+=\s*\1\s*;\s*\}'
        match = re.search(pattern_nat, code_str, re.MULTILINE)
        if match:
            var_i, limit, var_total = match.groups()
            replacement = f"{var_total} += (long long){limit} * ({limit} - 1) / 2;"
            optimized = re.sub(pattern_nat, replacement, code_str)
            changes.append("C++: تحويل حلقة الجمع إلى صيغة O(1)")

        return optimized, changes


class RealCodeAnalyzer:
    def __init__(self):
        self.optimizer = MultiLanguageOptimizer()

    def analyze_and_optimize(self, code_str: str, language: str = "python") -> dict:
        start_time = time.perf_counter()
        lang = self.optimizer.normalize_language(language)
        
        if lang == "python":
            opt_code, changes = self.optimizer.optimize_python(code_str)
        elif lang == "js":
            opt_code, changes = self.optimizer.optimize_js(code_str)
        elif lang == "cpp":
            opt_code, changes = self.optimizer.optimize_cpp(code_str)
        elif lang == "rust":
            opt_code, changes = self.optimizer.optimize_rust(code_str)
        else:
            opt_code, changes = code_str, []

        execution_time = (time.perf_counter() - start_time) * 1000

        return {
            "success": True,
            "language": lang,
            "optimized_code": opt_code,
            "applied_optimizations": changes if changes else ["لم يتم تبسيط الكود لعدم وجود مطابقة."],
            "execution_time_ms": round(execution_time, 3)
        }