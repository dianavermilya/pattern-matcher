import string
from time import time
from random import randrange

def isvariable (s):
	return s[0] == "_"
def dont_care(a):
	return a == '?'
def match_element(a, b):
	if a == b:
		return True
	elif dont_care(a) or dont_care(b):
		return True
	elif isvariable(a) and isvariable(b):
		return "I don't know what to do!"
	elif isvariable(a):
		d = {a:b}
		return d
	elif isvariable(b):
		d = {b:a}
		return d	
	else:
		return False

def matchleft(a, b):
	if type(a) != list:
		return "the first argument is not a list."
	elif type(b) != list:
		return "the second argument is not a list."
	elif not a and not b:
		return True
	elif a == [] or b == []:
		return False
	elif (a == b or a == '?' or b == "?") == False:
		return False
	else:
		return matchleft(a[1:], b[1:])

def boundp(s, d):
	if isvariable(s) == False or type(d) != dict:
		return "bad inputs"
	return s in d

def bound_to(s, d):
	if boundp(s, d):
		return d[s]
	return False

print bound_to('_x', {'_x':'xvalue'})
print bound_to('_x', {'_y':'yvalue', '_x':'xvalue'})
print bound_to('_z', {'_y':'yvalue', '_x':'xvalue'})




