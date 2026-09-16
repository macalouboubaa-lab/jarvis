import React from "react";

export const VoiceWave: React.FC = () => {
  return (
    <div className="flex items-center gap-1 h-6">
      <span className="w-1 h-3 bg-cyan-accent animate-pulse" />
      <span className="w-1 h-5 bg-cyan-accent animate-pulse delay-75" />
      <span className="w-1 h-2 bg-cyan-accent animate-pulse delay-150" />
      <span className="w-1 h-6 bg-cyan-accent animate-pulse delay-100" />
    </div>
  );
};
