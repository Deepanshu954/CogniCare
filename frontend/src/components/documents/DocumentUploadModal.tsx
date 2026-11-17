"use client";

import React, { useState, useRef } from "react";
import { DocumentCategory, DocumentCreatePayload } from "@/types";
import {
  UploadCloud,
  FileText,
  Image as ImageIcon,
  X,
  AlertCircle,
  CheckCircle2,
  Calendar,
  UserCheck,
  Stethoscope,
} from "lucide-react";

interface DocumentUploadModalProps {
  patientId: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  onUpload: (payload: DocumentCreatePayload) => Promise<void>;
}

export const DocumentUploadModal: React.FC<DocumentUploadModalProps> = ({
  patientId,
  isOpen,
  onClose,
  onSuccess,
  onUpload,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePreviewUrl, setFilePreviewUrl] = useState<string | null>(null);

  const [title, setTitle] = useState("");
  const [documentType, setDocumentType] = useState<DocumentCategory>("PRESCRIPTION");
  const [doctorName, setDoctorName] = useState("");
  const [documentDate, setDocumentDate] = useState(
    new Date().toISOString().split("T")[0]
  );
  const [notes, setNotes] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleFileProcess = (file: File) => {
    setErrorMessage(null);

    // Validate mime type
    const validTypes = [
      "application/pdf",
      "image/png",
      "image/jpeg",
      "image/jpg",
      "image/webp",
    ];
    if (!validTypes.includes(file.type) && !file.type.startsWith("image/")) {
      setErrorMessage("Unsupported file type. Please upload a PDF or an Image (PNG, JPG, WEBP).");
      return;
    }

    // Validate size (15 MB max)
    if (file.size > 15 * 1024 * 1024) {
      setErrorMessage("File exceeds 15 MB limit. Please select a smaller file.");
      return;
    }

    setSelectedFile(file);

    // Auto-fill title if empty
    if (!title.trim()) {
      const cleanName = file.name.replace(/\.[^/.]+$/, "").replace(/[_-]/g, " ");
      setTitle(cleanName.charAt(0).toUpperCase() + cleanName.slice(1));
    }

    // Create Base64 data URL
    const reader = new FileReader();
    reader.onload = (e) => {
      setFilePreviewUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);
  };

  // Drag and Drop Handlers
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      handleFileProcess(file);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileProcess(e.target.files[0]);
    }
  };

  const removeSelectedFile = () => {
    setSelectedFile(null);
    setFilePreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile || !filePreviewUrl) {
      setErrorMessage("Please select or drop a file to upload.");
      return;
    }
    if (!title.trim()) {
      setErrorMessage("Please enter a document title.");
      return;
    }

    setIsUploading(true);
    setErrorMessage(null);

    try {
      await onUpload({
        title: title.trim(),
        document_type: documentType,
        doctor_name: doctorName.trim() || undefined,
        document_date: documentDate.trim() || undefined,
        notes: notes.trim() || undefined,
        file_name: selectedFile.name,
        file_type: selectedFile.type,
        file_size_bytes: selectedFile.size,
        file_data_url: filePreviewUrl,
      });
      onSuccess();
      onClose();
    } catch (err: any) {
      console.error("Upload error:", err);
      setErrorMessage(
        err?.response?.data?.detail || "Failed to upload document. Please try again."
      );
    } finally {
      setIsUploading(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl relative my-8">
        {/* Close Button */}
        <button
          onClick={onClose}
          disabled={isUploading}
          className="absolute top-5 right-5 text-slate-400 hover:text-white p-2 rounded-xl hover:bg-slate-800 transition"
          aria-label="Close"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-md">
              <UploadCloud className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Upload Medical Document</h2>
              <p className="text-xs text-slate-400">
                Upload prescriptions, condition details, or lab reports (PDF or Images)
              </p>
            </div>
          </div>
        </div>

        {errorMessage && (
          <div className="mb-4 p-3 rounded-xl bg-rose-950/80 border border-rose-700/80 flex items-center gap-2 text-rose-300 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Drag & Drop Zone */}
          {!selectedFile ? (
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all ${
                isDragging
                  ? "border-sky-400 bg-sky-950/40 scale-[1.01]"
                  : "border-slate-700 hover:border-slate-500 bg-slate-800/40 hover:bg-slate-800/70"
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf,image/png,image/jpeg,image/jpg,image/webp"
                onChange={handleFileInputChange}
                className="hidden"
              />
              <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center text-sky-400 mx-auto mb-3 shadow">
                <UploadCloud className="w-6 h-6 animate-pulse" />
              </div>
              <p className="text-sm font-bold text-white mb-1">
                Drag and drop your file here, or{" "}
                <span className="text-sky-400 underline">browse files</span>
              </p>
              <p className="text-xs text-slate-400">
                Supports PDF, PNG, JPG, or WEBP (Max 15 MB)
              </p>
              <div className="flex items-center justify-center gap-4 mt-3 text-[11px] text-slate-400">
                <span className="flex items-center gap-1">
                  <FileText className="w-3.5 h-3.5 text-rose-400" /> PDF Reports
                </span>
                <span className="flex items-center gap-1">
                  <ImageIcon className="w-3.5 h-3.5 text-emerald-400" /> Prescription Photos
                </span>
              </div>
            </div>
          ) : (
            /* Selected File Preview Box */
            <div className="p-4 rounded-2xl bg-slate-800/80 border border-slate-700 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3 overflow-hidden">
                {selectedFile.type.startsWith("image/") ? (
                  <div className="w-12 h-12 rounded-lg bg-slate-900 overflow-hidden shrink-0 border border-slate-700">
                    {filePreviewUrl ? (
                      /* eslint-disable-next-line @next/next/no-img-element */
                      <img
                        src={filePreviewUrl}
                        alt="Preview"
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <ImageIcon className="w-6 h-6 text-emerald-400 m-auto mt-3" />
                    )}
                  </div>
                ) : (
                  <div className="w-12 h-12 rounded-lg bg-rose-950/70 border border-rose-700/60 flex items-center justify-center shrink-0 text-rose-400">
                    <FileText className="w-6 h-6" />
                  </div>
                )}
                <div className="overflow-hidden">
                  <p className="text-sm font-bold text-white truncate">
                    {selectedFile.name}
                  </p>
                  <p className="text-xs text-slate-400">
                    {formatFileSize(selectedFile.size)} • {selectedFile.type || "Document"}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={removeSelectedFile}
                className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-700 transition shrink-0"
                title="Change File"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Document Category Selection */}
          <div>
            <label className="block text-xs font-bold text-slate-300 mb-1.5">
              Document Category <span className="text-rose-400">*</span>
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {[
                { type: "PRESCRIPTION", label: "Doctor Prescription" },
                { type: "MEDICAL_CONDITION", label: "Condition Details" },
                { type: "LAB_REPORT", label: "Lab / Test Report" },
                { type: "CLINICAL_NOTE", label: "Clinical Notes" },
                { type: "EMERGENCY_PLAN", label: "Emergency Plan" },
                { type: "OTHER", label: "Other Record" },
              ].map((item) => (
                <button
                  key={item.type}
                  type="button"
                  onClick={() => setDocumentType(item.type as DocumentCategory)}
                  className={`text-xs font-semibold py-2 px-3 rounded-xl border transition text-left ${
                    documentType === item.type
                      ? "bg-sky-500/20 border-sky-400 text-sky-200 font-bold"
                      : "bg-slate-800/60 border-slate-700 text-slate-400 hover:text-white"
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {/* Title Input */}
          <div>
            <label className="block text-xs font-bold text-slate-300 mb-1">
              Document Title <span className="text-rose-400">*</span>
            </label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Neurologist Prescription - Donepezil 10mg"
              className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white text-sm focus:outline-none focus:border-sky-400"
            />
          </div>

          {/* Doctor Name & Date Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1 flex items-center gap-1">
                <Stethoscope className="w-3.5 h-3.5 text-sky-400" />
                <span>Doctor / Specialist (Optional)</span>
              </label>
              <input
                type="text"
                value={doctorName}
                onChange={(e) => setDoctorName(e.target.value)}
                placeholder="e.g. Dr. Elena Vance"
                className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white text-sm focus:outline-none focus:border-sky-400"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-sky-400" />
                <span>Document Date</span>
              </label>
              <input
                type="date"
                value={documentDate}
                onChange={(e) => setDocumentDate(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white text-sm focus:outline-none focus:border-sky-400"
              />
            </div>
          </div>

          {/* Clinical Notes / Dosage textarea */}
          <div>
            <label className="block text-xs font-bold text-slate-300 mb-1">
              Clinical Notes / Dosage Instructions (Optional)
            </label>
            <textarea
              rows={2}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="e.g. Take 10mg with evening meal. Avoid skipping morning hydration."
              className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white text-sm focus:outline-none focus:border-sky-400"
            />
          </div>

          {/* Submit Actions */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              disabled={isUploading}
              className="px-5 py-2.5 rounded-xl text-sm font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isUploading || !selectedFile}
              className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-sky-500/20 disabled:opacity-50 transition cursor-pointer"
            >
              {isUploading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Uploading Document...</span>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Save & Attach Document</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
