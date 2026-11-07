#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "spearhead.json"

def add_unit(data, unit):
    data["unitTypes"] = [u for u in data["unitTypes"] if u["slug"] != unit["slug"]]
    data["unitTypes"].append(unit)

def add_spearhead(data, spearhead):
    data["spearheads"] = [s for s in data["spearheads"] if s["slug"] != spearhead["slug"]]
    data["spearheads"].append(spearhead)

def u(slug, name, keywords, stats, melee=None, ranged=None, abilities=None):
    return {"slug": slug, "name": name, "keywords": keywords, "dataSlateStats": stats,
            "rangedWeapons": ranged or [], "meleeWeapons": melee or [], "abilities": abilities or []}

def w(slug, name, attacks, hit, wound, rend, damage, abilities=None, range=None):
    weapon = {"slug": slug, "name": name, "attacks": attacks, "hit": hit, "wound": wound,
              "rend": rend, "damage": damage, "abilities": abilities or []}
    if range is not None:
        weapon["range"] = range
    return weapon

def ab(slug, name, trigger, effect):
    return {"slug": slug, "name": name, "trigger": trigger, "effect": effect}

def slot(unit, models=1, general=False, reinf=False):
    return {"unitTypeSlug": unit, "isGeneral": general, "modelCount": models, "isReinforcement": reinf}

