"use client";

import React, { useState } from "react";
import { Users, Briefcase, Award } from "lucide-react";

interface Role {
  id: string;
  name: string;
  department: string;
  seniority: string;
  pod: string;
  description: string;
}

const SAMPLE_ROLES: Role[] = [
  { id: "role-swe", name: "Staff Software Engineer", department: "Engineering", seniority: "L6", pod: "pod-build", description: "Distributed backend architecture, concurrency, and performance tuning." },
  { id: "role-frontend-engineer", name: "Senior Frontend Engineer", department: "Engineering", seniority: "L5", pod: "pod-build", description: "Next.js App Router, React 19, responsive UX, and Web Vitals." },
  { id: "role-agentic-workflow-architect", name: "Agentic Workflow Architect", department: "Engineering", seniority: "L7", pod: "pod-build", description: "Autonomous multi-agent swarms, self-healing graphs, and guardrails." },
  { id: "role-mlops-engineer", name: "MLOps Engineer", department: "Data & AI", seniority: "L6", pod: "pod-build", description: "High-throughput inference engines, ONNX compilation, and model registries." },
  { id: "role-product-director", name: "Product Director", department: "Product", seniority: "L7", pod: "pod-build", description: "Amazon Working Backwards PR/FAQ, roadmaps, and stakeholder alignment." },
  { id: "role-ux-ui-designer", name: "Staff UX/UI Designer", department: "Design", seniority: "L6", pod: "pod-build", description: "Design systems, typography, WCAG 2.2 accessibility, and micro-interactions." },
  { id: "role-general-counsel", name: "General Counsel", department: "Legal & Compliance", seniority: "L8", pod: "pod-gna", description: "Open source governance, commercial contracts, IP risk mitigation." },
  { id: "role-startup-cfo", name: "Startup CFO Advisor", department: "Finance", seniority: "L7", pod: "pod-gna", description: "Runway forecasting, unit economics, Cap table modeling, and treasury." },
  { id: "role-solopreneur-operator", name: "Solopreneur Operator", department: "People & Ops", seniority: "L8", pod: "pod-growth", description: "End-to-end autonomous business execution and rapid venture iteration." },
];

export function RoleMatrix() {
  const [selectedDept, setSelectedDept] = useState("All");

  const departments = ["All", "Engineering", "Data & AI", "Product", "Design", "Legal & Compliance", "Finance", "People & Ops"];

  const filteredRoles = SAMPLE_ROLES.filter((role) => {
    return selectedDept === "All" || role.department === selectedDept;
  });

  return (
    <div id="roles" className="space-y-6">
      {/* Department Filter */}
      <div className="flex flex-wrap gap-2 justify-center">
        {departments.map((dept) => (
          <button
            key={dept}
            onClick={() => setSelectedDept(dept)}
            className={`rounded-lg px-3.5 py-1.5 text-xs font-medium transition ${
              selectedDept === dept
                ? "bg-blue-600 text-white"
                : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
            }`}
          >
            {dept}
          </button>
        ))}
      </div>

      {/* Role Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredRoles.map((role) => (
          <div
            key={role.id}
            className="rounded-xl border border-slate-800/80 bg-slate-900/40 p-5 hover:border-slate-700 transition"
          >
            <div className="flex items-center justify-between">
              <span className="rounded bg-blue-500/10 px-2 py-0.5 text-xs font-mono font-semibold text-blue-400">
                {role.seniority}
              </span>
              <span className="text-xs font-mono text-slate-500">{role.pod}</span>
            </div>
            <h3 className="mt-3 font-semibold text-white text-base">{role.name}</h3>
            <span className="text-xs text-slate-400 font-medium">{role.department}</span>
            <p className="mt-2 text-xs text-slate-400 leading-relaxed">{role.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
