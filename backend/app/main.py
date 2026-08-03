from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from .ast_engine import UniversalASTOptimizer

app = FastAPI(
    title="Accelerated Code Engine API",
    description="محرك تبسيط وتسريع الأكواد برمجياً عبر التحليل الشجري والجبر الرمزي",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

optimizer = UniversalASTOptimizer()

class CodeRequest(BaseModel):
    code: str
    language: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "سيرفر منصة هندسة اللغات المسرّعة يعمل بنجاح."}

# معالجة الطلب سواء كان من /api/optimize أو /api/v1/optimize
@app.post("/api/optimize")
@app.post("/api/v1/optimize")
def optimize_code(req: CodeRequest):
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="الكود المدخل فارغ.")

    start_time = time.perf_counter()

    try:
        optimized_code, changes = optimizer.optimize(req.code, req.language)
        exec_time = (time.perf_counter() - start_time) * 1000

        return {
            "success": True,
            "language": req.language,
            "optimized_code": optimized_code,
            "applied_optimizations": changes if changes else ["لم يتم العثور على حلقة مطابقة للتبسيط الرمزي."],
            "execution_time_ms": round(exec_time, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء معالجة الكود: {str(e)}")