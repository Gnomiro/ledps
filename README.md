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
* Trigger
  * character holds Attack-Skills
  * combat simulator tries to trigger from character skill and otherwise falls-back to default (try, catch with eval)
   -> could replace divine bolt implementation; possibly not in this case as divine bolt cannot be used otherwie
* General
  * Move shred/penetration damage multiplication to outer loop in Character/Simulation; must only be applied once
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
  * Rename stats in all classes: talentStats, gearStats, skillStats, buffStats, tmpStats
* Environment/Simulator
  * Global container class managing Character, gearStats, buffStats, Skill, Enemy, etc -> reduced neccessary objects to pass around
* Skills
  * add skill _tags alongside _attributes for skill-damage scaling
  * make attributes not passed by constructor but set like _skillname
  * pass gearStats on init and add skillStats?
  * Global modifiers like warpath global more while channeling -> added to gearStats or gearStats + globalSkillStat = envirnomentStats?

[20:27] Oeller: Poison has less effect on bosses. Does that apply only for the built-in shred or also for 20 DoT damage? Not clear in the game guide.
In addition. Is the shred from poison as well limited by 20 stacks? Or is it possible top have poison shred stack to 20 alongside additional poison stack to further reduce the resistance?
[20:41] Mike W: built in shred only; not limited

[21:20] Mike W: poison shred is limited to 20. the resistance drop from poison itself isn't limited

[03:50] Hishoukitai: the 40% reduced ailment chance on hit with Sentinel's Warpath, is that a flat 40%? for example if i have 200% ignite does it drop it to 160% or is it 40% of that 200%, dropping it to 120%?
[04:13] Trasochi: It's multiplicative so if you have 200% chance it drops to 120%.

[09:20] Oeller: Since Manifest Strike has no tooltip: What are the scaling tags? Any Attributes?
[20:45] Mike W: Physical, Melee, Strength and Attunement.

[21:12] sir.hrsT: hello quick question : how is the interaction between Rive nodes "Execution" and "Savagery" for the third hit. Does the third Hit gets the dmg amp from hitting an ignited target and THAN consumes the ingnite to boost phys dmg or does it consume the ignite and doesnt get any boost from "Savagery"?
[21:24] Mike W: The bonus damage from hitting an ignited target gets calculated first then it consumes the ignite.

[01:13] Oeller: Is the Attackspeed of all Rive attacks 0.68182? Only info I found about attack speed in this thread. Posted by Trasochi in 2019...
[01:15] Trasochi: The first two parts of Rive's combo are 25% faster than a basic attack and the last is 7% faster.