#!/usr/bin/env python3
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

    # ========== DEATHRATTLE TOMB HOST ==========
    # Reuse existing deathrattle-skeletons (do not overwrite Bloodcrave datasheet).
    add_unit(data, u(
        "wight-king", "Wight King",
        ["hero", "infantry", "ward (6+)"],
        {"control": 2, "health": 5, "move": 4, "save": 3},
        melee=[w("baleful-tomb-blade", "Baleful Tomb Blade", 5, 4, 3, 1, 2, ["Crit(Mortal)"])],
        abilities=[ab("king-of-shambling-bones", "King of Shambling Bones", "Your Hero Phase",
            "Pick a friendly Deathrattle unit wholly within 12 inches of this unit to be the target. Roll a dice. On a 2+, add 1 to hit rolls for combat attacks made by the target for the rest of the turn.")],
    ))
    add_unit(data, u(
        "barrow-guard", "Barrow Guard",
        ["infantry", "ward (6+)"],
        {"control": 1, "health": 1, "move": 4, "save": 4},
        melee=[w("wight-blade", "Wight Blade", 2, 4, 3, 1, 1, ["Crit(Mortal)"])],
        abilities=[ab("guardians-of-the-king", "Guardians of the King", "Passive",
            "While your general is within this unit's combat range, both this unit and your general have Ward (5+).")],
    ))
    add_unit(data, u(
        "barrow-knights", "Barrow Knights",
        ["cavalry", "ward (6+)"],
        {"control": 1, "health": 3, "move": 10, "save": 4},
        melee=[
            w("barrow-lance", "Barrow Lance", 2, 4, 3, 1, 1, ["Crit(Mortal)", "Charge(+1 Damage)"]),
            w("skeletal-steeds-hooves-and-teeth", "Skeletal Steed's Hooves and Teeth", 2, 5, 3, 0, 1, ["Companion"]),
        ],
        abilities=[ab("cursed-to-rise-once-more", "Cursed to Rise Once More", "End of Your Turn",
            "You can return 1 slain model to this unit.")],
    ))
    add_spearhead(data, {
        "slug": "deathrattle-tomb-host",
        "factionSlug": "soulblight-gravelords",
        "name": "Deathrattle Tomb Host",
        "units": [
            slot("wight-king", general=True),
            slot("barrow-guard", 10),
            slot("barrow-knights", 5),
            slot("deathrattle-skeletons", 10),
            slot("deathrattle-skeletons", 10),
        ],
        "battleTraits": [
            ab("the-unquiet-dead", "The Unquiet Dead", "Once Per Battle (Army), Your Movement Phase",
               "One of your Deathrattle Skeletons units is not set up during the deployment phase. From the third battle round onwards, it can use The Rising Dead: set up this unit anywhere on the battlefield wholly within 3 inches of a battlefield edge and more than 6 inches from all enemy units."),
            ab("aura-of-antiquity", "Aura of Antiquity", "Once Per Turn (Army), Your Combat Phase",
               "Pick an enemy unit in combat with any friendly units to be the target. Roll a dice. On a 3+, subtract 1 from the Rend characteristic of the target's melee weapons until the start of your next turn."),
        ],
        "regimentAbilities": [
            ab("overwhelming-hordes", "Overwhelming Hordes", "Passive",
               "Add 1 to wound rolls for combat attacks made by friendly non-Hero units that target a unit that has fewer models than the attacking unit."),
            ab("deathmarch", "Deathmarch", "Once Per Turn (Army), Your Hero Phase",
               "Pick a friendly non-Hero unit that is not in combat to be the target. For the rest of the turn, add 1 inch to the target's Move characteristic and add 3 to its control score."),
        ],
        "enhancements": [
            ab("shyishan-blade", "Shyishan Blade", "Passive",
               "The Rend characteristic of your general's Baleful Tomb Blade is 2."),
            ab("stolen-animus", "Stolen Animus", "Passive",
               "Each time your general scores a critical hit, Heal (2) your general after the Attack ability has been resolved."),
            ab("propelled-by-hate", "Propelled by Hate", "Your Charge Phase",
               "Pick another friendly unit wholly within 12 inches of your general to be the target. You can re-roll charge rolls for the target for the rest of the turn."),
            ab("soul-drain-pendant", "Soul-Drain Pendant", "Once Per Battle, Any Combat Phase",
               "Pick an enemy unit in combat with your general to be the target. Roll a dice. On a 2+, the target has Strike-last for the rest of the turn."),
        ],
    })

    # ========== TYRANT'S BELLOW ==========
    # Distinct from Warglutt Marauders' Tyrant (meatcleavers / roaring warlord).
    add_unit(data, u(
        "tyrant-bellow", "Tyrant",
        ["hero", "infantry"],
        {"control": 5, "health": 8, "move": 6, "save": 4},
        ranged=[w("tyrant-bellow-ogor-pistols", "Ogor Pistols", 2, 4, 3, 1, "D3", ["Shoot in Combat"], range=10)],
        melee=[
            w("tyrant-bellow-thundermace", "Thundermace", 3, 4, 2, 2, 3),
            w("tyrant-bellow-beastskewer-glaive", "Beastskewer Glaive", 2, 4, 2, 1, 2, ["Anti-Monster(+1 Rend)"]),
        ],
        abilities=[ab("bully-of-the-first-degree", "Bully of the First Degree", "Your Hero Phase",
            "Pick a friendly unit wholly within 12 inches of this unit to be the target. You cannot pick this unit. Add 3 to the control score of the target until the start of your next turn.")],
    ))
    add_unit(data, u(
        "ironblaster", "Ironblaster",
        ["war machine"],
        {"control": 2, "health": 9, "move": 9, "save": 4},
        ranged=[w("ironblaster-cannon", "Ironblaster Cannon", 2, 4, 2, 2, "D3+3", range=18)],
        melee=[
            w("ironblaster-clubber", "Clubber", 2, 4, 2, 0, 2),
            w("ironblaster-rhinoxs-sharp-horns", "Rhinox's Sharp Horns", 2, 4, 2, 1, "D3", ["Companion"]),
        ],
        abilities=[ab("rhinox-charge", "Rhinox Charge", "Passive",
            "The Damage characteristic of this unit's Rhinox's Sharp Horns is 3 if it charged in the same turn.")],
    ))
    add_unit(data, u(
        "leadbelchers", "Leadbelchers",
        ["infantry"],
        {"control": 2, "health": 4, "move": 6, "save": 5},
        ranged=[w("leadbelcher-gun", "Leadbelcher Gun", "D3", 4, 3, 1, 1, range=15)],
        melee=[w("bludgeoning-blow", "Bludgeoning Blow", 2, 4, 2, 0, 2)],
        abilities=[ab("firing-from-the-belly", "Firing From the Belly", "Passive",
            "Add 1 to hit rolls for this unit's shooting attacks if it has not used a Move ability this turn.")],
    ))
    add_unit(data, u(
        "mournfang-pack", "Mournfang Pack",
        ["cavalry"],
        {"control": 2, "health": 6, "move": 9, "save": 4},
        melee=[
            w("culling-clubs-and-hackers", "Culling Clubs and Hackers", 3, 4, 2, 1, 2),
            w("mournfangs-tusks", "Mournfang's Tusks", 4, 4, 2, 1, 2, ["Companion"]),
        ],
        abilities=[ab("linebreakers", "Linebreakers", "Passive",
            "Subtract 1 from wound rolls for shooting attacks that target this unit.")],
    ))
    add_unit(data, u(
        "ogor-gluttons", "Ogor Gluttons",
        ["infantry"],
        {"control": 2, "health": 4, "move": 6, "save": 5},
        melee=[w("ogor-weapons", "Ogor Weapons", 4, 4, 2, 1, 2)],
        abilities=[ab("driven-by-hunger", "Driven by Hunger", "Passive",
            "Add 1 to charge rolls for this unit.")],
    ))
    add_spearhead(data, {
        "slug": "tyrants-bellow",
        "factionSlug": "ogor-mawtribes",
        "name": "Tyrant's Bellow",
        "units": [
            slot("tyrant-bellow", general=True),
            slot("mournfang-pack", 2),
            slot("ogor-gluttons", 3),
            slot("ogor-gluttons", 3),
            slot("leadbelchers", 4),
            slot("ironblaster", 1),
        ],
        "battleTraits": [
            ab("on-the-mawpath", "On the Mawpath", "Your Movement Phase",
               "Your Ironblaster, Mournfang Pack and 1 unit of Ogor Gluttons are not set up during the deployment phase. From the third battle round onwards they can use Bellowing Arrival: set up this unit anywhere on the battlefield, within 1 inch of a battlefield edge and more than 6 inches from all enemy units."),
        ],
        "regimentAbilities": [
            ab("pulverising-girth", "Pulverising Girth", "Once Per Phase, Any Charge Phase",
               "Pick any number of friendly units that charged this phase. For each of those units, pick an enemy unit in combat with it and roll a dice. On a 4+, inflict 1 mortal damage on that enemy unit."),
            ab("bred-for-toughness", "Bred for Toughness", "Passive",
               "Add 1 to the Health characteristic of your Ironblaster and your Mournfang Pack unit."),
        ],
        "enhancements": [
            ab("longstrider", "Longstrider", "Passive",
               "Your general has a Move characteristic of 8 inches instead of 6 inches."),
            ab("booming-roar", "Booming Roar", "Any Combat Phase",
               "Roll a dice. On a 4+, subtract 1 from hit rolls for attacks made by enemy units this phase while they are within 9 inches of your general."),
            ab("flask-of-stonehorn-blood", "Flask of Stonehorn Blood",
               "Once Per Battle, Reaction: Opponent declared an Attack ability and targeted your general",
               "Your general has Ward (3+) this phase."),
            ab("blubbergrub", "Blubbergrub", "Once Per Battle, Any Movement Phase",
               "Pick either your Ironblaster or your Mournfang Pack unit if it is within your general's combat range. Heal (D6) that unit."),
        ],
    })

    # ========== FANGS OF THE BLOOD GOD ==========
    add_faction(data, "blades-of-khorne", "Blades of Khorne")
    add_unit(data, u(
        "karanak", "Karanak",
        ["hero", "beast", "ward (6+)"],
        {"control": 2, "health": 7, "move": 8, "save": 5},
        melee=[w("savage-maws-and-goreslick-claws", "Savage Maws and Goreslick Claws", 6, 4, 3, 1, 2, ["Anti-Hero(+1 Rend)"])],
        abilities=[ab("stalk-the-prey", "Stalk the Prey", "Any Hero Phase",
            "This unit can move D6 inches. It cannot end that move in combat unless it was in combat at the start of that move and, if there is an enemy quarry on the battlefield, it must end that move closer to the quarry.")],
    ))
    add_unit(data, u(
        "flesh-hounds", "Flesh Hounds",
        ["beast", "ward (6+)", "reinforcements"],
        {"control": 1, "health": 2, "move": 8, "save": 6},
        melee=[w("blood-dark-claws", "Blood-dark Claws", 4, 4, 3, 0, 1)],
        abilities=[ab("unflagging-hunters", "Unflagging Hunters", "Passive",
            "Add 1 to charge rolls for this unit.")],
    ))
    add_unit(data, u(
        "claws-of-karanak", "Claws of Karanak",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 1, "move": 6, "save": 5},
        melee=[w("weapons-of-the-hunt", "Weapons of the Hunt", 3, 4, 3, 0, 1, ["Crit(2 Hits)"])],
        abilities=[ab("pack-hunters", "Pack Hunters", "Any Combat Phase",
            "Pick an enemy unit in combat with both this unit and a friendly Flesh Hounds unit to be the target. For the rest of the turn, this unit's combat attacks that target that enemy unit score critical hits on unmodified hit rolls of 5+.")],
    ))
    add_spearhead(data, {
        "slug": "fangs-of-the-blood-god",
        "factionSlug": "blades-of-khorne",
        "name": "Fangs of the Blood God",
        "units": [
            slot("karanak", general=True),
            slot("flesh-hounds", 5, reinf=True),
            slot("flesh-hounds", 5, reinf=True),
            slot("claws-of-karanak", 8, reinf=True),
        ],
        "battleTraits": [
            ab("the-quarry", "The Quarry", "Start of Battle Round",
               "If no enemy units are the quarry, pick an enemy unit to be the quarry (you can pick an enemy unit in reserve)."),
            ab("blood-drenched", "Blood-drenched", "Once Per Turn, End of Any Turn",
               "Pick a friendly unit that slew any enemy models using a Fight ability this turn to be the target. For the rest of the battle, the target's melee weapons have Crit (Mortal)."),
        ],
        "regimentAbilities": [
            ab("the-scent-of-blood", "The Scent of Blood", "Passive",
               "Add 1 to hit rolls and add 1 to wound rolls for combat attacks that target an enemy unit that had any damage points allocated to it this turn."),
            ab("savagery-upon-savagery", "Savagery Upon Savagery", "Once Per Battle, Any Combat Phase",
               "Pick a friendly unit in combat to be the target. For the rest of the turn, add 1 to the Attacks characteristic of the target's melee weapons. If the target is a Hero, add D3 to the Attacks characteristic of its melee weapons instead."),
        ],
        "enhancements": [
            ab("sustained-by-gore", "Sustained by Gore", "End of Any Turn", "Heal (D3) your general."),
            ab("evasive-hunter", "Evasive Hunter", "Passive",
               "Subtract 1 from hit rolls and wound rolls for shooting attacks that target your general."),
            ab("killing-pounce", "Killing Pounce", "Once Per Battle, Any Charge Phase",
               "For the rest of the turn, when making charge rolls for your general, you can roll an additional dice, to a maximum of 3, but if you do, they must finish that charge in combat with the quarry."),
            ab("furious-bites", "Furious Bites", "End of Any Turn",
               "If your general is in combat with the quarry, inflict D3 mortal damage on the quarry."),
        ],
    })

    # ========== SOULRAID HUNT ==========
    add_faction(data, "idoneth-deepkin", "Idoneth Deepkin")
    add_unit(data, u(
        "isharann-soulscryer", "Isharann Soulscryer",
        ["hero", "infantry"],
        {"control": 2, "health": 5, "move": 6, "save": 5},
        ranged=[w("scryfish-shoal", "Scryfish Shoal", 8, 5, 5, 0, 1, ["Shoot in Combat", "Companion"], range=10)],
        melee=[w("abyssal-touch", "Abyssal Touch", 3, 3, 4, 0, "D3")],
        abilities=[ab("ritual-of-the-creeping-mist", "Ritual of the Creeping Mist", "Your Hero Phase",
            "Pick a visible friendly unit wholly within 12 inches of this unit to be the target, then roll a dice. On a 3+, until the start of your next turn, subtract 1 from wound rolls for attacks that target that unit.")],
    ))
    add_unit(data, u(
        "akhelian-morrsarr-guard", "Akhelian Morrsarr Guard",
        ["cavalry", "fly"],
        {"control": 1, "health": 4, "move": 14, "save": 4},
        melee=[
            w("voltspear", "Voltspear", 2, 3, 4, 1, 1, ["Charge(+1 Damage)"]),
            w("fangmoras-fangs-and-lashing-tail", "Fangmora's Fangs and Lashing Tail", 3, 4, 3, 1, "D3", ["Companion"]),
        ],
        abilities=[ab("biovoltaic-blast", "Biovoltaic Blast", "Once Per Battle, Any Charge Phase",
            "If this unit charged this phase, pick an enemy unit within 1 inch of it to be the target, then roll a number of dice equal to the number of models in this unit. For each 4-5, inflict 1 mortal damage on the target. For each 6+, inflict D3 mortal damage on the target. Add 1 to each roll if there are more models in the target unit than this unit.")],
    ))
    add_unit(data, u(
        "akhelian-allopex", "Akhelian Allopex",
        ["cavalry", "fly"],
        {"control": 2, "health": 8, "move": 12, "save": 4},
        ranged=[w("razorshell-harpoon-launcher", "Razorshell Harpoon Launcher", 2, 3, 2, 1, 3, ["Anti-Monster(+1 Rend)"], range=18)],
        melee=[
            w("barbed-hooks-and-blades", "Barbed Hooks and Blades", 4, 3, 4, 1, 1),
            w("allopexs-ferocious-bite", "Allopex's Ferocious Bite", 3, 4, 2, 2, 2, ["Companion"]),
        ],
        abilities=[ab("bloodthirsty-predators", "Bloodthirsty Predators", "Passive",
            "Add 1 to the Attacks characteristic of this unit's Allopex's Ferocious Bite if it is within 6 inches of any damaged enemy units or if it is within 6 inches of any enemy units that have had any models slain in the same turn.")],
    ))
    add_unit(data, u(
        "namarti-thralls", "Namarti Thralls",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 1, "move": 6, "save": 5},
        melee=[w("lanmari", "Lanmari", 2, 3, 4, 1, 1, ["Anti-Infantry(+1 Rend)"])],
        abilities=[ab("sweeping-blows", "Sweeping Blows", "Passive",
            "Add 1 to the Damage characteristic of this unit's Lanmari for attacks that target an enemy Monster.")],
    ))
    add_spearhead(data, {
        "slug": "soulraid-hunt",
        "factionSlug": "idoneth-deepkin",
        "name": "Soulraid Hunt",
        "units": [
            slot("isharann-soulscryer", general=True),
            slot("akhelian-morrsarr-guard", 3),
            slot("akhelian-allopex", 1),
            slot("namarti-thralls", 5, reinf=True),
            slot("namarti-thralls", 5, reinf=True),
        ],
        "battleTraits": [
            ab("tides-of-death", "Tides of Death", "Passive",
               "In each battle round, all friendly units have the Tides of Death passive ability that corresponds to the current battle round number. Round 1 Low Tide: Subtract 1 from hit rolls for shooting attacks that target this unit. Round 2 Flood Tide: This unit can use a Run ability and still use Shoot and/or Charge abilities later in the turn. Round 3 High Tide: This unit has Strike-first. Round 4 Ebb Tide: This unit can use a Retreat ability and still use Shoot and/or Charge abilities later in the turn."),
        ],
        "regimentAbilities": [
            ab("way-of-the-cresting-wave", "Way of the Cresting Wave", "Passive",
               "Add 1 to the Rend characteristic of melee weapons used by friendly Namarti Thralls units that charged in the same turn."),
            ab("mind-flare", "Mind Flare", "Once Per Battle, Any Combat Phase",
               "Pick an enemy unit in combat with your general. Until the end of the phase, attacks made by that unit only score hits on unmodified hit rolls of 6."),
            ab("ethersea-predators", "Ethersea Predators", "Once Per Turn (Army), End of Any Turn",
               "Pick a friendly Cavalry unit that used a Fight ability this turn. Heal (D3) that unit."),
        ],
        "enhancements": [
            ab("arch-ritualist", "Arch-Ritualist", "Passive",
               "Add 1 to rolls for your general's 'Ritual of the Creeping Mist' ability."),
            ab("delicious-morsels", "Delicious Morsels", "Your Hero Phase",
               "Heal (1) each friendly Cavalry unit within your general's combat range."),
            ab("steelshell-armour", "Steelshell Armour", "Passive",
               "Ignore all modifiers to save rolls for your general (positive and negative)."),
        ],
    })

    # ========== CASTELITE COMPANY ==========
    # Steelhelms datasheet differs from Zenestra's (Consecrate vs Fanatical Followers).
    add_unit(data, u(
        "freeguild-cavalier-marshal", "Freeguild Cavalier-Marshal",
        ["hero", "cavalry"],
        {"control": 2, "health": 7, "move": 10, "save": 3},
        ranged=[w("dragoon-pistol", "Dragoon Pistol", 2, 3, 4, 1, 1, ["Shoot in Combat"], range=10)],
        melee=[
            w("master-forged-longsword", "Master-forged Longsword", 5, 3, 4, 1, 2),
            w("cavalier-marshal-warhorse-hooves", "Warhorse's Steel-shod Hooves", 2, 5, 3, 0, 1, ["Companion"]),
        ],
        abilities=[ab("decisive-commander", "Decisive Commander", "Your Hero Phase",
            "Pick a friendly Freeguild Steelhelms unit wholly within 12 inches of this unit to be the target and roll a dice. On a 2+, pick 1: On Your Feet!: If the target unit is not in combat, you can return D3 slain models to it. Yield No Quarter!: Add 3 to the target unit's control score until the start of your next turn.")],
    ))
    add_unit(data, u(
        "castelite-steelhelms", "Freeguild Steelhelms",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 1, "move": 5, "save": 4},
        melee=[w("castelite-freeguild-weapon", "Freeguild Weapon", 2, 4, 4, 0, 1)],
        abilities=[ab("consecrate-the-land", "Consecrate the Land", "Your Movement Phase",
            "If this unit is contesting an objective you control that is not contested by any enemy models, roll a dice. On a 3+, that objective is considered by you to be consecrated. Friendly units have Ward (6+) while they are contesting a consecrated objective. If your opponent gains control of a consecrated objective, it is no longer consecrated.")],
    ))
    add_unit(data, u(
        "freeguild-cavaliers", "Freeguild Cavaliers",
        ["cavalry"],
        {"control": 1, "health": 3, "move": 10, "save": 3},
        melee=[
            w("cavalier-weapon", "Cavalier Weapon", 3, 4, 4, 1, 1, ["Charge(+1 Damage)"]),
            w("cavaliers-warhorse-hooves", "Warhorse's Steel-shod Hooves", 2, 5, 3, 0, 1, ["Companion"]),
        ],
        abilities=[ab("devastating-charge", "Devastating Charge", "Any Charge Phase",
            "If this unit charged this phase, pick an enemy unit in combat with it to be the target and roll a dice. On a 2+, inflict D3 mortal damage on the target.")],
    ))
    add_unit(data, u(
        "ironweld-great-cannon", "Ironweld Great Cannon",
        ["war machine"],
        {"control": 2, "health": 8, "move": 3, "save": 4},
        ranged=[
            w("great-cannon-cannonball", "Great Cannon: Cannonball", 2, 4, 2, 2, "D3+2", range=24),
            w("great-cannon-grapeshot", "Great Cannon: Grapeshot", 5, 3, 3, 1, 2, range=12),
        ],
        melee=[w("crews-tools-and-sidearms", "Crew's Tools and Sidearms", 2, 4, 4, 0, 1)],
        abilities=[ab("shot-and-shell", "Shot and Shell", "Passive",
            "Each time this unit uses a Shoot ability, choose either the Cannonball or Grapeshot weapon characteristics for all the attacks it makes with its Great Cannon. The Cannonball can only be chosen if this unit has not used a Move ability that turn.")],
    ))
    add_spearhead(data, {
        "slug": "castelite-company",
        "factionSlug": "cities-of-sigmar",
        "name": "Castelite Company",
        "units": [
            slot("freeguild-cavalier-marshal", general=True),
            slot("castelite-steelhelms", 5, reinf=True),
            slot("castelite-steelhelms", 5, reinf=True),
            slot("freeguild-cavaliers", 5),
            slot("ironweld-great-cannon", 1),
        ],
        "battleTraits": [
            ab("the-officars-order", "The Officar's Order", "Once Per Battle, Start of Battle Round",
               "Pick a battle tactic card in your hand and place it face-down separately next to your other battle tactic cards. The information on it is still hidden from your opponent but make it clear which card is separate. The card stays separate until you use the command on it or score the battle tactic on it as described below. When you use the command on that card, it is not discarded but returns to your hand. Your opponent can check the information on it before it returns to your hand. The card goes back to being a normal battle tactic card, with the exception that you cannot use the command on it in the same phase it went back into your hand. If you did not use the command on the card you separated, you can still score the battle tactic on it at the end of your turn as normal if you met its conditions. If you do so, discard it as normal. If you neither used the command nor scored the battle tactic on the card, it automatically returns to your hand at the end of your turn."),
        ],
        "regimentAbilities": [
            ab("for-sigmar-charge", "For Sigmar, Charge!", "Once Per Battle, Your Charge Phase",
               "Use this ability before any Charge abilities are used this phase. Friendly Cavalry units that charge this phase have Strike-first this turn."),
            ab("ironweld-discipline", "Ironweld Discipline", "Once Per Battle, Enemy Shooting Phase",
               "Pick your Ironweld Great Cannon to use this ability. It can use the 'Shoot' ability as if it were your shooting phase."),
        ],
        "enhancements": [
            ab("flask-of-lethisian-darkwater", "Flask of Lethisian Darkwater", "End of Any Turn",
               "Heal (D6) your general."),
            ab("glimmering", "Glimmering", "Passive",
               "Each phase, you can re-roll 1 hit roll, or 1 wound roll, or 1 save roll made for your general."),
            ab("brazier-of-holy-flame", "Brazier of Holy Flame", "Once Per Battle, Start of Any Turn",
               "Pick a friendly Freeguild Steelhelms unit within your general's combat range. You can return up to D3 slain models to that unit."),
            ab("heirloom-blade", "Heirloom Blade", "Passive",
               "Add 1 to the Rend characteristic of your general's Master-forged Longsword."),
        ],
    })

    # ========== GNAWFEAST CLAWPACK ==========
    add_faction(data, "skaven", "Skaven")
    add_unit(data, u(
        "clawlord-on-gnaw-beast", "Clawlord on Gnaw-beast",
        ["hero", "cavalry", "ward (6+)"],
        {"control": 2, "health": 7, "move": 9, "save": 4},
        ranged=[w("ratling-pistol", "Ratling Pistol", "D6", 3, 3, 1, 1, ["Crit(Auto-wound)", "Shoot in Combat"], range=10)],
        melee=[
            w("warpforged-halberd", "Warpforged Halberd", 5, 3, 4, 1, 2),
            w("gnaw-beasts-chisel-fangs", "Gnaw-beast's Chisel Fangs", 4, 4, 3, 1, "D3", ["Companion"]),
        ],
        abilities=[ab("cornered-rat", "Cornered Rat", "Passive",
            "While this unit is damaged, add 3 to the Attacks characteristic of its Warpforged Halberd.")],
    ))
    add_unit(data, u(
        "grey-seer", "Grey Seer",
        ["hero", "wizard", "infantry"],
        {"control": 2, "health": 5, "move": 6, "save": 6},
        melee=[w("warpstone-staff", "Warpstone Staff", 3, 4, 4, 1, "D3")],
        abilities=[
            ab("will-of-the-horned-rat", "Will of the Horned Rat", "Your Hero Phase",
               "Pick a friendly unit wholly within 13 inches of this unit to be the target, then roll a dice. On a 3+, add the roll to the target's control score until the start of your next turn."),
            ab("wither", "Wither", "Your Hero Phase",
               "Pick a visible enemy unit within 13 inches of this unit to be the target, then make a casting roll of 2D6. On a 6+, inflict D3 mortal damage on the target."),
        ],
    ))
    add_unit(data, u(
        "warlock-engineer", "Warlock Engineer",
        ["hero", "infantry"],
        {"control": 2, "health": 5, "move": 6, "save": 5},
        ranged=[w("warplock-musket", "Warplock Musket", 2, 3, 3, 2, "D3", ["Crit(Auto-wound)"], range=24)],
        melee=[w("warpforged-dagger", "Warpforged Dagger", 3, 4, 4, 0, 2)],
        abilities=[ab("more-more-warp-energy", "More-More Warp Energy!",
            "Reaction: You declared a Shoot ability for this unit and it has not used a Move ability this turn",
            "Roll a dice. On a 2+, set the Damage characteristic of its Warplock Musket to 3 this phase. On a 1, inflict D3 mortal damage on this unit.")],
    ))
    add_unit(data, u(
        "clanrats", "Clanrats",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 1, "move": 6, "save": 5},
        melee=[w("rusty-blade", "Rusty Blade", 2, 4, 5, 0, 1)],
        abilities=[ab("seething-swarm", "Seething Swarm", "End of Any Turn",
            "You can return D3 slain models to this unit.")],
    ))
    add_unit(data, u(
        "rat-ogors", "Rat Ogors",
        ["infantry"],
        {"control": 1, "health": 4, "move": 6, "save": 5},
        ranged=[w("warpfire-gun", "Warpfire Gun", "2D6", 2, 4, 2, 1, ["Shoot in Combat"], range=10)],
        melee=[w("claws-blades-and-fangs", "Claws, Blades and Fangs", 5, 4, 3, 1, 2)],
        abilities=[
            ab("rat-ogors-composition", "Rat Ogors", "Passive",
               "This unit has 2 Rat Ogors armed with Claws, Blades and Fangs, and 1 Rat Ogor armed with a Warpfire Gun and Claws, Blades and Fangs."),
            ab("unleashed-warp-fury", "Unleashed Warp-Fury", "Once Per Battle, Any Combat Phase",
               "Inflict D3 mortal damage on this unit. Then, add 1 to the Attacks characteristic of its melee weapons this phase."),
        ],
    ))
    add_spearhead(data, {
        "slug": "gnawfeast-clawpack",
        "factionSlug": "skaven",
        "name": "Gnawfeast Clawpack",
        "units": [
            slot("clawlord-on-gnaw-beast", general=True),
            slot("grey-seer", 1),
            slot("warlock-engineer", 1),
            slot("clanrats", 10, reinf=True),
            slot("clanrats", 10, reinf=True),
            slot("rat-ogors", 3),
        ],
        "battleTraits": [
            ab("the-lurking-vermintide", "The Lurking Vermintide", "Once Per Battle, Deployment Phase",
               "Pick a friendly unit that has not been deployed to be the target. The target unit is set up in reserve in the tunnels below. Units in the tunnels below that have not used the 'Gnawhole Ambush' ability by the end of the third battle round are destroyed."),
            ab("gnawhole-ambush", "Gnawhole Ambush", "Your Movement Phase",
               "Pick a friendly unit that is in the tunnels below to use this ability. Set up that unit wholly within 6 inches of a corner of the battlefield and more than 9 inches from all enemy units."),
        ],
        "regimentAbilities": [
            ab("warpstone-laced-bullets", "Warpstone-Laced Bullets", "Once Per Battle, Your Shooting Phase",
               "Pick a ranged weapon a friendly unit is armed with. That weapon has Crit (Mortal) this phase."),
            ab("too-quick-to-hit-hit", "Too Quick to Hit-Hit", "Passive",
               "No mortal damage is inflicted on friendly units when they use Retreat abilities."),
        ],
        "enhancements": [
            ab("lead-the-seething-horde", "Lead the Seething Horde",
               "Reaction: You declared the 'Call for Reinforcements' ability",
               "Instead of using the set-up instructions in the 'Call for Reinforcements' ability, the replacement unit can be set up wholly within 13 inches of this unit and not in combat."),
            ab("skryre-connections", "Skryre Connections", "Passive",
               "Your general's Ratling Pistol has an Attacks characteristic of 2D6 instead of D6."),
            ab("warpstone-charm", "Warpstone Charm", "Passive",
               "Subtract 1 from save rolls for enemy units in combat with your general."),
            ab("cloak-of-stitched-victories", "Cloak of Stitched Victories", "Passive",
               "Your general has Ward (5+)."),
        ],
    })

    # ========== DARKOATH RAIDERS ==========
    add_faction(data, "slaves-to-darkness", "Slaves to Darkness")
    add_unit(data, u(
        "darkoath-warqueen", "Darkoath Warqueen",
        ["hero", "infantry", "ward (5+)"],
        {"control": 2, "health": 5, "move": 5, "save": 5},
        melee=[w("rune-etched-axe", "Rune-etched Axe", 5, 4, 3, 1, 2, ["Crit(Mortal)"])],
        abilities=[ab("oath-of-supremacy", "Oath of Supremacy", "Your Hero Phase",
            "Pick a friendly unit wholly within 12 inches of your general to be the target. Until the start of your next turn, add 1 to hit rolls for attacks made by the target.")],
    ))
    add_unit(data, u(
        "darkoath-savagers", "Darkoath Savagers",
        ["infantry"],
        {"control": 1, "health": 1, "move": 5, "save": 5},
        melee=[w("darkoath-weapons", "Darkoath Weapons", 2, 4, 3, 0, 1, ["Crit(Mortal)"])],
        abilities=[
            ab("godspeaker", "Godspeaker", "Passive", "1 model in this unit is a Godspeaker."),
            ab("visions-of-glory", "Visions of Glory", "Your Hero Phase",
               "If this unit includes a Godspeaker, roll 8 dice. For each 4+, until the start of your next turn, you can re-roll 1 hit roll, 1 wound roll, 1 run roll or 1 save roll for this unit."),
        ],
    ))
    add_unit(data, u(
        "darkoath-fellriders", "Darkoath Fellriders",
        ["cavalry", "reinforcements"],
        {"control": 1, "health": 3, "move": 12, "save": 5},
        melee=[
            w("fellrider-blades", "Fellrider Blades", 2, 4, 3, 0, 1, ["Charge(+1 Damage)"]),
            w("warsteeds-hooves", "Warsteed's Hooves", 2, 5, 3, 0, 1, ["Companion"]),
        ],
        abilities=[ab("swift-attackers", "Swift Attackers", "Passive",
            "Subtract 1 from hit rolls for shooting attacks that target this unit.")],
    ))
    add_unit(data, u(
        "darkoath-marauders", "Darkoath Marauders",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 1, "move": 5, "save": 5},
        melee=[w("raider-weapons", "Raider Weapons", 2, 4, 3, 0, 1)],
        abilities=[ab("glorious-death", "Glorious Death", "Passive",
            "Each time a model in this unit is slain by a combat attack and that model was in combat with the attacking unit, roll a dice. On a 5+, inflict 1 mortal damage on the attacking unit after the Fight ability has been resolved.")],
    ))
    add_spearhead(data, {
        "slug": "darkoath-raiders",
        "factionSlug": "slaves-to-darkness",
        "name": "Darkoath Raiders",
        "units": [
            slot("darkoath-warqueen", general=True),
            slot("darkoath-savagers", 10),
            slot("darkoath-fellriders", 5, reinf=True),
            slot("darkoath-marauders", 10, reinf=True),
        ],
        "battleTraits": [
            ab("oaths-of-darkness", "Oaths of Darkness", "Once Per Turn (Army), Your Hero Phase",
               "You can reveal 1 battle tactic card in your hand to your opponent. If you do so, that battle tactic card becomes your oath for the rest of the turn. While this battle tactic card is your oath, you can still use the command on it, or attempt to score the battle tactic on it, as normal. If you score the battle tactic on your oath this turn, your oath is fulfilled. Instead of discarding the card, it is placed to one side but you can still use the command on it. Once you do so, the card is discarded as normal. Fulfilled oaths placed to one side in this way do not count towards the 3 battle tactic cards you can have in your hand. If you use the command on your oath before it is scored, it is discarded as normal. At the end of the turn, if the oath is still in your hand and that oath has not been fulfilled, it ceases to be your oath."),
        ],
        "regimentAbilities": [
            ab("rage-of-arkhar", "Rage of Arkhar", "Once Per Turn (Army), Any Combat Phase",
               "Pick a friendly unit in combat to be the target. For the rest of the turn, add 1 to the Rend characteristic of the target's melee weapons. This does not affect Companion weapons."),
            ab("fearless-invaders", "Fearless Invaders", "Once Per Turn (Army), Your Movement Phase",
               "Pick a friendly unit in combat to be the target. If the target uses a Retreat ability this turn, no mortal damage is inflicted on it and it can still use Charge abilities later in the turn."),
        ],
        "enhancements": [
            ab("bloodthirsty-blade", "Bloodthirsty Blade", "Passive",
               "The Rend characteristic of your general's Rune-etched Axe is 2."),
            ab("godshadow-talisman", "Godshadow Talisman", "Passive",
               "Your general has Ward (4+)."),
            ab("champion-of-raids", "Champion of Raids", "Your Charge Phase",
               "Pick another friendly unit wholly within 12 inches of your general to be the target. The target can re-roll charge rolls for the rest of the turn."),
            ab("fell-ritualist", "Fell Ritualist", "Passive",
               "Each time you draw battle tactic cards, if your general is on the battlefield, you can choose to draw 1 additional battle tactic card, then put 1 of your battle tactic cards in your hand back at the bottom of your battle tactic deck."),
        ],
    })

    # ========== SCRAPGLUTT ==========
    add_unit(data, u(
        "mantrappers", "Mantrappers",
        ["hero", "infantry"],
        {"control": 5, "health": 7, "move": 6, "save": 5},
        ranged=[w("mantrapper-crossbow", "Mantrapper Crossbow", 2, 4, 2, 1, "D3", range=12)],
        melee=[
            w("frost-sabres-fangs", "Frost Sabre's Fangs", 3, 4, 3, 1, 1, ["Companion"]),
            w("culling-knife", "Culling Knife", 4, 4, 2, 1, 2),
        ],
        abilities=[
            ab("staying-useful", "Staying Useful", "Passive",
               "While any of this unit's Gnoblar or Frost Sabre tokens are on the battlefield, this unit has Ward (5+). Each time you make a successful ward roll for this unit, remove 1 of this unit's tokens from the battlefield. If this unit's Frost Sabre token has been removed, it can no longer attack with its Frost Sabre's Fangs."),
            ab("no-slacking", "No Slacking!", "Your Hero Phase",
               "Pick a friendly Infantry unit wholly within 12 inches of this unit. Roll a dice. On a 3+, add the result to the target's control score until the start of your next turn."),
        ],
    ))
    add_unit(data, u(
        "gnoblar-scraplauncher", "Gnoblar Scraplauncher",
        ["war machine"],
        {"control": 2, "health": 9, "move": 9, "save": 4},
        ranged=[w("piles-of-old-scrap", "Piles of Old Scrap", "3D6", 4, 4, 0, 1, ["Crit(Auto-wound)"], range=24)],
        melee=[
            w("scrappers-stabbers", "Scrappers' Stabbers", 7, 5, 5, 0, 1),
            w("scraplauncher-rhinoxs-sharp-horns", "Rhinox's Sharp Horns", 2, 4, 2, 1, "D3", ["Companion"]),
        ],
        abilities=[ab("rain-of-scrap", "Rain of Scrap", "Your Shooting Phase",
            "Pick an enemy unit that had any models slain this turn by this unit's shooting attacks to be the target. Subtract 1 from hit rolls for the target's attacks for the rest of the turn.")],
    ))
    add_unit(data, u(
        "gnoblars", "Gnoblars",
        ["infantry", "reinforcements"],
        {"control": 1, "health": 1, "move": 5, "save": 6},
        ranged=[w("sharp-stuff", "Sharp Stuff", 1, 4, 5, 0, 1, range=8)],
        melee=[w("motley-assortment-of-weapons", "Motley Assortment of Weapons", 1, 5, 5, 0, 1)],
        abilities=[ab("no-shortage-of-volunteers", "No Shortage of Volunteers", "End of Any Turn",
            "You can return D3 models to this unit.")],
    ))
    add_unit(data, u(
        "scrapglutt-ironguts", "Ironguts",
        ["infantry"],
        {"control": 2, "health": 4, "move": 6, "save": 5},
        melee=[w("scrapglutt-irongut-weapon", "Irongut Weapon", 3, 4, 2, 2, 3)],
        abilities=[ab("down-to-the-ironguts", "Down to the Ironguts", "Passive",
            "Ignore negative modifiers to this unit's control score.")],
    ))
    add_spearhead(data, {
        "slug": "scrapglutt",
        "factionSlug": "ogor-mawtribes",
        "name": "Scrapglutt",
        "units": [
            slot("mantrappers", general=True),
            slot("scrapglutt-ironguts", 2),
            slot("scrapglutt-ironguts", 2),
            slot("scrapglutt-ironguts", 4),
            slot("gnoblars", 12, reinf=True),
            slot("gnoblar-scraplauncher", 1),
        ],
        "battleTraits": [
            ab("better-late-than-never", "Better Late Than Never", "Your Movement Phase",
               "A unit of Ironguts with 4 models is not set up during the deployment phase. Instead, in the third battle round, that unit can use Let's Get Stuck In: set up this unit wholly within friendly territory, wholly within 6 inches of the battlefield edge, and not in combat."),
        ],
        "regimentAbilities": [
            ab("its-a-hard-life", "It's a Hard Life", "Any Hero Phase",
               "Pick a friendly Gnoblars unit within your general's combat range to be the target. Roll a D3. On a 2+: Heal (X) your general where X is an amount equal to the roll; 1 model in that Gnoblars unit is slain."),
            ab("frenzied-artillery", "Frenzied Artillery", "Passive",
               "If the unmodified charge roll for a friendly Gnoblar Scraplauncher is 6+, add 3 to the Attacks characteristic of the target's Companion weapons for the rest of the turn."),
        ],
        "enhancements": [
            ab("savage-instincts", "Savage Instincts",
               "Reaction: You declared a Fight ability for your general",
               "Pick a friendly unit that has not used a Fight ability this turn and is within your general's combat range to be the target. The target can be picked to use a Fight ability immediately after the Fight ability used by your general has been resolved."),
            ab("nasty-trap", "Nasty Trap", "Once Per Battle, Your Movement Phase",
               "Pick an enemy unit within 12 inches of your general to be the target. Give the target your general's Trap token. While the target has a Trap token, each time the target is picked to use a Move or Charge ability, roll a dice. On a 4+, that Move or Charge ability has no effect and the target's Trap token is removed."),
            ab("massive-bulk", "Massive Bulk", "Passive",
               "Add 2 to the Health characteristic of your general."),
            ab("veteran-hunter", "Veteran Hunter", "Once Per Battle, Any Hero Phase",
               "Pick an enemy unit within 12 inches of your general to be the target. For the rest of the turn, add 1 to the Rend characteristic of your general's combat attacks that target that unit."),
        ],
    })

    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Done: {len(data['factions'])} factions, {len(data['unitTypes'])} units, {len(data['spearheads'])} spearheads")
    for s in data["spearheads"]:
        print(f"  - {s['name']}")

if __name__ == "__main__":
    main()
