import React from "react";

export const MemoryCard: React.FC<{ fact: string; date?: string }> = ({ fact, date }) => (
  <div className="p-4 rounded-xl border border-cyan-500/20 bg-[#111827]/80 shadow-glow mb-3">
    <p className="text-sm text-[#E6F1FF]">{fact}</p>
    {date && <span className="text-xs text-gray-500 mt-2 block">{date}</span>}
  </div>
);
