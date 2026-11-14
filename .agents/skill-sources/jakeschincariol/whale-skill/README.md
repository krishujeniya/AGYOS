# The Whale skill

Eleven Claude skills that get you paying customers before you launch. Free, MIT, no signup, no API key.

`market-researcher` `demo-builder` `whale-hunter` `pre-sale` `requirements` `offer-builder`
`pricing` `follow-up` `objection-handler` `case-study` `launch-planner`

One acts as your market researcher, finding problems businesses already pay thousands to solve. Another
builds a demo showing how your product solves them. One finds the decision makers and pitches them. And the
craziest one is the pre-sale skill: it gets customers to pay up front and uses their requirements to build
the exact product.

So instead of building for a year and paying for marketing to find out nobody wants it, you find out with real
money first, and you build exactly what was paid for.

Nothing is ever sent or charged without your yes. Claude drafts, you approve, it goes out from your own
accounts. It can't promise that anyone will buy: only they can tell you that, and that's the point.

## Install

Paste this repo link into Claude and say `install skill`:

```
https://github.com/Jakeschincariol/whale-skill

install skill
```

Or as a plugin, in Claude Code:

```
/plugin marketplace add Jakeschincariol/whale-skill
/plugin install whale-skill@whale-skill
```

Claude Code namespaces plugin skills, so installed as a plugin they show up as
`/whale-skill:pre-sale` and so on. Copy the folders instead if you want plain `/pre-sale`:

```bash
git clone https://github.com/Jakeschincariol/whale-skill.git
cd whale-skill && cp -r market-researcher demo-builder whale-hunter pre-sale requirements offer-builder \
    pricing follow-up objection-handler case-study launch-planner ~/.claude/skills/
```

Keep all eleven together: they share `market-researcher/board.py`. No Claude Code at all? Paste any single
`SKILL.md` at the top of a chat and it runs as a mode. You lose the Python tools, but the method works.
The tools need Python 3.8 or newer. Nothing to pip install.

Works best with Claude's Gmail connector (email goes out from your own account) and the Stripe connector (the
checkout is in your own Stripe account). You need a Stripe account to take money. Stripe takes its normal fee.

## The eleven

| skill | job | what it does |
| --- | --- | --- |
| `market-researcher` | Market Researcher | Finds problems businesses already pay thousands to solve, with a source for every number, and sets up the board. |
| `demo-builder` | Demo Builder | Builds a clickable demo showing how your product solves it, with sample data and a banner that says so. |
| `whale-hunter` | Whale Hunter | Finds who signs the check at the company you want, and writes the pitch. |
| `pre-sale` | Pre-Sale | Gets customers to pay up front through your own Stripe: it isn't finished, here's the date, here's the way out. Tells you when you're validated, and holds you to the date. |
| `requirements` | Requirements | Turns what they asked for into the build list, ranked by the paid money behind each line. |
| `offer-builder` | Offer Builder | Writes the one-page offer they can say yes to, and refuses fake urgency and made-up proof. |
| `pricing` | Pricing | Sets the price from what they pay today, with the working shown. |
| `follow-up` | Follow-Up | Keeps the deal moving: a bump, something useful, a last note. Stops at the first no. |
| `objection-handler` | Objection Handler | Has an honest answer to every objection ready, and knows a no when it hears one. |
| `case-study` | Case Study | Turns the first customer into proof, from their real numbers, with their written approval of every word. |
| `launch-planner` | Launch Planner | Plans the launch once it's paid for, backwards from the dates you promised. |

## How to use it

Everything lands in a `whale/` folder in your project, and each skill reads what the last one wrote.

An example, the one in the reel: a founder with an idea for a product that chases late invoices.

1. **`market-researcher`** builds the table of problems businesses already pay for. The pick: freight companies pay
   about $6,400 a month to chase late invoices.
2. **`demo-builder`** builds Your Product: five late invoices, one button, "Chase all", $48,210.00 collected. A banner
   says it's sample data.
3. **`whale-hunter`** finds who decides at North Pier Logistics, and writes to the CFO: "North Pier pays about $6,400 a
   month to chase late invoices. We built a demo that does it automatically. Can I show you in 2 minutes?" You say yes.
4. **`follow-up`** bumps it once. She replies and books the demo.
5. **`pricing`** works it out: they pay $76,800 a year, so $24,000 is 31% of that. **`offer-builder`** writes the page.
   **`objection-handler`** has the answer when she asks, "What if you never ship it?"
6. **`pre-sale`** makes the Stripe link: $24,000.00, ships in 30 days, not finished yet, every dollar back if it doesn't ship.
   North Pier pays. Two more freight companies follow. VALIDATED: 3 paying customers, $54,000.00 in, $0.00 spent on marketing.
