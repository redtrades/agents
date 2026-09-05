# Asset 01: the cold email and its subject lines

2026-08-26. Written, not described. Uncommitted draft for Mike.

**What object this sells.** One named federal contract that ends inside the next 6 to 18 months, and
the file we build on it. Not a Sources Sought notice. The existing `templates/outreach/email-1-opener-v5-draft.md`
sells the notice object on an 8-day clock and stays as it is. This is a sibling for the recompete
object, where the clock is months and a second touch actually fits.

**Two gates carry over unchanged from the existing templates and are not negotiable.**

1. `templates/outreach/footer-v5-draft.md` verbatim, both brackets filled, including `This is an ad.`
2. Nothing sends until counsel clears the contact route. See REPORT §6.3 for a narrower question
   than the one currently open.

**One gate is new and specific to this email.** Every merged field is a verbatim copy of a value
returned by a public API call that is recorded in the order folder, with the retrieval timestamp
printed in the body. No field in this email is a derived judgment. That is what lets it go out
without twenty minutes of founder reading per firm.

---

## Form R, the recompete opener

**114 words unmerged, 118 merged.** Counted with a script against the worked example below, not
estimated. The gate is 120 and the merged number is the one that counts, because a long office name
is what pushes it over.

```
{first_name}, {pid}, your {office} contract, has an end date of
{end_date}. FPDS shows the same date as its potential end date, so
there are no option years recorded past it. Pulled {retrieved_at}.

That award drew {offers} offers. Since {first_year} you have {n_awards}
prime awards in NAICS {naics}, {pct}% of your {total_awards} total at
{agency_short}.

I build one file on one contract like that: what the office has paid
for the work, how many firms have bid on it, which requirements your
own record already covers, and a page of the ones it doesn't. $1,500.
You review it. I don't send anything to the government.

Want the free one-page read of your own record first?
```

If a merge lands over 120, shorten `{office}` first, then `{agency_short}`. Never cut the end-date
sentence, the price, or the CTA. Those three are what the email exists to carry.

**Two house-style notes, both Mike's call.**

- The live templates open the greeting with a long dash after `{first_name}`. This file uses a
  comma instead, because the commissioning brief bans that character. If the house style wins, swap
  it back and re-count: the dash adds one token.
- `{pct}` **floors, it does not round.** The worked example below computes 138 of 169 VA awards,
  which is 81.65%, and the email prints 81%. Same discipline as the dollar rule in `AGENTS.md`: the
  printed figure is never larger than the source supports.

Every send carries `templates/outreach/footer-v5-draft.md` verbatim, appended below the body and
excluded from the word count.

### Worked example, merged against a real public record

Retrieved from USASpending 2026-08-26. The firm has not been contacted and this is an illustration,
not a send. `{first_name}` is left unmerged on purpose: the owner's name is a contact field and
this file is not the place to publish one.

```
{first_name}, 36C24426N0808, your VA Pittsburgh contract, has an end
date of October 4 2027. FPDS shows the same date as its potential end
date, so there are no option years recorded past it. Pulled 2026-08-26.

That award drew 4 offers. Since 2014 you have 125 prime awards in NAICS
236220, 81% of your 169 total at the VA.

I build one file on one contract like that: what the office has paid
for the work, how many firms have bid on it, which requirements your
own record already covers, and a page of the ones it doesn't. $1,500.
You review it. I don't send anything to the government.

Want the free one-page read of your own record first?
```

Sources for every field in that merge:
`https://api.usaspending.gov/api/v2/search/spending_by_award/` and
`https://api.usaspending.gov/api/v2/awards/CONT_AWD_36C24426N0808_3600_-NONE-_-NONE-/`, both keyless,
both public, 1.3 seconds wall clock for the pair.

### Why each sentence is there

| Sentence | Job | Why it survives a skeptical read |
|---|---|---|
| `{pid}, your {office} contract, has an end date of {end_date}` | The whole email | It is their own money with a date on it. A stranger who knows their PIID and their end date has done work no bot template can fake |
| `FPDS shows the same date as its potential end date, so there are no option years recorded past it` | The finding | Reports what the field says, not what it means. The record could be incomplete and the sentence is still true. This is the citation register from the sample set, in an email |
| `Pulled {retrieved_at}` | Separates us from the cache | GovWin buyers complain the data is 24 to 48 hours stale and nobody prints a retrieval time (competitor-pain §2.2) |
| `That award drew {offers} offers` | The second fact | It is the number that decides whether a thing is worth an evening, and no free alert carries it |
| `{pct}% of your {total_awards} total at {agency_short}` | Concentration | An owner reads this as risk, which is the emotion that makes an end date matter |
| `$1,500. You review it. I don't send anything to the government.` | Price in public, scope fenced | Four of eleven competitors now hide price behind a demo (competitor-pain §1.3). Publishing it is the cheapest trust move available |
| `Want the free one-page read of your own record first?` | The ask | Asks for permission to give, not permission to sell. The CTA finding in `research/outreach-playbook/REPORT.md` already says an artifact ask beats a call ask |

