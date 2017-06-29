#!/usr/bin/python3

def main():
	
	newFile = []
	parties = ["vvd","cu","cda","d66","pvda","pvdd","gl","sp"]

	file = input("Which file you want to adapt to a latex table format? ")
	infile = open(file, "r")
	
	for line in infile:
		if line.startswith("MacBook-Pro-van-Hanneke"):
			x = line.replace(line,"\hline"+"\n")
			newFile.append(x)
		elif line.startswith("  Accuracy"):
			x = line.replace("\n","\\\\")
			newFile.append(x + "\n")
			newFile.append("\hline"+"\n")
		for i in parties:
			if line.startswith(i):
				x = line.replace("\n","\\\\")
				newFile.append(x + "\n")
	
		else:
			continue

	outfile = " ".join(newFile) 
	print(outfile)

if __name__ == '__main__':
    main()	
	 
