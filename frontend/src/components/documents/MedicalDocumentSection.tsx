"use client";

import React, { useState, useEffect, useCallback } from "react";
import { MedicalDocument, DocumentCategory, DocumentCreatePayload } from "@/types";
import { apiClient } from "@/lib/api";
import { DocumentUploadModal } from "./DocumentUploadModal";
import { DocumentViewerModal } from "./DocumentViewerModal";
import {
  FileText,
  Image as ImageIcon,
  UploadCloud,
  Plus,
  Search,
  Eye,
  Download,
  Trash2,
  Calendar,
  Stethoscope,
  Filter,
  AlertCircle,
  FileCheck,
} from "lucide-react";

interface MedicalDocumentSectionProps {
  patientId: string;
  isReadOnly?: boolean;
}

export const MedicalDocumentSection: React.FC<MedicalDocumentSectionProps> = ({
  patientId,
  isReadOnly = false,
}) => {
  const [documents, setDocuments] = useState<MedicalDocument[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState("");

  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [activeViewingDoc, setActiveViewingDoc] = useState<MedicalDocument | null>(null);
  const [isSectionDragging, setIsSectionDragging] = useState(false);

  const loadDocuments = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await apiClient.get<MedicalDocument[]>(
        `/patients/${patientId}/documents`
      );
      setDocuments(res.data);
    } catch (e) {
      console.error("Failed to load medical documents:", e);
    } finally {
      setIsLoading(false);
    }
  }, [patientId]);

  useEffect(() => {
    if (patientId) {
      loadDocuments();
    }
  }, [patientId, loadDocuments]);

  const handleUploadDocument = async (payload: DocumentCreatePayload) => {
    await apiClient.post(`/patients/${patientId}/documents`, payload);
    await loadDocuments();
  };

  const handleDeleteDocument = async (docId: string, title: string) => {
    if (!confirm(`Are you sure you want to delete "${title}"?`)) return;
    try {
      await apiClient.delete(`/patients/${patientId}/documents/${docId}`);
      setDocuments((prev) => prev.filter((d) => d.id !== docId));
    } catch (e) {
      console.error("Failed to delete document:", e);
      alert("Failed to delete document.");
    }
  };

  // Section-wide drag and drop trigger
  const handleSectionDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isReadOnly) {
      setIsSectionDragging(true);
    }
  };

  const handleSectionDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsSectionDragging(false);
  };

  const handleSectionDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsSectionDragging(false);

    if (!isReadOnly && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setIsUploadModalOpen(true);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const getCategoryBadge = (category: string) => {
    switch (category) {
      case "PRESCRIPTION":
        return {
          label: "Doctor Prescription",
          style: "bg-indigo-950/70 text-indigo-300 border-indigo-700/60",
        };
      case "MEDICAL_CONDITION":
        return {
          label: "Medical Condition",
          style: "bg-rose-950/70 text-rose-300 border-rose-700/60",
        };
      case "LAB_REPORT":
        return {
          label: "Lab / Test Report",
          style: "bg-emerald-950/70 text-emerald-300 border-emerald-700/60",
        };
      case "CLINICAL_NOTE":
        return {
          label: "Clinical Note",
          style: "bg-amber-950/70 text-amber-300 border-amber-700/60",
        };
      default:
        return {
          label: category.replace(/_/g, " "),
          style: "bg-sky-950/70 text-sky-300 border-sky-700/60",
        };
    }
  };

  // Filtered documents
  const filteredDocuments = documents.filter((doc) => {
    const matchesCategory =
      selectedCategory === "ALL" || doc.document_type === selectedCategory;
    const matchesSearch =
      doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (doc.doctor_name && doc.doctor_name.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (doc.notes && doc.notes.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  return (
    <div
      onDragOver={handleSectionDragOver}
      onDragLeave={handleSectionDragLeave}
      onDrop={handleSectionDrop}
      className={`bg-slate-900 border rounded-2xl p-6 shadow-md transition-all ${
        isSectionDragging
          ? "border-sky-400 ring-2 ring-sky-500/30 bg-slate-900/90"
          : "border-slate-800"
      }`}
    >
      {/* Section Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-sky-400" />
            <span>Medical Documents & Prescriptions</span>
          </h3>
          <p className="text-xs text-slate-400">
            Doctor prescriptions, clinical records, condition details, and lab reports
          </p>
        </div>

        {!isReadOnly && (
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsUploadModalOpen(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-xs font-bold shadow-md shadow-sky-500/20 transition cursor-pointer"
            >
              <UploadCloud className="w-4 h-4" />
              <span>Upload Document</span>
            </button>
          </div>
        )}
      </div>

      {/* Filter Tabs & Search Bar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 mb-6">
        {/* Category Filter Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 text-xs">
          {[
            { id: "ALL", label: "All Records" },
            { id: "PRESCRIPTION", label: "Prescriptions" },
            { id: "MEDICAL_CONDITION", label: "Condition Details" },
            { id: "LAB_REPORT", label: "Lab Reports" },
            { id: "CLINICAL_NOTE", label: "Clinical Notes" },
          ].map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-3 py-1.5 rounded-lg font-semibold transition shrink-0 ${
                selectedCategory === cat.id
                  ? "bg-sky-500/20 text-sky-300 border border-sky-400/50 font-bold"
                  : "bg-slate-800 text-slate-400 hover:text-white border border-slate-700/60"
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Search Input */}
        <div className="relative min-w-[220px]">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search documents or doctors..."
            className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-9 pr-3 py-1.5 text-xs text-white focus:outline-none focus:border-sky-400"
          />
        </div>
      </div>

      {/* Drag & Drop Hint Banner */}
      {!isReadOnly && (
        <div
          onClick={() => setIsUploadModalOpen(true)}
          className="mb-5 p-3 rounded-xl border border-dashed border-slate-700/80 bg-slate-800/30 hover:bg-slate-800/60 text-center cursor-pointer transition flex items-center justify-center gap-2 text-xs text-slate-400 hover:text-sky-300"
        >
          <UploadCloud className="w-4 h-4 text-sky-400 shrink-0" />
          <span>
            Tip: Drag and drop any prescription or medical image file here to upload instantly
          </span>
        </div>
      )}

      {/* Document Grid */}
      {isLoading ? (
        <div className="py-12 text-center text-slate-400 text-xs">
          Loading medical documents...
        </div>
      ) : filteredDocuments.length === 0 ? (
        <div className="py-12 text-center rounded-2xl bg-slate-800/30 border border-slate-800 p-8">
          <FileText className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <p className="text-white font-bold text-sm mb-1">No medical documents found</p>
          <p className="text-xs text-slate-400 max-w-sm mx-auto mb-4">
            Upload doctor prescriptions, medical condition diagnoses, or lab test reports.
          </p>
          {!isReadOnly && (
            <button
              onClick={() => setIsUploadModalOpen(true)}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold transition"
            >
              <Plus className="w-4 h-4" />
              <span>Add First Document</span>
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredDocuments.map((doc) => {
            const badge = getCategoryBadge(doc.document_type);
            const isPdf =
              doc.file_type === "application/pdf" ||
              doc.file_name.toLowerCase().endsWith(".pdf");

            return (
              <div
                key={doc.id}
                className="bg-slate-800/70 hover:bg-slate-800 border border-slate-700/80 hover:border-slate-600 rounded-2xl p-4 transition-all flex flex-col justify-between group shadow-sm"
              >
                <div>
                  {/* Top Header: Badge & Date */}
                  <div className="flex items-center justify-between gap-2 mb-2.5">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-md border ${badge.style}`}
                    >
                      {badge.label}
                    </span>
                    <span className="text-[11px] text-slate-400 flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {doc.document_date || new Date(doc.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  {/* Thumbnail / Visual Box */}
                  <div
                    onClick={() => setActiveViewingDoc(doc)}
                    className="h-28 rounded-xl bg-slate-900 border border-slate-700/70 mb-3 overflow-hidden flex items-center justify-center cursor-pointer relative group-hover:border-sky-500/50 transition"
                  >
                    {isPdf ? (
                      <div className="text-center p-3">
                        <FileText className="w-10 h-10 text-rose-400 mx-auto mb-1 group-hover:scale-110 transition" />
                        <span className="text-[10px] font-bold text-slate-300 block truncate max-w-[200px]">
                          PDF Document
                        </span>
                        <span className="text-[9px] text-slate-500">
                          {formatFileSize(doc.file_size_bytes)}
                        </span>
                      </div>
                    ) : doc.file_data_url ? (
                      /* eslint-disable-next-line @next/next/no-img-element */
                      <img
                        src={doc.file_data_url}
                        alt={doc.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition"
                      />
                    ) : (
                      <ImageIcon className="w-10 h-10 text-emerald-400" />
                    )}

                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1.5 text-white text-xs font-bold">
                      <Eye className="w-4 h-4" />
                      <span>Click to View</span>
                    </div>
                  </div>

                  {/* Title & Doctor */}
                  <h4
                    onClick={() => setActiveViewingDoc(doc)}
                    className="text-sm font-bold text-white mb-1 hover:text-sky-300 cursor-pointer line-clamp-1"
                    title={doc.title}
                  >
                    {doc.title}
                  </h4>

                  {doc.doctor_name && (
                    <p className="text-xs text-sky-400 flex items-center gap-1 mb-2 font-medium truncate">
                      <Stethoscope className="w-3.5 h-3.5 shrink-0" />
                      <span>{doc.doctor_name}</span>
                    </p>
                  )}

                  {doc.notes && (
                    <p className="text-xs text-slate-400 line-clamp-2 mb-3 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
                      {doc.notes}
                    </p>
                  )}
                </div>

                {/* Card Actions */}
                <div className="flex items-center justify-between pt-3 border-t border-slate-700/60 mt-2">
                  <span className="text-[11px] text-slate-400 font-medium">
                    {formatFileSize(doc.file_size_bytes)}
                  </span>

                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => setActiveViewingDoc(doc)}
                      className="p-1.5 rounded-lg text-slate-300 hover:text-sky-300 hover:bg-slate-700 transition"
                      title="View Document"
                    >
                      <Eye className="w-4 h-4" />
                    </button>

                    {doc.file_data_url && (
                      <a
                        href={doc.file_data_url}
                        download={doc.file_name}
                        className="p-1.5 rounded-lg text-slate-300 hover:text-emerald-300 hover:bg-slate-700 transition"
                        title="Download Document"
                      >
                        <Download className="w-4 h-4" />
                      </a>
                    )}

                    {!isReadOnly && (
                      <button
                        onClick={() => handleDeleteDocument(doc.id, doc.title)}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-700 transition"
                        title="Delete Document"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Upload Modal */}
      <DocumentUploadModal
        patientId={patientId}
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onSuccess={() => loadDocuments()}
        onUpload={handleUploadDocument}
      />

      {/* Viewer Modal */}
      <DocumentViewerModal
        document={activeViewingDoc}
        isOpen={!!activeViewingDoc}
        onClose={() => setActiveViewingDoc(null)}
      />
    </div>
  );
};
