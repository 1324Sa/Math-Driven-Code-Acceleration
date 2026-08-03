import sympy as sp

class DynamicSymbolicEngine:
    @staticmethod
    def simplify_loop(
        var_name: str, 
        start_val: str, 
        end_val: str, 
        body_expr: str, 
        is_inclusive: bool = True, 
        step: str = "1"
    ) -> str | None:
        """
        حساب المجموع التجميعي Sum(body_expr, (var, start, end)) رمزيًا عبر SymPy
        وتحويل الحلقات التكرارية إلى صيغة مغلقة ذات تعقيد زمن $O(1)$.
        """
        try:
            # 1. تعريف رمز متغير الحلقة كعدد صحيح
            i = sp.Symbol(var_name, integer=True)
            
            # 2. تحويل حدود البداية والنهاية والعبارة البرمجية إلى تعابير SymPy
            start_expr = sp.sympify(start_val)
            
            # استبدال عطف الأسس ^ بـ ** لتوافق بايثون و SymPy
            clean_body = body_expr.replace('^', '**')
            clean_end = str(end_val).replace('^', '**')
            
            body_sympy = sp.sympify(clean_body)
            end_expr = sp.sympify(clean_end)

            # 3. معالجة النطاق المفتوح (<) مقابل المغلق (<=)
            if not is_inclusive:
                end_expr = end_expr - 1

            # 4. معالجة خطوة التزايد (Step) إذا كانت أكبر من 1
            step_expr = sp.sympify(step)
            if step_expr != 1:
                # تحويل المتغير الحركي ليعبر عن عدد الخطوات: i = start + k * step
                k = sp.Symbol('k', integer=True)
                body_sympy = body_sympy.subs(i, start_expr + k * step_expr)
                
                # حساب عدد التكرارات الأقصى n_steps
                n_steps = sp.floor((end_expr - start_expr) / step_expr)
                
                total_sum = sp.summation(body_sympy, (k, 0, n_steps))
            else:
                # المجموع المباشر عند step = 1
                total_sum = sp.summation(body_sympy, (i, start_expr, end_expr))

            # 5. تبسيط وتجميع الحدود الناتجة
            simplified = sp.factor(sp.simplify(total_sum))

            return str(simplified)

        except Exception as e:
            print(f"[Symbolic Engine Error]: {e}")
            return None