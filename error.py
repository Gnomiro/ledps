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

  def __init__(self, element_):
    self.message = 'Warning: \'{}\' is an invalid duration.'.format(element_)
    super().__init__(self.message)
    pass
