import type { SQLiteDatabase } from 'expo-sqlite';

import type {
  AbilityRow,
  RosterUnit,
  SpearheadDetail,
  SpearheadSummary,
  WeaponRow,
} from './types';

export async function listSpearheads(
  db: SQLiteDatabase,
): Promise<SpearheadSummary[]> {
  return db.getAllAsync<SpearheadSummary>(
    `
    SELECT
      s.id AS id,
      s.slug AS slug,
      s.name AS name,
      f.name AS factionName,
      f.slug AS factionSlug
    FROM spearheads s
    JOIN factions f ON f.id = s.faction_id
    ORDER BY f.name, s.name
    `,
  );
}

async function loadKeywords(
  db: SQLiteDatabase,
  unitTypeId: number,
): Promise<string[]> {
  const rows = await db.getAllAsync<{ name: string }>(
    `
    SELECT k.name AS name
    FROM unit_keywords uk
    JOIN keywords k ON k.id = uk.keyword_id
    WHERE uk.unit_type_id = ?
    ORDER BY k.name
    `,
    [unitTypeId],
  );
  return rows.map((row) => row.name);
}

async function loadWeapons(
  db: SQLiteDatabase,
  unitTypeId: number,
): Promise<WeaponRow[]> {
  const rows = await db.getAllAsync<{
    id: number;
    slug: string;
    kind: 'ranged' | 'melee';
    name: string;
    range_inches: number | null;
    attacks: string;
    hit: number;
    wound: number;
    rend: number;
    damage: string;
    sort_order: number;
  }>(
    `
    SELECT
      id,
      slug,
      kind,
      name,
      range_inches,
      attacks,
      hit,
      wound,
      rend,
      damage,
      sort_order
    FROM weapons
    WHERE unit_type_id = ?
    ORDER BY kind DESC, sort_order
    `,
    [unitTypeId],
  );

  const weapons: WeaponRow[] = [];
  for (const row of rows) {
    const abilityRows = await db.getAllAsync<{ name: string }>(
      `
      SELECT a.name AS name
      FROM weapon_abilities wa
      JOIN abilities a ON a.id = wa.ability_id
      WHERE wa.weapon_id = ?
      ORDER BY wa.sort_order
      `,
      [row.id],
    );

    weapons.push({
      slug: row.slug,
      kind: row.kind,
      name: row.name,
      rangeInches: row.range_inches,
      attacks: row.attacks,
      hit: row.hit,
      wound: row.wound,
      rend: row.rend,
      damage: row.damage,
      sortOrder: row.sort_order,
      abilities: abilityRows.map((ability) => ability.name),
    });
  }

  return weapons;
}

async function loadUnitAbilities(
  db: SQLiteDatabase,
  unitTypeId: number,
): Promise<AbilityRow[]> {
  const rows = await db.getAllAsync<{
    slug: string;
    name: string;
    trigger: string;
    effect: string;
    sort_order: number;
  }>(
    `
    SELECT
      a.slug AS slug,
      a.name AS name,
      a.trigger AS trigger,
      a.effect AS effect,
      ua.sort_order AS sort_order
    FROM unit_abilities ua
    JOIN abilities a ON a.id = ua.ability_id
    WHERE ua.unit_type_id = ?
    ORDER BY ua.sort_order
    `,
    [unitTypeId],
  );

  return rows.map((row) => ({
    slug: row.slug,
    name: row.name,
    trigger: row.trigger,
    effect: row.effect,
    sortOrder: row.sort_order,
  }));
}

async function loadSpearheadAbilities(
  db: SQLiteDatabase,
  spearheadId: number,
  category: string,
): Promise<AbilityRow[]> {
  const rows = await db.getAllAsync<{
    slug: string;
    name: string;
    trigger: string;
    effect: string;
    category: string;
    sort_order: number;
  }>(
    `
    SELECT
      a.slug AS slug,
      a.name AS name,
      a.trigger AS trigger,
      a.effect AS effect,
      sa.category AS category,
      sa.sort_order AS sort_order
    FROM spearhead_abilities sa
    JOIN abilities a ON a.id = sa.ability_id
    WHERE sa.spearhead_id = ? AND sa.category = ?
    ORDER BY sa.sort_order
    `,
    [spearheadId, category],
  );

  return rows.map((row) => ({
    slug: row.slug,
    name: row.name,
    trigger: row.trigger,
    effect: row.effect,
    category: row.category,
    sortOrder: row.sort_order,
  }));
}

export async function getSpearheadDetail(
  db: SQLiteDatabase,
  slug: string,
): Promise<SpearheadDetail | null> {
  const header = await db.getFirstAsync<{
    id: number;
    slug: string;
    name: string;
    factionName: string;
    factionSlug: string;
  }>(
    `
    SELECT
      s.id AS id,
      s.slug AS slug,
      s.name AS name,
      f.name AS factionName,
      f.slug AS factionSlug
    FROM spearheads s
    JOIN factions f ON f.id = s.faction_id
    WHERE s.slug = ?
    `,
    [slug],
  );

  if (!header) {
    return null;
  }

  const unitRows = await db.getAllAsync<{
    id: number;
    sort_order: number;
    is_general: number;
    is_reinforcement: number;
    model_count: number;
    unit_type_id: number;
    unit_type_slug: string;
    unit_type_name: string;
    control: number;
    health: number;
    move: number | string;
    save: number;
  }>(
    `
    SELECT
      su.id AS id,
      su.sort_order AS sort_order,
      su.is_general AS is_general,
      su.is_reinforcement AS is_reinforcement,
      su.model_count AS model_count,
      ut.id AS unit_type_id,
      ut.slug AS unit_type_slug,
      ut.name AS unit_type_name,
      ut.control AS control,
      ut.health AS health,
      ut.move AS move,
      ut.save AS save
    FROM spearhead_units su
    JOIN unit_types ut ON ut.id = su.unit_type_id
    WHERE su.spearhead_id = ?
    ORDER BY su.sort_order
    `,
    [header.id],
  );

  const units: RosterUnit[] = [];
  for (const row of unitRows) {
    const [keywords, weapons, abilities] = await Promise.all([
      loadKeywords(db, row.unit_type_id),
      loadWeapons(db, row.unit_type_id),
      loadUnitAbilities(db, row.unit_type_id),
    ]);

    units.push({
      id: row.id,
      sortOrder: row.sort_order,
      isGeneral: row.is_general === 1,
      isReinforcement: row.is_reinforcement === 1,
      modelCount: row.model_count,
      unitTypeSlug: row.unit_type_slug,
      unitTypeName: row.unit_type_name,
      control: row.control,
      health: row.health,
      move: row.move,
      save: row.save,
      keywords,
      weapons,
      abilities,
    });
  }

  const [battleTraits, regimentAbilities, enhancements] = await Promise.all([
    loadSpearheadAbilities(db, header.id, 'battle_trait'),
    loadSpearheadAbilities(db, header.id, 'regiment'),
    loadSpearheadAbilities(db, header.id, 'enhancement'),
  ]);

  return {
    ...header,
    units,
    battleTraits,
    regimentAbilities,
    enhancements,
  };
}
