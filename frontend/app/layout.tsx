import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agent-Ready Merchant OS",
  description: "AI-native commerce operations for merchants",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
