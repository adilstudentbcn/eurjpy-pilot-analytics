# Your project's niche: the cheat sheet

DS403 · session 9 · *Finding a niche with data and agents*. The notebook is `session-09-niche.ipynb`, the deck
`session-09.pdf`, the files `examples/session-09/`. Every step names its notebook block: open it, change the inputs
named there, run it.

## 1. The one rule: the ledger

Every number that enters your estimate goes through `fact(name, low, high, unit, kind, source)`. No row, no number.

| Kind | Where it comes from | It may set |
|---|---|---|
| `open` | official statistics (Eurostat, INE, BLS, World Bank) | a **level**: how many, how much |
| `partial` | your own users, a waitlist, a pilot, a fake door | a **rate**, for the people it covers |
| `research` | a provider's report, a deep-research answer you checked, reviews, conversations | an input you did not observe |
| `assumption` | your guess, said out loud, with a range | nothing for long: research it next |
| `simulated` | LLM personas, agent-based journeys | a **shape** (which option ranks higher), **never a level** |

## 2. Thirteen steps for your niche

| # | Step | Block | Give your agent | Done when |
|---|---|---|---|---|
| 1 | Write the brief: product, 3–5 niches (who × job), the decision and its date, what would stop you | 0 | `niche_brief.md` | one page, in your repo |
| 2 | Population per group $N_x$ (age bands, country) | 1 | — | Eurostat query in the ledger |
| 3 | Budget per group $b(x)$: an open spending or subscription rate for your category | 8b | — | `open` rows with the query |
| 4 | Your own data: each rate as a Beta posterior per group; the funnel as a chain | 2, 2b | `analyst_agent.md` | intervals, not points |
| 5 | **Reweight** your sample to the population; say whom it cannot speak for | 3b | — | $u$ and $n_{\text{eff}}$ reported |
| 6 | Segments by behaviour, crossed with your groups | 3 | — | one table |
| 7 | Competitors: price, model, audience, source | 5 | `competitor_scan.md` | `competitors.csv` with URLs |
| 8 | Features from their descriptions and reviews; importance per group (lift, Kano) | 5b, 6b | `feature_extraction.md` | agreement with the lexicon checked |
| 9 | Conversations: jobs, pains, share of voice; who is missing | 6 | `social_listening.md` | exact quotes, no names |
| 10 | Overlap $q(x)$: bounds, independence, a bridge; the qualified audience | 8b | — | the assumption named |
| 11 | The key user journey per group; where your product shows value | 8c | `journey_simulator.md` | the ranking, not the level |
| 12 | Combine the signals: label texts with several weak rules, join direct and indirect evidence in one model, list each source's bias, report belief and ignorance | 8d | `feature_extraction.md` | agreement across **different** biases |
| 13 | Two routes within 3×; P10–P50–P90; variants ranked by P10; research the top input; update | 8, 9, 10 | `deep_research_prompt.md` | the next question written down |

## 3. The formulas

**Conditional probability and the chain rule** (every rate has a "given"; a funnel is a chain):

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad P(\text{pay}) = \prod_k P(\text{step}_k \mid \text{steps}_{<k})$$

**Total probability** (segments add up) and **Bayes** (assigning, updating):

