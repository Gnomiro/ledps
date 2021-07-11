# LEDPS v0.2

## Mostly supported
* Paladin/sentinel bleed-relevant talents
* Beastmaster/primalist poison-relevant talents
* Ailments: Bleed, Ignite, Poison, Plague, BlindingPoison
* ResistanceShred: Physical, Poison
* Supported attack types: Default, Melee, Spell, Throw
* Skills: Rive, ManifestStrike, DivineBolt, SentinelAxeThrower, SerpentStrike

## Not supported yet
* Hit damage
* Armour daamge reduction
* Multi target encounter

## Open questions
* Can Trigger trigger?
* Does buff effect scale buff stats like onHit as from aspectOfTheViper?
* Buff (e.g., Aspect of the Shark) every 3 seconds?
  * Trigger with 100% chance
  * Create buff-skill with 0% trigger/onHit chance and 3s cooldown which applies aspect of the shark
  * Mabe a general skill-type which gets the 'to be applied' buff as input?
* Buffs which fall of after hit?
  * check for them on attack?

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
* Skills
  * Refactor skill-talents like character talents
* Character
  * Split talents into classpecific files in subfolder
  * handle amstery differently and allow talent access to all class-trees within a class
* Implement rotation system to incorporate stuff like Holy Symbols and Divine Aura as skills and not hard-coded
* Refactor modifier to track them differently
  * Add BuffEffect less/more multiplier
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
