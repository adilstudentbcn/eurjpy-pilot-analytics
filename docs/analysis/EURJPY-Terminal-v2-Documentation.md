# EUR/JPY Intelligence Terminal v2
## Complete Technical & Conceptual Documentation

---

## 1. What It Is

A self-contained, single HTML-file trading advisor built specifically for EUR/JPY on the 15-minute timeframe. You open it in any browser, upload your inputs, and get an institutional-grade analysis with trade levels, risk assessment, and a follow-up chat — all powered by Claude AI with no backend server, no database, no installation.

The entire app lives in one `.html` file: ~925 lines combining HTML structure, CSS styling, and JavaScript logic in one portable document you can save to your desktop and open anywhere.

---

## 2. Tech Stack

### Frontend
| Layer | Technology | Why |
|---|---|---|
| Structure | Vanilla HTML5 | No framework needed for a single-page tool |
| Styling | Vanilla CSS with CSS custom properties (variables) | Full control, no dependencies, dark theme via `:root` vars |
| Logic | Vanilla JavaScript (ES2020+) | `async/await`, `FileReader API`, `fetch API` — no build step |
| File reading | Browser `FileReader API` | Reads images and CSV files locally, no upload to any server |

### AI / Backend
| Component | Technology | Purpose |
|---|---|---|
| Main AI model | **Claude Sonnet 4.6** (`claude-sonnet-4-6`) | Vision + reasoning for the main trade analysis |
| News AI | **Claude Sonnet 4.6** + `web_search_20250305` tool | Live web search for off-calendar JPY risk factors |
| API endpoint | `https://api.anthropic.com/v1/messages` | Anthropic Messages API — no API key needed inside Claude.ai |
| Image format | Base64-encoded, passed as `type: "image"` content blocks | Multi-modal vision — Claude reads images directly |

### Previous version (Gemini)
The original app used `gemini-2.0-flash` via Google's API, requiring the user to manage their own Gemini API key, with rate limits on the free tier. This version uses the Anthropic API, which when run inside Claude.ai requires no key and has no free-tier throttling.

---

## 3. Architecture — How Data Flows

```
USER INPUTS
├── 1-6 Calendar screenshots (PNG/JPG)  →  base64 → Claude Vision
├── 1   Chart screenshot   (PNG/JPG)    →  base64 → Claude Vision
├── 1   CSV file           (.csv/.txt)  →  parsed locally → text stats → Claude text
├── Live News              (optional)   →  Claude web search → text → Claude text
└── Manual Context         (optional)   →  plain text → Claude text

                    ↓
        ALL assembled into one Claude API request
        (text prompt + multiple image blocks)
                    ↓
        Claude returns JSON
        tryRecoverJSON() handles any truncation
                    ↓
        renderResult() builds the UI card
                    ↓
        Chat loop uses same images + context for follow-ups
```

---

## 4. Application Modes

### 🌙 Night-Before Planning
Used the evening before a trading session. You upload:
- Tomorrow's ForexFactory calendar (no actuals yet, only forecasts)
- The current 15m chart showing the close-of-day structure

The AI identifies the most likely scenarios for tomorrow, pending order levels, and pre-session risk. Confidence is automatically biased lower because JPY blind spots cannot be confirmed pre-session.

### ⚡ Live Trading Execution
Used during the live session. You upload:
- The calendar with **released actuals** visible (beat/miss vs forecast)
- The live 15m chart showing how price is reacting right now

The AI compares the actual vs forecast, reads the chart reaction, and gives an immediate execution decision.

---

## 5. Input Modules

### 5a. Calendar — Multi-Image Upload
**The single biggest UX improvement from the original.** ForexFactory calendars are long and require scrolling. The original app only accepted one screenshot, so events at the bottom of the day were invisible to the AI.

