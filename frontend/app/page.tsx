'use client';

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { Zap, Play, AlertCircle, ShieldCheck, Code2, Calculator, ChevronDown, ChevronUp } from 'lucide-react';

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), {
  ssr: false,
  loading: () => <div className="p-4 text-slate-500 text-sm">جاري تحميل محرر الأكواد...</div>
});

interface OptimizationResponse {
  success: boolean;
  language?: string;
  original_code?: string;
  optimized_code?: string;
  complexity?: string;
  math_explanation?: string;
  verification?: {
    verified: boolean;
    reason: string;
    speedup_factor?: string;
    orig_time?: string;
    opt_time?: string;
  };
  error_details?: string;
  status?: string;
}

export default function Home() {
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('python');
  const [showExplanation, setShowExplanation] = useState<boolean>(true);
  const [inputCode, setInputCode] = useState<string>(
`def process_data(n):
    total = 0
    for i in range(1, n + 1):
        total += i ** 2 + 3 * i
    return total`
  );
  
  const [result, setResult] = useState<OptimizationResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleOptimize = async () => {
    setLoading(true);
    setErrorMessage('');
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          code: inputCode, 
          language: selectedLanguage 
        }),
      });

      if (!response.ok) {
        throw new Error(`خطأ من السيرفر: ${response.status}`);
      }

      const data: OptimizationResponse = await response.json();
      setResult(data);

      if (!data.success && data.error_details) {
        setErrorMessage(data.error_details);
      }
    } catch (err: any) {
      setErrorMessage("تعذر الاتصال بالسيرفر! تأكد من تشغيل uvicorn على البورت 8000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 font-sans" dir="rtl">
      {/* Header */}
      <header className="flex flex-wrap justify-between items-center pb-6 border-b border-slate-800 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-emerald-400 flex items-center gap-2">
            <Zap className="w-8 h-8 text-yellow-400" /> منصة هندسة معالجة اللغات المسرّعة
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            تبسيط الأكواد ديناميكياً بواسطة مكتبات الجبر الرمزي، التفاضل والتكامل، والجبر الخطي الإحصائي
          </p>
        </div>

        <div className="flex items-center gap-4 flex-wrap">
          <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-xl">
            <Code2 className="w-4 h-4 text-emerald-400" />
            <label htmlFor="lang-select" className="text-xs font-medium text-slate-300">اللغة:</label>
              // قم بتحديث جزء الخيارات الخاص باختيار اللغة داخل page.tsx:
          <select
             id="lang-select"
             value={selectedLanguage}
             onChange={(e) => setSelectedLanguage(e.target.value)}
             className="bg-slate-800 text-emerald-400 font-mono text-xs rounded-lg px-3 py-1 border border-slate-700 focus:outline-none focus:border-emerald-500 cursor-pointer"
            >
            <option value="python">Python 🐍</option>
            <option value="cpp">C++ ⚡</option>
            <option value="c">C 🔵</option>
            <option value="java">Java ☕</option>
            <option value="javascript">JavaScript 📜</option>
            <option value="rust">Rust 🦀</option>
          </select>
          </div>

          <button
            onClick={handleOptimize}
            disabled={loading}
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-6 py-2.5 rounded-xl transition-all shadow-lg flex items-center gap-2 cursor-pointer disabled:opacity-50"
          >
            <Play className="w-4 h-4 fill-current" />
            {loading ? "جاري الاشتقاق..." : "🚀 تطبيق التسريع الآن"}
          </button>
        </div>
      </header>

      {/* تنبيه الخطأ */}
      {errorMessage && (
        <div className="mt-4 p-4 bg-rose-900/40 border border-rose-700 rounded-xl flex items-center gap-3 text-rose-300 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* شارة التحقق الحتمي ونسبة التسريع */}
      {result?.verification && result.verification.verified && (
        <div className="mt-4 p-4 bg-emerald-950/50 border border-emerald-800 rounded-xl flex flex-wrap justify-between items-center gap-4 text-emerald-300 text-sm">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <span>{result.verification.reason}</span>
          </div>
          {result.verification.speedup_factor && (
            <div className="flex items-center gap-4 font-mono text-xs bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800" dir="ltr">
              <span>Speedup: <strong className="text-yellow-400">{result.verification.speedup_factor}</strong></span>
              <span>Orig: {result.verification.orig_time}</span>
              <span>Opt: {result.verification.opt_time}</span>
            </div>
          )}
        </div>
      )}

      {/* شبكة المحررات */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        
        {/* 1. محرر الكود المدخل */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl flex flex-col">
          <div className="bg-slate-800/80 p-3 border-b border-slate-700 text-xs font-mono text-emerald-400 font-bold flex justify-between items-center">
            <span>📝 الكود المدخل ({selectedLanguage.toUpperCase()}):</span>
            <span className="text-slate-400 text-[10px]">Active Input</span>
          </div>
          <div className="p-2 bg-slate-950 flex-1" dir="ltr">
            <textarea
              value={inputCode}
              onChange={(e) => setInputCode(e.target.value)}
              placeholder="Write your code here..."
              className="w-full h-[380px] bg-slate-950 text-emerald-300 font-mono text-sm p-4 rounded-xl border border-slate-800 focus:outline-none focus:border-emerald-500 resize-none leading-relaxed text-left"
              spellCheck={false}
              dir="ltr"
            />
          </div>
        </div>

        {/* 2. محرر النتيجة المسرّعة */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl flex flex-col">
          <div className="bg-slate-800/80 p-3 border-b border-slate-700 text-xs font-mono text-cyan-400 font-bold flex justify-between items-center">
            <span>🚀 الكود المبسط والمسرّع ({selectedLanguage.toUpperCase()}):</span>
            {result?.complexity && (
              <span className="bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded text-[10px]">
                {result.complexity}
              </span>
            )}
          </div>
          <div className="p-2 bg-slate-950 flex-1" dir="ltr">
            {result?.optimized_code ? (
              <textarea
                readOnly
                value={result.optimized_code}
                className="w-full h-[380px] bg-slate-950 text-cyan-300 font-mono text-sm p-4 rounded-xl border border-slate-800 focus:outline-none resize-none leading-relaxed text-left"
                dir="ltr"
              />
            ) : (
              <div className="h-[380px] flex items-center justify-center text-slate-500 text-sm border border-dashed border-slate-800 rounded-xl" dir="rtl">
                اضغط على "تطبيق التسريع الآن" ليظهر الكود المسرّع هنا
              </div>
            )}
          </div>
        </div>

      </div>

      {/* مكون التفسير بالمعادلة الرياضية والحسابية والمنطقية */}
      {result?.math_explanation && (
        <div className="mt-6 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <button
            onClick={() => setShowExplanation(!showExplanation)}
            className="w-full bg-slate-800/80 p-4 flex justify-between items-center text-emerald-400 font-bold text-sm hover:bg-slate-800 transition cursor-pointer"
          >
            <div className="flex items-center gap-2">
              <Calculator className="w-5 h-5 text-yellow-400" />
              <span>تفسير الكود بالمعادلة الرياضية والحسابية والمنطقية</span>
            </div>
            {showExplanation ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
          </button>

          {showExplanation && (
            <div className="p-5 bg-slate-950 border-t border-slate-800">
              <pre className="font-mono text-xs text-slate-300 leading-relaxed whitespace-pre-wrap bg-slate-900/60 p-4 rounded-xl border border-slate-800 text-left" dir="ltr">
                {result.math_explanation}
              </pre>
            </div>
          )}
        </div>
      )}
    </main>
  );
}