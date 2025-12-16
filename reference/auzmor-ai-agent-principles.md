# Auzmor AI Agent Design Principles

**Source**: Sonu Sam, Auzmor
**Format**: 14-slide presentation
**Extracted**: 2025-12-15
**Images**: `../research-sources/presentations/extracted/`

---

## Table of Contents

1. [Context Engineering](#1-context-engineering)
2. [The Core Problem](#2-the-core-problem)
3. [Team of Agents](#3-team-of-agents)
4. [Model Serving](#4-model-serving)
5. [Memory & Persistence](#5-memory--persistence)
6. [Trust & Observability](#6-trust--observability)
7. [LangGraph Middleware](#7-langgraph-middleware)
8. [Leveraging Small Language Models (SLMs)](#8-leveraging-small-language-models-slms)
9. [Infrastructure Strategy](#9-infrastructure-strategy)
10. [Building Resilient AI Agents (Title)](#10-building-resilient-ai-agents)
11. [What's on the Horizon](#11-whats-on-the-horizon)
12. [Human-in-the-Loop (HITL)](#12-human-in-the-loop-hitl)
13. [Tools & Capabilities](#13-tools--capabilities)
14. [Streaming & Rendering (UX)](#14-streaming--rendering-ux)

---

## 1. Context Engineering

**Subtitle**: Managing What the Model Sees

### Dynamic Instructions
- Change the system prompt based on the active node
- A "Coder" agent needs different rules and context than a "Reviewer" agent

### Managing History
- Long conversations break models and increase costs
- **Strategy**: Automatically **Summarize** old interactions to keep context short, or **Trim** the oldest messages to stay within token limits

### Just-In-Time Context
- Don't "stuff" the prompt with every possible document
- Inject specific data or schemas only when the agent **actually needs** them for the current step

**Image**: `slide-01-context-engineering.jpg`

---

## 2. The Core Problem

**Subtitle**: Why simple chains aren't enough

### Linear Chains (DAGs)
- Good for fixed inputs → outputs (e.g., RAG)

### The Limitation
- Real-world tasks require loops, error correction, and dynamic decision-making

### The Solution: LangGraph
- A library for building stateful, multi-actor applications with **cyclic graph capabilities**

**Image**: `slide-02-core-problem.jpg`

---

## 3. Team of Agents

**Subtitle**: The "Supervisor" Pattern

### Concept
- Single-purpose agents are more reliable than one "God Model"

### Architecture
- **Supervisor Node** (LLM): Acts as the router/manager
- **Worker Nodes**: Specialized tools (e.g., Coder, Researcher, Reviewer)

### Flow
```
Supervisor delegates task → Worker executes → Worker returns output to Supervisor
```
- Supervisor decides next step or finishes

**Image**: `slide-03-team-of-agents.jpg`

---

## 4. Model Serving

**Subtitle**: Flexible Infrastructure & Model Agnosticism

### Serving Options

**Cloud APIs**:
- Immediate access to frontier models (e.g., OpenAI, Anthropic, Google Vertex)
- Zero infrastructure management

**Self-Hosted**:
- Deploying open-weights models (e.g., Llama 3, Mistral) within your own VPC
- Using engines like vLLM or Ollama
- Essential for data privacy and long-term cost control

### Code-Level Abstraction

**The Goal**: Decouple application logic from specific model providers

**Configuration-Driven**:
- The codebase should NOT contain hardcoded API calls (e.g., `client.chat.completions`)
- Instead, use a unified interface where changing from GPT-4 to Claude-3.5 is a single line change in a YAML/JSON configuration file

**Benefit**: Future-proofs the application against model deprecation or price hikes without requiring code refactors

**Image**: `slide-04-model-serving.jpg`

---

## 5. Memory & Persistence

**Subtitle**: Giving Agents a "Brain"

### Short-term Memory

**Mechanism**: Checkpointers (e.g., PostgresSaver, RedisSaver)

**Function**: Saves the state at every step. Allows pausing/resuming workflows.

### Long-term Memory

**Mechanism**: Vector Databases / Knowledge Graphs

**Function**: Storing user preferences or facts across distinct conversation threads

**Image**: `slide-05-memory-persistence.jpg`

---

## 6. Trust & Observability

**Subtitle**: Building Confidence in Autonomous Systems

### The "Black Box" Problem
- Agents can take unexpected paths
- Without visibility into their internal logic, you cannot trust them in production environments

### Deep Tracing
- Visualize the full execution graph
- See every decision point, tool call, and state change in real-time
- Understand *why* an agent made a specific choice

### Langfuse (Open Source Observability)

**Integration**: A dedicated platform that plugs directly into LangGraph to capture every step of the agent's execution

**Core Capabilities**:
- Provides a unified dashboard to inspect detailed traces
- Track token usage and costs
- Monitor latency across different environments to ensure system health

**Image**: `slide-06-trust-observability.jpg`

---

## 7. LangGraph Middleware

**Subtitle**: Native Lifecycle Hooks

### What is it?
- A feature that allows you to inject logic *around* model and tool calls without cluttering your node code
- It functions like "interceptors" or "wrappers" found in web frameworks

### Key Capabilities

**Centralized Reliability**:
- Instead of implementing error handling inside every single agent node, middleware handles retries and fallbacks globally
- If a primary model fails, the system handles the switch automatically

**Safety & Compliance (PII)**:
- Acts as a security gate that can automatically scan and redact sensitive information (like PII) from inputs before they are sent to the model
- Ensures data doesn't leak

**Image**: `slide-07-langgraph-middleware.jpg`

---

## 8. Leveraging Small Language Models (SLMs)

**Subtitle**: Efficiency, Quantization, and Hardware Independence

### The "Specialist" Advantage
- SLMs trade broad world knowledge for speed
- They rival frontier models on specific tasks like classification or summarization but run much faster

### Quantization (Compression)
- Reduces model weight precision to shrink memory footprint
- Allows larger models to run on smaller hardware with minimal accuracy loss

### Hardware Implications
- Lowers the barrier to entry
- Capable models can now run on consumer laptops or cheap cloud instances
- Removes the need for massive GPU clusters

### Cons
- **Lower Reasoning**: Struggles with complex logic or ambiguity
- **Context Reliance**: Needs perfect context (RAG) to function well
- **Fragility**: Highly sensitive to prompt phrasing compared to GPT-4 class models

**Image**: `slide-08-small-language-models.jpg`

---

## 9. Infrastructure Strategy

**Subtitle**: Self-Hosted vs. Cloud (LangSmith)

| Feature | Self-Hosted (OSS) | Cloud (LangSmith) |
|---------|-------------------|-------------------|
| Deployment | Docker/K8s (Control plane required) | Managed Serverless |
| Data Privacy | Air-gapped / VPC internal | SaaS Compliance (SOC2) |
| Observability | Custom Setup (Jaeger/Langfuse) | Native Tracing & Evaluation |
| Maintenance | High (DevOps overhead) | Low (Fully Managed) |

**Image**: `slide-09-infrastructure-strategy.jpg`

---

## 10. Building Resilient AI Agents

**Type**: Title Slide

### Key Points
1. Building Resilient AI Agents is the presentation focus
2. Orchestration and reliability are key patterns
3. LangGraph facilitates infrastructure and agent control

**Author**: Sonu Sam, Auzmor

**Image**: `slide-10-building-resilient-agents.jpg`

---

## 11. What's on the Horizon

**Subtitle**: Maturing the AI Engineering Stack

### Evals
- Moving from manual inspection to programmatic scoring
- Using "Judge Models" to score outputs on metrics like Answer Relevance, Faithfulness, and Hallucination frequency

### Automated Testing (CI/CD for AI)
- Treating prompts and agent logic like code
- Implementing pipelines that run "Golden Datasets" (known inputs/outputs) to catch regressions before deployment

### Fine-Tuning
- Moving beyond prompt engineering
- Training small, specialized models on your own data to strictly adhere to complex formats, tone, or internal jargon where generic models fail

**Image**: `slide-11-whats-on-horizon.jpg`

---

## 12. Human-in-the-Loop (HITL)

**Subtitle**: Safety, Oversight, and Collaboration

### The Concept
- The agent is not fully autonomous
- It pauses at critical junctures for user input

### Mechanism

**Interruption**:
- Configure the graph to interrupt before sensitive actions (e.g., sending an email or deploying code)

**State Inspection**:
- The UI fetches the current thread state so the user can review the agent's plan

### User Actions

**Approve**: The user signals the agent to continue execution

**Edit/Feedback**: The user modifies the state (e.g., edits the email draft) or provides feedback, prompting the agent to replan

**Image**: `slide-12-human-in-the-loop.jpg`

---

## 13. Tools & Capabilities

**Subtitle**: Extending Capabilities: Custom Tools & MCP

### Custom Tools (Structured Approach)

**Definition**: Bespoke integrations with strict schemas wrapping business logic

**Implementation**: Define input schemas using Pydantic classes for structure

**Benefit**: Ensures LLM adherence to data structures and provides rigorous pre-execution validation for high reliability

### Model Context Protocol (MCP)

**The Problem**: Unscalable to maintain individual integrations for every external service

**The Solution**: A universal open standard standardizing AI model connections to data sources

**How it works**: Run an "MCP Server"; agents automatically detect and utilize exposed tools, eliminating connection boilerplate

**Image**: `slide-13-tools-capabilities.jpg`

---

## 14. Streaming & Rendering (UX)

**Subtitle**: Managing Latency and Rich Output

### Streaming Strategy

**The Problem**: LLMs are slow. Waiting for a full response hurts the user experience.

**Token Streaming**: Stream text character-by-character to reduce "Time to First Byte"

**Message Streaming**: Stream full data objects when tools return structured data (like JSON for charts)

### Rendering Markdown

**Rich Text Support**: LLMs output raw Markdown. Your UI must interpret this to render Tables, Code Blocks, and Lists properly.

**Implementation Overview**: Use a standard Markdown component (e.g., react-markdown) combined with plugins (like remark-gfm) to ensure complex formatting (like GitHub-style tables) displays correctly to the user.

**Image**: `slide-14-streaming-rendering.jpg`

---

## Key Takeaways

1. **Use LangGraph** for complex, stateful agent workflows (not simple DAGs)
2. **Supervisor Pattern** beats monolithic "God Models"
3. **Configuration-driven** model serving for flexibility
4. **Checkpoint everything** for pause/resume and debugging
5. **Observability is critical** - use Langfuse or LangSmith
6. **Middleware** handles cross-cutting concerns (retries, PII)
7. **SLMs** are fast but need perfect context
8. **HITL** for safety on sensitive actions
9. **MCP Protocol** for scalable tool integrations
10. **Stream everything** for better UX

---

## Cross-References

- For Google Cloud implementation: See `youtube-agent-factory.md`
- For architecture diagrams: See `architecture-diagrams.md`
- For consolidated context: See `context-summary.md`
