# CTD — Production Report Tools

Tooling behind the *Close to Disaster* GEN AI production reports published at
[sachdm/ctd-ai-reports](https://github.com/sachdm/ctd-ai-reports).

All report figures come from **read-only** pulls of the CTD Airtable base
(`appFVGyWTPCqLcpvm` — GEN AI SHOTCODES, GEN AI ASSETS, GEN AI REPORTS).
Nothing here writes to the base.

## What's here

```
scripts/
  build_ios.py              Master Report PDF generator (ReportLab, iOS-style cards)
tools/
  krea-pipeline/
    generate.py             Batch shot generator — Krea API (Nano Banana Pro)
    shots.yaml              Locked prompt blocks + per-shot briefs
    RUN_SMOKE_TEST.command  One-image test run (~$0.15)
    README.md               Setup and daily use
.gitignore                  Blocks API keys, media, raw Airtable dumps
```

## Master Report PDF

```
pip install reportlab
python3 scripts/build_ios.py            # writes reports/CTD_AI_Master_Report.pdf
CTD_PDF_OUT=out.pdf python3 scripts/build_ios.py
```

The figures are set inline in `build_ios.py` (July 23 snapshot). To refresh,
re-run the Airtable queries listed in the report's *Method & sources* section
and update the values.

## Krea pipeline

See `tools/krea-pipeline/README.md`. Needs `KREA_API_KEY` in the environment
or a git-ignored `tools/krea-pipeline/.krea_key`. **Never commit the key.**

## Report refresh workflow (Aug 14 / Aug 31 rebuilds)

The later rebuilds were run as Claude Cowork sessions rather than standalone
scripts:

1. Pull live tables from the CTD Airtable base (Airtable connector).
2. Export to the `ctd_*.csv` files and `data.json` in the reports repo.
3. Recompute KPIs (AI share per cut, generate-to-use, re-spins, pipeline).
4. Re-render the HTML pages and cross-check figures between pages.
5. Regenerate the PDF and commit to `sachdm/ctd-ai-reports`.

The session scripts from those rebuilds were not found on disk and are not in
this repo yet.

## Rules

- Read-only against Airtable.
- No credentials in the repo — rotate any key that gets committed.
- No `.mov` / `.mp4` media in version control.
