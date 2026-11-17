"use client";

import React from "react";
import { MedicalDocument } from "@/types";
import {
  X,
  Download,
  ExternalLink,
  FileText,
  Image as ImageIcon,
  Calendar,
  Stethoscope,
  Info,
} from "lucide-react";

interface DocumentViewerModalProps {
  document: MedicalDocument | null;
  isOpen: boolean;
  onClose: () => void;
}

export const DocumentViewerModal: React.FC<DocumentViewerModalProps> = ({
  document: doc,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !doc) return null;

  const isPdf =
    doc.file_type === "application/pdf" || doc.file_name.toLowerCase().endsWith(".pdf");

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case "PRESCRIPTION":
        return "bg-indigo-500/20 text-indigo-300 border-indigo-500/40";
      case "MEDICAL_CONDITION":
        return "bg-rose-500/20 text-rose-300 border-rose-500/40";
      case "LAB_REPORT":
        return "bg-emerald-500/20 text-emerald-300 border-emerald-500/40";
      case "CLINICAL_NOTE":
        return "bg-amber-500/20 text-amber-300 border-amber-500/40";
      case "EMERGENCY_PLAN":
        return "bg-red-500/20 text-red-300 border-red-500/40";
      default:
        return "bg-sky-500/20 text-sky-300 border-sky-500/40";
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-3xl max-w-4xl w-full p-6 shadow-2xl relative my-auto flex flex-col max-h-[92vh]">
        {/* Header */}
        <div className="flex items-start justify-between gap-4 pb-4 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1.5 flex-wrap">
              <span
                className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${getCategoryColor(
                  doc.document_type
                )}`}
              >
                {doc.document_type.replace(/_/g, " ")}
              </span>
              {doc.document_date && (
                <span className="flex items-center gap-1 text-xs text-slate-400">
                  <Calendar className="w-3.5 h-3.5" />
                  {doc.document_date}
                </span>
              )}
              {doc.doctor_name && (
                <span className="flex items-center gap-1 text-xs text-slate-300 font-medium">
                  <Stethoscope className="w-3.5 h-3.5 text-sky-400" />
                  {doc.doctor_name}
                </span>
              )}
            </div>
            <h2 className="text-xl font-bold text-white">{doc.title}</h2>
            <p className="text-xs text-slate-400">
              {doc.file_name} • {formatFileSize(doc.file_size_bytes)}
            </p>
          </div>

          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-2 rounded-xl hover:bg-slate-800 transition shrink-0"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Clinical Notes Banner */}
        {doc.notes && (
          <div className="my-3 p-3 rounded-xl bg-slate-800/80 border border-slate-700/80 flex items-start gap-2.5 text-xs text-slate-300">
            <Info className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-sky-300 block mb-0.5">
                Clinical Details & Instructions:
              </span>
              <span>{doc.notes}</span>
            </div>
          </div>
        )}

        {/* Document Content Viewport */}
        <div className="flex-1 overflow-y-auto my-3 bg-slate-950 rounded-2xl border border-slate-800 p-2 flex items-center justify-center min-h-[350px]">
          {isPdf ? (
            doc.file_data_url ? (
              <iframe
                src={doc.file_data_url}
                title={doc.title}
                className="w-full h-[540px] rounded-xl border-none"
              />
            ) : (
              <div className="text-center p-8">
                <FileText className="w-16 h-16 text-rose-400 mx-auto mb-3" />
                <p className="text-white font-bold mb-2">PDF Document Ready</p>
                <p className="text-xs text-slate-400 mb-4">{doc.file_name}</p>
                <a
                  href={`/api/v1/patients/${doc.patient_id}/documents/${doc.id}/file`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>Open PDF in Tab</span>
                </a>
              </div>
            )
          ) : doc.file_data_url ? (
            /* eslint-disable-next-line @next/next/no-img-element */
            <img
              src={doc.file_data_url}
              alt={doc.title}
              className="max-h-[540px] w-auto max-w-full object-contain rounded-xl shadow-lg"
            />
          ) : (
            <div className="text-center p-8">
              <ImageIcon className="w-16 h-16 text-emerald-400 mx-auto mb-3" />
              <p className="text-white font-bold mb-2">Medical Image</p>
              <p className="text-xs text-slate-400">{doc.file_name}</p>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-3 border-t border-slate-800">
          <div className="text-xs text-slate-400 hidden sm:block">
            Uploaded on {new Date(doc.created_at).toLocaleDateString()}
          </div>

          <div className="flex items-center gap-3 ml-auto">
            {doc.file_data_url && (
              <a
                href={doc.file_data_url}
                download={doc.file_name}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition"
              >
                <Download className="w-4 h-4 text-sky-400" />
                <span>Download File</span>
              </a>
            )}

            <button
              onClick={onClose}
              className="px-5 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold transition"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