**How it works:**
- A thumbnail strip (`.cal-drop`) replaces the single upload box
- Click empty area → file picker opens with `multiple` attribute
- Drag and drop multiple files directly onto the strip
- Each image gets a `Cal 1 / Cal 2 / Cal 3…` label thumbnail
- Individual ✕ button removes any specific screenshot
- Maximum 6 screenshots (covers even high-event days like NFP or FOMC)
- An `+ Add more` tile appears after first upload for additional images

**How images are sent to Claude:**
Each image is preceded by a text label so Claude knows the reading order:
```
[Calendar screenshot 1 of 3]
[image block]
[Calendar screenshot 2 of 3]
[image block]
[Calendar screenshot 3 of 3]
[image block]
```
The prompt explicitly tells Claude: *"treat them as one continuous calendar in order"*.

**JS implementation:** `FileReader.readAsDataURL()` converts each image to base64. Images are stored in `S.calImgs[]` as `{ mime, base64, url }` objects. `renderCalThumbs()` rebuilds the thumbnail strip on every change.

---

### 5b. Chart — Single Image Upload
One 15-minute MT4/MT5 screenshot. Stored as `S.chartImg = { mime, base64 }`. Renders as a full preview with a ✕ clear button.

---

### 5c. CSV Price Data Parser
**Why it exists:** Claude reading a chart image can only estimate price levels visually. The CSV parser converts your raw MT4/MT5 OHLCV export into exact numbers Claude can reason about precisely.

**Expected CSV format** (MT4/MT5 default export):
```
YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume
2026.09.02,09:00,185.066,185.069,184.663,184.776,6331
```

**What the parser extracts and sends to Claude:**
```
━━ CSV PRICE DATA (15M EURJPY) ━━
Total bars loaded : 847
Last bar timestamp: 2026.09.02 09:00
Current price     : 184.776
20-bar High       : 185.740  |  20-bar Low: 184.538  |  Range: 120.2 pips
Avg volume (20)   : 2650     |  Last bar vol: 6331  (238% of avg)
20-bar trend      : BEARISH (96.4 pip loss first→second half)
Last 5-bar H/L    : 185.412 / 184.663
⚠️ MAJOR VOLUME SPIKE on last candle (238% of avg) — institutional/news-driven move confirmed

Last 5 bars detail:
  [2026.09.02 07:45] Bear | O:185.393 H:185.412 L:185.261 C:185.332 | Vol:3119 (117% avg)
  [2026.09.02 08:00] Bear | O:185.331 H:185.336 L:185.235 C:185.268 | Vol:2707 (102% avg)
  [2026.09.02 08:15] Bear | O:185.267 H:185.315 L:185.189 C:185.237 | Vol:3006 (113% avg)
  [2026.09.02 08:45] Bear | O:185.209 H:185.210 L:185.068 C:185.070 | Vol:3031 (114% avg)
  [2026.09.02 09:00] Bear | O:185.066 H:185.069 L:184.663 C:184.776 | Vol:6331 (238% avg) ⚠️ VOL SPIKE
```

**Volume spike thresholds:**
- `> 180% of 20-bar average` → `△ elevated vol` flag
- `> 200% of 20-bar average` → `⚠️ VOL SPIKE` flag
- `> 300% of 20-bar average` → `⚠️ MAJOR VOLUME SPIKE — institutional/news-driven move confirmed`

**Trend detection:** Compares average close of bars 1–10 vs bars 11–20 of the last 20 candles. Reports the pip difference so Claude knows whether the recent bias is bullish or bearish and by how much.

---

### 5d. Live News Search
**The blind-spot killer.** This is the feature that directly addresses what went wrong on September 2, 2026 — Ueda's G20 hawkish remarks and the US-Iran oil spike were completely off-calendar but moved EUR/JPY 120 pips.

**How it works:**
1. You click **🔍 Fetch Live News**
2. The app calls Claude API with the `web_search_20250305` tool enabled
3. Claude searches the web for 5 specific topics (see prompt below)
4. Results appear in the purple news panel
5. You read the results — if anything concerns you, paste key points into the Manual Context box before running the main analysis

