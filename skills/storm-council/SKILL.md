---
name: storm-council
description: "Run any complex question, idea, or design decision through a dynamic council of AI domain experts based on the STORM methodology. The council dynamically generates personas relevant to your specific topic, allows them to research independently, peer-review each other, and synthesizes a final verdict. MANDATORY TRIGGERS: 'storm council this', 'run the storm council', 'deep research this proposal', 'pressure-test this architecture'. STRONG TRIGGERS: 'what are the blind spots of this design', 'evaluate this from multiple angles', 'get expert perspectives on this'. Do NOT trigger on simple factual lookups or basic coding tasks. DO trigger when the user presents a complex decision with stakes, multiple options, or requires deep, multi-faceted analysis."
---

# STORM Council (Agent-Native Referee Protocol)

This skill utilizes a dynamic agentic council inspired by the Stanford OVAL STORM methodology. It relies heavily on your native `invoke_subagent` tool.

**Crucial Constraint:** You must use the `storm_referee.py` script to manage the state of the council. The script will tell you exactly what to do at each phase. You CANNOT advance until the script permits it. Furthermore, you must strictly obey any `MANDATORY TOOL CONSTRAINT` printed by the script; if it forbids certain tools, do not use them.

## Execution

1. **Initialization:** Run the script to start the council.
   ```bash
   cd /home/rcrede/.gemini/config/skills/storm-council/scripts
   pixi run python storm_referee.py init "<the user's raw proposal>" --num_experts 5
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY HALT` instructions. **Follow them exactly**.
3. **Yielding:** When you see a `MANDATORY HALT`, you must STOP calling tools and allow execution to yield so that your subagents can reply.
4. **Submitting:** As subagents reply in your context window, submit their responses via the command line:
   ```bash
   pixi run python storm_referee.py submit_expert --persona "X" --response "..."
   ```
5. **Advancing:** When all experts are submitted, run:
   ```bash
   pixi run python storm_referee.py advance_to_review
   ```
6. **Synthesis:** At the final phase, run `get_synthesis_payload` and write the final verdict in Markdown. You do not need to wait for further review.
