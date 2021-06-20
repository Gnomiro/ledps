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
* ArmourShred
  * include armour in damage calculation; not easy but has no impact on ailment damage
* Duration
  * Stats for reduced duration; minimum value for reduction should be -100%
* Trigger
  * character holds Attack-Skills
  * combat simulator tries to trigger from character skill and otherwise falls-back to default (try, catch with eval)
   -> could replace divine bolt implementation; possibly not in this case as divine bolt cannot be used otherwie
* General
  * DualWielding: Weapon Aps is not a direct more multiplierfor MeleeAttackSpeed. DualWielding averages both weapon ApS and applies the average as more multiplier
  * Manage skill provided global modifers: Currently, i.e. for warpath, workaround in test.py
* Multitarget, currently global 'enemies' in skill.py
  * Multiplies relevant modifers with monster hit count
    * Done for Rive ignites
    * Missing for AxeThrower and Manifest Strike (multiprocs possible?)
* Cooldowns
  * Cooldown recovery must be considered at some point; possible in application while using gearStats-Data
* Stats
  * Rename stats in all classes: talentStats, gearStats, skillStats, buffStats, tmpStats
* Environment/Simulator
  * Global container class managing Character, gearStats, buffStats, Skill, Enemy, etc -> reduced neccessary objects to pass around
* Skills
  * add skill \_tags within constructor
  * constructor gets gearStats for attributes
   -> with character implementation this can be passed from equipment to skill within simulator
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

[23:16] Oeller: What is the attack time of Serpent Strike? According to my current simulations it seems to hit faster than every 0.68182s. More like 0.6 * 0.68182s per attack. And what about swipe. Do you mind sharing these information?
Nevermind. The discrepancy seems to be related to Venomous Intent from Serpent Strike. It gives the skill a chance to proc Poison Spit but says nothing about the proc chance. Any information? An additional question regarding this: Although it does no hit damage it is assumed to be a spell hit and will apply bleed etc if provided by 'bleed on Hit', doens't it?
[00:35] Mike W: Poison spells don't apply those things generally. It typically requires a damage hit to apply effects like bleed chance.
[00:35] Mike W: That's why serpent strike has base physically damage
[00:36] Mike W: I don't go those numbers on mobile sorry.
[00:42] Oeller: I'm just confused by the wording on Poison Spit: 'a projectile spell that poisons on hit,  'the poisoning projectile inflicts poison on hit [...] the projectile does not deal any other damage on hit'.
So it only applies an additional poison on hit and procs no other on Hit effects as they need damaging hits?
[00:42] Mike W: Unless that one specifically has something extra set up for it that I don't remember, yes.
[00:44] Oeller: Thanks. So it probably provides only a marginal damage increase even if it procs on every hit (no chance specified). Wording could be improved. I will make a suggestion.
[00:46] Mike W: Every application of poison reduces the target's poison resistance. So it does have a multiplicative damage increase with your other poison applications.
[00:47] Oeller: Yes. But it has inherent duration reduction of 0.35; considering DR  of penetration for a lot of stacks it is probably not the best. Poison/ailment Duration could provide a better scaling