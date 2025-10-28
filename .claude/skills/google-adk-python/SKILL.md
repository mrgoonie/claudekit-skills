# Google ADK Python Skill

You are an expert guide for Google's Agent Development Kit (ADK) Python - an open-source, code-first toolkit for building, evaluating, and deploying AI agents.

## When to Use This Skill

Use this skill when users need to:
- Build AI agents with tool integration and orchestration capabilities
- Create multi-agent systems with hierarchical coordination
- Implement workflow agents (sequential, parallel, loop) for predictable pipelines
- Integrate LLM-powered agents with Google Search, Code Execution, or custom tools
- Deploy agents to Vertex AI Agent Engine, Cloud Run, or custom infrastructure
- Evaluate and test agent performance systematically
- Implement human-in-the-loop approval flows for tool execution

## Core Concepts

### Agent Types

**LlmAgent**: LLM-powered agents capable of dynamic routing and adaptive behavior
- Define with name, model, instruction, description, and tools
- Supports sub-agents for delegation and coordination
- Intelligent decision-making based on context

**Workflow Agents**: Structured, predictable orchestration patterns
- **SequentialAgent**: Execute agents in defined order
- **ParallelAgent**: Run multiple agents concurrently
- **LoopAgent**: Repeat execution with iteration logic

**BaseAgent**: Foundation for custom agent implementations

### Key Components

**Tools Ecosystem**:
- Pre-built tools (google_search, code_execution)
- Custom Python functions as tools
- OpenAPI specification integration
- Tool confirmation flows for human approval

**Multi-Agent Architecture**:
- Hierarchical agent composition
- Specialized agents for specific domains
- Coordinator agents for delegation

## Installation

```bash
# Stable release (recommended)
pip install google-adk

# Development version (latest features)
pip install git+https://github.com/google/adk-python.git@main
```

## Implementation Patterns

### Single Agent with Tools

```python
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

agent = LlmAgent(
    name="search_assistant",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant that searches the web for information.",
    description="Search assistant for web queries",
    tools=[google_search]
)
```

### Multi-Agent System

```python
from google.adk.agents import LlmAgent

# Specialized agents
researcher = LlmAgent(
    name="Researcher",
    model="gemini-2.5-flash",
    instruction="Research topics thoroughly using web search.",
    tools=[google_search]
)

writer = LlmAgent(
    name="Writer",
    model="gemini-2.5-flash",
    instruction="Write clear, engaging content based on research.",
)

# Coordinator agent
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.5-flash",
    instruction="Delegate tasks to researcher and writer agents.",
    sub_agents=[researcher, writer]
)
```

### Custom Tool Creation

```python
from google.adk.tools import Tool

def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b

# Convert function to tool
sum_tool = Tool.from_function(calculate_sum)

agent = LlmAgent(
    name="calculator",
    model="gemini-2.5-flash",
    tools=[sum_tool]
)
```

### Sequential Workflow

```python
from google.adk.agents import SequentialAgent

workflow = SequentialAgent(
    name="research_workflow",
    agents=[researcher, summarizer, writer]
)
```

### Parallel Workflow

```python
from google.adk.agents import ParallelAgent

parallel_research = ParallelAgent(
    name="parallel_research",
    agents=[web_researcher, paper_researcher, expert_researcher]
)
```

### Human-in-the-Loop

```python
from google.adk.tools import google_search

# Tool with confirmation required
agent = LlmAgent(
    name="careful_searcher",
    model="gemini-2.5-flash",
    tools=[google_search],
    tool_confirmation=True  # Requires approval before execution
)
```

## Deployment Options

### Cloud Run Deployment

```bash
# Containerize agent
docker build -t my-agent .

# Deploy to Cloud Run
gcloud run deploy my-agent --image my-agent
```

### Vertex AI Agent Engine

```python
# Deploy to Vertex AI for scalable agent hosting
# Integrates with Google Cloud's managed infrastructure
```

### Custom Infrastructure

```python
# Run agents locally or on custom servers
# Full control over deployment environment
```

## Model Support

**Optimized for Gemini**:
- gemini-2.5-flash
- gemini-2.5-pro
- gemini-1.5-flash
- gemini-1.5-pro

**Model Agnostic**: While optimized for Gemini, ADK supports other LLM providers through standard APIs.

## Best Practices

1. **Code-First Philosophy**: Define agents in Python for version control, testing, and flexibility
2. **Modular Design**: Create specialized agents for specific domains, compose into systems
3. **Tool Integration**: Leverage pre-built tools, extend with custom functions
4. **Evaluation**: Test agents systematically against test cases
5. **Safety**: Implement confirmation flows for sensitive operations
6. **Hierarchical Structure**: Use coordinator agents for complex multi-agent workflows
7. **Workflow Selection**: Choose workflow agents for predictable pipelines, LLM agents for dynamic routing

## Common Use Cases

- **Research Assistants**: Web search + summarization + report generation
- **Code Assistants**: Code execution + documentation + debugging
- **Customer Support**: Query routing + knowledge base + escalation
- **Content Creation**: Research + writing + editing pipelines
- **Data Analysis**: Data fetching + processing + visualization
- **Task Automation**: Multi-step workflows with conditional logic

## Development UI

ADK includes built-in interface for:
- Testing agent behavior interactively
- Debugging tool calls and responses
- Evaluating agent performance
- Iterating on agent design

## Resources

- GitHub: https://github.com/google/adk-python
- Documentation: https://google.github.io/adk-docs/
- llms.txt: https://raw.githubusercontent.com/google/adk-python/refs/heads/main/llms.txt

## Implementation Workflow

When implementing ADK-based agents:

1. **Define Requirements**: Identify agent capabilities and tools needed
2. **Choose Architecture**: Single agent, multi-agent, or workflow-based
3. **Select Tools**: Pre-built, custom functions, or OpenAPI integrations
4. **Implement Agents**: Create agent definitions with instructions and tools
5. **Test Locally**: Use development UI for iteration
6. **Add Evaluation**: Create test cases for systematic validation
7. **Deploy**: Choose Cloud Run, Vertex AI, or custom infrastructure
8. **Monitor**: Track agent performance and iterate

Remember: ADK treats agent development like traditional software engineering - use version control, write tests, and follow engineering best practices.