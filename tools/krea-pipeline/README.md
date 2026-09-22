# CTD shot iterator (Krea / Nano Banana Pro)

Batch-generates your Lac-Mégantic shots through Krea's API so you can run
4–8 variations per shot in one command instead of pasting prompts one at a
time.

## Setup (once)

1. Get an API key: krea.ai → your workspace → **API Tokens** → create key.
   (API usage bills separately from your subscription — top up balance in
   the same screen. Nano Banana Pro costs $0.15 per 1K/2K image, $0.30 for 4K.)
2. In Terminal:

   ```
   cd krea-pipeline
   pip install requests pyyaml
   export KREA_API_KEY=paste_your_key_here
   ```

## Daily use

```
python generate.py --list                    # preview all composed prompts
python generate.py CTD_AI_WheelsDerail       # run one shot (4 variations)
python generate.py CTD_AI_WheelsDerail -n 8  # more iterations
python generate.py                           # run every shot
python generate.py --ref livery.png          # lock livery with a reference image
python generate.py --resolution 4K CTD_AI_LMR_Outskirts01
```

Results land in `renders/<SHOT_CODE>/`, and `renders/contact_sheet.html`
rebuilds after every run — open it in a browser to review all variations
side by side with their prompts.

## The important file: shots.yaml

- **blocks** — your locked language. `TRAIN` is the livery/consist block,
  `FIRE`, `NIGHT`, `STYLE`. Edit once, every shot inherits it.
- **shots** — each shot's brief with `{TRAIN}`-style placeholders.
  Add new shots by copying an entry.

## The livery reference trick

Download your approved livery frame from Krea, save it as `livery.png` in
this folder, then run everything with `--ref livery.png`. Nano Banana Pro
will match the locomotive to that image — far more consistent than text.

## Notes

- Generations you make via API also appear in your Krea assets.
- If a run stops with "out of API credits", top up in API settings.
- Keep downloading your keepers — never leave the only copy in the browser.
