# Spearhead Omnibus

Reference data for Age of Sigmar Spearhead armies, authored as JSON and compiled to SQLite for mobile apps.

`Wallsmasher Stomp` is real reference data. `Boulderhead Raid` is a small fixture that reuses `mancrusher-gargant` so the schema can prove cross-spearhead unit-type sharing and ability categories.

## Layout

| Path | Role |
|---|---|
| [`spearhead.json`](spearhead.json) | Authoring source (factions, shared unit types, spearhead rosters) |
| [`schema.sql`](schema.sql) | Normalized SQLite schema |
| [`scripts/import_spearhead.py`](scripts/import_spearhead.py) | JSON → SQLite importer |
| [`dist/spearhead.sqlite`](dist/spearhead.sqlite) | Bundled reference database |
| [`apps/spearhead-companion`](apps/spearhead-companion) | Expo React Native companion app |

## Build the database

Requires Python 3.10+ (stdlib only):

```bash
python3 scripts/import_spearhead.py
```

Options:

```bash
python3 scripts/import_spearhead.py \
  --json spearhead.json \
  --schema schema.sql \
  --db dist/spearhead.sqlite
```

## React Native companion

```bash
cd apps/spearhead-companion
npm start
```

The app lists each spearhead as a button and opens a detail screen backed by `assets/databases/spearhead.sqlite`. Sync that asset after rebuilding the DB:

```bash
python3 scripts/import_spearhead.py
cd apps/spearhead-companion && npm run sync-db
```

## Mobile app loading

Ship `dist/spearhead.sqlite` as a read-only asset. On first launch (or when the asset version changes), copy it into the app sandbox, then open it with your platform SQLite stack.

### iOS (Swift / GRDB or SQLite.swift)

1. Add `spearhead.sqlite` to the app bundle.
2. Copy from bundle → Application Support if missing or outdated.
3. Open the copied file read-only (or read-write if you later add user tables in a separate DB).

```swift
let bundleURL = Bundle.main.url(forResource: "spearhead", withExtension: "sqlite")!
let support = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
let dest = support.appendingPathComponent("spearhead.sqlite")
if !FileManager.default.fileExists(atPath: dest.path) {
    try FileManager.default.createDirectory(at: support, withIntermediateDirectories: true)
    try FileManager.default.copyItem(at: bundleURL, to: dest)
}
// open dest with GRDB / SQLite.swift
```

### Android (Room / SQLDelight / raw SQLiteOpenHelper)

1. Put `spearhead.sqlite` in `assets/`.
2. On first open, copy assets → `context.getDatabasePath("spearhead.sqlite")`.
3. Point Room/SQLDelight at that path, or use `SQLiteDatabase.openDatabase(..., OPEN_READONLY)`.

```kotlin
val outFile = context.getDatabasePath("spearhead.sqlite")
if (!outFile.exists()) {
    outFile.parentFile?.mkdirs()
    context.assets.open("spearhead.sqlite").use { input ->
        outFile.outputStream().use { output -> input.copyTo(output) }
    }
}
```

### Flutter (sqflite / drift)

1. Add the file under `assets/` and declare it in `pubspec.yaml`.
2. Copy from assets into `getDatabasesPath()` before opening.

Prefer a **rules DB** (this file) separate from any **user DB** (saved lists, wound trackers). Query joins against `unit_types`, `weapons`, and `*_abilities`; do not parse `spearhead.json` at runtime in production.

## Useful queries

Spearheads for a faction:

```sql
SELECT s.slug, s.name
FROM spearheads s
JOIN factions f ON f.id = s.faction_id
WHERE f.slug = 'sons-of-behemat'
ORDER BY s.name;
```

Roster with datasheet stats:

```sql
SELECT su.sort_order, ut.name, su.is_general, su.is_reinforcement,
       ut.control, ut.health, ut.move, ut.save
FROM spearhead_units su
JOIN unit_types ut ON ut.id = su.unit_type_id
JOIN spearheads s ON s.id = su.spearhead_id
WHERE s.slug = 'wallsmasher-stomp'
ORDER BY su.sort_order;
```

Enhancements for a spearhead:

```sql
SELECT a.name, a.trigger, a.effect
FROM spearhead_abilities sa
JOIN abilities a ON a.id = sa.ability_id
JOIN spearheads s ON s.id = sa.spearhead_id
WHERE s.slug = 'wallsmasher-stomp' AND sa.category = 'enhancement'
ORDER BY sa.sort_order;
```
