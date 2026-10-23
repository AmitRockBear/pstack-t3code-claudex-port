### Babysit

Use the bundled [babysit skill](../../babysit/SKILL.md) as the single babysitting policy. Opening a PR does not start monitoring. Merge or landing requests belong to [Shipping](shipping.md) and still require explicit authorization.

1. Classify the request. A status question is one read-only check. Addressing named comments stays within that scope. In T3, monitor/watch/babysit uses the skill's parent-owned `watch_pull_request` path and ends the turn; outside T3, use its harness-monitoring or polling path.
2. Before acting on the first status read, confirm that the PR or stack it reports matches the request, and name the current merge frontier. Use `gh` and verify the current head. Ensure there is only one babysitter for the requested scope.
3. Follow the skill's bot validation, written replies, current-head Code/Security Review completion, CI handling, rebase and root-to-tip stack rules. Treat a T3 wake as a notice to inspect readiness. Apply the 15-minute quiet-green rule only outside T3.
4. Stop according to the skill and report addressed/dismissed comments by review round with reasons. Keep material scope/product decisions with the user. Babysitting starts no extra agent review or UI verification unless requested; after a comment fix, return the exact delta and focused check receipts so the root applies verify-change before dispatching further verification.

**Reply:** current PR/stack state, comments addressed and dismissed grouped by round, reasons, pending decisions and remaining blockers. Include PR links. Babysitting alone never authorizes merging.
