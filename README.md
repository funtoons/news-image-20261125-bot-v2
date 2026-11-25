# The World in One Page — 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/funtoons/news-image-20261125-bot-v2/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/funtoons/news-image-20261125-bot-v2/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the [make.fun bounty "Sum up 25 November's world news in one image"](https://make.fun/bounty/news-image-20261125): a program that draws a one-page newspaper summing up Wednesday 25 November 2026.

## What it draws

- **40 verified stories** (10 top stories + 30 ALSO ON), every one checked against two or more independent outlets for 25 November 2026, with sources named on each story.
- A **dotted world map** ("WHERE IT HAPPENED") with numbered pins matching the stories.
- **The Day in Numbers** (6 figures), a **UTC timeline**, region tabs with counts, and a **Date-Check Audit** listing stories that were checked and deliberately left out because they happened on another day (ICJ Myanmar ruling 19 Nov, COP31 collapse 22 Nov, Senegal CAS ruling 24 Nov, Zambia treason committal 23 Nov, Real Madrid 5-1 PSV 24 Nov).
- Top stories include the Phala Phala ruling in South Africa, the Shenzhou-24 launch carrying Pakistan's first astronaut, the Australia–Solomon Islands treaty, tankers hit by mines in the Strait of Hormuz, and the Cartagena hostage rescue.

## Run

```sh
python3 main.py
```

The program is pure Python standard library (no Pillow, no network, no randomness, no timestamps). It writes `entry.png` (1024x1024, under 1 MiB) to the directory in `MAKEFUN_OUTPUT_DIR`, or `/output` by default. Two runs write byte-identical files.
