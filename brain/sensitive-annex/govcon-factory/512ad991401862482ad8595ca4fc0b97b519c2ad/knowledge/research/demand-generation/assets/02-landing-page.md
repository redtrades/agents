# Asset 02: landing page above the fold, and the one-paragraph answer

2026-08-26. Written, not described. Uncommitted draft for Mike.

Replaces nothing. `sop/MARKETING.md` Door 1 specifies the page's parts (UEI box, free report,
newsletter, sample). This file writes the words for the top of it and adds the free read as the
first CTA.

---

## Above the fold

### Headline

> **Your federal contracts are public. So is the date each one runs out.**

Rejected alternatives and why: "Win more federal contracts" (a claim `brand/offer.md` forbids and
every competitor makes), "Federal contract intelligence for small business" (says nothing, and
SamSearch already owns "the operating system for government contracting"), "Stop missing
opportunities" (fear framing, and the buyer has heard it from the registration shops).

### Subhead

> Put in your UEI. You get back, free and with no account: every prime contract in your name, the
> date each one ends, whether the record shows any option years left past that date, and how many
> firms bid on it. Every line links to the federal record it came from and carries the minute we
> pulled it.

### Primary control

```
[  UEI  (12 characters)  ]   [ Show me my record ]

No account. No credit card. Nothing gets emailed to you unless you ask.
```

### Under the control, three lines and nothing else

> Then, if one of those contracts is worth chasing, **$1,500** buys the file on it: what the office
> has paid for the work, who else can bid, what your own record already covers, and one page listing
> the blanks only you can fill.
>
> Read a finished file in full before you give me anything. [Every sample we have built is here.]
>
> Mike Ninov, a service-disabled veteran-owned small business. You review the file. You submit it.
> I don't send anything to the government.

### The row across the bottom of the fold

Four short items, each a link, no icons.

| Read a full sample | See the price | Who I am | Files I refused, and why |
|---|---|---|---|

That last one links to the refusal log: below the fill floor there is nothing to buy, and we publish
the count. It is the strangest link on any page in this market, which is the point of putting it in
the fold. competitive-assessment §8.3 argues it is also the least copyable thing we have, because a
vendor whose footer reads "never say no bid" can copy the marketing line in an afternoon and cannot
copy a counter that goes up.

### The identity strip, immediately below the fold

Not decoration. competitive-assessment §9.3 found that when a small firm asks an AI assistant who can
help them bid, the answer names businesses that look like businesses, and the software tier gets
named zero times across eleven queries. SAS-GPS publishes a legal entity, a founding year, two phone
numbers, a physical address and named references, and gets named. We publish none of the five.

```
Ninov [entity name] · service-disabled veteran-owned small business
Founded [year] · [street address] · [phone] · mike@[domain]
Files approved by: Mike Ninov. Every file carries his name.
```

Fill the brackets before the page ships. Four of the five are free and take an afternoon. The fifth,
an attributable customer reference, does not exist yet and must not be simulated.

### The price line, stated as the differentiator it now is

Of every services provider appearing on page one of the eleven buyer-intent searches, **not one
publishes a price**, including SAS-GPS, which advertises "Transparent Pricing" and gates the number
behind a seven-field form (competitive-assessment §10.2, observed 2026-08-26). The only published
prices anywhere in that demand picture are Fiverr gigs at $90 to $250 and PrimeRFP's $90 pilot.
A published four-figure fixed price is therefore a genuinely differentiated thing to put above the
fold, and it costs nothing to test.

---

## What am I buying, in one paragraph

For the offer page, the order confirmation, and any reply that asks the question directly.

> One contract, one file. You name a federal contract that ends in the next 6 to 18 months, or I
> name one from your own award record. I write down what the public record says about it: what the
> contracting office has obligated on this work and when, how many firms bid the last time it was
> competed, what the official competition flag says next to that offer count, how the incumbent's
> record looks, which of the requirements your own past awards already cover, and which ones they
> don't. Every number links to the federal record it came from, with the date and time I pulled it.
> The last page is the list of things the public record cannot answer, so you know exactly what you
> still have to write yourself. $1,500, paid once, no subscription, nothing to cancel. If the record
> says the thing was never contestable, the file says that in the first paragraph and you don't pay
> me for it.

**Word count 163.** Long for a paragraph and deliberately so: every clause is a thing the buyer
would otherwise have to ask, and this market's buyers have been burned by scope that lived in a
sales call rather than in writing (competitor-pain §2.7).

---

## The free one-page read, specified

This is the conversion mechanism, so it gets a spec rather than a description. See REPORT §3.

**What it contains.** Nothing but fields copied verbatim from a public API response, one line each,
each with a permalink and a retrieval timestamp.

```
YOUR RECORD, pulled 2026-08-26 14:02 ET
Firm: {legal_name}   UEI: {uei}

Prime awards, FY{y0} to date .......... {n}      [link]
NAICS you have actually been paid in ... {top_5_with_counts}
Agencies .............................. {top_3_with_shares}

CONTRACTS ENDING IN THE NEXT 6 TO 18 MONTHS
{pid}  {office}
  Current end date .................... {end}          [link]
  Potential end date .................. {pot}          [link]
  Option years recorded past current ... {yes|no|not recorded}
  Offers received on this award ....... {n | not recorded}
  Official competition flag ........... {extent_competed_description}
  Set-aside .......................... {type_set_aside_description}
{repeat}

WHAT THIS PAGE DOES NOT TELL YOU
- Whether the office intends to recompete, extend, bridge, or stop buying.
- Anything that is not in FPDS. Missing is missing, not zero.
- Any judgment about whether you should bid. That is the paid file.
```

**Why this exact shape.** It needs zero founder judgment, which is the whole design constraint. Every
line is a verbatim field with a link, so `gate_runner.py`-style mechanical checking is sufficient and
Mike's twenty-minute review budget is never spent on a free artifact. A wrong number on a public page
is a reputation gate failure under the existing rules, and the only reliable way to avoid one at
volume is to publish nothing that required a human to decide anything.

**What it must never contain.** A score, a recommendation, a probability, a dollar estimate we
computed, or the sentence "you should bid on this." Two competitors have independently landed on
facts-not-scores (offer-design §5.5). We go further by keeping the free artifact free of even the
implicit judgment that a ranking creates.
