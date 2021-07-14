import sys
sys.path.append('..')

import modifier

import unittest, copy

class ModifierTestCase(unittest.TestCase):

  # run before every test
  def setUp(self):
    pass

  # run after every test
  def tearDown(self):
    pass

  def test_multiplier(self):
    modifier_ = modifier.Modifier()
    modifier2_ = modifier.Modifier()

    modifier_.setIncrease(1., 'physical', 'spell', attackType_ = 'melee') # spell is overriden by provided keyword
    modifier_.setIncrease(7., 'physical', 'dot')
    modifier_.addIncrease(7., 'physical', 'dot')
    modifier_.addIncrease(11., 'melee')
    modifier_.addIncrease(2., 'hit')
    modifier_.setMore(2., 'physical')
    modifier_.addMore(2., 'physical')
    modifier_.addMore(2., 'physical', 'melee')
    modifier_.addIncrease(200., 'physical') # should be overriden
    modifier_.setIncrease(4., 'physical')
    modifier_.addIncrease(2., 'physical')
    modifier_.addIncrease(2., 'physical', 'bow')
    modifier_.addIncrease(5., 'physical', 'melee')
    modifier_.addIncrease(100., 'physical', 'melee', 'hit')
    modifier_.addIncrease(12., 'physical', 'melee', 'hit')
    modifier_.addIncrease(6., 'fire', 'melee', 'hit')

    self.assertEqual(12. + 100. + 5. + 2. + 4. + 2. + 11. + 1., modifier_.getIncrease('physical', 'melee', 'hit'))
    self.assertEqual(11., modifier_.getIncrease('melee'))
    self.assertEqual(0., modifier_.getIncrease())
    self.assertEqual(11. + 5. + 2. + 4. + 1., modifier_.getIncrease('melee', 'physical'))
    self.assertEqual(11., modifier_.getIncrease('fire', 'melee'))
    self.assertEqual(6. + 11. + 2., modifier_.getIncrease('fire', 'melee', 'hit'))
    self.assertEqual(2., modifier_.getIncrease('hit'))
    self.assertEqual(2. + 4., modifier_.getIncrease('physical', 'spell'))

    self.assertEqual((1. + 2.) * (1. + 2.), modifier_.getMore('physical'))
    self.assertEqual((1. + 2.) * (1. + 2.) * (1. + 2.), modifier_.getMore('physical', 'melee'))
    self.assertEqual(1., modifier_.getMore('fire'))

    self.assertEqual((1. + 2.) * (1. + 2.) * (1. + 2.) * (1. + (11. + 5. + 2. + 4. + 1.)), modifier_.getMultiplier('physical', 'melee'))
    self.assertEqual(1. * (1. + (11.)), modifier_.getMultiplier('melee'))
    self.assertEqual((1. + 2.) * (1. + 2.) * (1. + (2. + 4.)), modifier_.getMultiplier('physical', 'spell'))

    modifier3_ = copy.deepcopy(modifier_)
    self.assertEqual(modifier3_.getIncrease('physical'), modifier_.getIncrease('physical'))
    modifier3_.addIncrease(2, 'physical')
    self.assertEqual(modifier3_.getIncrease('physical'), modifier_.getIncrease('physical') + 2.)
    modifier3_.addMore(2., 'physical')
    self.assertEqual(modifier3_.getMore('physical'), modifier_.getMore('physical') * (1. + 2.))

    beforeI = modifier_.getIncrease('physical')
    beforeM = modifier_.getMore('physical')
    modifier_ += modifier3_
    self.assertEqual(beforeI + modifier3_.getIncrease('physical'), modifier_.getIncrease('physical'))
    self.assertEqual(beforeM * modifier3_.getMore('physical'), modifier_.getMore('physical'))

    modifier_ = modifier2_ + modifier3_

    self.assertEqual(modifier2_.getIncrease('physical') + modifier3_.getIncrease('physical'), modifier_.getIncrease('physical'))
    self.assertEqual(modifier2_.getMore('physical') * modifier3_.getMore('physical'), modifier_.getMore('physical'))

    print(modifier_)
    # modifier_.addMore(2., 'melee', 'hit')
    modifier3_ = copy.deepcopy(modifier_)
    factor = 0.3
    modifier3_.scaleByFactor(factor)
    self.assertEqual(modifier3_.getIncrease('melee') / factor, modifier_.getIncrease('melee'))
    self.assertEqual((modifier3_.getMore('melee', 'hit') - 1.) / factor + 1., modifier_.getMore('melee', 'hit'))

    pass

  def test_penetration(self):
    modifier_ = modifier.Modifier()

    modifier_.addPenetration(7., 'fire')
    modifier_.setPenetration(2., 'fire')
    modifier_.addPenetration(2., 'fire')
    modifier_.addPenetration(-2., 'physical')

    self.assertEqual(4., modifier_.getPenetration('fire', 'physical', elementType_ = 'fire')) # left to right overrides type; specified keyword always has the highest priority

    modifier2_ = modifier.Modifier()
    modifier2_.setPenetration(3., 'physical')
    modifier2_ += modifier_
    self.assertEqual(1., modifier2_.getPenetration('physical'))
    self.assertEqual(-2., modifier_.getPenetration('physical'))

    modifier3_ = modifier2_ + modifier_
    self.assertEqual(modifier2_.getPenetration('physical') + modifier_.getPenetration('physical'), modifier3_.getPenetration('physical'))
    self.assertEqual(modifier2_.getPenetration('fire') + modifier_.getPenetration('fire'), modifier3_.getPenetration('fire'))
    self.assertEqual(modifier2_.getPenetration('lightning') + modifier_.getPenetration('lightning'), modifier3_.getPenetration('lightning'))
    pass

  def test_attribute(self):
    modifier_ = modifier.Modifier()

    modifier_.addAttribute(7., 'strength')
    modifier_.setAttribute(2., 'strength')
    modifier_.addAttribute(2., 'strength')
    modifier_.addAttribute(-2., 'dexterity')

    self.assertEqual(4., modifier_.getAttribute('strength', 'dexterity', attributeType_ = 'strength')) # left to right overrides type; specified keyword always has the highest priority

    modifier2_ = modifier.Modifier()
    modifier2_.setAttribute(3., 'dexterity')
    modifier2_ += modifier_
    self.assertEqual(1., modifier2_.getAttribute('dexterity'))
    self.assertEqual(-2., modifier_.getAttribute('dexterity'))

    modifier3_ = modifier2_ + modifier_
    self.assertEqual(modifier2_.getAttribute('dexterity') + modifier_.getAttribute('dexterity'), modifier3_.getAttribute('dexterity'))
    self.assertEqual(modifier2_.getAttribute('strength') + modifier_.getAttribute('strength'), modifier3_.getAttribute('strength'))
    self.assertEqual(modifier2_.getAttribute('vitality') + modifier_.getAttribute('vitality'), modifier3_.getAttribute('vitality'))
    pass

  def test_duration(self):
    modifier_ = modifier.Modifier()
    modifier2_ = modifier.Modifier()

    # durationModifierType_ = ['onHit', 'effect', 'duration']

    modifier_.addDuration('poison', 2., 'onHit')
    modifier_.addDuration('poison', 2., 'effect')
    modifier_.addDuration('poison', 3., 'effect')
    modifier_.addDuration('poison', 2., 'effect', 'more')
    modifier_.addDuration('poison', 3., 'effect', 'more')
    modifier_.addDuration('poison', 3., 'onHit', 'melee', 'more')
    modifier_.addDuration('poison', 3., 'onHit', 'more')

    modifier_.addDuration('bleed', 3., 'effect', 'more')
    modifier_.addDuration('bleed', 3., 'effect', 'more')
    self.assertEqual(16., modifier_.getDurationMore('bleed', 'effect'))

    modifier2_.setDuration('poison', 0., 'effect', 'more') # -> value is set to 1 as it is the default multiplier
    self.assertEqual(1., modifier2_.getDurationMore('poison', 'effect'))
    modifier2_.setDuration('poison', 1., 'effect', 'more') # -> value is set to 2 as it adds a 100% more multilier to the base of 1
    self.assertEqual(2., modifier2_.getDurationMore('poison', 'effect'))

    modifier_ += modifier2_

    self.assertEqual(16., modifier_.getDurationMore('bleed', 'effect'))
    self.assertEqual(24., modifier_.getDurationMore('poison', 'effect'))
    self.assertEqual(2., modifier2_.getDurationMore('poison', 'effect'))
    self.assertEqual(0., modifier2_.getDurationIncrease('poison', 'effect'))
    self.assertEqual(5., modifier_.getDurationIncrease('poison', 'effect'))

    self.assertEqual((1. + 2) * (1. + 3) * (1. + 3.), modifier_.getDurationMultiplier('poison', 'onHit', 'melee'))
    self.assertEqual((1. + 2) * (1. + 3), modifier_.getDurationMultiplier('poison', 'onHit'))
    pass

  def test_trigger(self):
    modifier_ = modifier.Modifier()
    modifier2_ = modifier.Modifier()

    # durationModifierType_ = ['onHit', 'effect', 'duration']

    modifier_.addTrigger('aspectOfTheShark', 2., 'onHit')
    modifier_.addTrigger('aspectOfTheShark', 2., 'effect')
    modifier_.addTrigger('aspectOfTheShark', 3., 'effect')
    modifier_.addTrigger('aspectOfTheShark', 2., 'effect', 'more')
    modifier_.addTrigger('aspectOfTheShark', 3., 'effect', 'more')
    modifier_.addTrigger('aspectOfTheShark', 3., 'onHit', 'melee', 'more')
    modifier_.addTrigger('aspectOfTheShark', 3., 'onHit', 'more')

    modifier_.addTrigger('divineBolt', 3., 'effect', 'more')
    modifier_.addTrigger('divineBolt', 3., 'effect', 'more')
    self.assertEqual(16., modifier_.getTriggerMore('divineBolt', 'effect'))

    modifier2_.setTrigger('aspectOfTheShark', 0., 'effect', 'more') # -> value is set to 1 as it is the default multiplier
    self.assertEqual(1., modifier2_.getTriggerMore('aspectOfTheShark', 'effect'))
    modifier2_.setTrigger('aspectOfTheShark', 1., 'effect', 'more') # -> value is set to 2 as it adds a 100% more multilier to the base of 1
    self.assertEqual(2., modifier2_.getTriggerMore('aspectOfTheShark', 'effect'))

    modifier_ += modifier2_

    self.assertEqual(16., modifier_.getTriggerMore('divineBolt', 'effect'))
    self.assertEqual(24., modifier_.getTriggerMore('aspectOfTheShark', 'effect'))
    self.assertEqual(2., modifier2_.getTriggerMore('aspectOfTheShark', 'effect'))
    self.assertEqual(0., modifier2_.getTriggerIncrease('aspectOfTheShark', 'effect'))
    self.assertEqual(5., modifier_.getTriggerIncrease('aspectOfTheShark', 'effect'))

    self.assertEqual((1. + 2) * (1. + 3) * (1. + 3.), modifier_.getTriggerMultiplier('aspectOfTheShark', 'onHit', 'melee'))
    self.assertEqual((1. + 2) * (1. + 3), modifier_.getTriggerMultiplier('aspectOfTheShark', 'onHit'))
    pass

if __name__ == '__main__':
  unittest.main()