# NOTICE for the skills-only distribution

This distribution contains MIT-licensed work from three upstream sources. The copyright notices and license terms travel beside this file.

## Upstream sources

| Included work | Upstream | Copyright | License |
| --- | --- | --- | --- |
| pstack-derived skills, principles, scripts, and the `comment-sicko` definition | [cursor/plugins/pstack](https://github.com/cursor/plugins/tree/e46364b8be46000b7df0f260550cd712afbb8d36/pstack), with later additions from [3fe2823](https://github.com/cursor/plugins/tree/3fe2823ce17c1656c222d4b7c59d3f82fbf20143/pstack) , [4612556](https://github.com/cursor/plugins/tree/4612556/pstack), [7314f72](https://github.com/cursor/plugins/tree/7314f72/pstack), and updates through [8b3326d](https://github.com/cursor/plugins/tree/8b3326d99fd4b993cb33a24dad8af03175c642c5/pstack) (pstack v0.15.30) | (c) 2026 Lauren Tan | [MIT](LICENSE) |
| `deslop`, `thermo-nuclear-code-quality-review`, `make-pr-easy-to-review`, `fix-ci`, `fix-merge-conflicts`, `get-pr-comments`, and `what-did-i-get-done` | [cursor/plugins/cursor-team-kit](https://github.com/cursor/plugins/tree/e46364b8be46000b7df0f260550cd712afbb8d36/cursor-team-kit) | (c) 2026 Cursor | [MIT](LICENSE-cursor-team-kit) |

The pstack-claude port changes runtime names, tool calls, model defaults, and supporting prose. The port's modifications and additions are (c) 2026 Michael Denyer under the same [MIT license](LICENSE). The [repository notice](https://github.com/michael-denyer/pstack-claude/blob/main/NOTICE.md) records full provenance. The [change log](https://github.com/michael-denyer/pstack-claude/blob/main/CHANGES.md) records each release, and [`tools/forks.json`](https://github.com/michael-denyer/pstack-claude/blob/main/tools/forks.json) names each file the port forks and why.

The added `thermos` and `thermo-nuclear-review` skills derive from [cursor/plugins/thermos](https://github.com/cursor/plugins/tree/118e73b0e196e4d49d5aade7ce6dd8985a621f68/thermos), copyright (c) 2026 Cursor, under [MIT](LICENSE-thermos), through the pstack-claude port. Their local adaptations preserve T3 routing and explicit activation.
