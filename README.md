# LEDPS v0.2

## Mostly supported
* Paladin/sentinel bleed-relevant talents
* Ailments: Bleed, Ignite, Poison
* ResistanceShred: Physical, Poison
* Supported attack types: Default, Melee, Spell, Throw
* Skills: Rive, ManifestStrike, DivineBolt, SentinelAxeThrower

## Not supported yet
* Hit damage
* Armour daamge reduction
* Multi target encounter

## Open questions
* Can Trigger trigger?

## Coding/naming conventions
* Naming style: 'camilleCase'
* Class intern variables with leading '\_': '\_variableName'
* Input variables with trailing '\_': 'variableName\_'
* Temporary variables have no '\_'
* Variables/objects start with lowercase letter
* Classes start with uppercase letter
* Function definitions should end either with return or pass

## ToDo-shortlist
* Add more comments
* Implement rotation system to incorporate stuff like Holy Symbols and Divine Aura as skills and not hard-coded
* Refactor modifier to track them differently
  * Account for flat damage
  * Sort by elements
  * Seperate by hit, damageOverTime
  * Generic increases added to both categories
* Equipment-Manager
  * DualWielding: Weapon Aps is not a direct more multiplierfor MeleeAttackSpeed. DualWielding averages both weapon ApS and applies the average as more multiplier
* ArmourShred
* Duration
  * Duration changes should check for minimum value -> smalles duration should be 0 because -1 identifies objects with infinite duration
  * Global modifiers like warpath's 'global more while channeling' should possibly be handled as a buff
* Implement enemy class to handle enemy armour and resistances -> tracked by simulator and/or collection
* Cooldowns
  * Cooldown recovery must be considered
  * Split into scalable and non-scalable cooldowns
