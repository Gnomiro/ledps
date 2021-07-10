import error

def validateInput(name_, required_, **provided_):

  # test if all required entries are provided by provided_
  if not all([r in provided_.keys() for r in required_]):
    raise error.MissingDurationArgument(name_, required_, **provided_) from None