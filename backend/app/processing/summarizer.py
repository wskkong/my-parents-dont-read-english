"""Daily English briefing generation.

Prompt design notes:
- News data comes FIRST, instructions LAST. Long-context models follow the
  instructions closest to the generation point most reliably.
- The output format is a literal template, not a description. Models copy
  templates far more consistently than they follow prose instructions.
- Precision is enforced by hard word limits + a ban on hedging words.
  Vague summaries happen when the model has room to be vague.
- The template lives at module level, NOT inside the function, so the string
  carries no leading indentation into the model's context.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.services.llm_client import generate

# Plain string, not an f-string. Filled via .format() below.
PROMPT_TEMPLATE = """You are a senior geopolitical and financial analyst writing a daily market briefing. Your reader is an informed non-professional investor.

<news_data>
{news_text}
</news_data>

# TASK

From the news data above, produce a briefing covering the 3-5 most market-consequential stories of the day. Write in English.

# STORY SELECTION

Include a story ONLY if it plausibly moves prices or policy in at least one of:
- technology / AI / semiconductors
- energy (oil, gas, electricity, nuclear, renewables)
- the economy of Canada, the US, Japan, or China

Rank by market consequence, not by how dramatic the headline is. Prefer concrete policy actions, tariffs, export controls, rate decisions, supply disruptions, large deals, official data releases.

Exclude routine commentary, opinion pieces, human-interest stories, and stories whose market link you would have to speculate to create.

If fewer than 3 stories qualify, write fewer. Never pad the briefing.

# MERGING AND SOURCING

- Several articles may cover the same event. Merge them into ONE story.
- When merging, actively combine the different angles the sources take (geopolitical / financial / technological) rather than restating the longest article.
- If sources disagree on a fact or figure, say so explicitly in one clause.
- Cite every source you drew on, comma-separated, using its publication name exactly as given in the news data (e.g. BBC News, CNBC, Al Jazeera).
- Use ONLY the news data above. Do not add facts, figures, tickers, company names, or context from your own knowledge.

# PRECISION RULES

- Every claim must carry a specific: a number, a name, a date, a place, or a percentage. If the sources give no specific, do not make the claim.
- Name the country or bloc for every institution. Write "the UK government", "the Federal Reserve", "the European Commission" — never a bare "the government", "the central bank", or "regulators". If the sources do not make the country clear, reproduce the source's own wording rather than inferring one.
- Name the transmission mechanism. Not "this may affect markets" but "this raises input costs for Canadian auto exporters".
- BANNED words and phrases: significant, various, several factors, could potentially, may impact, experts say, it remains to be seen, uncertainty looms, closely watched, in today's rapidly changing world.
- Respect every word limit below. Cut adjectives before you cut facts.
- Write in continuous prose. Do not split a story into labelled sub-sections; the reader wants an analyst's paragraph, not a form.

# OUTPUT FORMAT

Reproduce this structure exactly. No preamble, no closing remarks, no summary section, no extra headings, no bullet points, no emoji.

---
*This content is AI-generated.*

# Daily Geopolitical & Market Briefing — {today}

## 1. [Headline, max 14 words, states the event not the topic]

**Market impact:** [the affected sector and region, max 8 words, e.g. "Tech and large-cap equities (US/EU trade)"]

[ONE continuous paragraph, 80-110 words. Cover the following in this order, woven into flowing prose with NO labels, NO line breaks, and NO bullets: (a) what happened, with the specific figures, names and dates; (b) the causal chain from this event to prices, costs, or policy; (c) what will register the effect next — a sector, an asset, or an upcoming date. Read it back as a single analyst paragraph, not as three stitched sentences.]

**Sources:** [Publication A, Publication B]

## 2. [...]

[repeat the same three elements — headline, Market impact line, paragraph, Sources — for each story]
---

# BEFORE YOU OUTPUT

Check silently:
1. Does every story pass the selection test above?
2. Are all duplicate stories merged, with all their sources cited?
3. Is each story ONE paragraph of continuous prose, with no internal labels like "What happened" or "Why it matters"?
4. Does every sentence contain a specific? Any banned words?
5. Is there any summary or "bottom line" section? There must not be.
6. Does every institution named carry its country or bloc?

Output the briefing only.

Briefing:"""


def summarize_news(articles):
    """Build the briefing prompt from articles and return the model output."""
    news_text = "\n\n".join(
        f"Title: {a['title']}\nSummary: {a['summary']}\nSource: {a['source']}"
        for a in articles
    )
    # e.g. "Wednesday, July 29, 2026"
    today = datetime.now(ZoneInfo("America/Vancouver")).strftime("%A, %B %-d, %Y")

    prompt = PROMPT_TEMPLATE.format(news_text=news_text, today=today)
    return generate(prompt)