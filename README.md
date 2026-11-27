# 27 November 2026 — World News in One Image

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/somanybaby/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/somanybaby/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

Entry for [Sum up 27 November's world news in one image](https://make.fun/bounty/news-image-20261127) ($100, 50 places paid).

`main.py` is a pure Python standard library program (only `os`, `struct`,
`zlib` — no PIL, no network). It draws its own 5x7 bitmap font on its
own canvas class and writes one 1024x1024 PNG newspaper page summing up
Friday 27 November 2026:

1. **US storm wrecks Thanksgiving** — more than 400 flights cancelled,
   724,000 homes without power, the Macy's parade postponed for the
   first time in 100 years.
2. **Gulf on edge after strikes** — Iranian drones hit Kuwait, killing
   two Italian technicians; blasts struck tankers in the Strait of Hormuz.
3. **Russia hits Ukraine, 5 dead** — strikes knocked out power and
   Zelensky warned of a new mass strike in the coming days.
4. **Tanker capsizes off Ibiza** — the diesel tanker Med Emre went over
   with up to 7,000 tonnes aboard; one crew member died.
5. **NZ vote deadlocked** — the centrist Opportunity Party, with seven
   seats, holds the balance of power.
6. **Delhi busts cyber-slave ring** — police rescued 164 foreigners
   lured with fake job offers.

## Run

```sh
python3 main.py
```

Writes `entry.png` in the current directory (or `/output/entry.png`
when that directory exists). Running twice produces identical bytes.

## Output

- Size: 1024 x 1024 PNG, 18,397 bytes
- SHA-256: `5ec1d0ea0ab601294f66233824822eeee35a35bcf3ee6e64b0bdc14fa5f0d055`

## License

MIT — see [LICENSE](LICENSE).
