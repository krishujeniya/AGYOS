"use client";

import React, { useState } from "react";
import { Search, BookOpen, Layers } from "lucide-react";

interface Skill {
  name: string;
  category: string;
  description: string;
}

const SAMPLE_SKILLS: Skill[] = [
  { name: "agyos-orchestrator", category: "Core", description: "Autonomous 5-gate lifecycle controller and state transition governor." },
  { name: "fastapi-pro", category: "Backend", description: "Production FastAPI async patterns, dependency injection, and Pydantic v2 schemas." },
  { name: "nextjs-best-practices", category: "Frontend", description: "App Router architecture, React Server Components, and Turbopack optimization." },
  { name: "cloudflare-workers-expert", category: "Infra", description: "Edge computing, D1 database binding, KV namespaces, and Cloudflare Pages." },
  { name: "systematic-debugging", category: "Quality", description: "Root cause reproduction, differential review, and isolated bugfix ratchets." },
  { name: "rust-pro", category: "Backend", description: "Master Rust async patterns, memory safety, and high-throughput zero-cost abstractions." },
  { name: "security-auditor", category: "Security", description: "DevSecOps scanning, OWASP Top 10 analysis, and credential redaction." },
  { name: "ai-engineer", category: "AI & Data", description: "LLM fine-tuning, prompt optimization, RAG pipelines, and EVPI decision trees." },
];

export function SkillExplorer() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");

  const categories = ["All", "Core", "Backend", "Frontend", "Infra", "Quality", "Security", "AI & Data"];

  const filteredSkills = SAMPLE_SKILLS.filter((skill) => {
    const matchesSearch =
      skill.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      skill.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === "All" || skill.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div id="skills" className="space-y-6">
      {/* Search and Category Filters */}
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3.5 top-3 h-4 w-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search 2,289 capabilities..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-xl border border-slate-800 bg-slate-900/80 py-2.5 pl-10 pr-4 text-sm text-slate-200 placeholder-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <div className="flex flex-wrap gap-1.5 w-full sm:w-auto">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`rounded-lg px-3 py-1.5 text-xs font-medium transition ${
                selectedCategory === cat
                  ? "bg-blue-600 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Skills Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredSkills.map((skill) => (
          <div
            key={skill.name}
            className="group rounded-xl border border-slate-800/80 bg-slate-900/40 p-5 hover:border-slate-700 transition hover:bg-slate-900/60"
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold text-blue-400">{skill.category}</span>
              <BookOpen className="h-4 w-4 text-slate-600 group-hover:text-blue-400 transition" />
            </div>
            <h3 className="mt-2 font-mono text-sm font-semibold text-white tracking-wide">{skill.name}</h3>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">{skill.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
