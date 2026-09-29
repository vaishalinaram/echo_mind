# How Hindsight stopped my content agent from repeating rejected ideas

The first version of my content agent had a short memory and a bad habit: it kept recommending a post format we had already rejected, three weeks in a row. The analytics were right every time. The judgment was wrong every time. That gap is the whole story of this project.

I build EchoMind, an AI content strategist. It looks at a brand's publishing history and decides what to post next: which editorial pillar to feed, which format to use, and the angle to take. The hard part was never the analytics. It was getting the agent to *remember* what worked, what the brand's voice is, and what a human already shot down, so it stops relitigating settled decisions. I solved that by giving it long‑term memory with [Hindsight, an agent memory engine](https://github.com/vectorize-io/hindsight).

## What the system does and how it hangs together

EchoMind runs on two engines that answer two different questions.

A deterministic SQLite layer answers the objective question: **which pillar is under‑served right now?** That is just arithmetic over the post history: actual share versus target share, days since the last post in each pillar, engagement by format. No model needed, and no room for hallucination.

A memory layer answers the subjective question: **how do we win that pillar for this brand?** That is voice, guardrails, and every accept/edit/reject a human has ever given. This is where [Hindsight](https://hindsight.vectorize.io/) lives.

A Streamlit UI stitches them together, and a small LLM writes the final narrative. The important design decision is the split. The math decides *what* is missing; memory decides *how* to fill it. Keeping those separate meant I could trust the numbers and still let the agent get smarter over time.

## The core story: memory has to change the decision, not just the wording

My first attempt was the obvious one. I recalled some context from memory and pasted it into the prompt so the narrative sounded more on‑brand. It read better. But the *recommendation itself* never changed. The agent still proposed the rejected format; it just described it more eloquently. That is theater, not memory.

So I moved the memory influence out of the prose and into the decision. Each brand gets its own Hindsight memory bank, created with a mission and a disposition that make it reason like a skeptical strategist rather than a search index:

```python
STRATEGIST_MISSION = (
    "I am a senior content strategist. I track what content was published, what "
    "performed well, which editorial pillars are over- or under-served, and the "
    "brand's voice and guardrails. I learn from every acceptance, edit, and "
    "rejection, and I recommend the next piece of content with clear causal "
    "justification grounded in past evidence."
)
STRATEGIST_DISPOSITION = {"skepticism": 4, "literalism": 3, "empathy": 3}
```

When it is time to recommend, I recall context across Hindsight's three native memory types instead of inventing my own tagging scheme:

```python
brand_constraints = self._recall_texts(
    bank_id, "Brand voice, guardrails, audience, and taboos", ["world"], limit)
relevant_experiences = self._recall_texts(
    bank_id, f"Past recommendations, critiques, and outcomes related to: {query}",
    ["experience"], limit)
belief_texts = self._recall_texts(
    bank_id, f"Strategic patterns and learnings related to: {query}",
    ["observation"], limit)
```

Those three types map cleanly onto how a strategist actually thinks. `world` facts are the fixed rules ("never post beginner tutorials"). `experience` is the episodic history of what I recommended and how the human reacted. And `observation` is the part I did not have to build: Hindsight consolidates repeated experiences into deduplicated, evidence‑grounded beliefs on its own. I get "carousels underperform for this audience" as an emergent observation, not something I hard‑coded. If you have only ever used a vector store, [this is the difference between retrieval and memory](https://vectorize.io/what-is-agent-memory).

Then the actual decision. The deterministic engine proposes the best‑performing format. Memory gets to override it when it recalls that a human rejected that exact format:

```python
rejected = [t for t in (experiences + beliefs) if "reject" in t.lower()]
if rejected and len(formats) > 1 and baseline:
    base_name = baseline.get("format_name", "")
    if any(self._mentions_format(e, base_name) for e in rejected):
        alt = formats[1]
        plan["format"] = alt
        plan["adjusted"] = True
        plan["adjustments"].append(
            f"Past feedback rejected '{base_name}', so I switched to the next "
            f"best performer, '{alt.get('format_name')}'."
        )
```

It is deliberately boring code. The intelligence is not in the `if` statement; it is in the fact that the rejection is *there to recall at all*, weeks later, in a form the agent can act on. That is the part Hindsight makes trivial and that I would otherwise have spent the whole project building and getting wrong.

## What it looks like in practice

Here is a real before/after from the example brand's data.

The gap analysis says the "Engineering Culture & Leadership" pillar is starved: 6.7% of recent output against a 20% target, last post 26 days ago. The best‑performing format overall is a document carousel. So the memory‑blind version confidently recommends a culture carousel.

The problem: a human had already rejected a culture carousel and left a critique that the audience prefers technical teardowns over culture posts. With memory on, the agent recalls that experience, keeps the pillar (the math is not wrong about the gap), and switches the format to a technical thread. It also sets the angle from the recalled critique: lead with a concrete incident and a real timeline, not opinion. Same underlying analytics, a materially different recommendation, and a one‑line explanation of exactly which past decision changed its mind.

The feedback loop closes the circle. Every accept, edit, or reject is retained as an experience, so the *next* recommendation already knows about it. The agent's confidence visibly climbs as evidence accumulates, because there is more recalled support behind each call. Interaction one is generic. Interaction ten feels like it has been on the team for a quarter.

## Lessons learned

**Put memory in the decision, not the prompt.** The temptation is to recall some text and let the model "consider" it. That produces nicer paragraphs and identical decisions. If memory does not change a branch in your code, a metric, or a ranked choice, you have built a better narrator, not a better agent. The moment I let a recalled rejection flip the recommended format, the whole thing stopped feeling like a demo and started feeling like a colleague.

**Let the memory engine own consolidation.** I originally planned to build a "beliefs" table and write rules to promote repeated feedback into durable lessons. Hindsight's observations did that for me: it merges repeated evidence into stable, deduplicated beliefs and refines them as new evidence arrives. Deleting my half‑built belief store was the best code I removed all week.

**Model your domain onto world / experience / observation.** Trying to force everything through one bucket with clever tags was a dead end. Splitting brand rules (world), decision history (experience), and learned patterns (observation) made recall queries obvious and kept the agent from confusing a fixed guardrail with a soft preference.

**Degrade honestly.** Memory is a network dependency, and it will be down sometimes. My agent falls back to deterministic‑only analytics and *says so* in the UI. It never silently swaps to a mock or pretends to remember. Users forgive a system that admits "memory is offline"; they do not forgive one that quietly gets dumber.

**Respect the client's concurrency model.** My most annoying dead end: I parallelized the three recall calls with a thread pool to shave latency, and got `Timeout context manager should be used inside a task`. The Hindsight client wraps an async HTTP session that does not like being driven from multiple threads. I reverted to sequential calls, left a comment explaining why, and moved on. The recalls are fast enough that it never mattered.

If you are building an agent that has to make the same kind of decision more than once, the memory layer is not a nice‑to‑have; it is the difference between a stateless tool and something that compounds. I would start with [Hindsight](https://github.com/vectorize-io/hindsight) again without hesitation, and I would put memory in the decision on day one.
