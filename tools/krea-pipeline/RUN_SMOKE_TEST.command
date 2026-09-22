#!/bin/bash
# CTD — Krea pipeline smoke test: one WheelsDerail image (~$0.15)
cd "$(dirname "$0")"
echo "Installing deps (first run only)..."
pip3 install -q requests pyyaml 2>/dev/null || python3 -m pip install -q requests pyyaml
echo
echo "=== SMOKE TEST: 1 image, CTD_AI_WheelsDerail ==="
python3 generate.py CTD_AI_WheelsDerail -n 1
status=$?
echo
if [ $status -eq 0 ]; then
  echo "✓ Done. Check the renders folder."
  open renders 2>/dev/null
else
  echo "✗ Something failed — screenshot this window and show Claude."
fi
echo
read -p "Press Enter to close..."
