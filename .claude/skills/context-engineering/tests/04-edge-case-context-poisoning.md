---
name: edge-case-context-poisoning
type: task
concepts: [context-degradation, context-poisoning, security]
timeout: 120
---

# Prompt
Users are injecting adversarial prompts into our chatbot that corrupt the agent's behavior for the rest of the session. Even after the malicious message, the agent keeps behaving incorrectly. What's happening and how do I prevent it?

# Expected
- [ ] Identifies context poisoning as degradation pattern
- [ ] Explains how malicious content persists in context window
- [ ] Recommends input validation/sanitization
- [ ] Suggests context isolation or session segmentation
- [ ] May recommend masking or filtering strategies
- [ ] References context-degradation.md for poisoning patterns
