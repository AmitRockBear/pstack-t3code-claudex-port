import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const checker = fileURLToPath(new URL("./check-plan.mjs", import.meta.url));
const playbook = fs.readFileSync(new URL("../playbooks/multi-phase-plan.md", import.meta.url), "utf8");
const skeleton = playbook.match(/````markdown\n([\s\S]*?)\n````/)[1].replace(
  "<absolute-path-to-installed-verify-change-SKILL.md>",
  fileURLToPath(new URL("../../verify-change/SKILL.md", import.meta.url))
);

function checkPlan(t, text) {
  const directory = fs.mkdtempSync(path.join(process.env.PSTACK_TEST_OUTPUT_DIR ?? os.tmpdir(), "pstack-plan-check-"));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  const file = path.join(directory, "plan.md");
  fs.writeFileSync(file, text);
  return { file, result: spawnSync(process.execPath, [checker, file], { encoding: "utf8" }) };
}

test("a plan copied outside the plugin passes and resolves its verification skill", (t) => {
  const { file, result } = checkPlan(t, skeleton);
  assert.equal(result.status, 0, result.stderr);
  const reference = skeleton.match(/\[verify-change\]\(([^)]+)\)/)[1];
  assert.ok(path.isAbsolute(reference));
  assert.ok(fs.existsSync(path.resolve(path.dirname(file), reference)));
});

test("a plan without independent verification is rejected", (t) => {
  const { result } = checkPlan(t, skeleton.replace("One independent verifier", "The implementation owner"));
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Verify, live/);
});

test("a plan without the shared verification policy is rejected", (t) => {
  const { result } = checkPlan(t, skeleton.replace(/\[verify-change\]\([^)]+\)/, "a private checklist"));
  assert.equal(result.status, 1);
  assert.match(result.stderr, /shared verify-change policy/);
});
