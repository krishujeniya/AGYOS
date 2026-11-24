"use client";

import React, { useState } from "react";
import { Search, Compass, Terminal, Cpu, ShieldCheck } from "lucide-react";
import { SkillExplorer } from "../features/skill-explorer";
import { RoleMatrix } from "../features/role-matrix";

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<"skills" | "roles">("skills");

  return (
    <div className="mx-auto max-w-7xl px-6 py-12">
      {/* Hero Section */}
      <section className="text-center py-12 border-b border-slate-800/60 pb-16">
        <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-1.5 text-xs font-medium text-blue-400 mb-6">
          <Cpu className="h-3.5 w-3.5" />
          Autonomous Multi-Agent Kernel & 104-Role Matrix
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl text-white">
          AGYOS Cognitive Operating System
        </h1>
        <p className="mt-4 max-w-2xl mx-auto text-base sm:text-lg text-slate-400">
          The autonomous execution kernel for AGY CLI. Plan, build, review, test, and ship software under strict engineering invariants with 2,289 skill runbooks.
        </p>

        {/* Quick CLI Banner */}
        <div className="mt-8 max-w-xl mx-auto rounded-xl border border-slate-800 bg-slate-900/90 p-4 shadow-2xl backdrop-blur">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2 font-mono">
            <span>Terminal</span>
            <span className="text-blue-400">bash</span>
          </div>
          <div className="flex items-center gap-2 font-mono text-sm text-slate-200">
            <span className="text-blue-500 select-none">$</span>
            <code>bin/agyos decide &quot;Implement tenant isolation adapter&quot; --json</code>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <section className="mt-12">
        <div className="flex items-center justify-center gap-4 mb-8">
          <button
            onClick={() => setActiveTab("skills")}
            className={`flex items-center gap-2 rounded-lg px-5 py-2.5 text-sm font-semibold transition ${
              activeTab === "skills"
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/25"
                : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
            }`}
          >
            <Search className="h-4 w-4" />
            Skill Catalog (2,289 Skills)
          </button>
          <button
            onClick={() => setActiveTab("roles")}
            className={`flex items-center gap-2 rounded-lg px-5 py-2.5 text-sm font-semibold transition ${
              activeTab === "roles"
                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/25"
                : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
            }`}
          >
            <Compass className="h-4 w-4" />
            104-Role Enterprise Matrix
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === "skills" ? <SkillExplorer /> : <RoleMatrix />}
      </section>

      {/* Architecture Highlights */}
      <section id="architecture" className="mt-20 border-t border-slate-800/80 pt-16">
        <div className="text-center mb-12">
          <h2 className="text-2xl font-bold text-white">7-Step Autonomous Cycle</h2>
          <p className="mt-2 text-sm text-slate-400">
            Every task transitions deterministically across 7 stages without manual intervention.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
            <span className="text-xs font-mono font-bold text-blue-400">01 / THINK</span>
            <h3 className="mt-2 font-semibold text-white">Intent & EVPI</h3>
            <p className="mt-1 text-xs text-slate-400 leading-relaxed">
              Compiles natural language prompt to typed TaskContract and assigns specialist roles.
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
            <span className="text-xs font-mono font-bold text-blue-400">02 / PLAN</span>
            <h3 className="mt-2 font-semibold text-white">Blueprint & Gates</h3>
            <p className="mt-1 text-xs text-slate-400 leading-relaxed">
              Generates architectural blueprints, acceptance criteria, and structured checkpoints.
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
            <span className="text-xs font-mono font-bold text-blue-400">03 / BUILD</span>
            <h3 className="mt-2 font-semibold text-white">Maker TDD</h3>
            <p className="mt-1 text-xs text-slate-400 leading-relaxed">
              Executes RED ➔ GREEN ➔ REFACTOR cycles with monotonic test ratchets.
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
            <span className="text-xs font-mono font-bold text-blue-400">04-07 / SHIP</span>
            <h3 className="mt-2 font-semibold text-white">Review & Delivery</h3>
            <p className="mt-1 text-xs text-slate-400 leading-relaxed">
              Checker audit, remote CI execution, and fast-forward delivery strictly to main.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
