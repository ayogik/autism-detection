import scipy.stats as stats
import numpy as np

def convert(p):
    degree = int(p[-2:])
    shortened = p[0] + p[2:-4]
    returnable = "0."
    for i in range(1, degree):
        returnable += "0"
    returnable += shortened
    return returnable

def mean(series):
    total = 0.0
    for num in series:
        total += num
    return (total/len(series))

'''
data = open("data_for_analysis", "r")

for line in data:
    line.strip("\n")
    halves = line.split(" ")
    nonASD, ASD = halves[0], halves[1]
    nonASD_data = nonASD.split(",")
    nonASD_data = nonASD_data[:len(nonASD_data)-1]
    ASD_data = ASD.split(",")
    ASD_data = ASD_data[:len(ASD_data)-1]


    for i in range(0, len(nonASD_data)):
        nonASD_data[i] = float(nonASD_data[i])

    for i in range(0, len(ASD_data)):
        ASD_data[i] = float(ASD_data[i])


    #print nonASD_data
    #print ASD_data
    t, p = stats.ttest_ind(nonASD_data, ASD_data, equal_var = False)
    print convert(str(p))


    addto = open("analyzed_data", "a+")

    addto.write((convert(str(p)) + "\n"))

    addto.close()

data.close()


freqdata = open("freqdata_for_analysis", "r")

for line in freqdata:
    line.strip('\n')
    halves = line.split(' ')
    asd, non_asd = halves[0].split(','), halves[1].split(',')[1:-1]
    type = asd[0]
    asd = asd[1:-1]
    #print type

    for i in range(0, len(asd)):
        asd[i] = float(asd[i])
    for i in range(0, len(non_asd)):
        non_asd[i] = float(non_asd[i])

    if len(asd) > 1 and len(non_asd) > 1:
        t, p = stats.ttest_ind(non_asd, asd, equal_var = False)
        #print p

        addto = open("analyzed_freqdata", "a+")

        ptoprint = str(p)

        addto.write((type + "," + ptoprint + ","))

        if p < 0.05:
            if mean(asd) > mean(non_asd):
                addto.write("ASD")
            else:
                addto.write("Non-ASD")

        addto.write('\n')

        addto.close()

freqdata.close()
'''

data = open("freqdata_nonASD", "r")
out = open("freqnonASD_avg", "w+")
for line in data:
    line.strip("\n")
    datum = line.split(',')[1:-1]
    if len(datum) > 1:
        toavg = []
        for num in datum:
            toavg.append(float(num))
        sum = 0
        for num in toavg:
            sum += num
        toadd = sum/len(toavg)
        out.write(str(toadd) + '\n')

data.close()
out.close()