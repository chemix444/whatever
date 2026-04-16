# whatever

A tiny terminal typing-speed test. No dependencies beyond the Python stdlib.

## Usage

```
python whatever.py                # 15-word prompt
python whatever.py --words 30     # longer prompt
python whatever.py --seed 7       # deterministic prompt
```

Type the prompt as shown, hit Enter, and you'll see your WPM, accuracy, and
elapsed time. WPM uses the standard "5 characters = 1 word" definition and
counts only characters typed correctly at the same position as the target.

## Tests

```
python -m pytest
```