**The news search prompt sent to Claude:**
```
Today is [weekday, date]. I am about to trade EUR/JPY.
Search the web for current information on these 5 topics:

1. BOJ/Bank of Japan: Any statements TODAY from Governor Ueda,
   Deputy Himino, or board member Takata? Current BOJ rate hike
   expectations — is a hike priced in for the next meeting?

2. Japanese Yen (JPY): Current USD/JPY and EUR/JPY approximate
   levels. Any MOF (Ministry of Finance) or currency diplomat
   "intervention" warnings?

3. WTI Crude Oil: Current price? Up or down today by how much?
   Any US-Iran or Middle East news driving oil?

4. Global Risk Sentiment: Are major equity markets (Nikkei 225,
   S&P 500, DAX) up or down today? VIX level — risk-on or risk-off?

5. EUR Drivers: Any ECB news, Eurozone data, or key EUR/USD
   movement today?

Format: bold the topic title, then 2-3 bullet points each
with specific numbers.
```

**Why these 5 topics specifically:** They map exactly to the 6 JPY blind spots in the system prompt (BOJ narrative, intervention risk, oil/energy, carry trade sentiment, geopolitical). Any one of them being active can override everything on the ForexFactory calendar.

---

### 5e. Manual Context Box
Free-text field where you paste anything the AI should know that isn't captured by images or CSV. Examples:
- *"Ueda spoke at G20, signalled Sept 18 hike. WTI at $91."*
- *"COT data shows record JPY short positioning — unwind risk elevated."*
- *"Client flow desks report heavy EUR selling from Asian sovereign funds."*
- *"Nikkei down 1.8% overnight, VIX at 18.5."*

This text is appended to the API prompt under `ADDITIONAL TRADER CONTEXT`.

---

## 6. The System Prompt (Master Prompt) — Full Detail

This is the core intellectual asset of the app. The original Gemini version had ~4 lines. The new prompt is a structured intelligence brief covering everything the original missed.

### Section 1: Identity
```
You are an elite institutional EUR/JPY analyst specialising in
15-minute intraday trading. Your primary competitive edge is
detecting the off-calendar JPY risks that cause unexpected crashes
— risks completely invisible on ForexFactory.
```

### Section 2: JPY Blind Spots (the most important section)
Six specific risk factors that standard economic calendars completely miss:

**Blind Spot 1 — BOJ Rate Hike Narrative**
The BOJ entered a tightening cycle in 2024. Hawkish signals from Governor Ueda, Deputy Himino, or hawk board member Takata move JPY 50–150 pips even when not on the calendar. These appear in G7/G20 sideline press remarks, Diet parliamentary testimony, and post-meeting interviews. The prompt includes a real example: *September 2026 — Ueda's G20 remarks fully priced a Sept 18 BOJ hike → EUR/JPY crashed 120 pips in the Asia session with no calendar entry.*

**Blind Spot 2 — MOF FX Intervention Risk**
Japan's Ministry of Finance actively defends the yen. Critical zones: USD/JPY above 158–160, EUR/JPY above 185–188. Warning signs include MOF diplomat "closely watching / decisive action" language. Actual intervention = 200–400 pip EUR/JPY crash in minutes with zero calendar warning.

**Blind Spot 3 — Oil Price / Energy Shock**
Japan imports 90%+ of its energy. WTI above $85 = JPY headwind; $90+ = critical threshold. A US-Iran conflict creating an oil spike hits EUR/JPY from both sides simultaneously: USD strengthens (EUR weakens) AND risk-off triggers JPY safe-haven buying.

**Blind Spot 4 — Carry Trade Unwind Risk**
Trillions in leveraged yen carry trades (borrow cheap JPY, buy high-yield assets). Any risk-off shock can trigger a violent cascading unwind. Early warning signs: Nikkei falling >1%, VIX spiking, S&P futures down. Once unwind begins, EUR/JPY can fall 100–200 pips with no economic release. Historical reference: *July 2024 carry unwind — USD/JPY fell 20+ yen in 3 weeks after a 15bp BOJ hike.*

