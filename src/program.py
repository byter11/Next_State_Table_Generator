import math
from tabulate import tabulate
def main():
	arr = input("Enter Counter Sequence: ")
	choice = input("Choose Flip Flop (JK or D): ")
	
	counter = list(map(int, arr.split(' ')))
	cols = math.ceil(( math.log10(max(counter))/math.log10(2) + 1 ))
	rows = len(counter)
	table = gettable(rows, cols, choice)
	filltable(counter,table,cols)
	if choice == "JK":
		header = "Inputs(J0,K0,J1,K1...)"
		makeJK(table,rows,cols)
	elif choice== "D":
		header = "Inputs(D0,D1...)"
		for row in table:
			row[2] = row[1]
	print(tabulate(table, headers=["Current State", "Next State", header],tablefmt="fancy_grid",numalign="center",stralign="center"))
	#printTable(table)
	input("Press Enter")
	
def gettable(rows, columns, choice):
	foo = 0
	flipflop = {'JK':2, 'D':1}
	table = [ [  [foo for i in range(columns)],
			     [foo for j in range(columns)],
			     [foo for k in range(columns * flipflop[choice])]  ] 
										for l in range(rows) ]
	return table

def printTable(a):
	print("First State\tNext State")
	for row in a:
		for col in row:
			print(col,sep=" | ",end='\t')
		print("")
		
def filltable(counter, table,cols):
	for i in range(len(counter)):
		foo = 0
		binarr = [foo for i in range(cols)]
		num = str(bin(counter[i]).replace("0b",""))
		rng = cols-len(num)
		
		for j in range(rng,cols):
			table[i][0][j] = int(num[j-rng])
			
	for i in range(len(counter)):
		if i==len(counter)-1:
			table[i][1] = table[0][0]
		else:
			table[i][1] = table[i+1][0]
			
def makeJK(table, rows, cols):
	
	for m in range(rows):
		j = 0
		k = 1
		for n in range(cols):
			if table[m][0][n] == 0 and table[m][1][n] == 0:
				table[m][2][j] =  0
				table[m][2][k] = 'X'
				j += 2
				k += 2
			elif table[m][0][n] == 0 and table[m][1][n] == 1:
				table[m][2][j] =  1
				table[m][2][k] = 'X'
				j += 2
				k += 2
			elif table[m][0][n] == 1 and table[m][1][n] == 0:
				table[m][2][j] =  'X'
				table[m][2][k] = 1
				j += 2
				k += 2
			elif table[m][0][n] == 1 and table[m][1][n] == 1:
				table[m][2][j] =  'X'
				table[m][2][k] = 0
				j += 2
				k += 2
	
main()
