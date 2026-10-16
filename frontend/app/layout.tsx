import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Universal Task AI — Command Center",
  description: "A secure workspace for AI tasks, workflows, agents, and automation.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
