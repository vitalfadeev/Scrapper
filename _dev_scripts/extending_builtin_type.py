#
# def should_equal_def(self, value):
#     if self != value:
#         raise ValueError, "%r should equal %r" % (self, value)
#
# class MyPatchedInt(int):
#     should_equal=should_equal_def
#
# class MyPatchedStr(str):
#     should_equal=should_equal_def
#
# import __builtin__
# __builtin__.str = MyPatchedStr
# __builtin__.int = MyPatchedInt
#
# int(1).should_equal(1)
# str("44").should_equal("44")
from pipe import *
x = range(100) | where(lambda x: x % 2 == 0) | add
x = [] | where(lambda x: x % 2 == 0) | add
print( type(x) )

