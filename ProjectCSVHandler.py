
# the csv file I was given was very messy and un clear for regular reading. This file was made to clean up the mess and make parsing alot easier.
import re
file  = open("test.csv")
job= ""
jobs= []
secondfile = open("FormattedSheet.csv","w")
secondfile.close()
secondfile = open("FormattedSheet.csv","a")
for line in file:
    line = re.sub("\,+", ",", line)
    line = re.sub('\ +', ",", line)
    line = line.replace(", "," ")
    line = line.replace(":,\n",":")
    if line != ",\n":
        if line != "":
            secondfile.write(line)



