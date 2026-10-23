# Slack conversations

Use the Slack plugin for conversation evidence. Follow [Evidence sources](../source-playbook.md) for source access, executing-provider restrictions and lookup delegation.

1. Discover the installed Slack plugin's search and thread-read tools in the executing Codex session, loading deferred tools when necessary.
2. Give the worker the question, code anchor, repository/PR links, known people/channels, time window, read-only scope, and expected cited findings.
3. Search PR URLs, feature names, symbols, or error strings; narrow by author, channel, and date when supported by the actual tool schema.
4. Fetch the whole relevant thread before interpreting a message as a decision.
5. Report missing tools, authentication failures, inaccessible channels, retention limits, or unsearched private conversations as gaps.
6. Return channel, permalink or thread identifier, participants, dates, attributable original wording, and the queries actually run; the caller waits for completion and verifies the report.

Keep the lookup read-only and return the cited conversation evidence to the caller.
