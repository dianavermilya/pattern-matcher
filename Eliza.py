import string
from time import time
from random import randrange
import copy

def isvariable (s):
	return s[0] == "_"

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
	if rule[0] == "rule" and type(rule[1]) == list and type(rule[2]) == list:
		return True
	return False

def rule_input (rule):
	if isrule(rule):
		return rule[1]
	return "that wasn't a rule!"

def rule_response (rule):
	if isrule(rule):
		return rule[2]
	return "that wasn't a rule!"

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

"""
This function takes in a list of words that make up the user input, and a nested list of rules.
It sorts out the rules for statements and the rules for questions  looks for a match within the 
correct rule list.
If a match is found, it returns Eliza's response.  If not, it returns an empty list.
"""
def apply_rules(input_lst, rules):
	rule_found = False
	while rules != [] and rule_found == False:
		subst_dict = match(rule_input(rules[0]), input_lst)
		if subst_dict:
			rule_found = True
		else:
			rules = rules[1:]		
	if rule_found:
		res = substitute(rule_response(rules[0]), subst_dict)
		return ' '.join(res)
	else:
		return ""

s1 = ['rule', ['my', '_X', 'thinks', 'I', 'am', '_y'], ['do', 'you', 'think',
'you', 'are', '_y', '?']]
s2 = ['rule', ['my', '_X', 'says', 'I', 'am', '_y'], ['do', 'you', 'think', 'you',
'are', '_y', '?']]
s3 = ['rule', ['I', 'feel', '_X'], ['why', 'do', 'you', 'think', 'you', 'feel',
'_X', '?']]
s4 = ['rule', ['my', 'S_Z', 'thinks', 'I', 'am', 'S_y'], ['do', 'you', 'think',
'you', 'are', 'S_y', '?']]
s5 = ['rule', ['i',  'am', '_Z'], ['Hmm... \nDoes that bother you?']]
q1 = ['rule', ['Am', 'I', '_X'], ['do', 'you', 'think', 'you' , 'are', '_X', '?']]
q2 = ['rule', ['Do', 'you', 'think', 'I', 'am', '_X'], ['What I think does not really matter.']]
rule_lst = [[s1, s2, s3, s4, s5], [q1, q2]]

def eliza(rule_lst):
	default_Sresponses = ["Go on", "Wait, I don't understand", "Say more about that."]
	default_Qresponses = ["I'm not sure",  "You need to answer that for yourself."]
	fname = raw_input("What is your first name?\n")
	#get a random number of seconds to wait
	randtime = randrange(1,3)
	time1 = time()
	while time() < time1 +randtime: #wait 1-5 seconds
		x = 1
	print "Hi " + fname + ", I am Eliza.  What has been on your mind recently?"

	#begin input, match and apply rules and responses
	user_input = raw_input()
	num_inputs = 0
	# while number of inputs < 10 and input not equal to stop
	while user_input != "Bye" and num_inputs < 100:
		num_inputs = num_inputs + 1
		user_input = string.split(user_input) #split user input
		for i in range(len(user_input)):
			user_input[i] = user_input[i].lower()
		r = copy.deepcopy(rule_lst)
		if user_input[-1][-1] != '?':
			rules = r[0] #statements
			default_responses = default_Sresponses
		else:
			rules = r[1] #questions
			user_input[-1] = user_input[-1][:-1]
			default_responses = default_Qresponses
		resp = apply_rules(user_input, rules)
		if resp == "":
			resp = default_responses[randrange(0, (len(default_responses) - 1))]
		print resp
		user_input = raw_input()
	if user_input == "stop":
		print "Bye.  I am glad we talked.  And I am here, you know, whenever you want to talk."
	else:
		print "Ah!  I have got to go, I am really sorry.  We should talk again soon though."

print eliza(rule_lst)




