import React from "react";
import Link from "next/link";
import { MessageSquare, Brain, Briefcase, Settings } from "lucide-react";

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-16 md:w-64 bg-[#0A0E1A]/90 border-r border-cyan-500/20 flex flex-col p-4">
      <div className="font-bold text-cyan-accent text-lg mb-8 hidden md:block tracking-wider">JARVIS</div>
      <nav className="flex flex-col gap-4">
        <Link href="/chat" className="flex items-center gap-3 text-gray-300 hover:text-cyan-accent p-2 rounded-lg hover:bg-cyan-500/10 transition-colors">
          <MessageSquare size={20} /> <span className="hidden md:inline">Discussion</span>
        </Link>
        <Link href="/memory" className="flex items-center gap-3 text-gray-300 hover:text-cyan-accent p-2 rounded-lg hover:bg-cyan-500/10 transition-colors">
          <Brain size={20} /> <span className="hidden md:inline">Mémoire</span>
        </Link>
        <Link href="/jobs" className="flex items-center gap-3 text-gray-300 hover:text-cyan-accent p-2 rounded-lg hover:bg-cyan-500/10 transition-colors">
          <Briefcase size={20} /> <span className="hidden md:inline">Opportunités</span>
        </Link>
        <Link href="/settings" className="flex items-center gap-3 text-gray-300 hover:text-cyan-accent p-2 rounded-lg hover:bg-cyan-500/10 transition-colors">
          <Settings size={20} /> <span className="hidden md:inline">Paramètres</span>
        </Link>
      </nav>
    </aside>
  );
};
