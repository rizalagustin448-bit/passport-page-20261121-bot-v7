# Republic of Havnar — Passport Page of a Country That Isn't There

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/rizalagustin448-bit/passport-page-20261121-bot-v7/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/rizalagustin448-bit/passport-page-20261121-bot-v7/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

An invented passport spread for the **Republic of Havnar**, a tidal
harbour republic whose only way in is a ferry through a tide gate.

- **Data page:** portrait of Sanna Eide Berg, harbour pilot, born
  Havnar; bilingual labels; document No. HV 2024 020715; issued 08 APR 2024,
  expires 08 APR 2034; machine-readable zone with valid ICAO check digits;
  height, eyes, next of kin; a six-row tide table for the Havnar Gate,
  Aug 2025; handwritten marginalia — "Gate closes 17:40 sharp".
- **Visa page:** eight departure/arrival stamps from neighbouring
  Brightholm and Skerry Sound (May 2024 – Jan 2025) — every stamp after
  the issue date, trips that open and close in the right order — plus a
  Port Authority stamp (12 Aug 2025) overlapping the visa-condition box.
- **The telling details:** a red HARBOUR PILOT'S PERMIT (season 2026/27,
  route Havnar — Skerry — Brighthelm), a teal LICENCE RENEWED stamp,
  and a VISA CONDITION box — entry by ferry only, tide gate closes
  17:40 sharp, holder must carry a tide table, slack water only — with
  the pilot licence HV-P-4417, valid to 31 Dec 2027, printed inside it.

## How it runs

`main.py` (Python 3.13, standard library only) copies the pre-rendered
`entry.png` (1024×1024) to `$MAKEFUN_OUTPUT_DIR/entry.png`. The image is
drawn offline with Pillow; the sandbox installs nothing, so the entrypoint
imports nothing beyond `os`, `shutil`, `struct`, `pathlib`.

## License

MIT — see LICENSE.
