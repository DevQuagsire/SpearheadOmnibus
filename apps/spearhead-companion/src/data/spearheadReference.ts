export type ReferenceBlock =
  | { kind: 'paragraph'; text: string }
  | { kind: 'bullets'; items: string[] }
  | {
      kind: 'ability';
      name: string;
      timing?: string;
      declare?: string;
      effect: string;
      keywords?: string;
    }
  | { kind: 'named'; name: string; text: string }
  | { kind: 'phases'; phases: string[] };

export type ReferenceSection = {
  slug: string;
  title: string;
  blocks: ReferenceBlock[];
};

/** Official Spearhead Reference card content (eng 24.09). */
export const spearheadReferenceSections: ReferenceSection[] = [
  {
    slug: 'pre-battle-sequence',
    title: 'Pre-Battle Sequence',
    blocks: [
      {
        kind: 'bullets',
        items: [
          'Roll off. Winner chooses who is attacker and who is defender.',
          'Attacker picks regiment ability and enhancement, then defender does so.',
          'Defender chooses Aqshy or Ghyran side of realm battlefield.',
          'Defender picks deployment map (horizontal or diagonal) and chooses which territory is theirs.',
          'Defender sets up 1 large and 1 small terrain feature. Then attacker does the same. Each terrain feature must be set up wholly within friendly territory, more than 6" from all other terrain features and more than 3" from both long battlefield edges and enemy territory. Terrain features cannot be set up on objectives.',
        ],
      },
    ],
  },
  {
    slug: 'deployment',
    title: 'Deployment',
    blocks: [
      {
        kind: 'paragraph',
        text: 'Attacker sets up their army first, followed by the defender. Each unit must be set up wholly within friendly territory and more than 6" from enemy territory.',
      },
    ],
  },
  {
    slug: 'start-of-battle-round',
    title: 'Start of Battle Round Sequence',
    blocks: [
      {
        kind: 'bullets',
        items: [
          'First battle round: attacker chooses who takes the first turn. Later battle rounds: players make a priority roll (Core Rules, 12.0).',
          'Determine underdog (Core Rules, 12.0).',
          'Draw twist card.',
          'Players draw battle tactic cards.',
          'Start of Battle Round abilities are used.',
        ],
      },
    ],
  },
  {
    slug: 'seizing-the-initiative',
    title: 'Seizing the Initiative',
    blocks: [
      {
        kind: 'paragraph',
        text: 'If the player who went second in the previous battle round wins the priority roll and chooses to go first in the current battle round, they do not draw any battle tactic cards for that battle round unless they are the underdog and the difference in victory points between the players is 5 or more.',
      },
    ],
  },
  {
    slug: 'battle-tactics-cards',
    title: 'Battle Tactics Cards',
    blocks: [
      {
        kind: 'bullets',
        items: [
          'Start of first battle round: draw 3 battle tactic cards.',
          'Start of second or later battle round: discard any battle tactic cards in your hand if you wish. Then if you have less than 3 battle tactic cards in your hand, keep drawing them until you have 3.',
        ],
      },
    ],
  },
  {
    slug: 'victory-points',
    title: 'Victory Points',
    blocks: [
      {
        kind: 'paragraph',
        text: 'At the end of each of your turns:',
      },
      {
        kind: 'bullets',
        items: [
          'Score 1 victory point if you control at least one objective.',
          'Score 1 victory point if you control two or more objectives.',
          'Score 1 victory point if you control more objectives than your opponent.',
          'Score 1 victory point for each battle tactic you completed this turn.',
        ],
      },
    ],
  },
  {
    slug: 'call-for-reinforcements',
    title: 'Call for Reinforcements',
    blocks: [
      {
        kind: 'ability',
        name: 'Call for Reinforcements',
        timing: 'Once Per Turn, Your Movement Phase',
        declare: 'Pick a friendly Reinforcements unit that has been destroyed.',
        effect:
          'Set up an identical replacement unit on the battlefield, wholly within friendly territory, wholly within 6" of the battlefield edge and not in combat. Each Reinforcements unit can only be replaced once. Replacement units cannot themselves be replaced.',
        keywords: 'Core',
      },
    ],
  },
  {
    slug: 'terrain',
    title: 'Terrain',
    blocks: [
      {
        kind: 'named',
        name: 'Large Terrain Feature',
        text: 'Cover, Obscuring, Unstable',
      },
      {
        kind: 'named',
        name: 'Small Terrain Feature',
        text: 'Cover, Unstable',
      },
      {
        kind: 'named',
        name: 'Cover',
        text: 'Subtract 1 from hit rolls for attacks that target a unit that is behind or wholly on this terrain feature, unless that unit charged or has the Fly keyword.',
      },
      {
        kind: 'named',
        name: 'Obscuring',
        text: 'A unit cannot be targeted by shooting attacks if it is behind or wholly on this terrain feature, unless it has the Fly keyword.',
      },
      {
        kind: 'named',
        name: 'Unstable',
        text: 'Models can move across but cannot be set up on or end any type of move on any part of this terrain feature that is more than 1" tall.',
      },
    ],
  },
  {
    slug: 'universal-core-abilities',
    title: 'Universal Core Abilities',
    blocks: [
      {
        kind: 'ability',
        name: 'Normal Move',
        timing: 'Your Movement Phase',
        declare: 'Pick a friendly unit that is not in combat to use this ability.',
        effect:
          'That unit can move a distance up to its Move characteristic. That unit cannot move into combat during any part of that move.',
        keywords: 'Core, Move',
      },
      {
        kind: 'ability',
        name: 'Run',
        timing: 'Your Movement Phase',
        declare: 'Pick a friendly unit that is not in combat to use this ability.',
        effect:
          'Make a run roll of D6. That unit can move a distance up to its Move characteristic added to the run roll. That unit cannot move into combat during any part of that move.',
        keywords: 'Core, Move, Run',
      },
      {
        kind: 'ability',
        name: 'Retreat',
        timing: 'Your Movement Phase',
        declare: 'Pick a friendly unit that is in combat to use this ability.',
        effect:
          "Inflict D3 mortal damage on that unit. That unit can move a distance up to its Move characteristic. That unit can move through the combat ranges of any enemy units but cannot end that move within an enemy unit's combat range.",
        keywords: 'Core, Move, Retreat',
      },
      {
        kind: 'ability',
        name: 'Shoot',
        timing: 'Your Shooting Phase',
        declare:
          "Pick a friendly unit that has not used a Run or Retreat ability this turn to use this ability. Then, pick one or more enemy units as the target(s) of that unit's attacks.",
        effect: 'Resolve shooting attacks against the target unit(s).',
        keywords: 'Core, Attack, Shoot',
      },
      {
        kind: 'ability',
        name: 'Charge',
        timing: 'Your Charge Phase',
        declare:
          'Pick a friendly unit that is not in combat and has not used a Run or Retreat ability this turn to use this ability. Then, make a charge roll of 2D6.',
        effect:
          'That unit can move a distance up to the value of the charge roll. That unit can move through the combat ranges of any enemy units and must end that move within ½" of an enemy unit. If it does so, the unit using this ability has charged.',
        keywords: 'Core, Move, Charge',
      },
      {
        kind: 'ability',
        name: 'Fight',
        timing: 'Any Combat Phase',
        declare:
          "Pick a friendly unit that is in combat or that charged this turn to use this ability. That unit can make a pile-in move. Then, if that unit is in combat, you must pick one or more enemy units as the target(s) of that unit's attacks.",
        effect: 'Resolve combat attacks against the target unit(s).',
        keywords: 'Core, Attack, Fight',
      },
    ],
  },
  {
    slug: 'universal-weapon-abilities',
    title: 'Universal Weapon Abilities',
    blocks: [
      {
        kind: 'named',
        name: 'Anti-X (+1 Rend)',
        text: "Add 1 to this weapon's Rend characteristic if the target has the keyword after 'Anti-' or fulfils the condition after 'Anti-'. Multiples of this ability are cumulative. For example, if a weapon has both Anti-charge (+1 Rend) and Anti-Hero (+1 Rend), then add 2 to the Rend characteristic of the weapon for attacks that target a Hero that charged in the same turn.",
      },
      {
        kind: 'named',
        name: 'Charge (+1 Damage)',
        text: "Add 1 to this weapon's Damage characteristic if the attacking unit charged this turn.",
      },
      {
        kind: 'named',
        name: 'Companion',
        text: 'This weapon is not affected by abilities used by a friendly unit that affect the Attacks characteristic or the attack sequence.',
      },
      {
        kind: 'named',
        name: 'Crit (2 Hits)',
        text: 'If an attack made with this weapon scores a critical hit, that attack scores 2 hits on the target unit instead of 1. Make a wound roll for each hit.',
      },
      {
        kind: 'named',
        name: 'Crit (Auto-wound)',
        text: 'If an attack made with this weapon scores a critical hit, that attack automatically wounds the target. Make a save roll as normal.',
      },
      {
        kind: 'named',
        name: 'Crit (Mortal)',
        text: 'If an attack made with this weapon scores a critical hit, that attack inflicts mortal damage on the target unit equal to the Damage characteristic of that weapon and the attack sequence ends.',
      },
      {
        kind: 'named',
        name: 'Shoot in Combat',
        text: 'This weapon can be used to make shooting attacks even if the attacking unit is in combat.',
      },
    ],
  },
  {
    slug: 'phases',
    title: 'Phases',
    blocks: [
      {
        kind: 'phases',
        phases: [
          'Start of Turn',
          'Hero Phase',
          'Movement Phase',
          'Shooting Phase',
          'Charge Phase',
          'Combat Phase',
          'End of Turn',
        ],
      },
    ],
  },
];

export function sectionSearchText(section: ReferenceSection): string {
  const parts: string[] = [section.title];
  for (const block of section.blocks) {
    switch (block.kind) {
      case 'paragraph':
        parts.push(block.text);
        break;
      case 'bullets':
        parts.push(...block.items);
        break;
      case 'ability':
        parts.push(
          block.name,
          block.timing ?? '',
          block.declare ?? '',
          block.effect,
          block.keywords ?? '',
        );
        break;
      case 'named':
        parts.push(block.name, block.text);
        break;
      case 'phases':
        parts.push(...block.phases);
        break;
    }
  }
  return parts.join(' ').toLowerCase();
}
