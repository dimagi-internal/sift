# Connect 2027 themes — the lens for roadmap and backlog work

Set by Connect product leadership (shared by Mary Rocheleau, 2026-10-27). These are the five
themes Connect prioritizes for 2027 — not in priority order. The numbers are the themes' own IDs
(the full list has more; only these five are prioritized). Read this before any triage, stale
review or roadmap question, and judge tickets against it.

| # | Theme (= CCC `Goal` value) | Outcome | Measured by |
|---|---|---|---|
| 01 | Reliable self-serve FLW identity | FLWs sign up, receive OTPs and recover accounts without Dimagi | >90% of recoveries without Dimagi; OTP delivery success rate by country |
| 02 | Program integrity and audit trail | Every paid visit is verifiable and traceable to the FLW; bad visits are caught before invoicing | % of paid visits covered by a verification or audit step; flagged visits removed pre-invoice |
| 05 | Platform health, security and support | Safer, faster releases; partners and Delivery self-serve common issues | Lead time for changes; zero open high/critical security findings; tech escalations per month |
| 07 | LLO network and multi-org model | Grow and match qualified LLOs and third-party PMs with less Dimagi brokering | # active LLOs; days from solicitation to signed LLO; # programs run by third-party PMs |
| 10 | Data access for LLOs, funders and Labs | All Prod data reachable via API; LLOs and funders see their own data | % of Prod tables exposed via API (target 100%); # LLOs/funders with self-serve access |

## Where it lives in Jira
- CCC roadmap items carry the theme in the **`Goal`** field (`customfield_14111`, multi-select;
  values are the theme names above, exactly). An item may hold more than one goal.
- Goal is the *why*; **Product Area** (`customfield_10448`) and **Platform** (`customfield_10434`)
  are the *what/where*. Keep all three — don't use one to stand in for another.
- Goals were first assigned by Mary on 2026-10-27 (52 items). The PM decides what gets a goal:
  Sift proposes candidates, it never sets Goal without approval. Borderline fits she declined
  then (e.g. PersonalID recovery items left out of 01) are her call — don't re-propose them
  unprompted; raise them only as a coverage gap against a theme's metric.

## How Sift uses it
- **Rank by theme.** In triage reports, lead with work that moves a theme's metric. Priority
  drift now includes: P1–P3 / Prioritized items with no Goal, and goal-tagged items sitting
  stale.
- **Off-goal work is a finding, not a defect.** Report the count of open CCC items with no Goal,
  and call out the in-flight ones (Prioritized / Implementation / Technical Spec) — those are
  the ones a PM should either tie to a theme or deprioritize. Don't propose closing an item just
  because it has no goal.
- **Coverage gaps.** For each theme, check whether its metric has work behind it. A theme whose
  metric has no tagged in-flight item gets flagged (e.g. 10's "LLOs see their own data").
- **Stale reviews.** A goal-tagged item that's stuck gets a nudge to its owner, not a close.
- **New / untagged items.** Suggest a Goal (or "none") alongside Product Area and Platform.
- **CCCT.** Delivery work inherits its theme from the CCC item its epic implements; use that to
  rank delivery tickets, but don't write Goal onto CCCT.
