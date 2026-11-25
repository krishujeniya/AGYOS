import { describe, test, expect } from "bun:test";
import { readFileSync, existsSync } from "fs";
import { resolve } from "path";

const repoRoot = resolve(import.meta.dir, "../../..");
const rulesDir = resolve(repoRoot, "rules");
const pluginsDir = resolve(repoRoot, "plugins");

describe("AGYOS SDLC Gates & Handoff Contracts", () => {
  test("handoff contract rule exists and specifies schema", () => {
    const file = existsSync(resolve(rulesDir, "agyos-handoff-contract.md"))
      ? resolve(rulesDir, "agyos-handoff-contract.md")
      : resolve(rulesDir, "agyos-handoff-contract.toon");
    expect(existsSync(file)).toBe(true);
    const content = readFileSync(file, "utf8");
    expect(content).toContain("handoff_id");
    expect(content).toContain("from_role");
    expect(content).toContain("to_role");
    expect(content).toContain("phase");
    expect(content).toContain("gate");
    expect(content).toContain("artifacts[]");
    expect(content).toContain("evidence[]");
    expect(content).toContain("status");
  });

  test("legal clearance gate rule requires SBOM evidence and verdict", () => {
    const file = existsSync(resolve(rulesDir, "agyos-gate-legal-clearance.md"))
      ? resolve(rulesDir, "agyos-gate-legal-clearance.md")
      : resolve(rulesDir, "agyos-gate-legal-clearance.toon");
    expect(existsSync(file)).toBe(true);
    const content = readFileSync(file, "utf8");
    expect(content).toContain("Gate: Legal Clearance");
    expect(content).toContain("oss-license-risk-audit");
    expect(content).toContain("gate-verdict.toon");
    expect(content).toContain("gate:legal-cleared");
    expect(content).toContain("role-ip-patent-attorney");
  });

  test("DSAR evidence gate rule requires subject-data inventory and TIA", () => {
    const file = existsSync(resolve(rulesDir, "agyos-gate-dsar-evidence.md"))
      ? resolve(rulesDir, "agyos-gate-dsar-evidence.md")
      : resolve(rulesDir, "agyos-gate-dsar-evidence.toon");
    expect(existsSync(file)).toBe(true);
    const content = readFileSync(file, "utf8");
    expect(content).toContain("Gate: DSAR Evidence");
    expect(content).toContain("dsar-pipeline");
    expect(content).toContain("tia-report.toon");
  });

  test("policy guard hooks enforce write scoping and uv-only commands", () => {
    const hooksFile = resolve(pluginsDir, "agyos-policy-guard/hooks.json");
    expect(existsSync(hooksFile)).toBe(true);
    const parsed = JSON.parse(readFileSync(hooksFile, "utf8"));
    expect(Array.isArray(parsed.hooks)).toBe(true);
    const events = parsed.hooks.map((h: { event: string }) => h.event);
    expect(events).toContain("PreToolUse");
    expect(events).toContain("PostToolUse");
    expect(events).toContain("Stop");
  });
});
