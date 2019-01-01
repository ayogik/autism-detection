import numpy as np
import nltk
from collections import defaultdict
from LSA import *
from array import array
import math

bad_types = ['SYM', '$', '"', '(', ')', ',', '--', '.', ':', '']
freq = defaultdict(int)
perc_freq = defaultdict(float)

filename = "nonASD/101.txt" #update file name
source = open(filename, "r")
last = False
toAdd = []
text = []
for line in source:
    string = (line.strip('\n'))
    if string[0:4] == '*CHI':
        text.append(string[6:])

source.close()

knndata = []
knnsource = open('knn_data', 'r')
for line in knnsource:
    line.strip('\n')
    string = line.split(',')
    for num in range(1, len(string)):
        string[num] = float(string[num])
    type = string[0]
    string = string[1:]
    string.append(type)
    knndata.append(string)
knnsource.close()

def analyze(text, list):
    tokenized = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokenized)
    '''
    for i in range(0, len(tagged))[::-1]:
        if tagged[i][1] in bad_types:
            tagged.remove(tagged[i])
    '''
    list.append(tagged)

analyzed = []
for line in text:
    analyze(line, analyzed)
#print analyzed

def freq_analysis(list):
    num_words = 0
    for line in list:
        for word in line:
            if word[1] not in bad_types:
                freq[word[1]] += 1
                num_words += 1

    for key, value in freq.items():
        perc_freq[key] += 1.0*value/num_words
        '''
        print (key, value)

    print num_words

    for key, value in perc_freq.items():
        print (key, value)
        '''

freq_analysis(analyzed)


test = LSA()
for d in text: #THIS IS WHERE TO LIMIT SAMPLE SIZE
    test.parse(d)
    test.build()
#test.printA()
test.svd()
lsanalyzed = test.S
lsanalyzed = sorted(lsanalyzed, reverse = True)

#print lsanalyzed

def eu_dist(first, second):
    distance = 0
    if len(first) < (len(second)-1):
        length = len(first)
    else:
        length = len(second)-1
    #print length
    length = 3
    for x in range(0, length):
        distance += (first[x] - second[x])**2
    return math.sqrt(distance)

def getneighbors(trainingset, testdata, k):
    distances = []
    for a in range(len(trainingset)):
        dist = eu_dist(testdata, trainingset[a])
        distances.append([trainingset[a], dist])
    distances.sort(key=lambda x: x[1]) #key=operator.itemgetter(1)
    print distances
    neighbors = []
    for n in range(0, k):
        #print distances[n][0]
        neighbors.append(distances[n][0])
    print neighbors
    return neighbors

def add_lsa(filename, addfrom):
    update = open(filename, "r")
    master = []
    toAdd = []
    for line in update:
        line.strip("\n")
        edit = line.split(",")
        if '' in edit:
            edit.remove('')
        if '\n' in edit:
            edit.remove('\n')
        #val_list = line.split(",")
        if edit != []:
            master.append(edit)
    update.close()
    print len(addfrom)

    if len(master) < len(addfrom):
        for i in range(0, len(master)):
            add = master[i]
            add.append(addfrom[i])
            toAdd.append(add)
        for i in range(len(master), len(addfrom)):
            toAdd.append([addfrom[i]])
    else:
        for i in range (0, len(addfrom)):
            add = master[i]
            add.append(addfrom[i])
            toAdd.append(add)
        for i in range (len(addfrom), len(master)):
            toAdd.append(master[i])

    #print toAdd

    update = open(filename, "w")
    for line in toAdd:
        update.write("\n")
        for num in line:
            update.write((str(num) + ","))
    update.close()

def add_freq(filename, addfrom):
    update = open(filename, "r")
    toAdd = defaultdict(list)
    for line in update:
        line.strip("\n")
        pre = line.split(",")
        for i in range (1, len(pre)):
            if pre[i] != "\n" and pre[i] != "":
                toAdd[pre[0]] += [pre[i]]
    update.close()

    addFrom = [[key, val] for key,val in addfrom.iteritems()]
    for pair in addFrom:
        toAdd[pair[0]] += [str(pair[1])]

    add = [[key, val] for key,val in toAdd.iteritems()]
    update = open(filename, "w")
    for pair in add:
        update.write((str(pair[0]) + ","))
        for num in range(0, len(pair[1])):
            update.write((str(pair[1][num]) + ","))
        update.write("\n")

def add_knn(tag):
    update = open("knn_data", "a")

    update.write(tag)
    for item in lsanalyzed:
        update.write(',' + str(item))
    update.write('\n')

    update.close()

if "sets_nonASD" in filename:
    #add_lsa("nonASD_data", lsanalyzed)
    #add_freq("freqdata_nonASD", perc_freq)
    #add_knn('nonASD')
    print lsanalyzed

elif "sets_ASD" in filename:
    add_lsa("ASD_data", lsanalyzed)
    add_freq("freqdata_ASD", perc_freq)
    add_knn("ASD")

elif "testing" in filename:
    k = 3
    neighbors = getneighbors(knndata, lsanalyzed, k)
    print lsanalyzed
    print neighbors
    avg = 0.0
    for type in neighbors:
        print type[-1]
        if type[-1] == "ASD":
            avg += 1.0
    avg /= k
    print avg
    if avg > 0.5:
        print "ASD"
    else:
        print "Non-ASD"


out = open("data", "w")
out.write("TEST DATA:")
out.write("\nLSA NUMBERS:")
for i in range(0, len(lsanalyzed)):
    out.write(("\n" + str(i+1) + "," + str(lsanalyzed[i])))
out.write("\n\nFREQ NUMBERS:")
for i in perc_freq:
    out.write(("\n" + i + "," + str(perc_freq[i])))
out.close()

