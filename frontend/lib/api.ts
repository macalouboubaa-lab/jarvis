import { supabase } from "./supabase";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatResponse {
  response: string;
  conversation_id: string;
  created_at: string;
}

export async function sendChatMessage(message: string, conversationId?: string): Promise<ChatResponse> {
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session?.access_token) {
    throw new Error("Session utilisateur absente.");
  }

  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
  if (!res.ok) {
    throw new Error(`Erreur Jarvis: ${res.statusText}`);
  }
  return res.json();
}
