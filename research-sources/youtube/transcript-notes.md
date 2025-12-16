here is the tranacript - for the youtube - https://www.youtube.com/watch?v=XCGbDx7aSks&t=579s

That's a great demo walkthrough! This is from "The Agent Factory" podcast featuring Vlad Klesnikov and Remy Gustambski (Google Cloud Developer Advocate).
Key takeaways from the transcript:
Anti-gravity (Firebase Studio/Project IDX):

AI-powered IDE with asynchronous agents that do planning and coding in the background
Creates implementation plans you can review and comment on before execution
Has a browser extension for automated UI testing
Three review policies: "request review" (default), "agent decides," and "always proceed" (sandbox only)
Uses Gemini 3 Pro as the underlying model

Nano Banana Pro (Gemini 3 Pro Image Generation):

Reasoning capabilities built-in
Can use Google Search to find information for image generation
Generates 2K/4K resolution images natively
Excellent text rendering in images (a major improvement over previous models)
Can create infographics from blog posts by understanding and extracting key information

What they built:
A slides agent that generates presentation decks using:

Google Cloud Agent Starter Pack (provides boilerplate + Terraform for deployment)
MCP server for image generation/storage
ADK (Agent Development Kit)

Interesting workflow insights:

Used planning mode to iterate on the implementation plan before coding
Could comment on the plan like a collaborative document
Anti-gravity automatically tested the agent using its browser extension
The agent noticed the slides didn't include image links and wanted to investigate/fix it

