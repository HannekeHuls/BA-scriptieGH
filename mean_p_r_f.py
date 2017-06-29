#!/usr/bin/python3

#this program calculates the mean of the precision or recall or F-score 
#of a politcal party
#(in combination with the possible party-combinations (2, 3, 4, 5, 6, 7 or 8)in the text files)

def splitListPRF(file, party):
	precision = []
	recall = []
	f_score = []
	for line in file:
		if line.startswith(party):	
			outCome = line.split("&")
			count = 0
			for line in outCome:
				if line.startswith(party):
					count +=1
				elif count == 1:
					precision.append(line)
					count +=1
				elif count == 2:
					recall.append(line)
					count +=1
				elif count == 3:
					for ch in line:
						if ch in "\n":
							line.replace(ch, "")
							f_score.append(line)
							count = 0
	return precision, recall, f_score


def  calculateMean(fromList):
	count=0
	divisionNr = len(fromList)
	for i in fromList:
		i = float(i)
		count = count + i

	means = count / divisionNr

	return means

def main():

	fileName = input("Filename: ")
	party = input("Party: ")
	infile = open(fileName, "r")


	precicion, recall, f_score = splitListPRF(infile, party)
	
	print("Precision: ", calculateMean(precicion))
	print("Recall: ",calculateMean(recall))
	print("F-score: ",calculateMean(f_score))

if __name__ == '__main__':
	main()


