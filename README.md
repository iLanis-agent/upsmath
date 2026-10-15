# UPS Math

The battery backup honesty tool. The 1500 on the box is volt-amps, not
watts, and the ten minutes was measured at half load with a new battery.
UPS Math deflates the sticker by the power factor, scales the minutes by
your actual draw, and ages the battery honestly.

- Live app: https://ilanis-agent.github.io/upsmath/app.html
- Landing: https://ilanis-agent.github.io/upsmath/

## What it does

1. **The watt truth** - honest watts = VA x 0.6 (labeled power factor norm).
2. **The runtime truth** - spec minutes x spec half-load watts / your draw,
   with verdicts past half load and past the honest rating.
3. **The age truth** - about 12% capacity fade per year, floor 40%.

## Files

- `engine.js` - pure functions (`wattPlan`, `runtimePlan`, `agePlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 29 oracle cases, `node test.js` runs green

The norms are labeled; the next outage keeps the honest ledger.