def main():
    data = json.loads(JSON_PATH.read_text())

    # ========== ZENESTRA'S ZEALOTS ==========
    add_unit(data, u(
        "freeguild-marshal-and-relic-envoy", "Freeguild Marshal and Relic Envoy",
        ["hero", "infantry"],
        {"control": 2, "health": 5, "move": 5, "save": 3},
        ranged=[w("duelling-pistols", "Duelling Pistols", 4, 3, 4, 1, 1, ["Shoot in Combat"], range=10)],
        melee=[w("master-forged-weapon", "Master-forged Weapon", 5, 3, 4, 1, 2)],
        abilities=[
            ab("relic-envoy", "Relic Envoy", "Passive",
               "The Relic Envoy is a token. While a friendly unit other than this unit has the Relic Envoy token, add 1 to wound rolls for that unit's combat attacks. If this unit is destroyed, remove the Relic Envoy token from the battlefield."),
            ab("marshals-orders", "Marshal's Orders", "Your Hero Phase",
               "Pick a visible friendly unit wholly within 12 inches of this unit to be the target. Remove this unit's Relic Envoy token from the battlefield, then give it to the target."),
        ],
    ))
    add_unit(data, u(
        "pontifex-zenestra", "Pontifex Zenestra, Matriarch of the Great Wheel",
        ["hero", "priest", "infantry", "ward (4+)"],
        {"control": 2, "health": 9, "move": 5, "save": 5},
        melee=[w("sceptre-of-the-wheel", "Sceptre of the Wheel", 3, 4, 4, 1, "D3")],
        abilities=[ab("vessel-of-sigmar", "Vessel of Sigmar", "Your Hero Phase",
            "Pick up to 3 visible friendly or enemy units to be the targets. Roll a D3 for each target. On a 2+: if friendly, it has Ward (5+) until the start of your next turn; if enemy, inflict mortal damage equal to the roll.")],
    ))
    add_unit(data, u(
        "freeguild-command-corps-whisperblade", "Freeguild Command Corps Whisperblade",
        ["infantry"],
        {"control": 1, "health": 2, "move": 5, "save": 6},
        melee=[w("enchanted-rapier", "Enchanted Rapier", 4, 3, 4, 2, 2)],
        abilities=[ab("forewarned-is-forearmed", "Forewarned is Forearmed", "Passive",
            "While it is your turn, this unit has Strike-first.")],
    ))
    add_unit(data, u(
        "freeguild-command-corps-arch-knight", "Freeguild Command Corps Arch-Knight and Retinue",
        ["infantry", "reinforcements"],
        {"control": 2, "health": 2, "move": 5, "save": 4},
        melee=[w("command-weapons", "Command Weapons", 3, 3, 4, 1, 1)],
        abilities=[
            ab("arch-knight-composition", "Arch-Knight and Retinue", "Passive",
               "This unit comprises 1 Arch-Knight, 1 Great Herald, 1 War Surgeon, 1 Soul Shepherd and 1 Mascot Gargoylian."),
            ab("talented-champions", "Talented Champions", "Once Per Turn, Reaction: You used a command",
               "After that command has been resolved, return the card to your hand."),
        ],
    ))
    add_unit(data, u(
        "freeguild-steelhelms", "Freeguild Steelhelms",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 1, "move": 5, "save": 4},
        melee=[w("freeguild-weapons", "Freeguild Weapons", 2, 4, 4, 0, 1)],
        abilities=[ab("fanatical-followers", "Fanatical Followers", "Any Combat Phase",
            "Return 1 slain model to this unit.")],
    ))
    add_spearhead(data, {
        "slug": "zenestras-zealots",
        "factionSlug": "cities-of-sigmar",
        "name": "Zenestra's Zealots",
        "units": [
            slot("freeguild-marshal-and-relic-envoy", general=True),
            slot("pontifex-zenestra", 1),
            slot("freeguild-command-corps-whisperblade", 1),
            slot("freeguild-command-corps-arch-knight", 5, reinf=True),
            slot("freeguild-steelhelms", 5, reinf=True),
            slot("freeguild-steelhelms", 5, reinf=True),
        ],
        "battleTraits": [
            ab("fierce-zealots", "Fierce Zealots", "Passive",
               "Add 3 to the control scores of friendly Freeguild Steelhelms units."),
            ab("lady-of-the-wheel", "Lady of the Wheel", "Passive",
               "Each time a friendly model is slain by a combat attack, roll a number of dice equal to that model's Health characteristic. For each 5+, inflict 1 mortal damage on the attacking unit after the Fight ability has been resolved."),
            ab("shadowy-spymaster", "Shadowy Spymaster", "Your Movement Phase",
               "Your Whisperblade is not set up during deployment. From the second battle round onwards it can use Sudden Ambush: set up this unit within 6 inches of an enemy unit and not in combat."),
        ],
        "regimentAbilities": [
            ab("stand-fast-comrades", "Stand Fast, Comrades", "Once Per Battle, Your Hero Phase",
               "Pick a visible friendly non-Hero unit wholly within 12 inches of your general. The target has Ward (4+) until the start of the next battle round."),
            ab("fervent-rush", "Fervent Rush", "Once Per Turn (Army), Your Movement Phase",
               "Pick a friendly unit to use this ability. This unit can use Charge abilities this turn even if it used a Run ability in the same turn."),
        ],
        "enhancements": [
            ab("step-to-it", "Step to It!", "Once Per Turn, Reaction: You declared a Run ability for a non-Hero unit wholly within 12 inches of your general",
               "Do not make a run roll. Instead, add 6 inches to that non-Hero unit's Move characteristic for that Run ability."),
            ab("ardent-demand", "Ardent Demand", "Any Combat Phase",
               "Pick a visible friendly non-Hero unit wholly within 12 inches of your general. Add 1 to hit rolls for the target's combat attacks for the rest of the turn."),
            ab("devout-commander", "Devout Commander", "Passive",
               "Add 1 to the Attacks characteristic and the Rend characteristic of your general's Master-forged Weapon."),
        ],
    })

    # ========== CURSED SHACKLEHORDE ==========
    add_unit(data, u(
        "spirit-torment", "Spirit Torment",
        ["hero", "infantry", "fly", "ward (5+)"],
        {"control": 2, "health": 5, "move": 8, "save": 5},
        melee=[w("shacklegheist-chains", "Shacklegheist Chains", 5, 4, 3, 1, 2, ["Crit(Auto-wound)"])],
        abilities=[ab("captured-soul-energy", "Captured Soul Energy", "Your Hero Phase",
            "Pick a friendly unit wholly within 12 inches of this unit to be the target. Roll a dice. On a 3+, add 1 to wound rolls for the target's combat attacks for the rest of the turn.")],
    ))
    add_unit(data, u(
        "chainghasts", "Chainghasts",
        ["infantry", "fly", "ward (5+)"],
        {"control": 2, "health": 3, "move": 8, "save": 6},
        ranged=[w("ghastflails-ranged", "Ghastflails", 2, 4, 3, 2, 1, ["Crit(Auto-wound)"], range=12)],
        melee=[w("ghastflails-melee", "Ghastflails", 2, 4, 3, 2, 1, ["Crit(Auto-wound)"])],
        abilities=[ab("another-link-in-the-chain", "Another Link in the Chain", "Your Combat Phase",
            "Roll a dice. Add 1 to the roll if this unit is wholly within 12 inches of any friendly Spirit Torments. On a 3+, for the rest of the turn, add 1 to hit rolls for combat attacks made by friendly units while they are wholly within 12 inches of this unit.")],
    ))
    add_unit(data, u(
        "bladegheist-revenants", "Bladegheist Revenants",
        ["infantry", "fly", "ward (5+)"],
        {"control": 1, "health": 2, "move": 8, "save": 6},
        melee=[w("tomb-greatblade", "Tomb Greatblade", 2, 3, 3, 1, 1, ["Crit(Auto-wound)"])],
        abilities=[ab("thrashing-desperation", "Thrashing Desperation", "Passive",
            "While this unit contests an objective you control, enemy units cannot end a charge move within 1/2 inch of this unit unless the unmodified charge roll was 5 or more.")],
    ))
    add_unit(data, u(
        "dreadscythe-harridans", "Dreadscythe Harridans",
        ["infantry", "fly", "ward (5+)"],
        {"control": 1, "health": 2, "move": 8, "save": 6},
        melee=[w("scythed-limbs", "Scythed Limbs", 3, 4, 4, 1, 1, ["Crit(Auto-wound)"])],
        abilities=[ab("harrowing-shrieks", "Harrowing Shrieks", "Passive",
            "Enemy units cannot be healed or have slain models returned to them while they are in combat with this unit.")],
    ))
    add_unit(data, u(
        "dreadblade-harrows", "Dreadblade Harrows",
        ["cavalry", "fly", "ward (5+)"],
        {"control": 1, "health": 3, "move": 12, "save": 6},
        melee=[
            w("dreadblade", "Dreadblade", 4, 4, 3, 1, 2, ["Crit(Auto-wound)"]),
            w("ethereal-steeds-ghostly-hooves-and-teeth", "Ethereal Steed's Ghostly Hooves and Teeth", 3, 5, 3, 0, 1, ["Crit(Auto-wound)", "Companion"]),
        ],
        abilities=[ab("phantasmal-discorporation", "Phantasmal Discorporation", "Once Per Battle, Your Movement Phase",
            "Remove this unit from the battlefield and set it up again on the battlefield more than 6 inches from all enemy units.")],
    ))
    add_spearhead(data, {
        "slug": "cursed-shacklehorde",
        "factionSlug": "nighthaunt",
        "name": "Cursed Shacklehorde",
        "units": [
            slot("spirit-torment", general=True),
            slot("chainghasts", 2),
            slot("bladegheist-revenants", 5), slot("bladegheist-revenants", 5),
            slot("dreadscythe-harridans", 5), slot("dreadscythe-harridans", 5),
            slot("dreadblade-harrows", 2),
        ],
        "battleTraits": [
            ab("ethereal-shacklehorde", "Ethereal", "Passive",
               "Ignore negative modifiers to save rolls for friendly units."),
            ab("spectral-procession", "Spectral Procession", "Once Per Turn (Army), Your Movement Phase",
               "1 of your Bladegheist Revenants units and 1 of your Dreadscythe Harridans units start the battle in reserve. From the second battle round onwards use Cackling Arrival: pick 1 of your units in reserve and set it up anywhere more than 6 inches from all enemy units."),
        ],
        "regimentAbilities": [
            ab("discorporate-shacklehorde", "Discorporate", "Once Per Turn (Army), Any Hero Phase",
               "Pick a friendly unit to be the target. Roll a dice. On a 3+, add 1 to save rolls for the target for the rest of the turn."),
            ab("mounting-dread", "Mounting Dread", "Once Per Turn (Army), End of Any Turn",
               "Pick a friendly unit to be the target. Roll a dice. On a 2+, subtract the current battle round number from the control scores of enemy units while they are in combat with the target."),
        ],
        "enhancements": [
            ab("deathly-possessor", "Deathly Possessor", "Any Combat Phase",
               "Pick an enemy Hero within 12 inches of your general to be the target, then pick another enemy unit within the target's combat range to be the victim. Roll a D3. On a 2+, pick one: inflict mortal damage on the target equal to the roll, or on the victim equal to the roll."),
            ab("tales-of-horror", "Tales of Horror", "Once Per Battle, Any Combat Phase",
               "Pick an enemy Infantry or Cavalry unit within 6 inches of your general. For the rest of the battle, if the target is replaced using Call for Reinforcements, halve the number of models in the replacement unit, rounding up."),
            ab("spectral-howl", "Spectral Howl", "Once Per Battle, Any Hero Phase",
               "Pick an enemy unit within 12 inches of your general. For the rest of the turn, subtract 1 from the number of dice rolled when making charge rolls for the target, to a minimum of 1."),
            ab("unholy-visage", "Unholy Visage", "Your Hero Phase",
               "Pick a visible enemy unit within 6 inches of your general. Roll a dice. On a 3+, the target must immediately use a Retreat ability as if it were the enemy movement phase."),
        ],
    })

    # ========== BLEAK HOST ==========
    add_unit(data, u(
        "spoilpox-scrivener", "Spoilpox Scrivener",
        ["hero", "infantry", "ward (5+)"],
        {"control": 2, "health": 5, "move": 4, "save": 5},
        ranged=[w("disgusting-sneezes", "Disgusting Sneezes", "D6", 2, 4, 0, 1, ["Shoot in Combat"], range=7)],
        melee=[w("distended-maw", "Distended Maw", 3, 4, 3, 1, 2)],
        abilities=[ab("keep-counting-im-watching-you", "Keep Counting, I'm Watching You", "Your Hero Phase",
            "Pick a friendly Plaguebearers unit wholly within 14 inches of this unit. Pick 1 until the start of your next turn: Tally of Blows: Add 1 to the Attacks characteristic of the target's melee weapons. Recorded Stamina: Add 1 to save rolls for the target.")],
    ))
    add_unit(data, u(
        "pusgoyle-blightlord", "Pusgoyle Blightlord",
        ["cavalry", "fly", "ward (5+)"],
        {"control": 2, "health": 8, "move": 8, "save": 4},
        melee=[
            w("blighted-scythe", "Blighted Scythe", 3, 3, 3, 2, 1),
            w("rot-flys-mouthparts-and-sting", "Rot Fly's Mouthparts and Sting", 6, 4, 2, 0, 1, ["Companion"]),
        ],
        abilities=[ab("wrack-and-ruin", "Wrack and Ruin", "Any Charge Phase",
            "If this unit charged this phase, pick an enemy unit within 1 inch of it to be the target and roll a dice. On a 2+, inflict D3 mortal damage on the target.")],
    ))
    add_unit(data, u(
        "putrid-blightkings", "Putrid Blightkings",
        ["infantry", "ward (5+)"],
        {"control": 1, "health": 3, "move": 4, "save": 3},
        melee=[w("blighted-weapon", "Blighted Weapon", 4, 3, 3, 1, 1)],
        abilities=[ab("relentless-attackers", "Relentless Attackers", "End of Any Turn",
            "Pick an enemy Infantry unit in combat with this unit. Roll a dice for each model in this unit within the target's combat range. For each roll that exceeds the target's Health characteristic, inflict 1 mortal damage on it.")],
    ))
    add_unit(data, u(
        "plaguebearers", "Plaguebearers",
        ["infantry", "ward (5+)"],
        {"control": 1, "health": 2, "move": 4, "save": 6},
        melee=[w("plaguesword", "Plaguesword", 1, 4, 3, 0, 1, ["Crit(Mortal)"])],
        abilities=[ab("cloud-of-flies", "Cloud of Flies", "Passive",
            "Subtract 1 from hit rolls for shooting attacks that target this unit.")],
    ))
    add_spearhead(data, {
        "slug": "bleak-host",
        "factionSlug": "maggotkin-of-nurgle",
        "name": "Bleak Host",
        "units": [
            slot("spoilpox-scrivener", general=True),
            slot("pusgoyle-blightlord", 1), slot("pusgoyle-blightlord", 1),
            slot("putrid-blightkings", 5),
            slot("plaguebearers", 5), slot("plaguebearers", 5),
        ],
        "battleTraits": [
            ab("diseased", "Diseased", "Passive",
               "Each time an attack made by a friendly model scores a critical hit, you receive 1 disease point, to a maximum of 7."),
            ab("the-infectious-hosts", "The Infectious Hosts", "Your Movement Phase",
               "One of your Pusgoyle Blightlords and one of your Plaguebearers units are not set up during deployment. From the third battle round onwards they can use Daemonic Summoning: set up this unit anywhere more than 6 inches from all enemy units."),
            ab("nurgles-embrace", "Nurgle's Embrace", "End of Any Turn",
               "Spend any number of your disease points. For each disease point spent, pick an enemy unit in combat with any of your units and roll a dice. On a 4+, inflict 1 mortal damage on that unit (you can pick the same enemy unit more than once)."),
        ],
        "regimentAbilities": [
            ab("locus-of-fecundity", "Locus of Fecundity", "Once Per Phase, Your Hero Phase",
               "Pick a friendly unit. Heal (D3) that unit."),
            ab("infested-with-wonders", "Infested with Wonders", "Passive",
               "Each time a friendly model is slain, before it is removed from play, you can pick an enemy unit within 1 inch of it and roll a dice. On a 4+, inflict 1 mortal damage on that unit."),
        ],
        "enhancements": [
            ab("gift-of-febrile-frenzy", "Gift of Febrile Frenzy", "Once Per Battle, Any Combat Phase",
               "Until the end of the phase, add 1 to the Attacks characteristic of melee weapons used by friendly units while they are wholly within 7 inches of your general."),
            ab("gardener-of-nurgle", "Gardener of Nurgle", "Your Movement Phase",
               "If your general is contesting an objective not contested by any enemy models, roll a dice. On a 3+, that objective is desecrated. Friendly units have Ward (4+) while contesting a desecrated objective. If your opponent gains control of it, it is no longer desecrated."),
            ab("pestilent-breath", "Pestilent Breath", "Your Shooting Phase",
               "Pick an enemy unit within 7 inches of your general and roll a dice for each model in that unit. For each 5+, inflict 1 mortal damage on that unit."),
            ab("summoner-of-plaguebearers", "Summoner of Plaguebearers", "End of Any Turn",
               "Pick a friendly Plaguebearers unit wholly within 14 inches of your general. Return 1 slain model to that unit."),
        ],
    })

    # ========== BLOODCRAVE HUNT ==========
    add_unit(data, u(
        "vampire-lord", "Vampire Lord",
        ["hero", "wizard", "infantry", "vampire", "ward (6+)"],
        {"control": 2, "health": 5, "move": 6, "save": 3},
        melee=[w("dynastic-war-relic", "Dynastic War-relic", 5, 3, 3, 1, 2)],
        abilities=[ab("vile-transference", "Vile Transference", "Your Hero Phase",
            "Pick a visible enemy unit within 6 inches of this unit to be the target, then make a casting roll of 2D6. On a 6+, roll a number of dice equal to the target's Health characteristic. For each 5+, inflict 1 mortal damage on the target and Heal (1) this unit.")],
    ))
    add_unit(data, u(
        "blood-knights", "Blood Knights",
        ["cavalry", "vampire", "ward (6+)"],
        {"control": 1, "health": 3, "move": 10, "save": 3},
        melee=[
            w("templar-lance-or-blade", "Templar Lance or Templar Blade", 3, 3, 3, 1, 1, ["Charge(+1 Damage)"]),
            w("nightmares-hooves-and-teeth", "Nightmare's Hooves and Teeth", 3, 5, 3, 0, 1, ["Companion"]),
        ],
        abilities=[ab("riders-of-ruin", "Riders of Ruin", "Passive",
            "Models in this unit can pass across enemy Infantry models as if this unit had Fly.")],
    ))
    add_unit(data, u(
        "vargheists", "Vargheists",
        ["infantry", "vampire", "fly", "ward (6+)"],
        {"control": 1, "health": 4, "move": 12, "save": 5},
        melee=[w("murderous-fangs-and-talons", "Murderous Fangs and Talons", 3, 4, 3, 1, 2, ["Crit(2 Hits)"])],
        abilities=[ab("the-scent-of-gore", "The Scent of Gore", "Any Combat Phase",
            "Add 1 to wound rolls for attacks made by this unit that target a damaged unit.")],
    ))
    add_unit(data, u(
        "deathrattle-skeletons", "Deathrattle Skeletons",
        ["infantry", "ward (6+)"],
        {"control": 1, "health": 1, "move": 4, "save": 5},
        melee=[w("ancient-weapon", "Ancient Weapon", 2, 4, 4, 0, 1)],
        abilities=[ab("skeleton-legion", "Skeleton Legion", "Passive",
            "For each slain model from this unit, make a legion roll of D6. For each 5+, return 1 slain model to this unit.")],
    ))
    add_spearhead(data, {
        "slug": "bloodcrave-hunt",
        "factionSlug": "soulblight-gravelords",
        "name": "Bloodcrave Hunt",
        "units": [
            slot("vampire-lord", general=True),
            slot("deathrattle-skeletons", 10), slot("deathrattle-skeletons", 10),
            slot("blood-knights", 5),
            slot("vargheists", 3),
        ],
        "battleTraits": [
            ab("the-hunger", "The Hunger", "Passive",
               "Each time a friendly Vampire unit uses a Fight ability, after all of its attacks have been resolved, Heal (X) that Vampire unit where X is the number of damage points allocated by those attacks."),
            ab("deaths-descent", "Death's Descent", "Your Movement Phase",
               "Your Vargheists unit is not set up during deployment. From the third battle round onwards they can use Swoop Down: set up this unit anywhere more than 6 inches from all enemy units."),
        ],
        "regimentAbilities": [
            ab("cloud-of-bats", "Cloud of Bats", "Once Per Battle, Your Movement Phase",
               "Remove your general from the battlefield and set them up again anywhere more than 6 inches from all enemy units."),
            ab("endless-legions", "Endless Legions", "Once Per Battle, Your Movement Phase",
               "Pick a friendly Deathrattle Skeletons unit that has been destroyed. You can set up a replacement unit with D6+4 models anywhere more than 6 inches from all enemy units."),
        ],
        "enhancements": [
            ab("ruinous-chargers", "Ruinous Chargers", "Any Charge Phase",
               "Pick your Blood Knights unit to use this ability if it charged this turn. Inflict D3 mortal damage on each enemy unit it passed across during that Charge ability."),
            ab("grave-sand-shard", "Grave-sand Shard", "Once Per Battle, Reaction: You declared the Skeleton Legion ability for a unit within 9 inches of your general",
               "Add 1 to each legion roll made for that unit."),
            ab("aura-of-night", "Aura of Night", "Passive",
               "Ignore negative modifiers to save rolls for shooting attacks that target your general."),
            ab("spirit-gale", "Spirit Gale", "Your Hero Phase",
               "Make a casting roll of 2D6. On a 7+, inflict 1 mortal damage on each enemy unit on the battlefield."),
        ],
    })

    # ========== FUSIL-PLATOON ==========
    add_unit(data, u(
        "fusil-major-on-ogor-warhulk", "Fusil-Major on Ogor Warhulk",
        ["hero", "infantry", "castelite"],
        {"control": 2, "health": 8, "move": 5, "save": 3},
        ranged=[w("long-fusil", "Long-Fusil", 3, 3, 3, 1, 2, range=24)],
        melee=[w("warhulks-mace", "Warhulk's Mace", 4, 4, 2, 2, 2)],
        abilities=[ab("mark-targets", "Mark Targets", "Your Shooting Phase",
            "Pick an enemy unit that was targeted by this unit's shooting attacks this turn. Add 1 to hit rolls for shooting attacks made by friendly units that target that unit for the rest of the turn.")],
    ))
    add_unit(data, u(
        "alchemite-warforger", "Alchemite Warforger",
        ["hero", "wizard", "infantry"],
        {"control": 2, "health": 5, "move": 5, "save": 5},
        melee=[w("tongstaff", "Tongstaff", 3, 4, 4, 1, "D3")],
        abilities=[ab("blazing-weapons", "Blazing Weapons", "Your Hero Phase",
            "Pick a friendly unit wholly within 12 inches of this unit to be the target, then make a casting roll of 2D6. On a 6+, the target's melee weapons have Crit (Mortal) until the start of your next turn.")],
    ))
    add_unit(data, u(
        "freeguild-fusiliers", "Freeguild Fusiliers",
        ["infantry", "castelite", "reinforcements"],
        {"control": 1, "health": 1, "move": 5, "save": 4},
        ranged=[w("fusil-cannon", "Fusil-cannon", 2, 4, 4, 1, 1, range=18)],
        melee=[w("bayonet", "Bayonet", 1, 4, 4, 0, 1)],
        abilities=[
            ab("blackpowder-squire", "Blackpowder Squire", "Passive",
               "While this unit has a Blackpowder Squire token, this unit's ranged weapons have Shoot in Combat."),
            ab("cant-stop", "Can't Stop!", "Once Per Turn (Army), Your Shooting Phase",
               "Pick another friendly Freeguild Fusiliers unit to be the target. Remove this unit's Blackpowder Squire token from the battlefield, then give it to the target."),
        ],
    ))
    add_unit(data, u(
        "wildercorps-hunters", "Wildercorps Hunters",
        ["infantry"],
        {"control": 1, "health": 1, "move": 5, "save": 5},
        ranged=[w("hunting-crossbow", "Hunting Crossbow", 2, 4, 4, 1, 1, range=15)],
        melee=[
            w("hunting-weapons", "Hunting Weapons", 2, 4, 4, 0, 1),
            w("trailhounds-ferocious-bite", "Trailhound's Ferocious Bite", 2, 4, 3, 0, 1),
        ],
        abilities=[
            ab("wildercorps-composition", "Wildercorps Hunters", "Passive",
               "Each model is armed with a Hunting Crossbow and Hunting Weapons. The Wildercorps Warden is also armed with a Trailhound's Ferocious Bite. 4 models are Trailhounds armed with a Trailhound's Ferocious Bite instead of any other weapons."),
            ab("expert-trackers", "Expert Trackers", "Deployment Phase",
               "This unit can use the 'Normal Move' ability as if it were your movement phase."),
        ],
    ))
    add_spearhead(data, {
        "slug": "fusil-platoon",
        "factionSlug": "cities-of-sigmar",
        "name": "Fusil-Platoon",
        "units": [
            slot("fusil-major-on-ogor-warhulk", general=True),
            slot("alchemite-warforger", 1),
            slot("freeguild-fusiliers", 6, reinf=True),  # 5 + squire token unit
            slot("freeguild-fusiliers", 5, reinf=True),
            slot("wildercorps-hunters", 11),
        ],
        "battleTraits": [
            ab("fortify-position", "Fortify Position", "Passive",
               "Subtract 1 from the Rend characteristic of weapons used for attacks that target friendly Castelite units if they did not use a Move ability in the same turn."),
            ab("respected-leader", "Respected Leader", "Once Per Battle, Deployment Phase",
               "Friendly Wildercorps Hunters units gain the Reinforcements keyword."),
        ],
        "regimentAbilities": [
            ab("well-provisioned", "Well Provisioned", "Once Per Turn (Army), Your Shooting Phase",
               "Pick a friendly non-Hero unit to be the target. Roll a dice. On a 3+, add 1 to wound rolls for that unit's shooting attacks for the rest of the phase."),
            ab("adept-tactician", "Adept Tactician", "Once Per Battle, Your Movement Phase",
               "Pick 2 friendly Freeguild Fusiliers units that have been destroyed and have not already been replaced. Set up a single replacement Freeguild Fusiliers unit with 10 models more than 6 inches from all enemy units."),
        ],
        "enhancements": [
            ab("brace", "Brace!", "Passive", "Your general has Ward (5+)."),
            ab("shield-bash", "Shield Bash", "Once Per Turn, Your Movement Phase",
               "Pick an enemy Infantry, War Machine or Cavalry unit in combat with your general. Roll a dice. On a 3+, the target must immediately use the Retreat ability as if it were the enemy movement phase."),
            ab("point-blank-volley", "Point-blank Volley", "Once Per Turn, Enemy Combat Phase",
               "Pick an enemy unit in combat with your general. Roll a D3. On a 2+, inflict an amount of mortal damage on the target equal to the roll."),
        ],
    })

    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Done: {len(data['factions'])} factions, {len(data['unitTypes'])} units, {len(data['spearheads'])} spearheads")
    for s in data["spearheads"]:
        print(f"  - {s['name']}")

if __name__ == "__main__":
    main()
