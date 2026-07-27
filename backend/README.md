# My Parents Don't Read English 📰

> A bilingual daily world & finance briefing — built so my parents, who don't read English, can still follow what's happening in the world and the markets.
>
> 一个中英双语的每日世界财经简报工具 —— 让不读英文的父母,也能了解世界大事和金融市场动态。

**🌐 Live demo: [my-parents-dont-read-english-production.up.railway.app](https://my-parents-dont-read-english-production.up.railway.app)**

---

## Why I built this / 为什么做这个

My parents don't read English, but they're still curious about what English-language publications report on geopolitical events and their impact on the financial markets. I built this simple web tool to translate, summarize, and generate a daily briefing so they can quickly grasp the most significant events of the day.

This is a simple daily briefing that draws from free news sources like BBC and CNBC. It uses AI to summarize what matters for tech / AI / energy markets, produces **two independent complete versions — English and Chinese** — and always links back to the original articles so readers can verify the facts themselves.

我的父母不读英文,但仍然好奇英文媒体如何报道地缘政治事件,以及这些事件对金融市场的影响。我做了这个简单的网页工具,用来翻译、总结并生成每日简报,让他们能快速抓住当天最重要的事件。

这是一个简单的每日简报,取材自 BBC、CNBC 等免费新闻源。它用 AI 总结出对科技 / AI / 能源市场重要的内容,生成**英文、中文两个独立完整版本**,并始终附上原文链接,让读者能自己核实事实。

---

## Features / 功能

- **Multi-source aggregation** — pulls from BBC, Al Jazeera, CNBC and more, with balanced coverage across sources
- **AI-generated bilingual briefing** — composes an English briefing first, then translates to a complete Chinese version (two independent versions, not mixed)
- **Fact vs. AI, clearly separated** — original headlines and source links are handled by code (never touched by AI, so URLs are never fabricated); AI-generated analysis is explicitly labeled 🤖
- **Automatic daily updates** — regenerates every morning at 6 AM (Vancouver time) via a scheduler
- **Clean web dashboard** — read it in the browser, toggle between English / 中文
- **Browsable archive** — all past briefings are saved and viewable in a dedicated archive page

中文:多源聚合、AI 双语简报(英文版→中文版两个独立版本)、事实与 AI 分析视觉分离(原文链接由代码处理、绝不经过 AI)、每日 06:00 自动更新、网页中英切换。

---

## Tech Stack / 技术栈

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI |
| Database | SQLite (local) / PostgreSQL (production), SQLModel ORM |
| AI | Google Gemini API |
| News ingestion | feedparser (RSS), httpx |
| Scheduling | APScheduler |
| Frontend | Jinja2 templates, marked.js (Markdown rendering) |
| Deployment | Railway |
| Tooling | uv (dependency management), Ruff |

---

## Architecture / 架构

An **API-first** design: the FastAPI backend is the single source of truth, so the same API can later serve a web frontend and a mobile app without changes.

```
Ingestion          Processing              Presentation
  news_fetcher  →   summarizer (EN)     →   FastAPI endpoints
  (multi-RSS)       translator (ZH)         Jinja2 dashboard
                    ↓
                  save to database
                    ↓
                  PostgreSQL
```

Design principles:
- **AI expresses, it doesn't provide facts** — precise data (URLs, numbers) is handled by code, not the model
- **Fail gracefully** — external services (network, AI) will fail; each layer handles failure appropriately instead of crashing
- **Config over hardcoding** — environment-adaptive (same code runs on SQLite locally and PostgreSQL in production)

---

## Running Locally / 本地运行

```bash
# 1. Install uv (dependency manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and enter
git clone https://github.com/wskkong/my-parents-dont-read-english.git
cd my-parents-dont-read-english/backend

# 3. Install dependencies
uv sync

# 4. Set up environment variables
#    Create a .env file with:
#    GEMINI_API_KEY=your_key_here
#    DATABASE_URL=sqlite:///./finance.db
#    TIMEZONE=America/Vancouver

# 5. Run
uv run uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` for the dashboard, or `/docs` for the interactive API.

To generate a briefing manually: `POST /admin/run-briefing` (via `/docs`).

---

## Roadmap / 后续规划

- [ ] Portfolio monitor — track holdings, composition, profit (multi-currency: CAD/USD/CNY)
- [ ] National & Local briefing levels (beyond International)
- [ ] Link world events to portfolio impact
- [ ] iOS app (SwiftUI, reusing the same API)

中文:持仓监控(多币种)、National/Local 层简报、新闻与持仓联动分析、iOS app。

---

## Note / 说明

This is a personal learning project, built while learning Python and full-stack development. AI-generated content in the briefing is clearly labeled; it is not financial advice.

这是一个个人学习项目,在学习 Python 和全栈开发的过程中构建。简报中 AI 生成的内容都有明确标注;不构成投资建议。