**Blind Spot 5 — Geopolitical Risk-Off**
US-Iran conflict, Middle East escalation, China slowdown, banking stress → JPY safe haven demand. Completely off-calendar. The prompt tells Claude: *"Ask: is there an active geopolitical conflict? If yes, carry trade unwind risk is elevated."*

**Blind Spot 6 — JGB Yield Dynamics**
Rising Japan 10Y JGB yield = BOJ tightening = JPY strengthens. Watch: US 10Y above 4.75% = global risk-off threshold.

### Section 3: Macro Synthesis Framework
```
EUR drivers: ECB rate path, Eurozone CPI/GDP, German data,
             political risk (France/Italy fiscal)
JPY drivers: BOJ tightening pace, intervention risk,
             oil sensitivity, carry positioning, JGB yields
USD data  → EUR/JPY via TWO channels:
            (1) EUR/USD direction
            (2) global risk sentiment shift
Risk-ON: Institutional carry = EUR/JPY rises.
Risk-OFF: Carry liquidation = EUR/JPY crashes.
```

### Section 4: Confidence Calibration Rules
```
HIGH:   Clear fundamental beat/miss + unambiguous technical
        alignment + ALL JPY blind spots confirmed inactive
MEDIUM: Mixed signals OR one blind spot uncertain/present
        — DEFAULT when JPY blind spot status unclear
LOW:    Multiple blind spots active, oil elevated,
        BOJ narrative building, carry unwind signs present
```
This is deliberately conservative. The default is MEDIUM, not HIGH. The AI has to actively confirm all blind spots are clear before giving HIGH confidence.

### Section 5: Technical Analysis Guidance
```
Use CSV price data when provided — exact numbers are more
reliable than visual chart estimation.
Look for: Market Structure Shifts (MSS), Order Blocks,
Liquidity Sweeps, Fair Value Gaps (FVG), volume spikes.
Volume spike context:
  2-3x average = significant institutional activity
  3x+          = news-driven institutional event confirmed
```

---

## 7. The Analysis API Call

### Request structure
```javascript
{
  model: "claude-sonnet-4-6",
  max_tokens: 1000,
  messages: [{
    role: "user",
    content: [
      { type: "text",  text: "[MASTER_PROMPT + MODE + CSV + NEWS + CONTEXT + JSON_SCHEMA]" },
      { type: "text",  text: "[Calendar screenshot 1 of N]" },
      { type: "image", source: { type: "base64", media_type: "image/png", data: "..." } },
      { type: "text",  text: "[Calendar screenshot 2 of N]" },
      { type: "image", source: { ... } },
      // ... more calendar images
      { type: "text",  text: "[15m EUR/JPY Chart]" },
      { type: "image", source: { ... } }
    ]
  }]
}
```

### JSON schema Claude must return
```json
{
  "signal":               "STRONG BUY | BUY | NEUTRAL | SELL | STRONG SELL",
  "headline":             "max 8 words",
  "confidence":           "HIGH | MEDIUM | LOW",
  "sentiment_environment":"RISK-ON | RISK-OFF | MIXED | UNCLEAR",
  "fundamental_bias":     "max 18 words — key calendar beat/miss impact only",
  "technical_view":       "max 18 words — structure, key level, volume flag only",
  "hidden_risks":         "max 20 words — named JPY risks or: NONE DETECTED",
  "entry":                "price or brief condition, max 6 words",
  "stop":                 "price only",
  "tp1":                  "price only",
  "tp2":                  "price only",
  "invalidation":         "price: reason max 6 words",
  "action":               "max 18 words",
  "risk_warnings":        ["max 12 words", "max 12 words"]
}
```

