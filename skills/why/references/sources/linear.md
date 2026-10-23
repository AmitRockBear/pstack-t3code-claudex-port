# Linear tickets

Use the Linear CLI, executable `linear`, for ticket descriptions, status, linked work, and product constraints.

1. Check `command -v linear`, `linear issue --help`, and the relevant subcommand help.
2. Fetch linked identifiers first with `linear issue view <issue-id>`.
3. Use `linear issue list --all --limit 100` for discovery within the installed CLI's assigned-issue scope; inspect help before requesting additional filters or wider searches.
4. Follow related issue or project identifiers through supported read commands and inspect the original decision wording.
5. Report any unavailable comments, parent issues, project documents, workspace search, or pagination as a coverage gap; assigned-issue listing does not search the whole workspace.

Return issue ID, URL when available, dates, the relevant original wording, and the commands/scope actually searched. Distinguish stale or duplicate tickets from independent evidence. Investigation uses read commands; ticket creation and updates require authorization from the parent task.
