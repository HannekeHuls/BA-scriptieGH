#!/usr/bin/python3

def main():
	file = input("Which file you want to read? ")
	infile = open(file, "r")

	acurracy = []
	for line in infile:
		if line.startswith("  Accuracy"):
			for ch in line:
				for ch in '\n':
					line = line.replace(ch,"")
					outCome = line.split(":")
					acurracy.append(outCome[1])

	count=0
	divisionNr = len(acurracy)

	for i in acurracy:
		i = float(i)
		count = count + i

	means = count/divisionNr
	print(means)

if __name__ == '__main__':
    main()	