**Why strict word limits?** The Anthropic API `max_tokens: 1000` limits the response length. With verbose field instructions ("write 1-2 sentences"), Claude would produce 900+ token responses that get cut off mid-JSON. Strict word limits keep the full JSON response under ~350 tokens, leaving comfortable headroom.

---

## 8. JSON Recovery System

Even with word limits, edge cases can still cause truncation (very long news input, many CSV lines). The `tryRecoverJSON()` function handles this:

**Step 1:** Try normal `JSON.parse()`. If it works, done.

**Step 2:** Scan character-by-character to find the position of the last **complete** closing quote (accounting for escape sequences). This identifies where the last fully-formed string value ended.

**Step 3:** Truncate the raw text to that position. Remove any trailing comma.

**Step 4:** Count all unclosed `{` braces and `[` brackets in the truncated string (skipping characters inside strings to avoid false positives).

**Step 5:** Append the correct closing characters (`]]}` etc.) to seal the JSON object.

**Step 6:** Try `JSON.parse()` on the repaired string.

**Step 7:** If still fails, show the user the first 400 characters of the raw response so they can diagnose the issue themselves.

This means even a 70%-complete response can often be recovered and rendered rather than showing a useless error.

---

## 9. Result Display

The result card renders 8 distinct sections:

| Section | What it shows |
|---|---|
| **Status pills** | Mode (Planning/Live), Confidence level, Sentiment environment (colour-coded) |
| **Headline** | 8-word summary of the trade thesis |
| **Signal badge** | BUY / SELL / NEUTRAL with arrow (↑↑ / ↑ / → / ↓ / ↓↓), colour-coded green/red/yellow |
| **Fundamental** | Calendar beat/miss impact in plain language |
| **Technical** | Chart structure, key level, volume assessment |
| **🚨 Hidden JPY Risks** | Orange box — the blind-spot detector. Shows NONE DETECTED (✅) or names the specific risk (⚠️ RISKS DETECTED) |
| **Key Levels grid** | 5-cell grid: Entry / Stop Loss / TP1 / TP2 / Invalidation — each colour-coded |
| **Risk Warnings** | Orange warning tiles for specific things to watch |
| **Execution** | One sentence: exactly what to do right now |

The result card border colour matches the signal: green for BUY variants, red for SELL variants, yellow for NEUTRAL.

---

## 10. Chat System

After the analysis renders, a follow-up chat appears beneath the result card.

**How context is seeded:** The first message in the conversation is automatically set to a summary of the analysis result including signal, headline, confidence, hidden risks, and key levels. The AI's opening response acknowledges the setup and invites questions.

**How multi-turn works:** Every follow-up call to the API sends the full conversation history, with the very first message including the system prompt AND all uploaded images (calendar + chart). This means the AI can still reference the visual inputs when answering follow-up questions like *"explain why you put the stop there"* or *"what if price sweeps the low first?"*

**What you can ask:**
- *"Why that specific stop level?"*
- *"What if ADP comes in much higher than forecast?"*
- *"What's the alternative bearish scenario?"*
- *"How would you adjust if price dips to 184.80 first?"*
- *"Should I reduce size given the BOJ risk you mentioned?"*

---

## 11. Design System

All colours are defined as CSS custom properties on `:root`, making the dark theme easy to maintain:

```css
:root {
  --bg:       #0d1117   /* deepest background */
  --bg1:      #161b22   /* card background */
  --bg2:      #21262d   /* input/element background */
  --bg3:      #2d333b   /* hover states */
  --bd:       #30363d   /* borders */
  --tx:       #e6e6e6   /* primary text */
  --tx2:      #8b949e   /* secondary text */
  --tx3:      #6e7681   /* muted text / labels */
  --blue:     #58a6ff   /* primary actions, entries */
  --green:    #3fb950   /* BUY, TP levels */
  --red:      #f85149   /* SELL, stop loss */
  --yel:      #d29922   /* NEUTRAL, warnings */
  --pur:      #bc8cff   /* Claude/AI, news elements */
  --ora:      #ff8700   /* risk warnings, hidden risks */
}
```

