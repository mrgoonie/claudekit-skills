---
description: Create a new agent skill
argument-hint: [prompt]
---

Ultrathink.

**IMPORTANT:** 
- Read this skill documentation carefully before starting: https://docs.claude.com/en/docs/claude-code/skills.md
- Read the Agent Skills Spec carefully before starting: `.claude/skills/agent_skills_spec.md`

Create a new **Agent Skill** for Claude Code based on the given prompt:
<prompt>$ARGUMENTS</prompt>

- **Skills location:** `./.claude/skills`
- Skill file name (uppercase): `SKILL.md`
- Skill folder name (hyphen-case): `<skill-name>`
- Full path: `./.claude/skills/<skill-name>/SKILL.md`
- Script files (if any): `./.claude/skills/<skill-name>/scripts/my-script.py` or `./.claude/skills/<skill-name>/scripts/my-script.sh`
- Reference files (if any): `./.claude/skills/<skill-name>/references/ref-0.md`

## References (MUST READ):
- [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview.md)
- [Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices.md)

## Important Notes:
- If you're given an URL, it's documentation page, use `Explorer` subagent to explore every internal link and report back to main agent, don't skip any link.
- If you receive a lot of URLs, use multiple `Explorer` subagents to explore them in parallel, then report back to main agent.
- If you receive a lot of files, use multiple `Explorer` subagents to explore them in parallel, then report back to main agent.