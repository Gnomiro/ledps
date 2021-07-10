class MissingDurationArgument(Exception):

  def __init__(self, name_, required_, **provided_):
    self.message = 'Warning: Duration object \'{}\' requires \'{}\' but received \'{}\' only.'.format(name_, required_, provided_.keys())
    super().__init__(self.message)
    pass

class InvalidElement(Exception):

  def __init__(self, element_):
    self.message = 'Warning: \'{}\' is an invalid element.'.format(element_)
    super().__init__(self.message)
    pass

class InvalidDuration(Exception):

  def __init__(self, duration_):
    self.message = 'Warning: \'{}\' is an invalid duration.'.format(duration_)
    super().__init__(self.message)
    pass

class InvalidDurationType(Exception):

  def __init__(self, duration_):
    self.message = 'Warning: \'{}\' is an invalid duration type.'.format(duration_)
    super().__init__(self.message)
    pass

class UnsupportedSkill(Exception):

  def __init__(self, skill_):
    self.message = 'Warning: \'{}\' is an unsupported skill.'.format(skill_)
    super().__init__(self.message)
    pass