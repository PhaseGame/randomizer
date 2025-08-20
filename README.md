# [@myballs](https://t.me/myballs) randomizer
Prize selection toolkit for @myballs events. Deterministic with a seed.

## Random Seed (🎲 dice-based)
The random seed used for selecting the winners is determined during a livestream on [@balls_tv](https://t.me/balls_tv). We roll 5 dice emojis 🎲 to generate a 5-digit number, which is used as the seed. Telegram guarantees the randomness of dice results.

- Seed is required (taken from the livestream dice rolls).
- Output file: `winners.csv` is written to the event’s directory.
- Example:
```bash
python run.py durov-glasses-20-aug --seed 461970
```

## Events
### durov-glasses-20-aug
Durov Glasses + Starz giveaway.

Run command:
```bash
python run.py durov-glasses-20-aug --seed {SEED}
```

## Reproducibility
- Using the same `--seed` with the same `data.csv` yields identical winners.