$$P(Y) = \sum_s P(Y \mid s)\,P(s), \qquad P(s \mid x) = \frac{P(x \mid s)\,P(s)}{\sum_{s'} P(x \mid s')\,P(s')}$$

**A rate from $k$ of $n$** (Beta prior, Binomial data), and comparing two options by draws:

$$p \mid k, n \sim \mathrm{Beta}(\alpha + k,\ \beta + n - k), \qquad P(p_A > p_B \mid \text{data}) \approx \frac{1}{M}\sum_{m} \mathbf{1}\big[p_A^{(m)} > p_B^{(m)}\big]$$

**Fusion**: the overlap of problem $A$ and budget $B$ within group $x$, the audience, and the bounds when nobody
measured the overlap:

$$q(x) = P(A \mid x)\,P(B \mid A, x), \qquad \text{audience} = \sum_x N_x\,q(x), \qquad \max(0,\ a + b - 1) \le q \le \min(a,\ b)$$

**Reweighting**: post-stratification, raking, inverse probability weighting:

$$w_i = \frac{N_{c(i)}/N}{n_{c(i)}/n}, \qquad w_i \leftarrow w_i\,\frac{N_{m,a}}{\sum_{j:\,m(j)=a} w_j}, \qquad w_i = \frac{1}{\hat\pi(x_i)}$$

**How far you can reweight**: the uncovered share, Kish's effective sample, the design effect, the distance, and the
worst-case bounds for the part you cannot see:

$$u = \sum_{c:\,n_c = 0} \frac{N_c}{N}, \quad n_{\text{eff}} = \frac{(\sum_i w_i)^2}{\sum_i w_i^2}, \quad \text{deff} \approx 1 + \mathrm{CV}^2(w), \quad \mathrm{TVD} = \tfrac12 \sum_c \left|\tfrac{n_c}{n} - \tfrac{N_c}{N}\right|$$

$$(1-u)\,\hat y_{\text{cov}} \;\le\; \bar y \;\le\; (1-u)\,\hat y_{\text{cov}} + u$$

**Evidence synthesis**: all the evidence about the parameters $\theta$ in one model; the product only when the data are
independent given $\theta$; Dempster–Shafer keeps ignorance apart from evidence against:

$$p(\theta \mid D_1, \dots, D_k) \propto p(\theta)\,p(D_1, \dots, D_k \mid \theta), \qquad p(D_1, \dots, D_k \mid \theta) = \prod_i p(D_i \mid \theta) \ \text{only if } D_i \perp D_j \mid \theta$$

$$\mathrm{Bel}(A) = \sum_{B \subseteq A} m(B), \qquad \mathrm{Pl}(A) = \sum_{B \cap A \neq \varnothing} m(B), \qquad \text{ignorance} = \mathrm{Pl} - \mathrm{Bel}$$

## 4. The thresholds

| Check | Pass | If not |
|---|---|---|
| Two routes to the market | within 3× | find the definition that differs |
| Uncovered population $u$ | ≤ 5% | change the target population, or collect the missing cells |
| Effective sample $n_{\text{eff}}$ | ≥ 30 per number | collect more, or merge cells |
| Largest weight | ≤ 10 × median | trim at 5 × median and report both |
| A bridge estimate | inside the Fréchet bounds | the definitions do not match: align them |
| An agent's number | equal to your recomputation | refuse it, show the difference |
| A deep-research figure | two sources opened by you | `assumption` until then |
| Simulated evidence | used for a ranking | never as a level |
| Agreement between sources | their biases differ | five copies of one survey are one piece of evidence |
| Two related reports | one likelihood | multiplying them manufactures confidence |

## 5. Open data that needs no key

| What | How |
|---|---|
| Eurostat, any table | `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<code>?format=JSON&geo=<XX>&lang=EN&…` |
| Population by age | `demo_pjangroup` (by 5-year group); by age × education: `lfsa_pgaed` |
| Household spending | `hbs_exp_t121` (COICOP, PPS per household; latest wave 2020) |
| Paid app subscriptions | `isoc_ec_ibgs`, `I_BHLFTS2` (health or fitness apps), `I_BAPP2` (other apps), by age |
| Reading, streaming | `ilc_scp27` (books, by age × education), `isoc_ci_ac_i` `I_IUVOD` (video on demand) |
| Spain in detail | INE Tempus3: `https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/<op>` |
| Public conversations | Hacker News: `https://hn.algolia.com/api/v1/search?query=<words>&tags=comment` |
| Apps and reviews | `https://itunes.apple.com/lookup?id=<id>`; reviews: `https://itunes.apple.com/us/rss/customerreviews/page=<1–10>/id=<id>/sortby=mostrecent/json` (500 at most per country) |

Another country: change `geo=ES` (Eurostat) and the store's country (`us`, `es`, `gb` …).

## 6. With Claude or ChatGPT

* **Outside the notebook**: paste the instruction file and a sample of your data into a chat; ask for the JSON it
  specifies; paste the answer into `outside_answer` (block 7) and run `check()`.
* **Inside**: put `ANTHROPIC_API_KEY` in Colab's secrets (the key icon); `ask_analyst()`, `ask_persona()` and
  `llm_features()` send the files for you. Read the code before you run it.
* **Never**: a number with no source; a simulated answer as a level; personal data in a prompt; one run treated as
  the answer (run it several times and report the spread).

## 7. In your journal, today

The top variant by P10 · the input that moves it most · whom your sample cannot speak for ($u$) · what you will
research next, how, and by when.
