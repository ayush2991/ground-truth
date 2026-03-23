import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ground Truth - Fact Checker",
  description: "Fact-check your text using NLI and web search",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        {children}
      </body>
    </html>
  );
}
