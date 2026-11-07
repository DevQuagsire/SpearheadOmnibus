#!/usr/bin/env python3
"""Add a batch of Spearhead armies extracted from Warhammer Community PDFs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "spearhead.json"


def add_faction(data, slug, name):
    if not any(f["slug"] == slug for f in data["factions"]):
        data["factions"].append({"slug": slug, "name": name})


def add_unit(data, unit):
    data["unitTypes"] = [u for u in data["unitTypes"] if u["slug"] != unit["slug"]]
    data["unitTypes"].append(unit)


def add_spearhead(data, spearhead):
    data["spearheads"] = [s for s in data["spearheads"] if s["slug"] != spearhead["slug"]]
    data["spearheads"].append(spearhead)


def u(slug, name, keywords, stats, melee=None, ranged=None, abilities=None):
    return {
        "slug": slug,
        "name": name,
        "keywords": keywords,
        "dataSlateStats": stats,
        "rangedWeapons": ranged or [],
        "meleeWeapons": melee or [],
        "abilities": abilities or [],
    }


def w(slug, name, attacks, hit, wound, rend, damage, abilities=None, range=None):
    weapon = {
        "slug": slug,
        "name": name,
        "attacks": attacks,
        "hit": hit,
        "wound": wound,
        "rend": rend,
        "damage": damage,
        "abilities": abilities or [],
    }
    if range is not None:
        weapon["range"] = range
    return weapon


def ab(slug, name, trigger, effect):
    return {"slug": slug, "name": name, "trigger": trigger, "effect": effect}


def slot(unit, models=1, general=False, reinf=False):
    return {
        "unitTypeSlug": unit,
        "isGeneral": general,
        "modelCount": models,
        "isReinforcement": reinf,
    }


def main():
    data = json.loads(JSON_PATH.read_text())

    # Factions
    for slug, name in [
        ("maggotkin-of-nurgle", "Maggotkin of Nurgle"),
        ("ogor-mawtribes", "Ogor Mawtribes"),
        ("hedonites-of-slaanesh", "Hedonites of Slaanesh"),
        ("cities-of-sigmar", "Cities of Sigmar"),
        ("soulblight-gravelords", "Soulblight Gravelords"),
    ]:
        add_faction(data, slug, name)

    # ========== BUBONIC CELL ==========
    add_unit(data, u(
        "rotbringer-sorcerer", "Rotbringer Sorcerer",
        ["hero", "wizard", "infantry", "ward (6+)"],
        {"control": 2, "health": 6, "move": 4, "save": 5},
        melee=[w("rotwood-staff", "Rotwood Staff", 3, 4, 3, 1, "D3")],
        abilities=[ab("fleshy-abundance", "Fleshy Abundance", "Your Hero Phase",
            "Pick a friendly unit wholly within 12 inches of this unit to be the target, then make a casting roll of 2D6. On a 6+, subtract 1 from wound rolls for attacks that target that friendly unit until the start of your next turn.")],
    ))
    add_unit(data, u(
        "nurglings", "Nurglings",
        ["beast", "ward (5+)"],
        {"control": 1, "health": 4, "move": 4, "save": 6},
        melee=[w("tiny-razor-sharp-teeth", "Tiny Razor-Sharp Teeth", 5, 5, 5, 0, 1, ["Crit(Auto-wound)"])],
        abilities=[ab("endless-swarm", "Endless Swarm", "End of Any Turn", "Heal (D3) this unit.")],
    ))
    add_unit(data, u(
        "beast-of-nurgle", "Beast of Nurgle",
        ["beast", "ward (5+)"],
        {"control": 1, "health": 8, "move": 7, "save": 5},
        melee=[w("filthy-claws-and-slobbering-maw", "Filthy Claws and Slobbering Maw", 5, 4, 3, 1, "D3", ["Companion"])],
        abilities=[ab("attention-seekers", "Attention Seekers", "Any Charge Phase",
            "If this unit charged this phase, pick an enemy unit in combat with it to be the target. Roll a D3. On a 2+, inflict an amount of mortal damage on the target equal to the roll.")],
    ))
    add_unit(data, u(
        "rotmire-creed", "Rotmire Creed",
        ["infantry", "ward (6+)", "reinforcements"],
        {"control": 1, "health": 1, "move": 5, "save": 6},
        ranged=[w("contagion-blowpipes", "Contagion Blowpipes", 2, 4, 3, 0, 1, ["Crit(Auto-wound)"], range=12)],
        melee=[w("bilewood-weapons", "Bilewood Weapons", 2, 4, 4, 0, 1)],
        abilities=[ab("bilewood-stilts", "Bilewood Stilts", "Passive",
            "No mortal damage is inflicted on this unit when it uses Retreat abilities.")],
    ))
    add_spearhead(data, {
        "slug": "bubonic-cell",
        "factionSlug": "maggotkin-of-nurgle",
        "name": "Bubonic Cell",
        "units": [
            slot("rotbringer-sorcerer", general=True),
            slot("nurglings", 3), slot("nurglings", 3),
            slot("beast-of-nurgle", 1),
            slot("rotmire-creed", 10, reinf=True),
        ],
        "battleTraits": [
            ab("cycle-of-corruption", "Cycle of Corruption", "Passive",
               "If it is the first battle round, roll a dice to determine which Cycle ability can be used this battle round (reroll 5s and 6s). Otherwise the next Cycle ability in sequence is used. 1 Numberless Pests: Subtract 1 from hit rolls for attacks that target friendly units. 2 Plague of Misery: While enemy units are within 6 inches of any friendly units, they cannot use abilities that heal or return slain models. 3 Burgeoning Filth: Subtract 3 from the control scores of enemy units while they are in combat with any friendly units. 4 Nauseous Revulsion: Subtract 1 from charge rolls for enemy units."),
        ],
        "regimentAbilities": [
            ab("corruption-of-the-land", "Corruption of the Land", "Once Per Turn (Army), End of Your Turn",
               "Pick a terrain feature, then roll a dice for each enemy unit within 3 inches of that terrain feature. On a 4+, inflict D3 mortal damage on that enemy unit."),
            ab("putrefied-ground", "Putrefied Ground", "Once Per Battle, Enemy Hero Phase",
               "For the rest of the turn: subtract 1 from the Move characteristic of enemy units; subtract 1 from run rolls for enemy units."),
        ],
        "enhancements": [
            ab("unnatural-vitality", "Unnatural Vitality", "Passive", "Your general has Ward (4+)."),
            ab("subcutaneous-suppuration", "Subcutaneous Suppuration", "Passive",
               "Subtract 1 from wound rolls for attacks that target your general."),
            ab("gaseous-emanation", "Gaseous Emanation", "Once Per Battle, Any Combat Phase",
               "Pick an enemy unit within your general's combat range to be the target. The target has Strike-last for the rest of the turn."),
            ab("overripe-deaths-heads", "Overripe Death's Heads", "Your Shooting Phase",
               "If your general is not in combat, pick a visible enemy unit within 7 inches of them to be the target. Roll a dice. On a 4+, inflict 1 mortal damage on the target."),
        ],
    })

    # ========== STONE LOBBAS ==========
    add_unit(data, u(
        "rock-hurler", "Rock-hurler",
        ["monster"],
        {"control": 5, "health": 12, "move": 8, "save": 5},
        ranged=[w("hurlin-rocks", "Hurlin' Rocks", 3, 4, 2, 1, "D3", range=12)],
        melee=[
            w("massive-club-and-rocks", "Massive Club and Rocks", 4, 4, 2, 1, 2),
            w("rock-hurler-eadbutt", "'Eadbutt", 1, 4, 2, 2, 3),
        ],
        abilities=[ab("drop-toss-or-roll", "Drop, Toss or Roll", "Your Shooting Phase",
            "Pick 1 of the following effects to apply to this unit for the rest of the turn. You cannot pick the same effect to apply to any other friendly units this turn. Drop: This unit's ranged weapons have Shoot in Combat. Toss: Add 6 inches to the Range characteristic of this unit's ranged weapons. Roll: Add 1 to hit rolls for this unit's shooting attacks.")],
    ))
    add_spearhead(data, {
        "slug": "stone-lobbas",
        "factionSlug": "sons-of-behemat",
        "name": "Stone Lobbas",
        "units": [
            slot("rock-hurler", general=True),
            slot("rock-hurler", reinf=True),
            slot("rock-hurler", reinf=True),
        ],
        "battleTraits": [
            ab("boulder-basher", "Boulder Basher", "Passive",
               "Mobs of Stone Lobbas are led by Boulder Bashers. Add the Hero keyword to your general's warscroll and remove the Reinforcements keyword."),
            ab("bowled-over", "Bowled Over", "Your Shooting Phase",
               "Pick an enemy unit that was allocated any damage points by a friendly unit's shooting attacks this turn to be the target. Roll a dice. On a 3+, until the start of your next turn, each time your opponent makes a charge roll for the target, they must change the highest D6 to match the lowest D6."),
            ab("close-one-eye", "Close One Eye!", "Your Hero Phase",
               "Pick your general to use this ability, then pick another friendly unit wholly within 12 inches of them to be the target. Add 1 to hit rolls for the target's shooting attacks for the rest of the turn."),
        ],
        "regimentAbilities": [
            ab("surly-sorts", "Surly Sorts", "Once Per Battle, Any Combat Phase",
               "Pick a friendly unit in combat to be the target. Add 1 to the Attacks characteristic of the target's melee weapons for the rest of the turn."),
            ab("greedy-and-grabby", "Greedy and Grabby", "Passive",
               "Add 5 to the control scores of friendly units."),
        ],
        "enhancements": [
            ab("ard-ead", "'Ard 'Ead", "Once Per Battle, Any Combat Phase",
               "Add 1 to hit rolls for combat attacks made with your general's 'Eadbutt for the rest of the turn."),
            ab("hungry-gobbler", "Hungry Gobbler", "End of Any Turn",
               "If any enemy models were slain by your general's combat attacks this turn, Heal (D3) your general."),
            ab("humongous-strides", "Humongous Strides", "Passive",
               "Add 1 to charge rolls for your general."),
            ab("lucky-rock", "Lucky Rock", "Once Per Battle, Your Shooting Phase",
               "Add 1 to the Attacks characteristic of your general's Hurlin' Rocks for the rest of the turn."),
        ],
    })

    # ========== WARGLUTT MARAUDERS ==========
    add_unit(data, u(
        "tyrant", "Tyrant",
        ["hero", "infantry"],
        {"control": 3, "health": 8, "move": 6, "save": 4},
        melee=[w("tyrants-meatcleavers", "Tyrant's Meatcleavers", 4, 4, 2, 2, 3)],
        abilities=[ab("roaring-warlord", "Roaring Warlord", "Your Hero Phase",
            "Pick a visible friendly unit within 12 inches of this unit to be the target. Roll a dice. On a 3+, for the rest of the turn, add 1 to charge rolls for the target.")],
    ))
    add_unit(data, u(
        "gluttons", "Gluttons",
        ["infantry"],
        {"control": 2, "health": 4, "move": 6, "save": 5},
        melee=[w("glutton-weapons", "Glutton Weapons", 4, 4, 2, 1, 2)],
        abilities=[ab("wall-of-meat", "Wall of Meat", "Passive",
            "Add 1 to save rolls for this unit if it has not charged in the same turn.")],
    ))
    add_unit(data, u(
        "ironguts", "Ironguts",
        ["infantry"],
        {"control": 2, "health": 4, "move": 6, "save": 4},
        melee=[w("irongut-weapon", "Irongut Weapon", 3, 4, 2, 2, 3)],
        abilities=[ab("stomping-marauders", "Stomping Marauders", "Passive",
            "Add 2 to this unit's control score if it charged in the same turn.")],
    ))
    add_unit(data, u(
        "maulbeast-cavalry", "Maulbeast Cavalry",
        ["cavalry"],
        {"control": 3, "health": 7, "move": 10, "save": 3},
        melee=[
            w("gutbiter-weapons", "Gutbiter Weapons", 3, 4, 2, 2, 3),
            w("maulbeasts-horns-and-fangs", "Maulbeast's Horns and Fangs", 4, 4, 2, 1, 2, ["Companion"]),
        ],
        abilities=[ab("shock-and-gore", "Shock and Gore", "Once Per Turn (Army), Your Combat Phase",
            "If this unit charged this turn, pick an enemy unit in combat with it to be the target. Roll a dice. On a 3+, for the rest of the turn, subtract 1 from wound rolls for the target's attacks.")],
    ))
    add_spearhead(data, {
        "slug": "warglutt-marauders",
        "factionSlug": "ogor-mawtribes",
        "name": "Warglutt Marauders",
        "units": [
            slot("tyrant", general=True),
            slot("gluttons", 2), slot("gluttons", 3),
            slot("ironguts", 3),
            slot("maulbeast-cavalry", 1), slot("maulbeast-cavalry", 1),
        ],
        "battleTraits": [
            ab("nomadic-warriors", "Nomadic Warriors", "Your Movement Phase",
               "Your unit of Gluttons with 3 models and 1 of your Maulbeast Cavalry units are not set up during deployment. From the third battle round onwards they can use More Ogors, My Lord!: set up this unit anywhere on the battlefield so that every model is within 1 inch of a battlefield edge and more than 6 inches from all enemy units."),
            ab("scoff-down-fresh-flesh", "Scoff Down Fresh Flesh", "End of Any Turn",
               "If an enemy unit was destroyed this turn, pick a friendly unit that used a Fight ability this turn. Pick 1 effect for the rest of the battle: Raw and Bloody Flesh: Add 1 to hit rolls for that unit's combat attacks if it charged in the same turn. Exotic Giblets: Subtract 1 from ward rolls for damage points inflicted by that unit's combat attacks. Steaming Brains: Add 3 to that unit's control score."),
        ],
        "regimentAbilities": [
            ab("brutish-barging", "Brutish Barging", "Once Per Battle, End of Your Turn",
               "Pick a friendly unit that charged this turn to be the target. The target can move up to 2D6 inches. It can move through the combat ranges of enemy units that it was in combat with at the start of that move but cannot end that move in combat."),
            ab("blinding-dust-clouds", "Blinding Dust Clouds", "Passive",
               "Subtract 1 from hit rolls for attacks that target friendly units that were set up in the same turn."),
        ],
        "enhancements": [
            ab("lungburster", "Lungburster", "Passive",
               "When making run rolls for friendly units wholly within 9 inches of your general, if you roll a 1-3, you can use a value of 4 instead."),
            ab("deathcheater", "Deathcheater", "Passive",
               "Your general has Ward (6+) while they are more than 3 inches from all other friendly units."),
            ab("gristlegobbler", "Gristlegobbler", "Once Per Battle, End of Any Turn",
               "Pick each enemy unit in combat with your general to be the targets. Inflict D3 mortal damage on each target. Then, Heal (3) your general."),
            ab("wallwrecker", "Wallwrecker", "Passive",
               "Your general can pass across terrain features as if they had Fly."),
        ],
    })

    # ========== MAWSEEKER MOB (same PDF) ==========
    add_unit(data, u(
        "butcher", "Butcher",
        ["hero", "wizard", "infantry", "ward (6+)"],
        {"control": 3, "health": 8, "move": 6, "save": 5},
        melee=[w("butchers-tools", "Butcher's Tools", 4, 4, 2, 2, 3)],
        abilities=[
            ab("butchers-cauldron", "Butcher's Cauldron", "Passive",
               "Your general's Butcher's Cauldron starts the battle empty. If this unit's Butcher's Cauldron is full, roll a D3 when declaring Rust-maw. On a 1, it becomes empty. On a 2+, you can add 2 to the casting roll."),
            ab("rust-maw", "Rust-maw", "Your Hero Phase",
               "Pick a visible enemy unit within 12 inches of this unit to be the target. Then, make a casting roll of 2D6. On a 6+, until the start of your next turn, subtract 1 from the Rend characteristic of the target's melee weapons."),
        ],
    ))
    add_unit(data, u(
        "cleavers", "Cleavers",
        ["infantry", "ward (6+)"],
        {"control": 2, "health": 4, "move": 6, "save": 5},
        melee=[w("cleavers-tools", "Cleaver's Tools", 4, 4, 2, 2, 3)],
        abilities=[ab("a-taste-for-the-arcane", "A Taste for the Arcane", "Passive",
            "This unit's melee weapons have Crit (2 Hits) while it is in combat with an enemy Wizard or Priest.")],
    ))
    add_unit(data, u(
        "gutseers", "Gutseers",
        ["infantry", "ward (6+)"],
        {"control": 2, "health": 4, "move": 6, "save": 5},
        melee=[w("gutseers-tools", "Gutseers' Tools", 3, 4, 2, 2, 3)],
        abilities=[ab("conduits-of-gut-magic", "Conduits of Gut Magic", "Once Per Turn (Army), Any Hero Phase",
            "The next time the Rust-maw ability is used by your general, measure the range and visibility of that ability from this unit instead of your general.")],
    ))
    add_unit(data, u(
        "gorger-mawpack", "Gorger Mawpack",
        ["infantry", "ward (6+)"],
        {"control": 2, "health": 5, "move": 6, "save": 6},
        melee=[w("clubs-claws-and-jaws", "Clubs, Claws and Jaws", 5, 4, 2, 1, 2)],
        abilities=[ab("bestial-hunger", "Bestial Hunger", "Passive",
            "In your charge phase, if this unit is not in combat and there are any enemy units within 12 inches of it, this unit must use the Charge ability, and if the charge roll would allow it to end the move within 1/2 inch of a visible enemy unit, it must do so.")],
    ))
    add_spearhead(data, {
        "slug": "mawseeker-mob",
        "factionSlug": "ogor-mawtribes",
        "name": "Mawseeker Mob",
        "units": [
            slot("butcher", general=True),
            slot("cleavers", 3), slot("gutseers", 3),
            slot("gorger-mawpack", 5, reinf=True),
        ],
        "battleTraits": [
            ab("wot-no-meat", "Wot? No Meat!?", "Passive",
               "Your general's Butcher's Cauldron starts the battle empty."),
            ab("chuck-em-in-the-pot", "Chuck 'Em in the Pot", "End of Any Turn",
               "You must use this ability if an enemy unit was destroyed this turn. Your general's Butcher's Cauldron becomes full."),
            ab("from-out-the-caverns", "From Out the Caverns", "Once Per Battle, Start of Battle Round",
               "Your Gorger Mawpack is not set up during deployment. From the second battle round onwards they can use Frenzied Hunters: set up this unit within 1 inch of a battlefield edge and more than 6 inches from all enemy units."),
        ],
        "regimentAbilities": [
            ab("dish-testers", "Dish Testers", "Any Combat Phase",
               "If your general's Butcher's Cauldron is full, pick a visible friendly unit wholly within 12 inches of them to be the target. Add 1 to hit rolls for the target's combat attacks for the rest of the turn. Then, your general's Butcher's Cauldron becomes empty."),
            ab("eager-procurers", "Eager Procurers", "Passive",
               "While your general's Butcher's Cauldron is empty, add 2 inches to the Move characteristic of friendly units while they are wholly within 12 inches of your general."),
        ],
        "enhancements": [
            ab("generous-portions", "Generous Portions", "End of Any Turn",
               "If your general's Butcher's Cauldron is full, Heal (1) each visible friendly unit wholly within 9 inches of your general."),
            ab("disgusting-eater", "Disgusting Eater", "Once Per Battle, Reaction: Opponent declared a Charge ability for a visible enemy unit within 12 inches of this unit",
               "Subtract D3 from the charge roll. If your general's Butcher's Cauldron is full, you can subtract 3 instead, but if you do so their Butcher's Cauldron becomes empty after that Charge ability has been resolved."),
            ab("hunger-pangs", "Hunger Pangs", "Start of First Battle Round",
               "Each friendly unit that is not in combat can move up to D3 inches. Friendly units that are not in combat and are wholly within 9 inches of your general while their Butcher's Cauldron is empty can move up to D6 inches instead. They cannot end those moves in combat."),
            ab("well-stocked-larder", "Well-stocked Larder", "Once Per Battle, Enemy Movement Phase",
               "Your general's Butcher's Cauldron becomes full."),
        ],
    })

    print("phase1 units/spearheads written...")
    # Continue in same script for remaining armies
    # ========== LURID DREAM ==========
    add_unit(data, u(
        "shardspeaker-of-slaanesh", "Shardspeaker of Slaanesh",
        ["hero", "wizard", "infantry"],
        {"control": 2, "health": 5, "move": 6, "save": 5},
        melee=[w("haze-staff", "Haze Staff", 3, 3, 4, 1, "D3")],
        abilities=[ab("vision-of-damnation", "Vision of Damnation", "Your Hero Phase",
            "Make a casting roll of 2D6. On a 6+, roll 6 dice. For each 4+, you receive 1 depravity point.")],
    ))
    add_unit(data, u(
        "slickblade-seekers", "Slickblade Seekers",
        ["cavalry", "reinforcements"],
        {"control": 1, "health": 4, "move": 12, "save": 5},
        melee=[
            w("slickblade-glaive", "Slickblade Glaive", 3, 3, 4, 1, 1, ["Charge(+1 Damage)"]),
            w("exalted-steeds-poisoned-tongue", "Exalted Steed's Poisoned Tongue", 3, 3, 4, 0, 1, ["Companion"]),
        ],
        abilities=[ab("unrivalled-velocity", "Unrivalled Velocity", "Passive",
            "You can re-roll charge rolls for this unit.")],
    ))
    add_unit(data, u(
        "blissbarb-archers", "Blissbarb Archers",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 1, "move": 6, "save": 6},
        ranged=[w("blissbarb-bow", "Blissbarb Bow", 2, 3, 4, 1, 1, range=18)],
        melee=[w("sybarite-blade", "Sybarite Blade", 1, 3, 4, 0, 1)],
        abilities=[
            ab("blissbarb-composition", "Blissbarb Archers", "Passive",
               "One unit has 5 Blissbarb Archers and 1 Blissbrew Homonculus. The other unit has 5 Blissbarb Archers. The Blissbarb Archers are each armed with a Blissbarb Bow and Sybarite Blade. The Blissbrew Homonculus is armed with a Sybarite Blade."),
            ab("light-footed-killers", "Light-footed Killers", "Passive",
               "This unit can use Shoot abilities even if it used a Run ability in the same turn."),
        ],
    ))
    add_unit(data, u(
        "slaangor-fiendbloods", "Slaangor Fiendbloods",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 3, "move": 6, "save": 5},
        melee=[
            w("razor-sharp-claws", "Razor-sharp Claws", 4, 4, 3, 1, 2),
            w("razor-sharp-claw-and-gilded-weapon", "Razor-sharp Claw and Gilded Weapon", 5, 4, 3, 1, 2),
        ],
        abilities=[
            ab("slaangor-composition", "Slaangor Fiendbloods", "Passive",
               "This unit has 2 Slaangor Fiendbloods armed with Razor-sharp Claws, and 1 Slaangor Fiendblood armed with a Razor-sharp Claw and Gilded Weapon."),
            ab("slaughter-at-any-cost", "Slaughter at Any Cost", "Enemy Shooting Phase",
               "This unit can use this ability if any damage points were allocated to it this turn. This unit can use the 'Normal Move' ability as if it were your movement phase."),
        ],
    ))
    add_spearhead(data, {
        "slug": "blades-of-the-lurid-dream",
        "factionSlug": "hedonites-of-slaanesh",
        "name": "Blades of the Lurid Dream",
        "units": [
            slot("shardspeaker-of-slaanesh", general=True),
            slot("blissbarb-archers", 6, reinf=True),
            slot("blissbarb-archers", 5, reinf=True),
            slot("slickblade-seekers", 5, reinf=True),
            slot("slaangor-fiendbloods", 3, reinf=True),
        ],
        "battleTraits": [
            ab("temptations-of-slaanesh", "Temptations of Slaanesh", "Passive",
               "You receive 6 temptation dice at the start of the battle round. Each time your opponent makes a failed hit, wound or save roll, you can offer them a temptation dice. If accepted, that roll is replaced with a 6. Each acceptance gains D6 depravity points; each rejection inflicts D3 mortal damage on that unit. Cumulative DP abilities: 12+ Tantalising Torment (Run then Charge); 18+ Sadistic Spite (melee Crit Mortal); 24+ Oblivious Indulgence (Ward 5+)."),
        ],
        "regimentAbilities": [
            ab("unparalleled-speed", "Unparalleled Speed", "Once Per Battle, Any Combat Phase",
               "Pick a friendly unit to use this ability. That unit has Strike-first this phase."),
            ab("locus-of-diversion", "Locus of Diversion", "Your Movement Phase",
               "Pick a friendly unit to use this ability. For the rest of the turn, that unit can use a Retreat ability and still use Shoot and/or Charge abilities later in the turn."),
        ],
        "enhancements": [
            ab("sceptre-of-domination", "Sceptre of Domination", "Any Combat Phase",
               "Roll a dice for each enemy unit in combat with your general. On a 5+, that unit has Strike-last this phase."),
            ab("cacophonic-choir", "Cacophonic Choir", "Your Hero Phase",
               "Make a casting roll of 2D6. On a 6+, make a cacophony roll of D6. Inflict D3 mortal damage on each enemy unit within 6 inches of your general that has a Control characteristic less than the cacophony roll."),
            ab("pendant-of-slaanesh", "Pendant of Slaanesh", "Your Hero Phase", "Heal (D3) your general."),
            ab("twisted-mirror", "Twisted Mirror", "Once Per Turn, Your Shooting Phase",
               "Pick an enemy unit within 9 inches of your general and roll a dice. On a 4+, subtract 1 from save rolls for that unit until the start of your next turn."),
        ],
    })

    # ========== EPICUREAN REVELLERS ==========
    add_unit(data, u(
        "thricefold-discord", "Thricefold Discord",
        ["infantry", "hero", "wizard", "ward (5+)"],
        {"control": 2, "health": 3, "move": 6, "save": 5},
        melee=[w("thricefold-arsenal", "Thricefold Arsenal", 3, 3, 3, 1, 2)],
        abilities=[
            ab("thricefold-court", "Thricefold Court", "Passive",
               "Each model in this unit is treated as an individual unit when determining the effect of the Favour Most Fickle battle trait."),
            ab("dispensers-of-favour", "Dispensers of Favour", "Your Hero Phase",
               "Pick up to X different friendly units wholly within 12 inches of this unit to be the targets, where X is the number of models in this unit. Then make a casting roll of 2D6. On a 6+, apply: Daemonettes get Anti-charge (+1 Rend); Seekers get +2 inches Move; Fiends get +1 hit for combat attacks until the start of your next turn."),
        ],
    ))
    add_unit(data, u(
        "fiends", "Fiends",
        ["beast", "ward (6+)"],
        {"control": 1, "health": 4, "move": 10, "save": 5},
        melee=[w("deadly-pincers-and-barbed-stinger", "Deadly Pincers and Barbed Stinger", 4, 4, 3, 1, "D3")],
        abilities=[ab("soporific-musk", "Soporific Musk", "Once Per Turn (Army), Any Charge Phase",
            "If this unit is not in combat, pick a visible enemy unit within 9 inches; if in combat, pick an enemy unit in combat with it. Roll a dice. On a 4+, the target has Strike-last for the rest of the turn.")],
    ))
    add_unit(data, u(
        "daemonettes", "Daemonettes",
        ["infantry", "reinforcements", "ward (6+)"],
        {"control": 1, "health": 1, "move": 6, "save": 6},
        melee=[w("piercing-claws", "Piercing Claws", 2, 3, 4, 1, 1)],
        abilities=[ab("lithe-and-swift", "Lithe and Swift", "Passive",
            "Add 1 to the Attacks characteristic of this unit's Piercing Claws if it charged in the same turn.")],
    ))
    add_unit(data, u(
        "seekers", "Seekers",
        ["cavalry", "ward (6+)"],
        {"control": 1, "health": 3, "move": 14, "save": 6},
        melee=[
            w("agonising-claws", "Agonising Claws", 3, 3, 4, 1, 1, ["Anti-Cavalry(+1 Rend)"]),
            w("steeds-poisoned-tongue", "Steed's Poisoned Tongue", 2, 3, 4, 0, 1, ["Companion"]),
        ],
        abilities=[ab("quicksilver-speed", "Quicksilver Speed", "Passive",
            "When making run rolls for this unit, if you roll a 1-3, you can use a value of 4 instead.")],
    ))
    add_spearhead(data, {
        "slug": "epicurean-revellers",
        "factionSlug": "hedonites-of-slaanesh",
        "name": "Epicurean Revellers",
        "units": [
            slot("thricefold-discord", 3, general=True),
            slot("fiends", 3),
            slot("daemonettes", 10, reinf=True),
            slot("daemonettes", 10, reinf=True),
            slot("seekers", 5),
        ],
        "battleTraits": [
            ab("favour-most-fickle", "Favour Most Fickle", "Passive",
               "Effects based on friendly units on the battlefield (not cumulative): 5+: +2 Control; 4: +1 hit and wound for combat including Companion; 3: +1 run and charge; 2: Ward (5+); 1: +2 Attacks to melee including Companion."),
            ab("bringers-of-degradation", "Bringers of Degradation", "Passive",
               "When alternating Fight abilities, when it is your turn you can pick 2 friendly Daemonettes units instead of 1."),
        ],
        "regimentAbilities": [
            ab("daemonic-onslaught", "Daemonic Onslaught", "Once Per Battle, Deployment Phase",
               "Pick a friendly Seekers or Fiends unit wholly within 12 inches of your general to be the target. The target can use the 'Normal Move' ability as if it were your movement phase."),
            ab("irresistible-soul-musk", "Irresistible Soul-musk", "Once Per Battle, Your Movement Phase",
               "Pick a visible friendly Seekers or Fiends unit wholly within 12 inches of your general. Remove the target and set it up again more than 6 inches from all enemy units."),
        ],
        "enhancements": [
            ab("high-courtiers", "High Courtiers", "Passive",
               "While your general is wholly within the combat range of a friendly Daemonettes unit, both units have Ward (5+)."),
            ab("twisted-grace", "Twisted Grace", "Passive",
               "When your general makes a pile-in move, if they charged in the same turn, add D6 inches to the distance they can move."),
            ab("excess-of-violence", "Excess of Violence", "Once Per Battle, Any Combat Phase",
               "Pick a visible friendly unit wholly within 12 inches of your general. The target's melee weapons, including Companion weapons, have Crit (2 Hits) until the start of your next turn."),
        ],
    })

    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Saved mid-batch: {len(data['factions'])} factions, {len(data['unitTypes'])} units, {len(data['spearheads'])} spearheads")
    return data

if __name__ == "__main__":
    main()
