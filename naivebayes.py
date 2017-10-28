#!/sw/bin/python

import math
import sys
import glob
import pickle
from dicts import DefaultDict

def naivebayes (dirs):
    """Train and return a naive Bayes classifier.  
        Return: array of tuples, one tuple per class.
        Each tuple contains the class name and the
        multinomial distribution over words associated with
        the class"""
    categories = []
    for dir in dirs:
	print(dir)
	countdict = files2countdict(glob.glob(dir+"/*"))
	categories.append((dir,countdict))
    return categories

def classify (categories, filename):
    """Given a trained naive Bayes classifier and a test document.
    Return: an array of tuples, each containing a class label.
    Sort the array by log-probability of the class, log p(c|d)"""
    answers = []
    print('Classifying ', filename)
    for c in categories:
	score = 0
	for word in open(filename).read().split():
	    word = word.lower()
	    score += math.log(c[1].get(word,1))
	answers.append((score,c[0]))
    answers.sort()
    return answers

def files2countdict (files):
    """Given an array of filenames.
        Return: a dictionary (keys=words, values= # of times that word occurred)."""
    d = DefaultDict(0)
    for file in files:
	for word in open(file).read().split():
	    d[word.lower()] += 1
    return d
	

if __name__ == '__main__':
    print('argv ', sys.argv)
    print("Usage: ", sys.argv[0], "classdir1 classdir2 [classdir3...] testfile")
    dirs = sys.argv[1:-1]
    testfile = sys.argv[-1]
    nb = naivebayes (dirs)
    print(classify(nb, testfile))
    pickle.dump(nb, open("classifier.pickle",'w'))
