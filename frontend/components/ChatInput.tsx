"use client";
import React, { useState, useRef } from "react";
import { Send, Mic, Square } from "lucide-react";

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  isLoading: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [text, setText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim() || isLoading) return;
    onSendMessage(text);
    setText("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleRecording = async () => {
    if (isRecording) {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      alert("Accès microphone non disponible");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative flex items-end gap-2 p-3 bg-[#111728]/80 backdrop-blur-md rounded-2xl border border-cyan-500/20 shadow-glow">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Demandez ou ordonnez à Jarvis..."
        rows={1}
        className="flex-1 max-h-32 bg-transparent text-[#E6F1FF] placeholder-gray-400 text-sm md:text-base resize-none focus:outline-none px-2 py-1"
      />
      <button
        type="button"
        onClick={toggleRecording}
        className={`p-2 rounded-xl transition-all ${
          isRecording ? "bg-red-500/20 text-red-400 border border-red-500 animate-pulse" : "text-cyan-accent hover:bg-cyan-500/10"
        }`}
      >
        {isRecording ? <Square size={20} /> : <Mic size={20} />}
      </button>
      <button
        type="submit"
        disabled={isLoading || !text.trim()}
        className="p-2 rounded-xl bg-cyan-accent/20 border border-cyan-accent text-cyan-accent hover:bg-cyan-accent hover:text-black transition-all disabled:opacity-40"
      >
        <Send size={20} />
      </button>
    </form>
  );
};
