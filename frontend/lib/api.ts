const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatResponse {
  response: string;
  conversation_id: string;
  created_at: string;
}

export async function sendChatMessage(message: string, conversationId?: string): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
  if (!res.ok) {
    throw new Error(`Erreur Jarvis: ${res.statusText}`);
  }
  return res.json();
}
