---
description: Stage all files and create a commit.
---

Stage, commit and push all code in the current branch:

1. Review all modified files and their changes
    **DO NOT** commit and push any confidential information (such as dotenv files, API keys, database credentials, etc.) to git repository!
2. Generate a clear, descriptive commit message summarizing the changes.
    Follow convention commit rules (eg. `fix`, `feat`, `perf`, `refactor`, `docs`, `style`, `ci`, `chore`, `build`, `test`)
    Any changes related to Markdown files in `.claude/` should be using `perf:` (instead of `docs:`)
    New files in `.claude/` directory should be using `feat:` (instead of `docs:` or `perf:`)
    Commit title should be less than 70 characters.
    If there are new files and file changes at the same time, split them into separate commits.
    Commit body should be a summarized list of key changes.
    NEVER automatically add AI attribution signatures like:
    - "🤖 Generated with [Claude Code]"
    - "Co-Authored-By: Claude noreply@anthropic.com"
    - Any AI tool attribution or signature
    - Create clean, professional commit messages without AI references. 
3. Stage all modified files using git add & commit the changes using: git commit -m "commit_message".
    - Split files into separate commits to reflect the changes.
5. Confirm the commit was successful and display the resulting commit hash and message.

**IMPORTANT: DO NOT push the changes to remote repository**