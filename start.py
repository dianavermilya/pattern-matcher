import string
from time import time
from random import randrange
import copy

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


def match1(pat, lst, pairs):
	if type(pat) != list or type(lst) != list:
		return False
	elif pat == [] and lst == []:
		return pairs
	elif pat == [] or lst == []:
		return False
	elif pat[0] == lst[0]:
		return match1(pat[1:], lst[1:], pairs)
	elif isvariable(pat[0]):
		if pat[0] in pairs:
			if pairs[pat[0]] == lst[0]:
				return match1(pat[1:], lst[1:], pairs)
			return False
		else:
			pairs[pat[0]] = lst[0]
			return match1(pat[1:], lst[1:], pairs)
	elif isseqvariable(pat[0]):
		return backtrack_match(pat[0], pat[1:], lst, [], pairs)
	else:
		return False



def match(pat, lst):
	return match1(pat, lst, {})

def substitute(pat, pairs):
	for i in range(len(pat)):
		if isvariable(pat[i]) or isseqvariable(pat[i]):
			pat[i] = pairs[pat[i]]
	return pat

def isrule(rule):
	if rule[0] == "rule" and type(rule[2]) == list and type(rule[3]) == list:
		return True
	return False

def lhs (rule):
	if isrule(rule):
		return rule[2]
	return "that wasn't a rule!"

def rhs (rule):
	if isrule(rule):
		return rule[3]
	return "that wasn't a rule!"

def apply_rule(pat, rule):
	assert isrule(rule) == True
	return fire_rule(pat, rhs(rule), match(lhs(rule), pat))

def fire_rule(pat, rhs, subs):
	if subs == {}:
		return pat
	return substitute(rhs, subs)

def isseqvariable(var):
	if var[:2] == "S_":
		return True
	return False

#helper function needed for backtrack match
#if adding the sequence variable-sqce pair to pairs allows the match
#to succeed, return true
def backtrack_match1(sv, pat, lst, sqce, pairs):
#print "in backtrack_match 1 with", sv, pat, lst, sqce, pairs
#print "sqce is ", sqce
	pairs[sv] = string.join(sqce)
	if match1(pat, lst, pairs):
		return True
def backtrack_match(sv, pat, lst, sqce, pairs):
#arguments are the sequence variable, the rest of the pattern, the
#list,
#the sequence list which is initially empty, and pairs
#print "backtrack_match with ", sv, pat, lst, sqce, pairs
#if len(lst) > 0:
#print "lst[0] is ", lst[0]
	if not(pat): #the seq variable was the last thing in the pattern
		newstring = string.join(lst)
		pairs[sv] = newstring
		return pairs
	elif not(lst):
		return False
	elif backtrack_match1(sv, pat, lst[1:], match_append(sqce, lst[0]), pairs):
	#if sv is bound to something and the rest matches
		pairs[sv] = string.join(sqce)
		return pairs
	else:
		return backtrack_match(sv, pat, lst[1:],sqce, pairs)

def match_append(sqce, x):
	sqce.append(x)
	return sqce

def apply_rules(pat, rules):
	rl = list(rules)
	rule_found = False
	while rl != [] and rule_found == False:
		subst = match(lhs(rl[0]), pat)
		if subst:
			rule_found = True
		else:
			rl = rl[1:]		
	if rule_found:
		res = substitute(rhs(rl[0]), subst)
		return ' '.join(res)
	else:
		return ""

r1 = ['rule', 1, ['my', '_X', 'thinks', 'I', 'am', '_y'], ['do', 'you', 'think',
'you', 'are', '_y', '?']]
r2 = ['rule', 2, ['my', '_X', 'says', 'I', 'am', '_y'], ['do', 'you', 'think', 'you',
'are', '_y', '?']]
r3 = ['rule', 3, ['I', 'feel', '_X'], ['why', 'do', 'you', 'think', 'you', 'feel',
'_X', '?']]
r4 = ['rule', 4, ['my', 'S_Z', 'thinks', 'I', 'am', 'S_y'], ['do', 'you', 'think',
'you', 'are', 'S_y', '?']]
rule_lst = [r1, r2, r3, r4]

def eliza(rule_lst):
	default_responses = ["Tell me more", "Go on", "That is ridiculous"]
	fname = raw_input("Please sign in with your first name ")
	print "Hello, " + fname + " Eliza will be with you shortly."
	#get a random number of seconds to wait
	randtime = randrange(1,5)
	time1 = time()
	while time() < time1 +randtime: #wait 1-5 seconds
		x = 1
	print "Hello, " + fname + " This is Eliza. What do you want to talk about today?"
	#begin input, match and apply rules and responses
	user_input = raw_input()
	num_inputs = 0
	# while number of inputs < 10 and input not equal to stop
	while user_input != "stop" and num_inputs < 10:
		num_inputs = num_inputs + 1
		user_input = string.split(user_input) #split user input
		#print user_input, rule_lst
		r = copy.deepcopy(rule_lst)
		resp = apply_rules(user_input, r)
		if resp == "":
			resp = default_responses[randrange(0, 2)]
		print resp
		user_input = raw_input()
	if user_input == "stop":
		print "I see we have touched upon a sensitive topic. We can continue next week."
	else:
		print "Your time is up. We can continue next week."

print eliza(rule_lst)