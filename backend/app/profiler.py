import time
import tracemalloc
from typing import Dict, Any

class ExecutionProfiler:
    """
    قياس الأداء والزمن واستخدام الذاكرة بدقة متناهية
    """
    @staticmethod
    def profile_function(func, *args, **kwargs) -> Dict[str, Any]:
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # تنفيذ الدالة
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        execution_time = end_time - start_time
        return {
            "result": result,
            "execution_time_seconds": round(execution_time, 6),
            "memory_peak_mb": round(peak / (1024 * 1024), 4)
        }