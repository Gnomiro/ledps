# Ailment
* "The damage number ticks you see from damage over time do not line up with the damage being dealt (showing a damage number for every time an enemy took damage from damage over time would result in far too much screen clutter), instead a combined damage number is shown for all damage over time taken every 0.5 seconds."
* "Enemies take less damage depending on their level, so the damage they take is lower than the damage you would expect to deal by just looking your base damage and increases."
* "Duration changes do not change the total damage of a single application of bleed. It just stretches the damage out if you increase the duration" - Seems wrong at least for bleed!!!!
* Armour does not reduce dot damage -> Shred irrelevant
* Resistance does -> Resistance Shred is good!

# Attack rate
* "Attack rate does multiply the base attack speed. Think of a 1.2 attack rate weapon as having a "20% more melee attack speed" mod."
* "Every ability has its own speed"
* "It will vary for some attacks, but for most it's about 0.68182 seconds"

# Questions
* Ailment damage still snapshotting or updated live? Duration and Effect snappshotted? - Did on March 8th 2020
* Ailments seem to snapshot!
* Can Trigger trigger? 
* Does a TriggerHit procc buffs like Undisputed? Should probably... -> Adapt TriggerSkills
 -> Buffs as Ailment resp. nonDamagingAilment/buff

# General
* Naming style: 'camilleCase'
* Class intern variables with leading '\_': '\_variableName'
* Input variables with trailing '\_': 'variableName\_'
* Temporary variables have no '\_'
* Variables/objects start with lowercase letter
* Classes start with uppercase letter
* Function definitions should end either with return or pass

# Notes
* Best way for counting occurences:
  active = {}
  for a in self.getActive(type):
    active[a.getName()] = active.get(a.getName(), 0) + 1

# Todo
* General
  * rename procs to trigger
  * DualWielding: Weapon Aps is not a direct more multiplierfor MeleeAttackSpeed. DualWielding averages both weapon ApS and applies the average as more multiplier
  * Allow addition from two Stats-objects
  * Manage skill provided global modifers: Currently, i.e. for warpath, workaround in test.py
* Multitarget, currently global 'enemies' in skill.py
  * Multiplies relevant modifers with monster hit count
    * Done for Rive ignites and Undisputed buffs
    * Missing for AxeThrower and Manifest Strike (multiprocs possible?)
* Cooldowns
  * Cooldown recovery must be considered at some point; possible in application while using gearStats-Data
* Stats
  * Rename stats in all classes: talentStats, gearStats, skillStats, buffStats, tempStats
  * Add getter/setter/adder to ensure multiplication/addition and enable the possibility of reducing stats-storage requirement by tracking only != 0 (resp 1) values
* Environment/Simulator
  * Global container class managing Character, Stats, Skill, Enemy, etc
* Skills
  * Global modifiers like warpath global more while channeling -> added to gearStats or gearStats + globalSkillStat = envirnomentStats?

[20:27] Oeller: Poison has less effect on bosses. Does that apply only for the built-in shred or also for 20 DoT damage? Not clear in the game guide.
In addition. Is the shred from poison as well limited by 20 stacks? Or is it possible top have poison shred stack to 20 alongside additional poison stack to further reduce the resistance?
[20:41] Mike W: built in shred only; not limited

[21:20] Mike W: poison shred is limited to 20.
the resistance drop from poison itself isn't limited

[03:50] Hishoukitai: the 40% reduced ailment chance on hit with Sentinel's Warpath, is that a flat 40%? for example if i have 200% ignite does it drop it to 160% or is it 40% of that 200%, dropping it to 120%?
[04:13] Trasochi: It's multiplicative so if you have 200% chance it drops to 120%.

[09:20] Oeller: Since Manifest Strike has no tooltip: What are the scaling tags? Any Attributes?
[20:45] Mike W: Physical, Melee, Strength and Attunement.