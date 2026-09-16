import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "Jarvis - Assistant Personnel Souverain",
  description: "Assistant IA full-stack souverain connecté à Supabase",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" className="dark">
      <body className="bg-[#0A0E1A] text-[#E6F1FF] min-h-screen flex">
        <Sidebar />
        <div className="flex-1 overflow-auto">{children}</div>
      </body>
    </html>
  );
}
