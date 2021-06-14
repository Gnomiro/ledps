# General
* Attackorder
  * Skill hits
  * Resolve skill effects, e.g., execution from Rive
  * Skill inflicts onHit-Effects like Ailments
  * OnHitTrigger like Manifest Strike or Undisputed-like buffs
* Only ailment application; no hit damage!
* Supported attack types: Default, Melee, Spell, Throw, Trigger
* Attack types provide a general interface
* Implemented skills:
  * Rive (partially talents)
  * Warpath (no talents yet)
* Implemented trigger skills:
  * Manifest Strike
  * Axe Thrower (Sentinel talent trigger, 1s cooldown)
  * Indomitable (Rive talent trigger on first hit)
* Partial multi-target support:
  * Buffs applied based on enemy count and ailment number are linearly scaled with global enemy variable

# HowTo
* todo

# ToDos
* Warpath:
  * Talents
  * Reduce onHit chance for ailments only, i.e., shred and ailments. currently for all onHit non-trigger effects
* Default attack routine:
  * Change order of duration and stats later to match class implementations
  * Make duration and stats a requirement?
* Skill provided global buffs like drainingAssault from warpath
  * Probably set a channeld-buff on attack which is overriden by similar skills?
* Default getAttacktime:
  * tempStats: Add stats per global add from Character/Environment or just pass it always?
* More skills
* Full multi-target support (probably never two enemies but at least consistent scaling for all buffs/debuffs) -> Move enemy number into Enemy-class