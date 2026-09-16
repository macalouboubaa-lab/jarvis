import React from "react";

interface ChatBubbleProps {
  sender: "user" | "assistant";
  content: string;
  time?: string;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ sender, content, time }) => {
  const isAssistant = sender === "assistant";
  return (
    <div className={`flex w-full mb-4 ${isAssistant ? "justify-start" : "justify-end"}`}>
      <div
        className={`max-w-[85%] md:max-w-[70%] rounded-2xl p-4 text-sm md:text-base backdrop-blur-sm ${
          isAssistant
            ? "bg-[#111827]/90 text-[#E6F1FF] border border-cyan-accent/30 shadow-glow"
            : "bg-[#7B61FF]/20 text-[#E6F1FF] border border-violet-accent/40 shadow-glowViolet"
        }`}
      >
        <div className="flex items-center justify-between mb-1 gap-4">
          <span className={`text-xs font-semibold uppercase tracking-wider ${isAssistant ? "text-cyan-accent" : "text-violet-accent"}`}>
            {isAssistant ? "Jarvis" : "Vous"}
          </span>
          {time && <span className="text-[10px] text-gray-400">{time}</span>}
        </div>
        <p className="whitespace-pre-wrap leading-relaxed">{content}</p>
      </div>
    </div>
  );
};
