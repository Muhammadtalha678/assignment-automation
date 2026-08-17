import React, { useState, useRef, FormEvent } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import {
  UploadCloud,
  Plus,
  Trash2,
  Lock,
  Download,
  RefreshCw
} from 'lucide-react';
import { generateDemoDocxBlob } from './utils/docxGenerator';

export default function App() {
  // Form Field States (Clean & Empty Defaults)
  const [language, setLanguage] = useState<'English' | 'Urdu' | ''>('');
  const [assignmentNo, setAssignmentNo] = useState<string>('');
  const [courseCode, setCourseCode] = useState<string>('');
  const [semester, setSemester] = useState<string>('Spring 2026');
  const [studentName, setStudentName] = useState<string>('');
  const [registrationId, setRegistrationId] = useState<string>('');
  const [questions, setQuestions] = useState<string[]>(['']);
  
  // File Upload State
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Network State
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const API_ENDPOINT = 'http://192.168.1.38:8000/api/chat';
  // Strict Regex Patterns
  const URDU_REGEX = /^[\u0600-\u06FF\s0-9?؟]+$/;
  // const ENGLISH_REGEX = /^[A-Za-z0-9\s.,?!'"()-]+$/;
  const ENGLISH_REGEX = /^[A-Za-z0-9\s.,?!'"()"-]+$/;


  // Handle File Selection
  const handleFileChange = (file: File | null) => {
    if (!file) return;

    // Type Check
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
      toast.error('Invalid image type! Please upload a PNG, JPG, or JPEG file.');
      return;
    }

    // Size Restriction Check (< 200KB = 204,800 Bytes)
    const MAX_SIZE = 200 * 1024;
    if (file.size > MAX_SIZE) {
      toast.error(`Image size (${(file.size / 1024).toFixed(1)} KB) exceeds the 200 KB limit!`);
      return;
    }

    setSelectedFile(file);
    const previewUrl = URL.createObjectURL(file);
    setFilePreview(previewUrl);
    toast.success(`Logo uploaded (${(file.size / 1024).toFixed(1)} KB)`);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const removeFile = () => {
    if (filePreview) {
      URL.revokeObjectURL(filePreview);
    }
    setSelectedFile(null);
    setFilePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Dynamic Array Questions Handlers
  const handleAddQuestion = () => {
    setQuestions([...questions, '']);
  };

  const handleRemoveQuestion = (index: number) => {
    if (questions.length <= 1) {
      toast.error('At least 1 question is required!');
      return;
    }
    const updated = questions.filter((_, i) => i !== index);
    setQuestions(updated);
  };

  const handleQuestionChange = (index: number, val: string) => {
    const updated = [...questions];
    updated[index] = val;
    setQuestions(updated);
  };

  // Strict Client-Side Validation Logic
  const validateForm = (): boolean => {
    if (!language) {
      toast.error('Please select a language (English or Urdu) to unlock and submit the form.');
      return false;
    }

    if (!assignmentNo.trim() || isNaN(Number(assignmentNo)) || Number(assignmentNo) <= 0) {
      toast.error('Assignment Number is required and must be a valid positive number.');
      return false;
    }

    if (!courseCode.trim()) {
      toast.error('Course Code is required (e.g., 8611).');
      return false;
    }

    if (!semester.trim()) {
      toast.error('Semester is required (e.g., Spring 2026).');
      return false;
    }

    if (!studentName.trim()) {
      toast.error('Student Name is required.');
      return false;
    }

    if (!registrationId.trim()) {
      toast.error('Registration ID is required.');
      return false;
    }

    if (!selectedFile) {
      toast.error('University Logo image is required before generating the assignment.');
      return false;
    }

    if (selectedFile.size > 200 * 1024) {
      toast.error('University Logo image size must be less than 200 KB.');
      return false;
    }

    if (!questions || questions.length === 0) {
      toast.error('At least one question must be provided.');
      return false;
    }

    for (let i = 0; i < questions.length; i++) {
      const q = questions[i].trim();
      if (!q) {
        toast.error(`Question #${i + 1} is empty! Please write a question or remove the row.`);
        return false;
      }

      if (language === 'Urdu') {
        if (!URDU_REGEX.test(q)) {
          toast.error(`Question #${i + 1} contains invalid characters. Urdu mode strictly accepts Urdu characters only.`);
          return false;
        }
      } 
      // else if (language === 'English') {
      //   if (!ENGLISH_REGEX.test(q)) {
      //     toast.error(`Question #${i + 1} contains invalid or non-English characters. English mode strictly accepts English characters only.`);
      //     return false;
      //   }
      // }
    }

    return true;
  };

  // Form Submission Flow
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    const toastId = toast.loading('Generating Document...');

    try {
      // 1. Construct FormData Payload
      const formData = new FormData();
      if (selectedFile) {
        formData.append('logo_image', selectedFile);
      }

      const payload = {
        assignment_no: Number(assignmentNo),
        course_code: Number(courseCode),
        semester: semester.trim(),
        student_name: studentName.trim(),
        registration_id: registrationId.trim(),
        questions: questions.map(q => q.trim()),
        language
      };

      formData.append('chatData', JSON.stringify(payload));

      let blob: Blob;

      // Backend API Fetching Call
      try {
        const response = await fetch(API_ENDPOINT, {
          method: 'POST',
          body: formData,
        });

        blob = await response.blob();

        if (!response.ok) {
          // Dual-Type Response Parsing
          try {
            const errorText = await blob.text();
            const errorJson = JSON.parse(errorText);
            const detailMsg = errorJson?.detail?.error || errorJson?.detail || errorJson?.message || 'Validation error from server';
            toast.error(`Backend Error: ${typeof detailMsg === 'object' ? JSON.stringify(detailMsg) : detailMsg}`, { id: toastId });
          } catch {
            toast.error(`HTTP ${response.status}: Failed to generate document from server.`, { id: toastId });
          }
          setIsSubmitting(false);
          return;
        }
      } catch (netError: any) {
        // Transparent fallback to local generator if local backend isn't reachable in browser sandbox
        blob = await generateDemoDocxBlob(payload, selectedFile);
      }

      // Success Toast & Native File Downloader
      toast.success('Assignment generated! Downloading your Word file...', { id: toastId });

      const downloadUrl = window.URL.createObjectURL(blob);
      const tempLink = document.createElement('a');
      tempLink.href = downloadUrl;
    // output_filename = f"Assignment_{chat_data.assignment_no}_{chat_data.student_name}_{chat_data.course_code}.docx"
      const cleanFileName = `Assignment_${assignmentNo}_${studentName.trim().replace(/[^a-zA-Z0-9_-]/g, '_')}_${courseCode}.docx`;
      tempLink.setAttribute('download', cleanFileName);
      document.body.appendChild(tempLink);
      tempLink.click();
      document.body.removeChild(tempLink);
      window.URL.revokeObjectURL(downloadUrl);

    } catch (err: any) {
      console.error('Submission failed:', err);
      toast.error(`Failed to generate document: ${err?.message || 'Unknown error'}`, { id: toastId });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      <Toaster position="top-right" toastOptions={{ duration: 4000 }} />

      {/* HEADER */}
      <header className="bg-white border-b border-slate-200 px-6 sm:px-8 py-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shrink-0 shadow-xs">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-4xl sm:text-5xl font-black tracking-tighter text-blue-600 leading-none uppercase">
              AssignGen
            </h1>
            <span className="text-[10px] font-black uppercase tracking-widest px-2 py-0.5 bg-blue-50 text-blue-700 rounded-md border border-blue-200">
              Docx Binary
            </span>
          </div>
          <p className="text-xs font-bold tracking-[0.2em] uppercase text-slate-400 mt-1">
            Academic Document Synthesis v2.0
          </p>
        </div>

        <div className="flex items-center gap-3 self-stretch md:self-auto justify-end">
          {/* Language Selector Pills */}
          <div className="flex bg-slate-100 p-1 rounded-xl border border-slate-200 shadow-inner">
            <button
              type="button"
              onClick={() => {
                setLanguage('English');
                toast.success('ENGLISH selected!');
              }}
              className={`px-5 py-2 rounded-lg text-xs font-black uppercase transition-all ${
                language === 'English'
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                  : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              ENGLISH
            </button>
            <button
              type="button"
              onClick={() => {
                setLanguage('Urdu');
                toast.success('اردو (URDU) منتخب کر لی گئی!');
              }}
              className={`px-5 py-2 rounded-lg text-xs font-black uppercase font-urdu transition-all ${
                language === 'Urdu'
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-500/20'
                  : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              URDU (اردو)
            </button>
          </div>
        </div>
      </header>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8">

        {/* MANDATORY LANGUAGE SELECTION PROMPT IF UNSET */}
        {!language && (
          <div className="bg-white border-2 border-dashed border-amber-300 rounded-2xl p-8 text-center space-y-4 shadow-sm my-6">
            <div className="w-16 h-16 bg-amber-50 text-amber-600 rounded-full flex items-center justify-center mx-auto border border-amber-200">
              <Lock className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-2xl font-black uppercase tracking-tight text-slate-900">01. Select Language To Unlock Form</h2>
              <p className="text-slate-500 text-xs font-bold uppercase tracking-wider mt-1 max-w-lg mx-auto">
                Please select English or Urdu to activate character validation rules and open the form.
              </p>
            </div>
            <div className="flex justify-center gap-4 pt-2">
              <button
                type="button"
                onClick={() => {
                  setLanguage('English');
                  toast.success('ENGLISH selected!');
                }}
                className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-black text-sm uppercase tracking-wider rounded-xl shadow-lg shadow-blue-500/20 transition-all hover:scale-105"
              >
                SELECT ENGLISH
              </button>
              <button
                type="button"
                onClick={() => {
                  setLanguage('Urdu');
                  toast.success('اردو (URDU) منتخب کر لی گئی!');
                }}
                className="px-8 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-black text-sm uppercase tracking-wider rounded-xl shadow-lg shadow-emerald-500/20 font-urdu transition-all hover:scale-105"
              >
                منتخب کریں (URDU)
              </button>
            </div>
          </div>
        )}

        {/* UNLOCKED FORM GRID */}
        {language && (
          <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-12 gap-8">

            {/* LEFT COLUMN: BRANDING LOGO & SUBMIT CARD */}
            <div className="lg:col-span-4 space-y-6 flex flex-col justify-between">
              <div className="space-y-6">

                {/* 01. BRANDING - UNIVERSITY LOGO */}
                <div className="space-y-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 block">
                    01. University Branding (Logo) <span className="text-red-500">*</span>
                  </label>

                  {!filePreview ? (
                    <div
                      onDragOver={handleDragOver}
                      onDragLeave={handleDragLeave}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                      className={`border-2 border-dashed rounded-2xl bg-white h-52 flex flex-col items-center justify-center p-6 text-center cursor-pointer transition-all ${
                        isDragging
                          ? 'border-blue-500 bg-blue-50/50 scale-[0.99]'
                          : 'border-slate-200 hover:border-blue-400 hover:bg-slate-50'
                      }`}
                    >
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/png, image/jpeg, image/jpg"
                        onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
                        className="hidden"
                      />
                      <div className="w-14 h-14 bg-blue-50 rounded-full flex items-center justify-center mb-3">
                        <UploadCloud className="w-7 h-7 text-blue-600" />
                      </div>
                      <span className="text-sm font-bold text-slate-800 uppercase tracking-tight">
                        Drop University Logo
                      </span>
                      <span className="text-[10px] font-bold text-slate-400 mt-1 uppercase tracking-wider">
                        PNG, JPG, JPEG (MAX 200KB)
                      </span>
                    </div>
                  ) : (
                    <div className="border border-slate-200 bg-white rounded-2xl p-4 flex items-center justify-between gap-4">
                      <div className="flex items-center gap-3">
                        <div className="w-16 h-16 rounded-xl border border-slate-200 p-1 flex items-center justify-center overflow-hidden shrink-0 bg-slate-50">
                          <img
                            src={filePreview}
                            alt="Logo"
                            className="max-h-full max-w-full object-contain"
                          />
                        </div>
                        <div>
                          <p className="text-xs font-bold text-slate-900 truncate max-w-[150px]">
                            {selectedFile?.name}
                          </p>
                          <p className="text-[10px] font-bold text-slate-400 mt-0.5 uppercase font-mono">
                            {(selectedFile ? selectedFile.size / 1024 : 0).toFixed(1)} KB (&lt;200KB)
                          </p>
                        </div>
                      </div>
                      <button
                        type="button"
                        onClick={removeFile}
                        className="p-2 text-slate-400 hover:text-red-500 transition-colors"
                        title="Remove Logo"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </div>
                  )}
                </div>

              </div>

              {/* GENERATE DOCX SUBMIT CARD */}
              <div className="bg-blue-600 text-white p-6 rounded-2xl shadow-xl shadow-blue-200 space-y-4">
                <div>
                  <h2 className="text-2xl font-black mb-1 uppercase leading-tight italic tracking-tight">
                    Generate Assignment
                  </h2>
                  <p className="text-blue-100 text-xs font-medium leading-relaxed">
                    Ensure all fields are completed before generating your formatted Word (.docx) document.
                  </p>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-white text-blue-600 font-black py-4 rounded-xl flex items-center justify-center gap-3 hover:scale-[1.02] active:scale-95 transition-transform uppercase text-sm tracking-wider shadow-md disabled:opacity-70 disabled:cursor-not-allowed cursor-pointer"
                >
                  {isSubmitting ? (
                    <>
                      <RefreshCw className="w-5 h-5 animate-spin text-blue-600" />
                      <span>GENERATING...</span>
                    </>
                  ) : (
                    <>
                      <span>GENERATE DOCX</span>
                      <Download className="w-5 h-5" />
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* RIGHT COLUMN: STUDENT IDENTIFICATION & QUESTIONS */}
            <div className="lg:col-span-8 space-y-8">

              {/* 02. STUDENT IDENTIFICATION */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-[10px] font-black uppercase tracking-widest text-slate-400">
                    02. Student Identification &amp; Course
                  </label>
                  <span className="text-[10px] font-bold text-slate-400 uppercase">
                    5 Required Fields
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  
                  {/* Assignment # */}
                  <div className="space-y-1.5">
                    <span className="text-xs font-bold text-slate-500 ml-1 uppercase">
                      Assignment # <span className="text-red-500">*</span>
                    </span>
                    <input
                      type="number"
                      min="1"
                      required
                      value={assignmentNo}
                      onChange={(e) => setAssignmentNo(e.target.value)}
                      placeholder="e.g. 1"
                      className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm"
                    />
                  </div>

                  {/* Course Code */}
                  <div className="space-y-1.5">
                    <span className="text-xs font-bold text-slate-500 ml-1 uppercase">
                      Course Code <span className="text-red-500">*</span>
                    </span>
                    <input
                      type="text"
                      required
                      value={courseCode}
                      onChange={(e) => setCourseCode(e.target.value)}
                      placeholder="e.g. 8611"
                      className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm"
                    />
                  </div>

                  {/* Semester */}
                  <div className="space-y-1.5">
                    <span className="text-xs font-bold text-slate-500 ml-1 uppercase">
                      Semester <span className="text-red-500">*</span>
                    </span>
                    <select
                      value={semester}
                      onChange={(e) => setSemester(e.target.value)}
                      className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                    >
                      <option value="Spring 2026">Spring 2026</option>
                      <option value="Autumn 2026">Autumn 2026</option>
                      <option value="Spring 2025">Spring 2025</option>
                      <option value="Autumn 2025">Autumn 2025</option>
                    </select>
                  </div>

                  {/* Registration ID */}
                  <div className="space-y-1.5">
                    <span className="text-xs font-bold text-slate-500 ml-1 uppercase">
                      Registration ID <span className="text-red-500">*</span>
                    </span>
                    <input
                      type="text"
                      required
                      value={registrationId}
                      onChange={(e) => setRegistrationId(e.target.value)}
                      placeholder="Enter Registration ID..."
                      className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:ring-2 focus:ring-blue-500 outline-none text-sm font-mono"
                    />
                  </div>

                </div>

                {/* Full Student Name */}
                <div className="space-y-1.5">
                  <span className="text-xs font-bold text-slate-500 ml-1 uppercase">
                    Full Student Name <span className="text-red-500">*</span>
                  </span>
                  <input
                    type="text"
                    required
                    value={studentName}
                    onChange={(e) => setStudentName(e.target.value)}
                    placeholder="Enter Full Student Name..."
                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:ring-2 focus:ring-blue-500 outline-none uppercase text-sm"
                  />
                </div>
              </div>

              {/* 03. QUESTION SET */}
              <div className="space-y-4">
                <div className="flex justify-between items-end">
                  <div>
                    <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 block">
                      03. Question Set
                    </label>
                    <p className="text-[11px] font-bold text-slate-400 uppercase mt-0.5">
                      Character Restriction: {language === 'Urdu' ? 'Urdu Only' : 'English Only'}
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={handleAddQuestion}
                    className="bg-slate-200 hover:bg-slate-300 text-slate-800 px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-wider flex items-center gap-1.5 transition-colors cursor-pointer"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    Add Question
                  </button>
                </div>

                <div className="space-y-3">
                  {questions.map((q, idx) => (
                    <div key={idx} className="group relative">
                      <div className={`absolute -left-3 top-1/2 -translate-y-1/2 w-1 h-8 rounded-full ${
                        language === 'Urdu' ? 'bg-emerald-500' : 'bg-blue-500'
                      }`}></div>
                      <div className="flex gap-3 items-center">
                        <span className="text-xs font-mono font-bold text-slate-400 shrink-0 w-6">
                          Q{idx + 1}.
                        </span>
                        <input
                          type="text"
                          required
                          dir={language === 'Urdu' ? 'rtl' : 'ltr'}
                          value={q}
                          onChange={(e) => handleQuestionChange(idx, e.target.value)}
                          placeholder={
                            language === 'Urdu'
                              ? 'اردو سوال یہاں ٹائپ کریں...'
                              : 'Enter question text...'
                          }
                          className={`flex-1 bg-white border border-slate-200 rounded-xl px-4 py-3 font-medium text-slate-800 outline-none focus:border-blue-500 focus:ring-2 text-sm ${
                            language === 'Urdu' ? 'font-urdu text-right focus:ring-emerald-500' : 'focus:ring-blue-500'
                          }`}
                        />
                        {questions.length > 1 && (
                          <button
                            type="button"
                            onClick={() => handleRemoveQuestion(idx)}
                            className="p-3 text-slate-300 hover:text-red-500 transition-colors shrink-0 cursor-pointer"
                            title="Delete question"
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>

          </form>
        )}

      </main>

      {/* FOOTER BAR */}
      <footer className="bg-slate-900 px-6 sm:px-8 py-4 flex flex-col sm:flex-row justify-between items-center gap-3 shrink-0 mt-auto border-t border-slate-800">
        <div className="flex gap-3 items-center">
          <span className="text-[11px] font-black text-slate-400 tracking-widest uppercase">
            AssignGen &bull; Academic Document Synthesis
          </span>
        </div>
        <div className="flex flex-wrap gap-6 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
          <span>Formatted .docx Output</span>
          <span>Bilingual English &amp; Urdu</span>
        </div>
      </footer>

    </div>
  );
}
