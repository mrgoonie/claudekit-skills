---
name: multi-agent-coordination
type: task
concepts: [multi-agent-patterns, context-isolation, coordination]
timeout: 180
---

# Prompt
I'm building a multi-agent system where agents keep duplicating work and their contexts get polluted with irrelevant information from other agents. How should I design the coordination to maintain context isolation?

# Expected
- [ ] Emphasizes context isolation principle ("Isolation prevents degradation")
- [ ] Recommends sub-agents for context isolation, not role-play
- [ ] Addresses cost implications (~15x single agent baseline)
- [ ] Suggests partitioning work across sub-agents
- [ ] May mention Write strategy (save context externally)
- [ ] References multi-agent-patterns.md for detailed patterns
