import React from "react";

export const JobCard: React.FC<{ title: string; company: string; status: string }> = ({ title, company, status }) => (
  <div className="p-4 rounded-xl border border-violet-500/30 bg-[#111827]/80 shadow-glowViolet mb-3 flex justify-between items-center">
    <div>
      <h3 className="font-semibold text-white">{title}</h3>
      <p className="text-xs text-gray-400">{company}</p>
    </div>
    <span className="text-xs px-2 py-1 rounded bg-violet-500/20 text-violet-accent uppercase font-bold">{status}</span>
  </div>
);