### What this email may not say

Everything in `brand/offer.md` under "Claims to AVOID," plus three specific to this object.

- Not "your contract is expiring and you need to act." The record shows an end date. The office may
  extend, bridge, absorb the work into a vehicle, or stop buying it. Say what the field says.
- Not "the incumbent's certification lapses first" unless a dated exit is in hand from a source we
  are allowed to use. See REPORT §2.2, rank 6.
- Not "your SAM registration expires." It is public, it is dated, it hits hard, and it is the exact
  sentence the registration scams open with (GSA IAE, BBB). Banned outright.

---

## Touch 2, sent 6 days later if no reply

Variant-neutral, no new claim, no new urgency. 57 words unmerged.

```
{first_name}, following up on {pid}. The one-page read is four
numbers: the end date, the potential end date, the offer count on the
award, and what {agency_short} has obligated on comparable work. Each
one links to the federal record it came from.

No charge and nothing to buy on that one. Reply "send it" and it's
yours.
```

[+ footer]

## Touch 3, sent 12 days after touch 1, then stop

50 words unmerged. Says the thing out loud and closes the loop.

```
{first_name}, last one from me on {pid}.

If you already know the end date and you have the evening to work the
recompete yourself, that is the right call and you should keep the
$1,500.

If you want the free read instead, it's still here. Otherwise I'll
leave you alone.
```

[+ footer]

Three touches, then permanent suppression whether or not they replied. At 1,484 firms in the pond
(REPORT §4.1) the list is a finite resource and a fourth touch spends it for nothing.

---

## Subject lines

Ranked. Each one is a fact from the body, not a tease. No firm name in the subject, because a merged
firm name in a subject line is what the registration scams do.

| # | Subject | Why |
|---|---|---|
| 1 | `{pid} ends {end_date_short}` | Six words, one of which only somebody who read their record could write. Nothing to distrust because there is nothing to sell in it |
| 2 | `no option years recorded past {end_date_short} on {pid}` | The finding in the subject. Longer, more specific, and it pre-answers "what do you want" |
| 3 | `{offers} offers on {pid}, and it ends {end_date_short}` | Leads with contestability. Use where the offer count is 1 or 2, which is the version that stings |
| 4 | `your {agency_short} work, and the date it runs out` | No PIID. The fallback when the PIID is long enough to look like a tracking string |
| 5 | `{pct}% of your federal revenue is on one contract` | Highest emotional hit and the highest risk of reading as a cold-call opener. Hold it for a second batch |

**Banned subjects,** each for a reason that comes off the fraud-adjacency finding in GTM §5.5:
anything with `Re:` or `Fwd:`, anything with a countdown, anything containing "opportunity,"
"urgent," "action required," "expiring," or the recipient's first name alone. Google's own sender
guidelines name most of these as deceptive display and subject practice
([Gmail sender guidelines](https://support.google.com/a/answer/81126), retrieved 2026-08-26).

---

## Send mechanics, sized to a 1,484-firm universe

The cold-email industry sizes infrastructure for 1,000 sends a day, which needs 35 to 50 mailboxes
across 12 to 25 domains ([maildeck](https://maildeck.co/blog/cold-email-infrastructure-cost-2026/),
vendor-published, retrieved 2026-08-26). None of that applies here. The entire pond is 1,484 firms
and each firm gets at most three touches, ever. That is one domain, one mailbox, and a send rate of
20 to 40 a day for a couple of months.

- One sending domain, SPF plus DKIM plus DMARC. Under 5,000 messages a day so the one-click
  unsubscribe header is not required, but include it anyway
  ([Gmail sender guidelines](https://support.google.com/a/answer/81126), retrieved 2026-08-26).
- Keep the Postmaster Tools spam rate under 0.10% and never let it touch 0.30%. Same source. At
  40 sends a day, three complaints in a week is already a problem, which is another reason the
  three-touch cap matters.
- The `no thanks` reply is same-day permanent suppression, per the existing footer file.
