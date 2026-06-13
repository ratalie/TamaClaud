# Contributing to TamaClaud 🥚

Thanks for wanting to help keep TamaClaud alive! Here's how to contribute.

## Ideas welcome

- New languages (i18n)
- New sprites or states
- VS Code extension (WIP — help wanted!)
- Sound effects on death/resurrection
- Evolution system (sprite changes after X calls without dying)
- Better Windows support

## How to contribute

1. Fork the repo
2. Create a branch: `git checkout -b my-feature`
3. Make your changes
4. Test locally: `python3 tamaclaud.py --status`
5. Commit: `git commit -m "feat: description"`
6. Push: `git push origin my-feature`
7. Open a Pull Request

## Adding a new language

1. Add your translation to the `TRANSLATIONS` dict in `tamaclaud.py`
2. Create `docs/README.xx.md` for your language
3. Add a badge to the main `README.md`

## Guidelines

- Keep it one file, zero dependencies (Python stdlib only)
- Test on both Windows and macOS/Linux if possible
- Have fun with it — this is a Tamagotchi, not enterprise software

## Issues

Found a bug? Have an idea? [Open an issue](https://github.com/ratalie/TamaClaud/issues).
