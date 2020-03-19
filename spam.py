############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Songmeng Wang"

############################################################
# Imports
############################################################
import email
import math
import os
from queue import PriorityQueue
# Include your imports here, if any are used.

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    tokens = []
    email_o = email.message_from_file(open(email_path))
    for line in email.iterators.body_line_iterator(email_o):
        tokens = tokens+line.split()
    return tokens

def log_probs(email_paths, smoothing):
    token_dict = {}
    for path in email_paths:
        tokens = load_tokens(path)
        for token in tokens:
            if token not in token_dict:
                token_dict[token] =1
            else:
                token_dict[token]+=1
    length = len(token_dict)
    counts = sum(token_dict.values())
    logs = {}
    for token,count in token_dict.items():
        logs[token] = math.log((count+smoothing)/(counts+smoothing*(length+1)))
    logs["<UNK>"] = math.log(smoothing/(counts+smoothing*(length+1)))
    return logs

    
class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        self.spam_paths = []
        self.ham_paths = []
        for path,dir,files in os.walk(spam_dir):
            for file in files:
                self.spam_paths.append(path+'/'+file)
        for path,dir,files in os.walk(ham_dir):
            for file in files:
                self.ham_paths.append(path+'/'+file)
        self.spam_logs = log_probs(self.spam_paths,smoothing)
        self.ham_logs = log_probs(self.ham_paths,smoothing)
        self.spam_prob = math.log(len(self.spam_paths)/(len(self.spam_paths)+len(self.ham_paths)))
        self.ham_prob = math.log(len(self.ham_paths)/(len(self.spam_paths)+len(self.ham_paths)))
        
    def is_spam(self, email_path):
        token_dict = {}
        tokens = load_tokens(email_path)
        for token in tokens:
            if token not in token_dict:
                token_dict[token] =1
            else:
                token_dict[token]+=1
        spam_prob = 0
        ham_prob = 0
        for token,count in token_dict.items():
            if token not in self.spam_logs:
                spam_prob += self.spam_logs["<UNK>"]
            else:
                spam_prob += self.spam_logs[token]
            if token not in self.ham_logs:
                ham_prob += self.ham_logs["<UNK>"]
            else:
                ham_prob += self.ham_logs[token]
        spam_prob += self.spam_prob
        ham_prob += self.ham_prob
        if spam_prob>ham_prob:
            return True
        return False
        

    def most_indicative_spam(self, n):
        ind_queue = PriorityQueue()
        for token, count in self.ham_logs.items():
            sol = math.exp(self.ham_logs[token])
            if token in self.spam_logs:
                sol += math.exp(self.spam_logs[token])
            else:
                sol += math.exp(self.spam_logs["<UNK>"])
            ind_queue.put((count-math.log(sol),token))
        return [ind_queue.get()[1] for i in range(n)]
            

    def most_indicative_ham(self, n):
        ind_queue = PriorityQueue()
        for token, count in self.spam_logs.items():
            sol = math.exp(self.spam_logs[token])
            if token in self.ham_logs:
                sol += math.exp(self.ham_logs[token])
            else:
                sol += math.exp(self.ham_logs["<UNK>"])
            ind_queue.put((count-math.log(sol),token))
        return [ind_queue.get()[1] for i in range(n)]


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
5 hours
"""

feedback_question_2 = """
starting this hw is hard,
begining with not understanding how the email work
and confuse with spam filter
"""

feedback_question_3 = """
I think this assignment is pretty nice
"""
