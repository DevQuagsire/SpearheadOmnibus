export type SpearheadSummary = {
  id: number;
  slug: string;
  name: string;
  factionName: string;
  factionSlug: string;
};

export type AbilityRow = {
  slug: string;
  name: string;
  trigger: string;
  effect: string;
  category?: string;
  sortOrder: number;
};

export type WeaponRow = {
  slug: string;
  kind: 'ranged' | 'melee';
  name: string;
  rangeInches: number | null;
  attacks: string;
  hit: number;
  wound: number;
  rend: number;
  damage: string;
  sortOrder: number;
  abilities: string[];
};

export type RosterUnit = {
  id: number;
  sortOrder: number;
  isGeneral: boolean;
  isReinforcement: boolean;
  modelCount: number;
  unitTypeSlug: string;
  unitTypeName: string;
  control: number;
  health: number;
  move: number | string;
  save: number;
  keywords: string[];
  weapons: WeaponRow[];
  abilities: AbilityRow[];
};

export type SpearheadDetail = {
  id: number;
  slug: string;
  name: string;
  factionName: string;
  factionSlug: string;
  units: RosterUnit[];
  battleTraits: AbilityRow[];
  regimentAbilities: AbilityRow[];
  enhancements: AbilityRow[];
};
