# Spearhead Companion

Expo React Native app that reads the bundled `spearhead.sqlite` rules database.

## Screens

1. **Spearhead Armies** — button per army from SQLite
2. **Army Details** — roster, weapons, battle traits, regiment abilities, enhancements

## Run

From this directory:

```bash
npm start
```

Then open iOS Simulator, Android emulator, or Expo Go.

## Sync the rules database

After regenerating the repo-root SQLite file:

```bash
# from repo root
python3 scripts/import_spearhead.py
cp dist/spearhead.sqlite apps/spearhead-companion/assets/databases/spearhead.sqlite
```

Or from this app folder:

```bash
npm run sync-db
```

Delete the app from the simulator/device (or clear its data) after replacing the asset if an older `spearhead.sqlite` was already imported — `expo-sqlite` only copies the asset when the destination DB is missing.
