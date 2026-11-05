import os
import json
import time
import uuid
import sqlite3
import hashlib
import secrets
from datetime import datetime, timezone
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles  # <-- FIXED: Added missing import
from pydantic import BaseModel, Field
import uvicorn

# =====================================================================
# CONFIGURATION & ENVIRONMENT VARIABLES
# =====================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
CALENDAR_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
NEWS_RSS_URL = "https://www.fxstreet.com/rss/news"
DB_PATH = "mvp.db"

app = FastAPI(title="MT4 AI Analyst - Local MVP Server")

# Serve files inside the 'static' folder under the URL path '/download'
app.mount("/download", StaticFiles(directory="static"), name="download")

# Simple in-memory cache for calendar & news
CACHE = {
    "cal_data": "",
    "cal_time": 0,
    "news_data": "",
    "news_time": 0,
}


# =====================================================================
# DATABASE SETUP (SQLite local equivalent of Postgres schema)
# =====================================================================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS plans (
            name TEXT PRIMARY KEY,
            price_usd INTEGER,
            daily_quota INTEGER,
            max_accounts INTEGER,
            live_search INTEGER
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            session_token TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS licenses (
            key TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            plan TEXT NOT NULL,
            status TEXT NOT NULL, -- 'active', 'past_due', 'canceled'
            expiry TEXT,
            max_accounts INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(plan) REFERENCES plans(name)
        );

        CREATE TABLE IF NOT EXISTS bound_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT NOT NULL,
            broker_server TEXT NOT NULL,
            account_number INTEGER NOT NULL,
            bound_at TEXT NOT NULL,
            UNIQUE(license_key, broker_server, account_number)
        );

        CREATE TABLE IF NOT EXISTS usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            day_utc TEXT NOT NULL,
            symbol TEXT,
            model_used TEXT,
            tokens_est INTEGER,
            cost_usd REAL,
            status TEXT
        );
    """)

    cur.execute("SELECT COUNT(*) FROM plans")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO plans (name, price_usd, daily_quota, max_accounts, live_search) VALUES (?, ?, ?, ?, ?)",
            [
                ("Free Trial", 0, 5, 1, 0),
                ("Pro Trader", 29, 25, 2, 1),
                ("Institutional", 79, 100, 5, 1),
            ],
        )

    cur.execute("SELECT COUNT(*) FROM users WHERE email = 'demo@trader.local'")
    if cur.fetchone()[0] == 0:
        pw_hash = hashlib.sha256(b"password123").hexdigest()
        now = datetime.now(timezone.utc).isoformat()
        cur.execute(
            "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
            ("demo@trader.local", pw_hash, now),
        )
        uid = cur.lastrowid
        cur.execute(
            "INSERT INTO licenses (key, user_id, plan, status, expiry, max_accounts) VALUES (?, ?, ?, ?, ?, ?)",
            ("EJT-DEMO-1234-5678", uid, "Pro Trader", "active", "2027-12-31", 2),
        )

    conn.commit()
    conn.close()


init_db()


# =====================================================================
# HELPER FUNCTIONS: AUTH, CALENDAR, NEWS & GEMINI
# =====================================================================
def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_current_user(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        return None
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE session_token = ?", (token,)
    ).fetchone()
    conn.close()
    return user


async def fetch_calendar(symbol: str) -> tuple[str, bool]:
    now = time.time()
    if CACHE["cal_data"] and (now - CACHE["cal_time"] < 1800):
        raw = CACHE["cal_data"]
    else:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                r = await client.get(
                    CALENDAR_URL, headers={"User-Agent": "Mozilla/5.0"}
                )
                if r.status_code == 200:
                    CACHE["cal_data"] = r.text
                    CACHE["cal_time"] = now
                    raw = r.text
                else:
                    return f"UNAVAILABLE (HTTP {r.status_code})", False
        except Exception as e:
            if CACHE["cal_data"]:
                raw = CACHE["cal_data"]
            else:
                return f"UNAVAILABLE ({str(e)})", False

    c1, c2 = symbol[:3].upper(), symbol[3:6].upper()
    try:
        events = json.loads(raw)
        filtered = [
            ev
            for ev in events
            if ev.get("impact") not in ("Low", "Holiday")
            and ev.get("country") in (c1, c2, "USD")
        ][:80]
        return json.dumps(filtered), True
    except Exception:
        return raw[:15000], True


async def fetch_news() -> str:
    now = time.time()
    if CACHE["news_data"] and (now - CACHE["news_time"] < 900):
        return CACHE["news_data"]
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(NEWS_RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                CACHE["news_data"] = r.text[:6000]
                CACHE["news_time"] = now
                return CACHE["news_data"]
    except Exception:
        pass
    return CACHE["news_data"] or "UNAVAILABLE"


def build_prompt(symbol: str, timeframe: str, tech: str, cal: str, news: str) -> str:
    now_gmt = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M")
    p = (
        f"You are an elite institutional market analyst for intraday trading on {symbol} "
        f"(chart timeframe {timeframe}). Now: {now_gmt} GMT.\n\n"
    )
    if "JPY" in symbol.upper():
        p += (
            "JPY BLIND SPOTS (check each; they move price with no calendar entry):\n"
            "1) BOJ hike narrative: hawkish remarks from Ueda, Himino or Takata move JPY 50-150 pips.\n"
            "2) MOF intervention risk: USD/JPY above 158-160, EUR/JPY above 185-188, 'closely watching' language.\n"
            "3) Oil shock: Japan imports 90%+ of its energy; WTI above 85 is a headwind, above 90 critical.\n"
            "4) Carry-trade unwind: Nikkei down over 1%, VIX spike, S&P futures down.\n"
            "5) Geopolitical risk-off.\n"
            "6) JGB yields rising or US 10Y above 4.75%.\n\n"
        )
    else:
        p += (
            "Identify the currencies or drivers behind this instrument and check off-calendar risks: "
            "central bank remarks, intervention talk, commodity moves (oil, gold), equity and VIX risk sentiment, "
            "bond yields, geopolitics.\n\n"
        )

    p += (
        "TASK: combine the chart data, the economic calendar and the news into one trading view.\n"
        "- Trust the chart numbers. Never invent price levels; entry, stop and targets must be consistent with the chart data and the ATR.\n"
        "- CONFIDENCE: HIGH only if the fundamental beat/miss is clear, technicals align and blind spots are confirmed inactive. "
        "MEDIUM is the default when something is unclear. LOW when several risks are active, or when calendar or news data are UNAVAILABLE.\n"
        "- If no good trade exists, signal NEUTRAL and set the price fields to 0.\n\n"
        f"=== CHART DATA (from the trader's MetaTrader 4 terminal) ===\n{tech}\n"
        f"=== ECONOMIC CALENDAR (raw JSON, ForexFactory/FairEconomy, this week) ===\n{cal}\n\n"
        f"=== NEWS FEED (raw RSS, may be empty) ===\n{news}\n\n"
        "Reply with ONLY one JSON object, no markdown, in this schema (prices as plain numbers, 0 if none):\n"
        '{"signal":"STRONG BUY|BUY|NEUTRAL|SELL|STRONG SELL","headline":"max 10 words","confidence":"HIGH|MEDIUM|LOW",'
        '"sentiment_environment":"RISK-ON|RISK-OFF|MIXED|UNCLEAR","fundamental_bias":"max 25 words","technical_view":"max 25 words",'
        '"key_events":"max 30 words: the events and news that matter now","hidden_risks":"max 25 words, or NONE DETECTED",'
        '"entry":0,"stop":0,"tp1":0,"tp2":0,"invalidation_price":0,"action":"max 25 words",'
        '"risk_warnings":["max 14 words","max 14 words"]}'
    )
    return p


def validate_levels(result: dict, bid: float, atr: float) -> dict:
    sig = str(result.get("signal", "NEUTRAL")).upper()
    direction = 1 if "BUY" in sig else (-1 if "SELL" in sig else 0)
    if direction == 0:
        return result

    e = float(result.get("entry") or 0)
    s = float(result.get("stop") or 0)
    t1 = float(result.get("tp1") or 0)
    t2 = float(result.get("tp2") or 0)

    valid = True
    if e <= 0 or s <= 0 or t1 <= 0:
        valid = False
    elif atr > 0 and (abs(e - bid) > 6 * atr or abs(e - s) > 8 * atr):
        valid = False
    elif direction > 0 and not (s < e < t1):
        valid = False
    elif direction < 0 and not (s > e > t1):
        valid = False
    return result


async def call_gemini_or_mock(
    prompt: str, symbol: str, bid: float, atr: float, digits: int, use_search: bool
) -> tuple[dict, str, bool]:
    if not GEMINI_API_KEY:
        step = atr if atr > 0 else (0.0020 if digits >= 4 else 0.20)
        entry = round(bid, digits)
        stop = round(bid - 1.5 * step, digits)
        tp1 = round(bid + 2.0 * step, digits)
        tp2 = round(bid + 3.5 * step, digits)
        inval = round(bid - 2.0 * step, digits)
        return (
            {
                "signal": "BUY",
                "headline": f"[LOCAL MOCK AI] Bullish momentum setup on {symbol}",
                "confidence": "MEDIUM",
                "sentiment_environment": "RISK-ON",
                "fundamental_bias": "Server verified license & fetched calendar. Set GEMINI_API_KEY env var for live AI.",
                "technical_view": f"Price holding near {entry} with ATR {round(step, digits)} supporting upside continuation.",
                "key_events": "Upcoming USD and macro releases filtered by local FastAPI server.",
                "hidden_risks": "NONE DETECTED (Mock Mode Active)",
                "entry": entry,
                "stop": stop,
                "tp1": tp1,
                "tp2": tp2,
                "invalidation_price": inval,
                "action": f"Consider long near {entry} targeting {tp1} with stop at {stop}.",
                "risk_warnings": [
                    "Local Mock Mode active - set GEMINI_API_KEY for live Gemini calls",
                    "Watch spread widening around tier-1 economic releases",
                ],
            },
            "mock-gemini-local",
            False,
        )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3},
    }
    if use_search:
        payload["tools"] = [{"google_search": {}}]
    else:
        payload["generationConfig"]["responseMimeType"] = "application/json"

    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}

    async with httpx.AsyncClient(timeout=90.0) as client:
        r = await client.post(url, headers=headers, json=payload)
        if r.status_code != 200 and use_search:
            payload.pop("tools", None)
            payload["generationConfig"]["responseMimeType"] = "application/json"
            use_search = False
            r = await client.post(url, headers=headers, json=payload)

        if r.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Upstream AI error HTTP {r.status_code}: {r.text[:200]}",
            )

        data = r.json()
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
        a, b = text.find("{"), text.rfind("}")
        if a < 0 or b < a:
            raise HTTPException(
                status_code=502, detail="Malformed JSON from upstream AI model"
            )
        parsed = json.loads(text[a : b + 1])
        return validate_levels(parsed, bid, atr), GEMINI_MODEL, use_search


# =====================================================================
# API ENDPOINT FOR THE THIN MT4 EA (POST /analyze)
# =====================================================================
class AnalyzeRequest(BaseModel):
    license_key: str = Field(..., min_length=5, max_length=64)
    account_number: int
    broker_server: str = Field(..., max_length=128)
    symbol: str = Field(..., max_length=32)
    timeframe: str = Field(..., max_length=16)
    bid: float
    ask: float
    atr: float
    digits: int = 5
    tech_summary: str = Field(..., max_length=15000)


@app.post("/analyze")
async def analyze_endpoint(req: AnalyzeRequest):
    conn = get_db()
    cur = conn.cursor()

    row = cur.execute(
        """
        SELECT l.key, l.plan, l.status, l.expiry, l.max_accounts,
               p.daily_quota, p.live_search
        FROM licenses l
        JOIN plans p ON l.plan = p.name
        WHERE l.key = ?
    """,
        (req.license_key.strip(),),
    ).fetchone()

    if not row:
        conn.close()
        raise HTTPException(
            status_code=403,
            detail="Invalid License Key.",
        )

    if row["status"] != "active":
        conn.close()
        raise HTTPException(
            status_code=403,
            detail=f"License is {row['status'].upper()}.",
        )

    bound = cur.execute(
        "SELECT * FROM bound_accounts WHERE license_key = ?", (req.license_key.strip(),)
    ).fetchall()

    is_bound = any(
        b["account_number"] == req.account_number
        and b["broker_server"] == req.broker_server
        for b in bound
    )

    if not is_bound:
        if len(bound) >= row["max_accounts"]:
            conn.close()
            raise HTTPException(
                status_code=403,
                detail=f"Account limit reached ({row['max_accounts']} max accounts for {row['plan']}).",
            )
        cur.execute(
            "INSERT INTO bound_accounts (license_key, broker_server, account_number, bound_at) VALUES (?, ?, ?, ?)",
            (
                req.license_key.strip(),
                req.broker_server,
                req.account_number,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()

    today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    used_today = cur.execute(
        "SELECT COUNT(*) FROM usage WHERE license_key = ? AND day_utc = ? AND status = 'ok'",
        (req.license_key.strip(), today_utc),
    ).fetchone()[0]

    if used_today >= row["daily_quota"]:
        conn.close()
        raise HTTPException(
            status_code=429,
            detail=f"Daily quota reached ({used_today}/{row['daily_quota']} analyses used today).",
        )

    conn.close()

    cal_str, cal_ok = await fetch_calendar(req.symbol)
    news_str = await fetch_news()

    prompt = build_prompt(
        req.symbol, req.timeframe, req.tech_summary, cal_str, news_str
    )
    result, model_used, grounded = await call_gemini_or_mock(
        prompt, req.symbol, req.bid, req.atr, req.digits, bool(row["live_search"])
    )

    conn = get_db()
    tokens_est = len(prompt) // 4 + 250
    cost_est = (
        0.0 if model_used.startswith("mock") else round(tokens_est * 0.0000015, 5)
    )
    conn.execute(
        "INSERT INTO usage (license_key, timestamp, day_utc, symbol, model_used, tokens_est, cost_usd, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            req.license_key.strip(),
            datetime.now(timezone.utc).isoformat(),
            today_utc,
            req.symbol,
            model_used,
            tokens_est,
            cost_est,
            "ok",
        ),
    )
    conn.commit()
    conn.close()

    result["cal_ok"] = "true" if cal_ok else "false"
    result["grounded"] = "true" if grounded else "false"
    result["quota_info"] = f"{used_today + 1}/{row['daily_quota']}"
    return JSONResponse(content=result)


# =====================================================================
# WEB PORTAL: LANDING PAGE, AUTH, DASHBOARD & STRIPE SIMULATOR
# =====================================================================
BASE_CSS = """
<style>
  :root { --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9; --accent: #1f6feb; --green: #238636; --red: #da3633; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; background: var(--bg); color: var(--text); margin: 0; padding: 0; }
  .nav { display: flex; justify-content: space-between; align-items: center; padding: 16px 32px; border-bottom: 1px solid var(--border); background: var(--card); }
  .container { max-width: 980px; margin: 32px auto; padding: 0 20px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 24px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 24px; }
  h1, h2, h3 { color: #fff; margin-top: 0; }
  .btn { display: inline-block; background: var(--accent); color: #fff; padding: 10px 18px; border-radius: 6px; text-decoration: none; border: none; cursor: pointer; font-weight: 600; font-size: 14px; }
  .btn-green { background: var(--green); }
  .btn-red { background: var(--red); }
  .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
  input, select { width: 100%; padding: 10px; margin: 8px 0 16px; background: var(--bg); border: 1px solid var(--border); color: #fff; border-radius: 6px; box-sizing: border-box; }
  .key-box { background: #010409; border: 1px dashed var(--accent); padding: 14px; font-size: 18px; font-weight: bold; color: #58a6ff; border-radius: 6px; letter-spacing: 1px; margin: 12px 0; }
  .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
  .badge-active { background: rgba(35,134,54,0.2); color: #3fb950; border: 1px solid #238636; }
  .badge-canceled { background: rgba(218,54,51,0.2); color: #f85149; border: 1px solid #da3633; }
  table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }
  th, td { border-bottom: 1px solid var(--border); padding: 10px; text-align: left; }
</style>
"""


@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    user = get_current_user(request)
    conn = get_db()
    plans = conn.execute("SELECT * FROM plans").fetchall()
    conn.close()

    plan_cards = ""
    for p in plans:
        plan_cards += f"""
        <div class="card">
            <h3>{p['name']}</h3>
            <h1 style="font-size:36px;">${p['price_usd']}<span style="font-size:16px;color:#8b949e;">/mo</span></h1>
            <p>✓ <b>{p['daily_quota']}</b> AI chart analyses / day</p>
            <p>✓ Up to <b>{p['max_accounts']}</b> MT4 accounts bound</p>
            <p>✓ Live Google Search Grounding: <b>{'Yes' if p['live_search'] else 'No'}</b></p>
            <a class="btn" href="/dashboard">Choose {p['name']}</a>
        </div>
        """

    dashboard_link = (
        f'<a class="btn" href="/dashboard">Go to Dashboard ({user["email"]})</a>'
        if user
        else '<a class="btn" href="/login">Login / Sign Up</a>'
    )

    return f"""
    <html><head><title>EJT AI Market Analyst - Local MVP</title>{BASE_CSS}</head>
    <body>
      <div class="nav">
        <div><strong style="color:#fff;font-size:18px;">📊 EJT AI Analyst (Local MVP)</strong></div>
        <div>{dashboard_link}</div>
      </div>
      <div class="container">
        <div class="card" style="text-align:center; padding: 40px 24px;">
          <h1>One-Click Institutional AI Analysis Inside MetaTrader 4</h1>
          <p style="font-size:18px; color:#8b949e; max-width:700px; margin: 12px auto 24px;">
            Reads your live MT4 chart, filters high-impact economic calendar events and breaking news on our server, and draws validated Entry, Stop, and Target levels directly on your chart.
          </p>
          <div style="background:#010409; display:inline-block; padding:12px 20px; border-radius:6px; border:1px solid var(--border);">
            🚀 <strong>Pre-Loaded Demo Key for Instant Testing:</strong> <code style="color:#58a6ff;">EJT-DEMO-1234-5678</code>
          </div>
          <div style="margin-top: 24px;">
            <a class="btn btn-green" href="/download/AI_Analyst_Thin_MT4.ex4" download>📥 Download MT4 Expert Advisor (.ex4)</a>
          </div>
        </div>

        <h2 style="margin-top:40px; text-align:center;">Simple, Transparent Pricing</h2>
        <div class="grid">{plan_cards}</div>

        <div class="card" style="margin-top:32px; font-size:13px; color:#8b949e;">
          <strong>Risk Notice:</strong> This software provides automated market commentary and technical/fundamental summaries only. The EA contains no order execution functions and never trades on your behalf. Not financial advice.
        </div>
      </div>
    </body></html>
    """


@app.get("/login", response_class=HTMLResponse)
def login_page(error: str = ""):
    err_html = f'<p style="color:#f85149;">{error}</p>' if error else ""
    return f"""
    <html><head><title>Login / Sign Up - EJT AI Analyst</title>{BASE_CSS}</head>
    <body>
      <div class="nav"><a href="/" style="color:#fff;text-decoration:none;">← Back to Home</a></div>
      <div class="container" style="max-width:460px;">
        <div class="card">
          <h2>Sign In or Create Account</h2>
          <p style="font-size:13px;color:#8b949e;">Demo account: <code>demo@trader.local</code> / <code>password123</code></p>
          {err_html}
          <form method="POST" action="/auth">
            <label>Email Address</label>
            <input type="email" name="email" required placeholder="trader@example.com" value="demo@trader.local">
            <label>Password</label>
            <input type="password" name="password" required value="password123">
            <label>Action</label>
            <select name="mode">
              <option value="login">Login to Existing Account</option>
              <option value="signup">Create New Account (Starts on Free Trial)</option>
            </select>
            <button type="submit" class="btn" style="width:100%;">Continue →</button>
          </form>
        </div>
      </div>
    </body></html>
    """


@app.post("/auth")
def auth_action(
    email: str = Form(...), password: str = Form(...), mode: str = Form(...)
):
    conn = get_db()
    cur = conn.cursor()
    email = email.strip().lower()
    pw_hash = hash_pw(password)
    token = secrets.token_hex(24)

    if mode == "signup":
        existing = cur.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            conn.close()
            return RedirectResponse(
                "/login?error=Email+already+registered.+Please+login.", status_code=303
            )
        now = datetime.now(timezone.utc).isoformat()
        cur.execute(
            "INSERT INTO users (email, password_hash, session_token, created_at) VALUES (?, ?, ?, ?)",
            (email, pw_hash, token, now),
        )
        uid = cur.lastrowid
        lic_key = "EJT-" + "-".join(secrets.token_hex(2).upper() for _ in range(3))
        cur.execute(
            "INSERT INTO licenses (key, user_id, plan, status, expiry, max_accounts) VALUES (?, ?, ?, ?, ?, ?)",
            (lic_key, uid, "Free Trial", "active", "2027-12-31", 1),
        )
        conn.commit()
    else:
        user = cur.execute(
            "SELECT * FROM users WHERE email = ? AND password_hash = ?",
            (email, pw_hash),
        ).fetchone()
        if not user:
            conn.close()
            return RedirectResponse(
                "/login?error=Invalid+email+or+password", status_code=303
            )
        cur.execute(
            "UPDATE users SET session_token = ? WHERE id = ?", (token, user["id"])
        )
        conn.commit()

    conn.close()
    resp = RedirectResponse("/dashboard", status_code=303)
    resp.set_cookie("session_token", token, httponly=True)
    return resp


@app.get("/logout")
def logout():
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie("session_token")
    return resp


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    conn = get_db()
    lic = cur_lic = conn.execute(
        """
        SELECT l.*, p.daily_quota, p.price_usd
        FROM licenses l
        JOIN plans p ON l.plan = p.name
        WHERE l.user_id = ?
    """,
        (user["id"],),
    ).fetchone()

    today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    used_today = conn.execute(
        "SELECT COUNT(*) FROM usage WHERE license_key = ? AND day_utc = ? AND status = 'ok'",
        (lic["key"], today_utc),
    ).fetchone()[0]

    accounts = conn.execute(
        "SELECT * FROM bound_accounts WHERE license_key = ?", (lic["key"],)
    ).fetchall()
    logs = conn.execute(
        "SELECT * FROM usage WHERE license_key = ? ORDER BY id DESC LIMIT 10",
        (lic["key"],),
    ).fetchall()
    conn.close()

    status_badge = (
        f'<span class="badge badge-active">ACTIVE</span>'
        if lic["status"] == "active"
        else f'<span class="badge badge-canceled">{lic["status"].upper()}</span>'
    )

    acc_rows = (
        "".join(
            f"<tr><td>{a['account_number']}</td><td>{a['broker_server']}</td><td>{a['bound_at'][:19]}</td></tr>"
            for a in accounts
        )
        or "<tr><td colspan='3' style='color:#8b949e;'>No MT4 accounts bound yet. Run the EA once in MT4 to auto-bind!</td></tr>"
    )

    log_rows = (
        "".join(
            f"<tr><td>{l['timestamp'][:19]}</td><td>{l['symbol']}</td><td>{l['model_used']}</td><td>~{l['tokens_est']}</td><td>${l['cost_usd']:.5f}</td></tr>"
            for l in logs
        )
        or "<tr><td colspan='5' style='color:#8b949e;'>No analyses run yet.</td></tr>"
    )

    return f"""
    <html><head><title>Subscriber Dashboard - EJT AI</title>{BASE_CSS}</head>
    <body>
      <div class="nav">
        <div><strong>📊 Subscriber Dashboard</strong> ({user['email']})</div>
        <div><a class="btn btn-outline" href="/logout">Log Out</a></div>
      </div>
      <div class="container">
        <div class="grid">
          <div class="card">
            <h3>Your MT4 License Key</h3>
            <div class="key-box">{lic['key']}</div>
            <p>Status: {status_badge} &nbsp;|&nbsp; Plan: <strong>{lic['plan']} (${lic['price_usd']}/mo)</strong></p>
            <p>Daily Quota Used Today ({today_utc} UTC): <strong>{used_today} / {lic['daily_quota']}</strong></p>
            <p style="font-size:13px; color:#8b949e;">
              Paste this key into your MT4 Expert Advisor inputs along with Server URL <code>http://127.0.0.1/analyze</code>.
            </p>
          </div>

          <div class="card">
            <h3>💳 Local Stripe Checkout & Webhook Simulator</h3>
            <p style="font-size:13px; color:#8b949e;">Test plan upgrades, failed cards, and subscription cancellations immediately:</p>
            <form method="POST" action="/checkout/simulate" style="margin-top:12px;">
              <label>Select Plan or Webhook Event to Simulate:</label>
              <select name="event_type">
                <option value="upgrade_pro">✅ Stripe Checkout: Subscribe to Pro Trader ($29/mo - 25/day)</option>
                <option value="upgrade_inst">✅ Stripe Checkout: Subscribe to Institutional ($79/mo - 100/day)</option>
                <option value="payment_failed">⚠️ Stripe Webhook: invoice.payment_failed (Deactivates Key -> 403 in MT4)</option>
                <option value="sub_canceled">❌ Stripe Webhook: customer.subscription.deleted (Cancels Key -> 403 in MT4)</option>
                <option value="reset_quota">🔄 Admin Test Tool: Reset Today's Usage Counter to 0</option>
                <option value="unbind_accounts">🔓 Admin Test Tool: Unbind All MT4 Accounts</option>
              </select>
              <button type="submit" class="btn btn-green" style="width:100%;">Execute Simulation</button>
            </form>
          </div>
        </div>

        <div class="card" style="margin-top:20px;">
          <h3>📦 Download Expert Advisor</h3>
          <p style="font-size:13px; color:#8b949e;">Download the thin client EA, attach it to your MT4 chart, and paste your license key into the inputs.</p>
          <a class="btn btn-green" href="/download/AI_Analyst_Thin_MT4.ex4" download>Download AI_Analyst_Thin_MT4.ex4</a>
        </div>

        <div class="card" style="margin-top:20px;">
          <h3>Bound MT4 Accounts ({len(accounts)} / {lic['max_accounts']} allowed)</h3>
          <table>
            <thead><tr><th>MT4 Account #</th><th>Broker Server</th><th>Bound At (UTC)</th></tr></thead>
            <tbody>{acc_rows}</tbody>
          </table>
        </div>

        <div class="card" style="margin-top:20px;">
          <h3>Recent AI Usage & Cost Log</h3>
          <table>
            <thead><tr><th>Time (UTC)</th><th>Symbol</th><th>Model</th><th>Est. Tokens</th><th>Est. Cost</th></tr></thead>
            <tbody>{log_rows}</tbody>
          </table>
        </div>
      </div>
    </body></html>
    """


@app.post("/checkout/simulate")
def simulate_stripe_event(request: Request, event_type: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    conn = get_db()
    cur = conn.cursor()
    lic = cur.execute(
        "SELECT key FROM licenses WHERE user_id = ?", (user["id"],)
    ).fetchone()
    key = lic["key"]

    if event_type == "upgrade_pro":
        cur.execute(
            "UPDATE licenses SET plan = 'Pro Trader', status = 'active', max_accounts = 2 WHERE key = ?",
            (key,),
        )
    elif event_type == "upgrade_inst":
        cur.execute(
            "UPDATE licenses SET plan = 'Institutional', status = 'active', max_accounts = 5 WHERE key = ?",
            (key,),
        )
    elif event_type == "payment_failed":
        cur.execute("UPDATE licenses SET status = 'past_due' WHERE key = ?", (key,))
    elif event_type == "sub_json" or event_type == "sub_canceled":
        cur.execute("UPDATE licenses SET status = 'canceled' WHERE key = ?", (key,))
    elif event_type == "reset_quota":
        cur.execute("DELETE FROM usage WHERE license_key = ?", (key,))
    elif event_type == "unbind_accounts":
        cur.execute("DELETE FROM bound_accounts WHERE license_key = ?", (key,))

    conn.commit()
    conn.close()
    return RedirectResponse("/dashboard", status_code=303)


if __name__ == "__main__":
    print("=================================================================")
    print("🚀 EJT AI Analyst Local Server Running at: http://127.0.0.1/analyze")
    print("🔑 Pre-loaded Test License Key:            EJT-DEMO-1234-5678")
    print("=================================================================")
    uvicorn.run(app, host="127.0.0.1", port=80)
