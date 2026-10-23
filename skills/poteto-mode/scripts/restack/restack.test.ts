import { describe, expect, test } from "bun:test";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const script = join(import.meta.dir, "restack.sh");

function repo() {
  const dir = mkdtempSync(join(tmpdir(), "restack-"));
  const git = (...args: string[]) => {
    const r = Bun.spawnSync(["git", ...args], { cwd: dir });
    if (r.exitCode !== 0) throw new Error(`git ${args.join(" ")}: ${r.stderr}`);
    return r.stdout.toString().trim();
  };
  const commit = (file: string, text: string) => {
    writeFileSync(join(dir, file), text);
    git("add", file);
    git("commit", "-qm", `${file}:${text}`);
    return git("rev-parse", "HEAD");
  };
  git("init", "-q", "-b", "main");
  git("config", "user.email", "t@t");
  git("config", "user.name", "t");
  commit("base.txt", "base");
  return { dir, git, commit };
}

function run(dir: string, args: string[]) {
  const r = Bun.spawnSync(["bash", script, ...args], { cwd: dir });
  return { code: r.exitCode, out: r.stdout.toString(), err: r.stderr.toString() };
}

describe("restack.sh", () => {
  test("rebases a two-level stack onto the new base and records old heads", () => {
    const { dir, git, commit } = repo();
    const oldBase = git("rev-parse", "HEAD");
    git("checkout", "-qb", "a");
    const aOld = commit("a.txt", "a");
    git("checkout", "-qb", "b");
    const bOld = commit("b.txt", "b");
    git("checkout", "-q", "main");
    const newBase = commit("main.txt", "trunk");
    const record = join(dir, "record.txt");

    const r = run(dir, ["--onto", newBase, "--old-base", oldBase, "--record", record, "a", "b"]);

    expect(r.code).toBe(0);
    expect(git("merge-base", "--is-ancestor", newBase, "a")).toBe("");
    expect(git("rev-parse", "b~1")).toBe(git("rev-parse", "a"));
    expect(readFileSync(record, "utf8")).toBe(`a ${aOld}\nb ${bOld}\n`);
  });

  test("stops at the first failed rebase and leaves later branches untouched", () => {
    const { dir, git, commit } = repo();
    const oldBase = git("rev-parse", "HEAD");
    git("checkout", "-qb", "a");
    commit("base.txt", "a-change");
    git("checkout", "-qb", "b");
    const bOld = commit("b.txt", "b");
    git("checkout", "-q", "main");
    const newBase = commit("base.txt", "conflicting-trunk");

    const r = run(dir, ["--onto", newBase, "--old-base", oldBase, "--record", join(dir, "rec"), "a", "b"]);

    expect(r.code).toBe(1);
    expect(r.err).toContain("rebase of a failed; stopped");
    expect(git("rev-parse", "b")).toBe(bOld);
    expect(git("status", "--porcelain", "--untracked-files=no")).toBe("");
  });
});
