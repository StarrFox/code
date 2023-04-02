"""
test:
def test():
    return 1


parser:
class Function(ParseNode):
    start = WordPattern("def")
    body = ParamVariable(regex="\w+", followed_by=VardanticParamVariable(regex="({})"))



"""


class ParseNode:
    pass




