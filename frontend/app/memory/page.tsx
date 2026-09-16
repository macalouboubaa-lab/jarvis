import React from "react";

export default function MemoryPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-cyan-accent mb-4">Mémoire Sémantique</h1>
      <p className="text-gray-400 text-sm mb-6">Souvenirs et faits mémorisés dans votre base Supabase.</p>
      <div className="p-4 rounded-xl border border-cyan-500/20 bg-[#111827]">
        Prêt pour l'interrogation via Mem0.
      </div>
    </div>
  );
}
