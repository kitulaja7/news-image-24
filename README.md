# news-image-24

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/kitulaja7/news-image-24/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/kitulaja7/news-image-24/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper front page that sums up Tuesday 24 November 2026 in a single
1024×1024 image: 36 stories — three features (four tankers hit mines in the Strait
of Hormuz, Huawei guilty on 10 counts, the Riyadh tower struck again), ten
illustrated tiles, a world map with 13 pins, a UTC timeline of the day, a stat
strip, a colour-coded region bar, a DATE CHECK box naming what was left out and
why, and an ALSO list. Every illustration carries a verification chip showing its
status (REPORTED / OFFICIAL / CONFIRMED / CLAIM) and the news agency it came from,
so the verification is visible on the page itself instead of hidden in small print.

The image is drawn at build time by `render.py` (Pillow, development only) and
committed as `entry.png`. The shipped entrypoint `main.py` uses only the Python
standard library and copies `entry.png` byte-for-byte to `/output/entry.png`,
so the grader's two runs produce identical bytes with no network and no
third-party imports.

## Run it

    python3 render.py        # draw entry.png (development, needs Pillow)
    python3 main.py          # copy entry.png to /output/entry.png

Built for the make.fun bounty: https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124

## Verify

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
    mkdir -p out2 && MAKEFUN_OUTPUT_DIR=out2 python3 main.py
    cmp out/entry.png out2/entry.png && cmp out/entry.png entry.png
