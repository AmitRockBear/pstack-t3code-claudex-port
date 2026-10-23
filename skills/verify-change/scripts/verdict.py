"""Record a verification verdict with its head, and check a claim against it.

record: verdict.py record --repo OWNER/REPO --pr N --head SHA --label LABEL --out FILE
check:  verdict.py check --record FILE --claim CLAIM [--head SHA]
carry-forward: verdict.py carry-forward --record FILE --head SHA --base SHA --base-branch BRANCH --reason TEXT --out FILE
check exits 1 when the claim is stronger than the recorded label or the head moved.
Without --head, check reads the PR's current head through gh.
"""

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, cast, get_args

Label = Literal["verified", "partially-verified", "blocked"]
LABELS: tuple[Label, ...] = get_args(Label)
RANK: dict[str, int] = {"blocked": 0, "partially-verified": 1, "verified": 2, "clean": 2}


@dataclass(frozen=True)
class Assessment:
    head: str
    base: str
    base_branch: str
    reason: str
    prior_record: str
    assessed_at: str


@dataclass(frozen=True)
class Verdict:
    repo: str
    pr: int
    head: str
    label: Label
    measured_at: str
    assessment: Assessment | None = None


def load(path: Path) -> Verdict:
    raw = json.loads(path.read_text())
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: verdict must be a JSON object")
    for key, kind in (("repo", str), ("pr", int), ("head", str), ("label", str), ("measured_at", str)):
        if not isinstance(raw.get(key), kind):
            raise ValueError(f"{path}: field {key!r} must be {kind.__name__}")
    if raw["label"] not in LABELS:
        raise ValueError(f"{path}: label must be one of {', '.join(LABELS)}")
    assessment = raw.get("assessment")
    if assessment is not None:
        if not isinstance(assessment, dict):
            raise ValueError(f"{path}: assessment must be an object")
        for key in Assessment.__dataclass_fields__:
            if not isinstance(assessment.get(key), str) or not assessment[key].strip():
                raise ValueError(f"{path}: assessment field {key!r} must be a nonempty string")
        assessment = Assessment(**assessment)
    return Verdict(raw["repo"], raw["pr"], raw["head"], cast(Label, raw["label"]), raw["measured_at"], assessment)


def current_head(repo: str, pr: int) -> str:
    out = subprocess.run(
        ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "headRefOid", "--jq", ".headRefOid"],
        check=True, capture_output=True, text=True,
    )
    return out.stdout.strip()


def check(verdict: Verdict, claim: str, head: str, base: str | None = None, base_branch: str | None = None) -> list[str]:
    problems = []
    expected_head = verdict.assessment.head if verdict.assessment else verdict.head
    if not head.startswith(expected_head) and not expected_head.startswith(head):
        problems.append(f"head moved: verdict applies to {expected_head}, PR head is {head}")
    if verdict.assessment and (base, base_branch) != (verdict.assessment.base, verdict.assessment.base_branch):
        problems.append("base changed or unavailable: reassess the evidence")
    if RANK[claim] > RANK[verdict.label]:
        problems.append(f"claim {claim!r} is stronger than the recorded label {verdict.label!r}")
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="verdict.py")
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--repo", required=True)
    rec.add_argument("--pr", required=True, type=int)
    rec.add_argument("--head", required=True)
    rec.add_argument("--label", required=True, choices=LABELS)
    rec.add_argument("--out", required=True, type=Path)
    chk = sub.add_parser("check")
    chk.add_argument("--record", required=True, type=Path)
    chk.add_argument("--claim", required=True, choices=tuple(RANK))
    chk.add_argument("--head")
    chk.add_argument("--base")
    chk.add_argument("--base-branch")
    carry = sub.add_parser("carry-forward")
    carry.add_argument("--record", required=True, type=Path)
    carry.add_argument("--head", required=True)
    carry.add_argument("--base", required=True)
    carry.add_argument("--base-branch", required=True)
    carry.add_argument("--reason", required=True)
    carry.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)

    if args.command == "record":
        verdict = Verdict(args.repo, args.pr, args.head, args.label, datetime.now(timezone.utc).isoformat())
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(asdict(verdict), indent=2) + "\n")
        print(f"recorded {verdict.label} for {verdict.repo}#{verdict.pr} at {verdict.head}")
        return 0

    verdict = load(args.record)
    if args.command == "carry-forward":
        if args.out.resolve() == args.record.resolve():
            parser.error("carry-forward must preserve the prior record; choose a different --out")
        if not all(value.strip() for value in (args.head, args.base, args.base_branch, args.reason)):
            parser.error("carry-forward requires a nonempty head, base, base branch and reason")
        assessment = Assessment(args.head, args.base, args.base_branch, args.reason, str(args.record.resolve()), datetime.now(timezone.utc).isoformat())
        verdict = replace(verdict, assessment=assessment)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(asdict(verdict), indent=2) + "\n")
        print(f"carried forward {verdict.label} to {assessment.head}; proof measured at {verdict.head}")
        return 0

    head = args.head or current_head(verdict.repo, verdict.pr)
    if verdict.assessment and (args.base is None or args.base_branch is None):
        if args.base is not None or args.base_branch is not None:
            parser.error("supply both --base and --base-branch, or neither to read them from GitHub")
        result = subprocess.run(
            ["gh", "pr", "view", str(verdict.pr), "--repo", verdict.repo, "--json", "baseRefOid,baseRefName"],
            check=True, capture_output=True, text=True,
        )
        context = json.loads(result.stdout)
        args.base, args.base_branch = context["baseRefOid"], context["baseRefName"]
    problems = check(verdict, args.claim, head, args.base, args.base_branch)
    for problem in problems:
        print(f"verdict check failed: {problem}", file=sys.stderr)
    if not problems:
        print(f"ok: {args.claim} applies at {head}; proof measured at {verdict.head}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
