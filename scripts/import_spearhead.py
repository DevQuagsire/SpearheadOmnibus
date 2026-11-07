#!/usr/bin/env python3
"""Import spearhead.json into a SQLite reference database."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "spearhead.json"
DEFAULT_SCHEMA = ROOT / "schema.sql"
DEFAULT_DB = ROOT / "dist" / "spearhead.sqlite"


def as_text(value: Any) -> str:
    return str(value)


def slugify(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "ability"


def canonicalize_weapon_rule(name: str) -> str:
    """Normalize spacing/case so Charge(+1 Damage) and Charge (+1 Damage) share a slug."""
    cleaned = " ".join(name.strip().split())
    cleaned = cleaned.replace(" (", "(")
    # Canonical title-ish form for Anti-* rules
    if cleaned.lower().startswith("anti-"):
        body = cleaned[5:]
        cleaned = "Anti-" + body[:1].upper() + body[1:]
    elif cleaned.lower().startswith("charge("):
        cleaned = "Charge" + cleaned[6:]
    elif cleaned.lower().startswith("crit("):
        cleaned = "Crit" + cleaned[4:]
    return cleaned


def normalize_ability(ability: Any) -> dict[str, str]:
    """Accept full ability objects or weapon-rule strings like Crit(Mortal)."""
    if isinstance(ability, str):
        name = canonicalize_weapon_rule(ability)
        return {
            "slug": f"weapon-rule-{slugify(name)}",
            "name": name,
            "trigger": "Weapon Rule",
            "effect": name,
        }
    if not isinstance(ability, dict):
        raise TypeError(f"Unsupported ability value: {ability!r}")
    required = ("slug", "name", "trigger", "effect")
    missing = [key for key in required if key not in ability]
    if missing:
        raise KeyError(f"Ability missing keys {missing}: {ability!r}")
    return {
        "slug": str(ability["slug"]),
        "name": str(ability["name"]),
        "trigger": str(ability["trigger"]),
        "effect": str(ability["effect"]),
    }


def upsert_ability(conn: sqlite3.Connection, ability: Any) -> int:
    normalized = normalize_ability(ability)
    slug = normalized["slug"]
    existing = conn.execute(
        "SELECT id, name, trigger, effect FROM abilities WHERE slug = ?",
        (slug,),
    ).fetchone()
    if existing is not None:
        _, name, trigger, effect = existing
        same = (
            name == normalized["name"]
            and trigger == normalized["trigger"]
            and effect == normalized["effect"]
        )
        if not same:
            raise ValueError(
                f"Ability slug '{slug}' is reused with different content. "
                "Give each distinct ability a unique slug."
            )
        return int(existing[0])

    conn.execute(
        """
        INSERT INTO abilities (slug, name, trigger, effect)
        VALUES (?, ?, ?, ?)
        """,
        (
            slug,
            normalized["name"],
            normalized["trigger"],
            normalized["effect"],
        ),
    )
    row = conn.execute("SELECT id FROM abilities WHERE slug = ?", (slug,)).fetchone()
    assert row is not None
    return int(row[0])


def upsert_keyword(conn: sqlite3.Connection, name: str) -> int:
    conn.execute(
        "INSERT INTO keywords (name) VALUES (?) ON CONFLICT(name) DO NOTHING",
        (name,),
    )
    row = conn.execute("SELECT id FROM keywords WHERE name = ?", (name,)).fetchone()
    assert row is not None
    return int(row[0])


def import_weapon(
    conn: sqlite3.Connection,
    unit_type_id: int,
    weapon: dict[str, Any],
    kind: str,
    sort_order: int,
) -> None:
    range_inches = weapon.get("range") if kind == "ranged" else None
    conn.execute(
        """
        INSERT INTO weapons (
            slug, unit_type_id, kind, name, range_inches,
            attacks, hit, wound, rend, damage, sort_order
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            unit_type_id = excluded.unit_type_id,
            kind = excluded.kind,
            name = excluded.name,
            range_inches = excluded.range_inches,
            attacks = excluded.attacks,
            hit = excluded.hit,
            wound = excluded.wound,
            rend = excluded.rend,
            damage = excluded.damage,
            sort_order = excluded.sort_order
        """,
        (
            weapon["slug"],
            unit_type_id,
            kind,
            weapon["name"],
            range_inches,
            as_text(weapon["attacks"]),
            int(weapon["hit"]),
            int(weapon["wound"]),
            int(weapon["rend"]),
            as_text(weapon["damage"]),
            sort_order,
        ),
    )
    weapon_id = int(
        conn.execute(
            "SELECT id FROM weapons WHERE slug = ?", (weapon["slug"],)
        ).fetchone()[0]
    )

    conn.execute("DELETE FROM weapon_abilities WHERE weapon_id = ?", (weapon_id,))
    for index, ability in enumerate(weapon.get("abilities") or []):
        ability_id = upsert_ability(conn, ability)
        conn.execute(
            """
            INSERT INTO weapon_abilities (weapon_id, ability_id, sort_order)
            VALUES (?, ?, ?)
            """,
            (weapon_id, ability_id, index),
        )


def import_unit_type(conn: sqlite3.Connection, unit_type: dict[str, Any]) -> int:
    stats = unit_type["dataSlateStats"]
    slug = unit_type["slug"]
    conn.execute(
        """
        INSERT INTO unit_types (slug, name, control, health, move, save)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            name = excluded.name,
            control = excluded.control,
            health = excluded.health,
            move = excluded.move,
            save = excluded.save
        """,
        (
            slug,
            unit_type["name"],
            int(stats["control"]),
            int(stats["health"]),
            as_text(stats["move"]),
            int(stats["save"]),
        ),
    )
    unit_type_id = int(
        conn.execute("SELECT id FROM unit_types WHERE slug = ?", (slug,)).fetchone()[0]
    )

    conn.execute("DELETE FROM unit_keywords WHERE unit_type_id = ?", (unit_type_id,))
    for keyword in unit_type.get("keywords") or []:
        keyword_id = upsert_keyword(conn, keyword)
        conn.execute(
            """
            INSERT INTO unit_keywords (unit_type_id, keyword_id)
            VALUES (?, ?)
            """,
            (unit_type_id, keyword_id),
        )

    conn.execute("DELETE FROM weapons WHERE unit_type_id = ?", (unit_type_id,))
    for index, weapon in enumerate(unit_type.get("rangedWeapons") or []):
        import_weapon(conn, unit_type_id, weapon, "ranged", index)
    for index, weapon in enumerate(unit_type.get("meleeWeapons") or []):
        import_weapon(conn, unit_type_id, weapon, "melee", index)

    conn.execute("DELETE FROM unit_abilities WHERE unit_type_id = ?", (unit_type_id,))
    for index, ability in enumerate(unit_type.get("abilities") or []):
        ability_id = upsert_ability(conn, ability)
        conn.execute(
            """
            INSERT INTO unit_abilities (unit_type_id, ability_id, sort_order)
            VALUES (?, ?, ?)
            """,
            (unit_type_id, ability_id, index),
        )

    return unit_type_id


def import_spearhead_abilities(
    conn: sqlite3.Connection,
    spearhead_id: int,
    abilities: list[dict[str, Any]],
    category: str,
) -> None:
    for index, ability in enumerate(abilities):
        ability_id = upsert_ability(conn, ability)
        conn.execute(
            """
            INSERT INTO spearhead_abilities (
                spearhead_id, ability_id, category, sort_order
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(spearhead_id, ability_id, category) DO UPDATE SET
                sort_order = excluded.sort_order
            """,
            (spearhead_id, ability_id, category, index),
        )


def validate_spearhead(spearhead: dict[str, Any]) -> None:
    generals = [u for u in spearhead["units"] if u.get("isGeneral")]
    if len(generals) != 1:
        raise ValueError(
            f"Spearhead '{spearhead['slug']}' must have exactly one general, "
            f"found {len(generals)}"
        )


def import_data(conn: sqlite3.Connection, data: dict[str, Any]) -> None:
    faction_ids: dict[str, int] = {}
    for faction in data["factions"]:
        conn.execute(
            """
            INSERT INTO factions (slug, name)
            VALUES (?, ?)
            ON CONFLICT(slug) DO UPDATE SET name = excluded.name
            """,
            (faction["slug"], faction["name"]),
        )
        faction_ids[faction["slug"]] = int(
            conn.execute(
                "SELECT id FROM factions WHERE slug = ?", (faction["slug"],)
            ).fetchone()[0]
        )

    unit_type_ids: dict[str, int] = {}
    for unit_type in data["unitTypes"]:
        unit_type_ids[unit_type["slug"]] = import_unit_type(conn, unit_type)

    for spearhead in data["spearheads"]:
        validate_spearhead(spearhead)
        faction_slug = spearhead["factionSlug"]
        if faction_slug not in faction_ids:
            raise KeyError(f"Unknown factionSlug: {faction_slug}")

        conn.execute(
            """
            INSERT INTO spearheads (slug, faction_id, name)
            VALUES (?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                faction_id = excluded.faction_id,
                name = excluded.name
            """,
            (spearhead["slug"], faction_ids[faction_slug], spearhead["name"]),
        )
        spearhead_id = int(
            conn.execute(
                "SELECT id FROM spearheads WHERE slug = ?", (spearhead["slug"],)
            ).fetchone()[0]
        )

        conn.execute(
            "DELETE FROM spearhead_units WHERE spearhead_id = ?", (spearhead_id,)
        )
        conn.execute(
            "DELETE FROM spearhead_abilities WHERE spearhead_id = ?", (spearhead_id,)
        )

        for index, unit in enumerate(spearhead["units"]):
            unit_type_slug = unit["unitTypeSlug"]
            if unit_type_slug not in unit_type_ids:
                raise KeyError(f"Unknown unitTypeSlug: {unit_type_slug}")
            conn.execute(
                """
                INSERT INTO spearhead_units (
                    spearhead_id, unit_type_id, is_general,
                    is_reinforcement, model_count, sort_order
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    spearhead_id,
                    unit_type_ids[unit_type_slug],
                    1 if unit.get("isGeneral") else 0,
                    1 if unit.get("isReinforcement") else 0,
                    int(unit.get("modelCount", 1)),
                    index,
                ),
            )

        import_spearhead_abilities(
            conn, spearhead_id, spearhead.get("battleTraits") or [], "battle_trait"
        )
        import_spearhead_abilities(
            conn, spearhead_id, spearhead.get("regimentAbilities") or [], "regiment"
        )
        import_spearhead_abilities(
            conn, spearhead_id, spearhead.get("enhancements") or [], "enhancement"
        )


def rebuild_database(json_path: Path, schema_path: Path, db_path: Path) -> None:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    schema_sql = schema_path.read_text(encoding="utf-8")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(schema_sql)
        import_data(conn, data)
        conn.commit()
    finally:
        conn.close()


def print_summary(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        counts = {
            table: conn.execute(f"SELECT COUNT(*) AS c FROM {table}").fetchone()["c"]
            for table in (
                "factions",
                "spearheads",
                "unit_types",
                "spearhead_units",
                "weapons",
                "abilities",
                "spearhead_abilities",
                "unit_abilities",
                "keywords",
            )
        }
        reuse = conn.execute(
            """
            SELECT ut.slug, COUNT(DISTINCT su.spearhead_id) AS spearhead_count
            FROM unit_types ut
            JOIN spearhead_units su ON su.unit_type_id = ut.id
            GROUP BY ut.id
            HAVING spearhead_count > 1
            """
        ).fetchall()
        print(f"Wrote {db_path}")
        for table, count in counts.items():
            print(f"  {table}: {count}")
        if reuse:
            print("Unit type reuse across spearheads:")
            for row in reuse:
                print(f"  {row['slug']}: {row['spearhead_count']} spearheads")
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = parser.parse_args(argv)

    rebuild_database(args.json, args.schema, args.db)
    print_summary(args.db)
    return 0


if __name__ == "__main__":
    sys.exit(main())
