import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AGYOS — Autonomous Cognitive Operating System",
  description: "Enterprise multi-agent cognitive kernel, 104-role matrix, and 2,289-skill catalog for AGY CLI.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#090d16] text-slate-100 antialiased selection:bg-blue-600 selection:text-white">
        <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-[#090d16]/80 backdrop-blur-md">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 font-bold text-white shadow-lg shadow-blue-500/20">
                A
              </span>
              <span className="text-xl font-bold tracking-tight text-white">AGYOS</span>
              <span className="rounded-full bg-blue-500/10 px-2.5 py-0.5 text-xs font-medium text-blue-400 border border-blue-500/20">
                v3.2.0
              </span>
            </div>
            <nav className="flex items-center gap-6 text-sm font-medium text-slate-300">
              <a href="#skills" className="transition hover:text-white">Skills</a>
              <a href="#roles" className="transition hover:text-white">Roles</a>
              <a href="#architecture" className="transition hover:text-white">Architecture</a>
              <a
                href="https://github.com/krishujeniya/AGYOS"
                target="_blank"
                rel="noreferrer"
                className="rounded-lg bg-slate-800 px-3.5 py-1.5 text-xs font-semibold text-white transition hover:bg-slate-700"
              >
                GitHub
              </a>
            </nav>
          </div>
        </header>
        <main>{children}</main>
        <footer className="border-t border-slate-800/80 py-12 text-center text-xs text-slate-500">
          <div className="mx-auto max-w-7xl px-6">
            <p>© 2026 AGYOS Cognitive Operating System. Designed for autonomous swarms and independent operators.</p>
            <p className="mt-2">Protected under Apache License 2.0. Author: Krish Ujeniya.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
