# Connect 2027 roadmap goals — the lens for roadmap and backlog work

Set by Connect product leadership (shared by Mary Rocheleau; themes 2026-10-27, full goals doc
2026-11-03). These are the five goals Connect prioritizes for 2027 — **not in priority order**.
They mostly shape the roadmap (`CCC`), but they are standing context for every Sift judgment:
how to categorize an item, what matters most, what's missing. Read this before any triage,
stale review, prioritization or roadmap question.

Full roadmap: [CCC roadmap view](https://dimagi.atlassian.net/jira/polaris/projects/CCC/ideas/view/3b1eec9a-a112-480e-a5fc-aae747ec61e6)

| # | Goal (CCC `Goal` value) | In one line | Measured by |
|---|---|---|---|
| 01 | Reliable self-serve FLW identity | FLWs sign up, log in and recover accounts with minimal / no help from Dimagi | >90% of recoveries without Dimagi; OTP delivery success rate by country |
| 02 | Program integrity and traceability (Jira value: `Program integrity and tracability`) | Every paid visit can be checked and traced back to the worker who did it | % of paid visits covered by a verification or audit step; flagged visits removed pre-invoice |
| 05 | Platform health, security and support | Scale to anticipated visit load; safer and faster releases | Lead time for changes; zero open high/critical security findings; tech escalations per month |
| 07 | LLO network and multi-org model | Grow and collect data on LLOs, and reflect it directly in the Connect product | # active LLOs; days from solicitation to signed LLO |
| 10 | Data access for LLOs, funders and Labs | All production data reachable by API; partners and funders see their own data | % of Prod tables exposed via API (target 100%); # LLOs/funders with self-serve access |

The numbers are the themes' own IDs (the full theme list is longer; only these five are
prioritized). Glossary: **FLW** frontline worker · **LLO** locally led organization · **PersonalID**
Connect's sign-in/identity service · **Labs** analytics/experimentation environment · **CCHQ**
CommCare HQ. Metrics come from the 2026-10-27 themes; the goals doc doesn't restate them.

## What each goal covers
Use these to decide which goal an item belongs to. An item can serve more than one (e.g.
"send all CCHQ form data to Connect" is both 02 and 10).

### 01 — Reliable self-serve FLW identity
**Why:** PersonalID is still friction when starting on Connect. Faster sign-up, targeted access
to Opportunities, and more data about FLWs to target Opportunities long-term.
- **OTP delivery** — more SMS vendors, per-country vendor switching, WhatsApp OTP with SMS
  fallback, warn users before they hit SMS send limits.
- **Smoother first-time sign-up** — pre-registration so PersonalID setup and device problems
  happen before the training session.
- **Knowing our users** — collect data to segment the FLW population and match people to
  opportunities.

### 02 — Program integrity and traceability
**Why:** As programs grow, visits must be real (not fraudulent) and traceable from visit →
Dimagi payment → LLO → specific FLW. Every visit verifiable; bad visits excluded before payment.
- **End-to-end audit trail** — DB-level change tracking across the payment lifecycle; per-visit
  activity history (verification rules run, audits incl. Labs, who approved/rejected and when);
  visit → invoice → payment status; per-worker history of Opportunities, Tasks, Actions (Prod
  and Labs).
- **Stronger verification** — verification assessments before invoice generation; AI image
  classifiers (e.g. measurement photo too zoomed) on the visit details page.
- **All form data from CCHQ to Connect** — not only payment forms; monitoring of when each form
  arrived and when its verification checks completed.
- **Catch problems before money moves** — visits rejected by verification rules, assessments or
  audits are removed from invoices; duplicate deliveries handled consistently so reporting and
  invoicing reconcile.
- **Openness with workers** — FLWs see why a visit was rejected and how verification works.

### 05 — Platform health, security and support
**Why:** Keep Connect secure, stable and scalable as visit volume grows; safer, faster releases.
- **Security** — AI-assisted security audit focused on API data access and permissions.
- **Reliability and scale** — load-test production; health-check endpoints and a public status
  page; split background job queues so nightly jobs don't block time-sensitive tasks (sign-up).
- **Engineering speed** — reusable UI component library; mobile code into feature packages
  (per-feature crash rate / coverage); consolidate CCHQ feature flags; upgrade deploy tooling.
- **Self-serve support** — user-facing and developer docs sites; faster KPI report.
- **Simpler setup** — reuse one CCHQ app across multiple opportunities.

### 07 — LLO network and multi-org model
**Why:** Move management of LLOs into the Connect product — run a solicitation, contract, and
see an organization's work history directly in Connect.
- **LLO Directory in product** — proper interface, org sign-up from the external Connect site,
  network KPIs (orgs in network, active orgs).
- **Solicitation to contract** — solicitations (in implementation) with contracts generated and
  processed in Connect.
- **Fewer manual handoffs** — email notifications on LLO invite/accept; one-step email invites
  for people without accounts; a "request access" flow instead of an error page.

### 10 — Data access for LLOs, funders and Labs
**Why:** All production data available via API, so Labs can build analysis/dashboards and
partners and funders see their own data without asking Dimagi.
- **Full API coverage** — inventory every Prod table and add missing APIs; remaining automation
  read/update endpoints; program-level export endpoints for user lifecycle and delivery KPIs.
- **More data into Connect** — all CommCare form data; Labs actions sent back to Prod as part of
  the audit record.
- **Better views** — Labs reports embedded in Connect; dashboards for multi-visit-per-beneficiary
  programs; a visit map for every program type; export filters by payment unit and user.
- **Open Chat Studio integration** — easier to configure, implement and pay FLWs for OCS work.

## Where it lives in Jira
- CCC roadmap items carry the goal in the **`Goal`** field (`customfield_14111`, multi-select).
  Match Jira's values exactly — note goal 02 is spelled `Program integrity and tracability` in
  Jira. An item may hold more than one goal.
- Goal is the *why*; **Product Area** (`customfield_10448`) and **Platform** (`customfield_10434`)
  are the *what/where*. Keep all three — don't use one to stand in for another.
- Goals were first assigned by Mary on 2026-10-27 (75 CCC items tagged as of 2026-11-03). The PM
  decides what gets a goal: Sift proposes candidates, it never sets Goal without approval.
  Borderline fits she declined (e.g. PersonalID recovery items left out of 01) are her call —
  don't re-propose them unprompted; raise them only as a coverage gap against a goal's metric.

## How Sift uses it
- **Categorize.** For any item — new, untagged, or asked about — name the goal(s) it serves (or
  "none") using the "What each goal covers" lists above, alongside Product Area and Platform.
- **Rank by goal.** In triage reports and prioritization answers, lead with work that moves a
  goal's metric. The goals are unordered — don't rank one goal above another; rank items by how
  directly they move a goal. Priority drift includes P1–P3 / Prioritized items with no Goal, and
  goal-tagged items sitting stale.
- **Off-goal work is a finding, not a defect.** Report the count of open CCC items with no Goal,
  and call out the in-flight ones (Prioritized / Implementation / Technical Spec) — those are
  the ones a PM should either tie to a goal or deprioritize. Don't propose closing an item just
  because it has no goal.
- **Coverage gaps.** For each goal, check whether its metric and its listed work have items
  behind them. A goal whose metric has no tagged in-flight item gets flagged.
- **Stale reviews.** A goal-tagged item that's stuck gets a nudge to its owner, not a close.
- **CCCT.** Delivery work inherits its goal from the CCC item its epic implements; use that to
  rank delivery tickets, but don't write Goal onto CCCT.