The colour system is semantic: orange means *"this requires your attention"*, red means *"loss / stop / sell"*, purple means *"AI-powered feature"*.

---

## 12. What the Original Gemini App Was Missing

| Gap | Root cause | Fix in v2 |
|---|---|---|
| Blind BUY on Sep 2, 2026 | Prompt had no JPY macro knowledge | 6 JPY blind spots + confidence calibration rules |
| Missed Ueda G20 comments | No news layer | Live news search with web_search tool |
| Missed oil spike at $91 | No news layer, no context | Oil price is one of 5 searched topics |
| Only one calendar screenshot | Single file input | Multi-image strip with drag & drop, up to 6 images |
| Price levels guessed from image | No CSV support | CSV parser sends exact OHLCV to AI |
| JSON truncation errors | Verbose schema, no recovery | Strict word limits + tryRecoverJSON() |
| Needed Gemini API key + rate limits | Free tier constraints | Claude API, no key needed inside Claude.ai |
| No follow-up questions possible | Gemini had no persistent chat | Full multi-turn chat with image context preserved |

---

## 13. Recommended Workflow

**The night before:**
1. Open app → select **Night-Before Planning**
2. Take 2–4 ForexFactory screenshots covering the full next trading day → upload all
3. Upload your 15m chart (end of day structure)
4. Click **Fetch Live News** → read the results, especially BOJ and oil sections
5. If anything concerning appears in news, paste a summary into Manual Context
6. Upload your OHLCV CSV if you have it
7. Click **Generate Analysis**
8. Read the **Hidden JPY Risks** section first — if it's orange, treat confidence as LOW regardless of signal
9. Use chat to stress-test the scenario: *"What if ADP misses badly?"*, *"What's my invalidation?"*

**The morning of / live:**
1. Switch to **Live Trading Execution**
2. Re-upload calendar with actuals now visible
3. Upload the fresh chart showing how price reacted
4. Run **Fetch Live News** again (things change overnight)
5. Generate new analysis
6. The AI now sees actual vs forecast and the real price reaction — execution decision is much more grounded

---

## 14. File Structure Summary

```
eurjpy-v2.html  (~925 lines, single file)
│
├── <style>  (lines 1–175)
│   ├── CSS variables / reset
│   ├── Header, mode buttons, card styles
│   ├── Calendar multi-upload (thumbnail strip)
│   ├── Chart single-upload
│   ├── CSV terminal display
│   ├── News / context sections
│   ├── Result card (signal, levels, risks, warnings)
│   ├── Chat styles
│   └── Responsive breakpoints
│
├── <body>  (lines 176–273)
│   ├── Header bar
│   ├── Mode selector card (Planning / Live)
│   ├── Calendar multi-image upload
│   ├── Chart single-image upload
│   ├── CSV upload card
│   ├── Market Intelligence card (news + context)
│   ├── Generate button
│   └── Result area (dynamically populated)
│
└── <script>  (lines 274–926)
    ├── S = { ... }              State object
    ├── MASTER_PROMPT            System prompt (the brain)
    ├── parseCSV()               OHLCV parser + stats formatter
    ├── md()                     Lightweight markdown → HTML
    ├── setMode()                Planning/Live toggle
    ├── renderCalThumbs()        Calendar thumbnail strip renderer
    ├── addCalFiles()            Multi-file reader for calendar
    ├── removeCalImg()           Remove one calendar image
    ├── readChartImg()           Single chart image reader
    ├── clearCSV()               CSV reset
    ├── fetchLiveNews()          Claude API + web_search call
    ├── tryRecoverJSON()         Truncated JSON recovery
    ├── runAnalysis()            Main Claude API call
    ├── renderResult()           Result card HTML builder
    ├── getSignalClass/Arrow()   Signal display helpers
    ├── sendChat()               Follow-up chat API call
    └── Event bindings           File inputs + drag & drop
```
