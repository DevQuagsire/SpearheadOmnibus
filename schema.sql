-- Spearhead Omnibus reference schema (SQLite)
-- Authoring source: spearhead.json → import via scripts/import_spearhead.py

PRAGMA foreign_keys = ON;

CREATE TABLE factions (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE spearheads (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    faction_id INTEGER NOT NULL REFERENCES factions(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    UNIQUE (faction_id, name)
);

CREATE TABLE unit_types (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    control INTEGER NOT NULL,
    health INTEGER NOT NULL,
    move TEXT NOT NULL,
    save INTEGER NOT NULL
);

CREATE TABLE spearhead_units (
    id INTEGER PRIMARY KEY,
    spearhead_id INTEGER NOT NULL REFERENCES spearheads(id) ON DELETE CASCADE,
    unit_type_id INTEGER NOT NULL REFERENCES unit_types(id) ON DELETE RESTRICT,
    is_general INTEGER NOT NULL DEFAULT 0 CHECK (is_general IN (0, 1)),
    is_reinforcement INTEGER NOT NULL DEFAULT 0 CHECK (is_reinforcement IN (0, 1)),
    model_count INTEGER NOT NULL DEFAULT 1 CHECK (model_count > 0),
    sort_order INTEGER NOT NULL DEFAULT 0
);

-- At most one general per spearhead
CREATE UNIQUE INDEX ux_spearhead_one_general
    ON spearhead_units(spearhead_id)
    WHERE is_general = 1;

CREATE TABLE keywords (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE unit_keywords (
    unit_type_id INTEGER NOT NULL REFERENCES unit_types(id) ON DELETE CASCADE,
    keyword_id INTEGER NOT NULL REFERENCES keywords(id) ON DELETE CASCADE,
    PRIMARY KEY (unit_type_id, keyword_id)
);

CREATE TABLE weapons (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    unit_type_id INTEGER NOT NULL REFERENCES unit_types(id) ON DELETE CASCADE,
    kind TEXT NOT NULL CHECK (kind IN ('ranged', 'melee')),
    name TEXT NOT NULL,
    range_inches INTEGER,
    attacks TEXT NOT NULL,
    hit INTEGER NOT NULL,
    wound INTEGER NOT NULL,
    rend INTEGER NOT NULL,
    damage TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    CHECK (
        (kind = 'ranged' AND range_inches IS NOT NULL)
        OR (kind = 'melee' AND range_inches IS NULL)
    )
);

CREATE TABLE abilities (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    trigger TEXT NOT NULL,
    effect TEXT NOT NULL
);

CREATE TABLE spearhead_abilities (
    id INTEGER PRIMARY KEY,
    spearhead_id INTEGER NOT NULL REFERENCES spearheads(id) ON DELETE CASCADE,
    ability_id INTEGER NOT NULL REFERENCES abilities(id) ON DELETE CASCADE,
    category TEXT NOT NULL CHECK (category IN ('battle_trait', 'regiment', 'enhancement')),
    sort_order INTEGER NOT NULL DEFAULT 0,
    UNIQUE (spearhead_id, ability_id, category)
);

CREATE TABLE unit_abilities (
    id INTEGER PRIMARY KEY,
    unit_type_id INTEGER NOT NULL REFERENCES unit_types(id) ON DELETE CASCADE,
    ability_id INTEGER NOT NULL REFERENCES abilities(id) ON DELETE CASCADE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    UNIQUE (unit_type_id, ability_id)
);

CREATE TABLE weapon_abilities (
    id INTEGER PRIMARY KEY,
    weapon_id INTEGER NOT NULL REFERENCES weapons(id) ON DELETE CASCADE,
    ability_id INTEGER NOT NULL REFERENCES abilities(id) ON DELETE CASCADE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    UNIQUE (weapon_id, ability_id)
);

CREATE INDEX ix_spearheads_faction_id ON spearheads(faction_id);
CREATE INDEX ix_spearhead_units_spearhead_id ON spearhead_units(spearhead_id);
CREATE INDEX ix_spearhead_units_unit_type_id ON spearhead_units(unit_type_id);
CREATE INDEX ix_weapons_unit_type_id ON weapons(unit_type_id);
CREATE INDEX ix_abilities_trigger ON abilities(trigger);
CREATE INDEX ix_keywords_name ON keywords(name);
CREATE INDEX ix_spearhead_abilities_spearhead_id ON spearhead_abilities(spearhead_id);
CREATE INDEX ix_spearhead_abilities_category ON spearhead_abilities(category);
CREATE INDEX ix_unit_abilities_unit_type_id ON unit_abilities(unit_type_id);
CREATE INDEX ix_weapon_abilities_weapon_id ON weapon_abilities(weapon_id);
