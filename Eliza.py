'''
This is a pattern matcher based on Appendix A of 
"A Python Pattern Matcher Project for an Introduction to Artificial Intelligence Course" 
by Cynthia J. Martincic, Ph.D. It was built as part of the Artificial Intelligence Class 
at Olin College of Engineering lead by Prof. Lynn Andrea Stein. 
License: MIT

by Diana Vermilya
February 15, 2013

'''

import string
from time import time
from random import randrange
import copy

def isvariable (s):
	return s[0] == "_"

""" This recursive function is used to find out if a piece of user input matches one
one of the patterns.  It looks at each word. If the word passes, it moves on to the next word.
if not, it returns False.  In the case of a match, match1 returns the variable dict after the
last word, so that it can be used in substitute.
"""
def match1(pat, lst, pairs):
	if type(pat) != list or type(lst) != list:
		return False
	elif pat == [] and lst == []:
		if pairs:
			return pairs
		else:
			return True
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

'''Calls match1.  This function is just a wrapper.'''
def match(pat, lst):
	return match1(pat, lst, {})
"""
#pronoun_dict is used for swapping out pronouns, so that if user says
"I have no friends", the pattern matcher would say "what makes you think you have no friends?"
instead of "what makes you think I have no friends?" (for example)
"""
pronoun_dict = {'i':'you', 'you':'me', 'my':'your', 'our':'your', 'am':'are', 'we':'you', 'me':'you', 'us':'you', 'mine':'yours', 'our':'yours', 'are':'am'}

def pronoun(phrase, pronoun_dict):
	words = phrase.split(" ")
	for i in range(len(words)):
		if words[i][-1].isalnum() == False:
			words[i] = words[i][:-1]
		if words[i] in pronoun_dict:
			words[i] = pronoun_dict[words[i]]
	return ' '.join(words)

"""
This functions swaps in the variables from the user input into the response
using the dictionary created by match and match1"""

def substitute(pat, pairs):
	for i in range(len(pat)):
		if isvariable(pat[i]) or isseqvariable(pat[i]):
			pat[i] = pronoun(pairs[pat[i]], pronoun_dict)
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
		responses = rule[2]
		return responses[randrange(0, (len(responses)))]
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

"""
The following variables are all the rules.  s1 - s19 are rules for statemsntes of the user.  q1 - q5 are rules for questions"""

s1 = ['rule', ['i',  'am', 'S_Z'], [['Why do you think you are', 'S_Z', '?'], ['Hmm... \nDoes that bother you?']
,["It is really good that you recognize that."], ['Why do you think that is?']]]
s2 = ['rule', ['I', 'feel', 'S_X'], [['why', 'do', 'you', 'think', 'you', 'feel',
'S_X', '?'], ["It is great that you recognize how you feel."]]]
s3 = ['rule', ['no'], [['OK, that makes sense.'], ['yeah, I agree'], ['I see.  Tell me more about you.']]]
s4 = ['rule', ['yes'], [['OK.  Can say more about that?'], ['Why?']]]
s5 = ['rule', ['S_X', 'thinks', 'I', 'am', 'S_y'], [['do', 'you', 'think', 'you', 'are', '_y', '?']]]
s6 = ['rule', ['S_X', 'thinks', 'S_y'], [['Do you agree?'], ['What matters is what you think.'], ['Do you think you are', 'S_y', '?']]]
s7 = ['rule', ['i', 'think', 'S_y'], [['Do you think that is reasonable?'], ['Why do you think', 'S_y', '?']]]
s8 = ['rule', ['S_X', 'says', 'I', 'am', 'S_y'], [['do', 'you', 'think', 'you', 'are', 'S_y', '?']]]
s9 = ['rule', ['S_X', 'says', 'S_y'], [['do', 'you', 'think' 'S_y', '?']]]
s10 = ['rule', ['S_X', 'a', 'lot', 'of', '_Y', 'S_Z'], [['Tell me about one of the', '_Y']]]
s11 = ['rule', ['i', 'have', 'S_X'], [['What makes you think you have', 'S_X', '?'], ['Why do you think you have', 'S_X', '?']]]
s12 = ['rule', ['because', 'S_X'], [['Why do you think', 'S_X', '?'], ['I see.  You think', 'S_X', '?']]]
s13 = ['rule', ['you', 'are', 'S_X'], [['You think I am ', 'S_X', '?'], ['Who I am, what I am like, and what I do are not important.']]]
s14 = ['rule', ['hello'], [['hi']]]
s15 = ['rule', ['hi'], [['hello']]]
s16 = ['rule', ['how', 'are', 'you', '?'], [['How I am is unimportant.  How are you?']]]
s17 = ['rule', ['i', 'do', 'not', 'know'], [['It is ok to not know.']]]
s18 = ['rule', ['i', 'know'], [['Good.']]]
s19 = ['rule', ['S_X'], [['What makes you think', 'S_X'], ["Go on"], ["Wait, I don't understand"], ["Say more about that."]]]

q1 = ['rule', ['am', 'i', '_X'], [['do', 'you', 'think', 'you' , 'are', '_X', '?']]]
q2 = ['rule', ['do', 'you', 'think', 'i', 'am', '_X'], [['What I think does not really matter.']]]
q3 = ['rule', ['why', 'S_X'], [['Why do you think?'], ['That is really a question for you to answer4 right?']]]
q4 = ['rule', ['do', 'you', 'S_X'], [['Whether I', 'S_X', 'or not does not matter.'], ['Do you', 'S_X', '?']]]
q5 = ['rule', ['S_X'], [['S_X', '?', 'Why are you asking me?'],["You need to answer that for yourself."], ["I'm not sure"]]]



rule_lst = [[s13, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s14, s15, s16, s17, s18, s19], [q1, q2, q3, q4, q5]]

"""Eliza program runs everything.  It manages the converstion and calls the other functions."""

def eliza(rule_lst):
	default_Sresponses = ["Go on", "Wait, I don't understand", "Say more about that."]
	default_Qresponses = ["You need to answer that for yourself.", "I'm not sure"]
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
			if len(user_input) > 30:
				resp = 'You said a lot of things, but I feel like I am missing your main point.  What are you really trying to say?'
			else:
				resp = default_responses[randrange(0, (len(default_responses)))]
		print resp
		user_input = raw_input()
	if user_input == "stop":
		print "Bye.  I am glad we talked.  And I am here, you know, whenever you want to talk."
	else:
		print "Ah!  I have got to go, I am really sorry.  We should talk again soon though."

print eliza(rule_lst)




