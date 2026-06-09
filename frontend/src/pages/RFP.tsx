import React from "react";
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { FileText, Upload, Plus, RefreshCw, Download, CheckCircle, AlertCircle } from "lucide-react";
import { rfpAPI } from "../lib/api";
import { PageHeader, StatCard, StatusBadge, EmptyState, Spinner } from "../components/shared";

export default function RFPPage() {
  const queryClient = useQueryClient();
  const [uploadOpen, setUploadOpen] = useState(false);
  const [selectedRFP, setSelectedRFP] = useState<string | null>(null);

  const { data: rfps, isLoading } = useQuery({
    queryKey: ["rfps"],
    queryFn: () => rfpAPI.list().then((r) => r.data.results ?? r.data),
  });

  const { data: detail } = useQuery({
    queryKey: ["rfp", selectedRFP],
    queryFn: () => rfpAPI.get(selectedRFP!).then((r) => r.data),
    enabled: !!selectedRFP,
  });

  const generateMutation = useMutation({
    mutationFn: (id: string) => rfpAPI.generate(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["rfps"] }),
  });

  const approveMutation = useMutation({
    mutationFn: (id: string) => rfpAPI.responses.approve(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["rfp", selectedRFP] }),
  });

  const totalSections = rfps?.reduce((a: number, r: any) => a + (r.section_count || 0), 0) ?? 0;
  const totalApproved = rfps?.reduce((a: number, r: any) => a + (r.approved_count || 0), 0) ?? 0;

  return (
    <div className="p-6 max-w-7xl">
      <PageHeader
        title="AI RFP Response Matrix"
        subtitle="Generate, review, and export enterprise RFP responses"
        action={
          <button onClick={() => setUploadOpen(true)} className="btn-primary">
            <Plus size={15} /> Upload RFP
          </button>
        }
      />

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <StatCard label="Total RFPs" value={rfps?.length ?? 0} icon={<FileText size={18} />} />
        <StatCard label="Total Sections" value={totalSections} icon={<FileText size={18} />} />
        <StatCard label="Approved Responses" value={totalApproved} icon={<CheckCircle size={18} />} />
        <StatCard
          label="Completion Rate"
          value={totalSections ? `${Math.round((totalApproved / totalSections) * 100)}%` : "—"}
          icon={<RefreshCw size={18} />}
        />
      </div>

      <div className="flex gap-6">
        {/* RFP List */}
        <div className="flex-1">
          <div className="card overflow-hidden">
            <div className="px-4 py-3 border-b border-gray-100">
              <h2 className="text-sm font-semibold text-gray-900">RFP Requests</h2>
            </div>
            {isLoading ? (
              <div className="flex justify-center py-12"><Spinner /></div>
            ) : !rfps?.length ? (
              <EmptyState
                icon={<FileText size={36} />}
                title="No RFPs yet"
                description="Upload your first RFP to start generating AI responses."
                action={<button onClick={() => setUploadOpen(true)} className="btn-primary">Upload RFP</button>}
              />
            ) : (
              <div className="divide-y divide-gray-50">
                {rfps.map((rfp: any) => (
                  <div
                    key={rfp.id}
                    onClick={() => setSelectedRFP(rfp.id)}
                    className={`px-4 py-3 cursor-pointer hover:bg-gray-50 transition-colors ${selectedRFP === rfp.id ? "bg-brand-50 border-l-2 border-brand-500" : ""}`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">{rfp.title}</p>
                        <p className="text-xs text-gray-400 mt-0.5">
                          {rfp.issuer || "Unknown issuer"} · {rfp.section_count} sections
                        </p>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        <StatusBadge status={rfp.status} />
                        {rfp.status === "review" && (
                          <button
                            onClick={(e) => { e.stopPropagation(); rfpAPI.export(rfp.id); }}
                            className="btn-secondary py-1 px-2 text-xs"
                          >
                            <Download size={12} /> Export
                          </button>
                        )}
                        {(rfp.status === "uploaded" || rfp.status === "review") && (
                          <button
                            onClick={(e) => { e.stopPropagation(); generateMutation.mutate(rfp.id); }}
                            disabled={generateMutation.isPending}
                            className="btn-secondary py-1 px-2 text-xs"
                          >
                            <RefreshCw size={12} className={generateMutation.isPending ? "animate-spin" : ""} />
                            Generate
                          </button>
                        )}
                      </div>
                    </div>
                    {rfp.section_count > 0 && (
                      <div className="mt-2">
                        <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-brand-500 rounded-full transition-all"
                            style={{ width: `${rfp.section_count ? (rfp.approved_count / rfp.section_count) * 100 : 0}%` }}
                          />
                        </div>
                        <p className="text-xs text-gray-400 mt-1">{rfp.approved_count}/{rfp.section_count} approved</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Response Review Panel */}
        {selectedRFP && detail && (
          <div className="w-96 shrink-0">
            <div className="card overflow-hidden">
              <div className="px-4 py-3 border-b border-gray-100">
                <h2 className="text-sm font-semibold text-gray-900 truncate">{detail.title}</h2>
                <p className="text-xs text-gray-400 mt-0.5">{detail.sections?.length ?? 0} sections</p>
              </div>
              <div className="overflow-y-auto max-h-[60vh] divide-y divide-gray-50">
                {detail.sections?.map((section: any) => (
                  <div key={section.id} className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs font-semibold text-gray-500 uppercase">{section.category || section.heading}</span>
                      {section.response && (
                        <span className={`badge text-xs ${section.response.approved ? "bg-green-100 text-green-700" : section.response.reviewed ? "bg-gray-100 text-gray-600" : "bg-yellow-100 text-yellow-700"}`}>
                          {section.response.approved ? "Approved" : section.response.reviewed ? "Reviewed" : "Pending"}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-gray-700 font-medium mb-2">{section.question}</p>
                    {section.response ? (
                      <>
                        <p className="text-xs text-gray-600 leading-relaxed mb-2 line-clamp-4">
                          {section.response.answer}
                        </p>
                        <div className="flex items-center gap-2">
                          <div className="flex-1 h-1 bg-gray-100 rounded-full">
                            <div
                              className="h-1 rounded-full bg-brand-500"
                              style={{ width: `${section.response.confidence_score * 100}%` }}
                            />
                          </div>
                          <span className="text-xs text-gray-400">{Math.round(section.response.confidence_score * 100)}%</span>
                          {!section.response.approved && (
                            <button
                              onClick={() => approveMutation.mutate(section.response.id)}
                              className="text-xs text-green-600 hover:text-green-700 font-medium"
                            >
                              Approve
                            </button>
                          )}
                        </div>
                        {section.response.compliance_gaps?.length > 0 && (
                          <div className="mt-2 flex items-center gap-1 text-xs text-amber-600">
                            <AlertCircle size={11} />
                            {section.response.compliance_gaps.length} compliance gap{section.response.compliance_gaps.length > 1 ? "s" : ""}
                          </div>
                        )}
                      </>
                    ) : (
                      <p className="text-xs text-gray-400 italic">No response generated yet.</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Upload Modal */}
      {uploadOpen && <UploadRFPModal onClose={() => setUploadOpen(false)} onSuccess={() => { setUploadOpen(false); queryClient.invalidateQueries({ queryKey: ["rfps"] }); }} />}
    </div>
  );
}

function UploadRFPModal({ onClose, onSuccess }: { onClose: () => void; onSuccess: () => void }) {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    const fd = new FormData();
    fd.append("title", title);
    fd.append("original_file", file);
    try {
      await rfpAPI.create(fd);
      onSuccess();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="card w-full max-w-md p-6">
        <h2 className="text-base font-bold text-gray-900 mb-4">Upload RFP Document</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1.5">Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
              placeholder="Q3 Enterprise RFP — Acme Corp"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1.5">File (PDF or DOCX)</label>
            <div
              className="border-2 border-dashed border-gray-200 rounded-lg p-6 text-center cursor-pointer hover:border-brand-400 transition-colors"
              onClick={() => document.getElementById("rfp-file")?.click()}
            >
              <Upload size={20} className="mx-auto text-gray-300 mb-2" />
              <p className="text-xs text-gray-500">{file ? file.name : "Click to select file"}</p>
              <input id="rfp-file" type="file" accept=".pdf,.docx" className="hidden" onChange={(e) => setFile(e.target.files?.[0] || null)} />
            </div>
          </div>
          <div className="flex gap-2 justify-end">
            <button type="button" onClick={onClose} className="btn-secondary">Cancel</button>
            <button type="submit" disabled={loading || !file} className="btn-primary">
              {loading ? <Spinner size={14} /> : <Upload size={14} />}
              {loading ? "Uploading..." : "Upload & Parse"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
