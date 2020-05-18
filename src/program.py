import math
from tabulate import tabulate
import pandas as pd
import xlsxwriter
import numpy

flipflop = {'JK':2, 'D':1}
choice = '0'
def main():
	arr = input("Enter Counter Sequence: ")
	global choice
	choice = input("Choose Flip Flop (JK or D): ")
	
	counter = list(map(int, arr.split(' ')))
	cols = math.ceil(( math.log10(max(counter))/math.log10(2) + 1 ))
	rows = len(counter)
	table = gettable(rows, cols)
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
	excelchoice = input("Generate XLSX File?(y/n) ")
	if(excelchoice == 'y' or excelchoice == 'Y'):
		makeexcel(table)
	
def gettable(rows, columns):
	foo = 0
	
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
def makeexcel(table):
	workbook = xlsxwriter.Workbook('_table.xlsx')
	worksheet = workbook.add_worksheet()
	worksheet.set_column(1,50,5)
	merge_format = workbook.add_format({
		'bold': 1,
		'border': 1,
		'align': 'center',
		})
	cell_format = workbook.add_format()
	cell_format.set_align('center')
	cell_format.set_align('vcenter')
	ln = len(table[0][0])
	worksheet.merge_range(0 , 0, 0, ln-1, "Current State",merge_format)
	worksheet.merge_range(0, ln, 0, ((ln-1)*2)+1, "Next State",merge_format)
	worksheet.merge_range(0, ((ln-1)*2)+2 , 0, (((ln-1)*4)+3), "Inputs", merge_format)
	for i in range(1,(len(table)+1)):
		line = table[i-1][0] + table[i-1][1] + table[i-1][2]
		for row,data in enumerate(line):
			worksheet.write(i,row,data,cell_format)
	workbook.close()
main()
