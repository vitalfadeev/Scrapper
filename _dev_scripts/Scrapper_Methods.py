import forbiddenfruit
import math


# list
# list.count()
def count( l ):
    return len( l )
forbiddenfruit.curse( list, "count", count )


# str
# str.len()
def len_( s ):
    return len( s )
forbiddenfruit.curse( str, "len", len_ )


# int
# str.sqrt()
def sqrt( i ):
    return math.sqrt( i )
forbiddenfruit.curse( int, "sqrt", sqrt )


# DEFAULT_EXCLUDE = (
#     '__weakref__',
#     '__module__',
#     '__dict__',
# )
#
# def extend(class_to_extend, exclude=DEFAULT_EXCLUDE):
#     def decorator(extending_class):
#         for k, v in extending_class.__dict__.items():
#             if k not in exclude:
#                 setattr(class_to_extend, k, v)
#         return class_to_extend
#     return decorator
#
#
# @extend(str)
# class Str:
#     def say_hello(self):
#         print("Hey " + self.name)
#
