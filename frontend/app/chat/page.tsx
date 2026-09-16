"use client";
import React, { useState } from "react";
import { ChatBubble } from "@/components/ChatBubble";
import { ChatInput } from "@/components/ChatInput";
import { sendChatMessage } from "@/lib/api";
import { ShieldCheck, Cpu } from "lucide-react";

interface Message {
  id: string;
  sender: "user" | "assistant";
  content: string;
  time: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init-1",
      sender: "assistant",
      content: "Bonjour Monsieur. Je suis Jarvis, votre assistant personnel souverain. Vos données restent strictement stockées dans votre propre base Supabase. Comment puis-je vous assister aujourd'hui ?",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (text: string) => {
    const userMsg: Message = {
      id: Date.now().toString(),
      sender: "user",
      content: text,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const data = await sendChatMessage(text);
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: "assistant",
        content: data.response,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: "assistant",
          content: `⚠️ Erreur : ${error.message}`,
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto px-4 py-6">
      <header className="flex items-center justify-between pb-4 border-b border-cyan-500/20 mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-cyan-accent/10 border border-cyan-accent flex items-center justify-center shadow-glow">
            <Cpu className="text-cyan-accent" size={22} />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              JARVIS <span className="text-xs font-normal text-cyan-accent uppercase tracking-widest px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-accent/30">Souverain</span>
            </h1>
            <p className="text-xs text-gray-400">GPT-4o-mini • Mem0 • Supabase pgvector</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs text-green-400 bg-green-500/10 px-3 py-1.5 rounded-full border border-green-500/30">
          <ShieldCheck size={14} />
          <span>Données souveraines</span>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto pr-2 space-y-2">
        {messages.map((msg) => (
          <ChatBubble key={msg.id} sender={msg.sender} content={msg.content} time={msg.time} />
        ))}
        {isLoading && (
          <div className="flex items-center gap-2 p-3 text-sm text-cyan-accent/80 animate-pulse">
            <div className="w-2 h-2 rounded-full bg-cyan-accent animate-ping" />
            <span>Jarvis réfléchit...</span>
          </div>
        )}
      </main>

      <footer className="pt-2">
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </footer>
    </div>
  );
}