7. **`requirements`** turns "Sync with QuickBooks" and "Weekly report to the CFO" into the build list, and you build exactly that.
8. **`launch-planner`** works back from the first promised date. The public launch waits until customers have it.
   **`case-study`** turns the first result into proof, with their approval.

(Your Product, North Pier, everyone at it, and every dollar here are fictional.)

## The tools

All standard-library Python. Nothing here reads a website or calls an API: Claude does the research and uses your connectors, and
the tools keep the board honest.

```bash
python3 market-researcher/board.py board                               # the board
python3 market-researcher/problems.py rank                             # problems, who pays, what they pay
python3 demo-builder/demo.py build --spec whale/demo.json              # the demo, one HTML file
python3 whale-hunter/hunter.py who --company north-pier                # who decides
python3 whale-hunter/hunter.py draft --deal north-pier --demo <link>   # the pitch
python3 pre-sale/presale.py link --deal north-pier                     # what to create in Stripe
python3 pre-sale/presale.py validated                                  # paying customers against your target
python3 pre-sale/presale.py due                                        # every date you promised
python3 requirements/reqs.py build                                     # the build list
python3 offer-builder/offer.py draft --deal north-pier                 # the offer
python3 pricing/price.py check --pay-month 6400 --price 24000          # what a price means for them
python3 follow-up/followup.py due                                      # who to follow up with today
python3 objection-handler/objections.py match --text "too expensive"   # what to say
python3 case-study/casestudy.py check --deal north-pier                # may this be used yet?
python3 launch-planner/launch.py gate                                  # may this launch yet?
```

Try any of them on the reel's example board with `--file market-researcher/whale.example.json`.
The tests live next to each tool:

```bash
for d in */; do python3 -m unittest discover -s "$d" -p "test_*.py"; done
```

## Fine print

**You are taking money for something that doesn't exist yet. Treat that seriously.** The buyer always sees that it isn't finished,
the date it ships and how they get their money back, right above the pay button. Don't take money for something you don't intend
to build. Promise a date you would bet on.

**Keep the money until it ships.** Stripe's guidance on pre-orders says they carry real risk, and recommends partial deposits, limiting
orders, realistic dates and keeping enough cash for refunds and disputes. A customer can dispute a card charge, and Stripe can hold funds.
Spend it, and you may not be able to pay it back.

**When a date slips, they hear it from you first.** They get the new date and their money back if it doesn't work for them. Only their yes
moves the date. In the US, the FTC's Mail, Internet, or Telephone Order Merchandise Rule covers most goods ordered online: ship when you
said (within 30 days if you said nothing), and if you can't, get consent to the delay or refund. Whether it covers your product is a
question for a lawyer.

**Nothing goes out without your yes.** Every email, offer and payment link is a draft until you approve that exact one. One yes per
message, never "yes to all". The tools refuse to log a message without it. They never touch a card number: buyers pay on Stripe's own page.

**Cold email, done legally.** Every opening email has a real subject, your real name and business, your postal address and a plain way to
opt out (CAN-SPAM). In the UK, EU and Canada, cold email to people needs a lawful basis or consent first: check before you email there. At
most 50 new pitches a day, and one person at a company at a time.

**Stop rules.** At the first "no" it stops, everywhere, for good. Follow-ups stop the moment a demo is booked, after 3 follow-ups, or 30 days
after the pitch. An unsubscribe goes on a suppression list no skill will email.

**Never invents anything.** No made-up numbers, customers, quotes, results or deadlines. Every figure on the board has a source or says it's
an estimate. Demos are labelled as sample data, and a case study needs the customer's written approval of every word.

**Public business information only.** The researcher and hunter read a company's own site and what people publish for work, never a person's
private life and nothing behind a login. They never guess an email address. A company's private numbers only count if the company gave them to you.

**Not legal, tax or financial advice.** Offers are templates: have a lawyer read your terms once. Money taken up front can have tax consequences, so
ask an accountant. "Validated" means companies paid. It doesn't mean the business will work.

## Files

```
market-researcher/ SKILL.md, board.py, problems.py, whale.example.json
demo-builder/      SKILL.md, demo.py, demo.example.json
whale-hunter/      SKILL.md, hunter.py, pitch.json
pre-sale/          SKILL.md, presale.py
requirements/      SKILL.md, reqs.py
offer-builder/     SKILL.md, offer.py
pricing/           SKILL.md, price.py
follow-up/         SKILL.md, followup.py, templates.json
objection-handler/ SKILL.md, objections.py, objections.json
case-study/        SKILL.md, casestudy.py
launch-planner/    SKILL.md, launch.py
*/test_*.py        unittest suite, offline
```

MIT. Made by [Jake Schincariol](https://opusjake.ai).
