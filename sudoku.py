import sys
import csv
import numpy as np
import math

# returns an array of lists with each list containing the possible values for each column
# Need to remove listZeros because self.possibleCandidates already contains all the zeros

class solveSudoku:
	""" The solveSudoku class contains variable and methods to solve a unsolved Sudoku puzzle. 
	The class contains methods that list possible choices for an empty cell of the Sudoku puzzle.
	An input puzzle is first analysed using techniques of finding naked pairs, applying the rule of one, 
	scanning rows, scanning columns, and finding hidden pairs. These techniques are described in depth at
	http://www.sudokuessentials.com/sudoku-strategy.html. If no solution is found applying these techniques,
	a recursive backtracking algorithm is applied the Sudoku grid. Further techniques, such as finding hidden
	triplets, could be added to the program to solve the Sudoku puzzle.
	"""

	def __init__(self,data):
		"""Inits solveSudoku class and finds the possible row, column, and nonet values. The Sudoku grid is stored as self.data."""
		self.data=data
		self.rowOptions=np.zeros((1,9),dtype=np.ndarray)
		self.colOptions=np.zeros((1,9),dtype=np.ndarray)
		self.nonetOptions=np.zeros((1,9),dtype=np.ndarray)
		self.possibleCandidates={}
		
				
	def findRowValues(self):
		"""Finds all the possible row values for a Sudoku puzzle and stores each row's values in the array rowOptions."""
		for x in range(0,9):
			rowValues=range(1,10)
			for y in range(0,9):
				try:
					rowValues.remove(self.data[x,y])
				except:
					pass
			self.rowOptions[0,x]=rowValues	
	
	def findColumnValues(self):
		"""Finds all the possible column values for a Sudoku puzzle and stores each column's value in the array colOptions."""
		for y in range(0,9):
			colValues=range(1,10)
			for x in range(0,9):
				try:
					colValues.remove(self.data[x,y])
				except:
					pass
			self.colOptions[0,y]=colValues
	
	def findNonetValues(self):
		"""Finds all the possible nonet values for a Sudoku puzzle and stores each nonet's values in the array nonetOptions.
		The nonnetOptions array is ordered starting at the upper left corner of the grid with 1, moving to right until the 
		end of the puzzle, then moving down and start from the left.
		"""
		for n in range(0,3):
			for m in range(0,3):
				nonetValues=range(1,10)
				for x in range(0+3*m,3+3*m):
					for y in range(0+3*n,3+3*n):
						try:
							nonetValues.remove(self.data[x,y])
						except:
							pass
				self.nonetOptions[0,3*m+n]=nonetValues
			
	def findZeros(self):
		"""Finds all the empty cells in the Sudoku puzzle. The (x,y) locations in a dictionary called possibleCandidates""" 
		for n in range(0,3):
			for m in range(0,3):
				for y in range(0+3*n,3+3*n):
					for x in range(0+3*m,3+3*m):
						if self.data[x,y]==0:
							self.possibleCandidates[(x,y)]=0					
							
	def initialize(self):
		"""Finds all the possible values for each unfilled cell in the Sudoku puzzle. Stores the possible values as a list
		in the dictionary possibleCandidates where the key is the (x,y) position of the cell""" 
		self.possibleCandidates={}
		self.findRowValues()
		self.findNonetValues()
		self.findColumnValues()
		self.findZeros()
		for (x,y) in self.possibleCandidates.keys():
			a=set(self.colOptions[0,y])&set(self.rowOptions[0,x])&set(self.nonetOptions[0,math.floor(y/3)+3*math.floor(x/3)])
			a=list(a)
			self.possibleCandidates[(x,y)]=a
			
	def runAlgorithms(self):
		"""Applies the algorithms to Sudoku puzzle of the solveSudoku object. The method cycles through all the empty cells of 
		the grid and removes any value that can be eliminated. If an algorithm finds an element, the cell is filled and the 
		possible candidates for each cell are updated. If the method can not update any cell, the grid is solved using a 
		recursive backtracking method called solveRecursively. If a solution is find it written as CSV file: sudokuOutput.csv
		"""
		while True:
			dataChanged=False
			for (x,y) in self.possibleCandidates.keys():
				self.findNakedPair()
				if self.ruleOfOne(x,y):
					dataChanged=True
					self.possibleCandidates.pop((x,y))
					self.removeValues(x,y)
					break
				elif self.scanRows(x,y):
					dataChanged=True
					self.possibleCandidates.pop((x,y))
					self.removeValues(x,y)
					break
				elif self.scanColumns(x,y):
					dataChanged=True
					self.possibleCandidates.pop((x,y))
					self.removeValues(x,y)
					break
				elif self.findHiddenRowCandidates(x,y):
					dataChanged=True
					self.possibleCandidates.pop((x,y))
					self.removeValues(x,y)
					break
				elif self.findHiddenColCandidates(x,y):
					dataChanged=True
					self.possibleCandidates.pop((x,y))
					self.removeValues(x,y)
					break
				elif self.findHiddenNonetCandidates(x,y):
					self.possibleCandidates.pop((x,y))
					dataChanged=True
					self.removeValues(x,y)
			# If the applied algorithms were not able to update the Sudoku grid, we apply the recursive backtracking algorthm. 
			if not dataChanged:
				for x in self.data.sum(axis=0):
					if x ==45:
						continue
					else:
						print "Solving using the recursive backtracking algorithm."
						self.data=self.solveRecursively(0,0,self.data)
				#Saving output as a CSV
				c = csv.writer(open("sudokuOutput.csv", "wb"))
				a=self.data[1,:]
				for x in range(0,9):
					a=self.data[x,:]
					c.writerow(a)
					
				print "The algorithms have produced the solution: "
				print self.data
				print "The solution has been saved to sudokuOutput.csv"
				sys.exit()
				
				
			
	
	def solveRecursively(self,row_num,col_num,array):
		"""Finds the solution for a Sudoku puzzle using a recursive backtracking algorithm. The algorithm saves the solution to sudokuOutput.csv 
		An improved algorithm would use the possible candidates of each cell found in the possibleCandidates attribute to reduce the available 
		values to sample."""
		if row_num>8:
			print "The recursive backtracking algorithm has produced the solution: "
			print array
			c = csv.writer(open("sudokuOutput.csv", "wb"))
			a=self.data[1,:]
			for x in range(0,9):
				a=self.data[x,:]
				c.writerow(a)
			print "The solution has been saved to sudokuOutput.csv"
			sys.exit()
				
		if array[(row_num,col_num)]!=0:
			if col_num<8:
				self.solveRecursively(row_num,col_num+1,array);
			else:
				self.solveRecursively(row_num+1,0,array)
		else:
			for i in range(1,10):
				if self.checkArray(row_num,col_num,i,array):
					array[(row_num,col_num)]=i
					#print "putting x={},y={} with element={}".format(row_num,col_num,i)
					if col_num<8:
						self.solveRecursively(row_num,col_num+1,array);
					else:
						self.solveRecursively(row_num+1,0,array)
			array[(row_num,col_num)]=0
		
	def checkArray(self,row_num,col_num,element,array):
		"""Helper function to solveRecursively that checks that an possible element for the empty cell (row_num,col_num) is not already 
		present in the row, column, or nonet of the cell position of (row_num,col_num). If the element is not present, True is returned. 
		"""
		for col_i in range(0,9):
			if (array[(row_num,col_i)]==element):
				return False
		for row_i in range(0,9):
			if array[(row_i,col_num)]==element:
				return False
		for x_index in [0,1,2]:
			x_value=3*math.floor(row_num/3)+x_index
			for y_index in range(0,3):
				y_value=3*math.floor(col_num/3)+y_index
				if array[(x_value,y_value)]==element:
					return False
		else:
			return True

	def findNakedPair(self):
		"""Finds if a naked pair (two empty cells with the same two possible values) is present in a row, column, or nonet and if 
		naked pair exists, removes those values from another possible values in the row, column, or nonent."""
		for (x_value,y_value) in self.possibleCandidates:
			if len(self.possibleCandidates[(x_value,y_value)])==2:
				[a,b]=self.possibleCandidates[(x_value,y_value)]
				for (x_value1,y_value1) in self.possibleCandidates:
					if x_value==x_value1 and y_value1!=y_value:
						if len(self.possibleCandidates[(x_value1,y_value1)])==2:
							if a in self.possibleCandidates[(x_value1,y_value1)] and b in self.possibleCandidates[(x_value1,y_value1)]:
								self.removeRowValues(x_value1,y_value1,x_value,y_value,a)
								self.removeRowValues(x_value1,y_value1,x_value,y_value,b)
					if x_value!=x_value and y_value==y_value1:
						if len(self.possibleCandidates[(x_value1,y_value1)])==2:
							if a in self.possibleCandidates[(x_value1,y_value1)] and b in self.possibleCandidates[(x_value1,y_value1)]:
								self.removeColValues(x_value1,y_value1,x_value,y_value,a)
								self.removeColValues(x_value1,y_value1,x_value,y_value,b)
					for x1 in range(0,3):
						x_index=3*math.floor(x_value/3)+x1
						for y1 in range(0,3):
							y_index=3*math.floor(y_value/3)+y1
							if (x_index,y_index) in self.possibleCandidates and x_index!=x_value and y_index!=y_value:
								if len(self.possibleCandidates[(x_index,y_index)])==2:
									if a in self.possibleCandidates[(x_index,y_index)] and b in self.possibleCandidates[(x_index,y_index)]:
										self.removeNonetValues(x_value1,y_value1,x_value,y_value,a)
										self.removeNonetValues(x_value1,y_value1,x_value,y_value,b)		
					
	def ruleOfOne(self,x,y):
		"""Applies the rule of one to each empty cell of the Sudoku puzzle. If the cell has only one possible value, the algorithm returns true.
		If there are more than one possible candidates, False is returned."""
		if len(self.possibleCandidates[(x,y)])==1:
			print "We have found {2} at position x={0},y={1} using scanning rows technique.".format(x,y,self.data[x,y])
			element=self.possibleCandidates[(x,y)].pop()
			self.data[x,y]=element
			return True
		return False		
	
	def scanRows(self, row_num,col_num):
		"""Scans the other two remaining rows of the nonet containing (row_num,col_num) to see if the value being tested is present 
		in those rows. If present in both rows and the two neighboring row cells of (row_num,col_num) are occupied, the value has 
		to be in (row_num,col_num). scanRows tests all possible candidates of (row_num,col_num) until a value is found. If no value is 
		found, False is returned.
		"""
		plus_row=row_num+1
		plus_col=col_num+1
		plus_col=plus_col%3+3*math.floor(col_num/3)
		plus_row=plus_row%3+3*math.floor(row_num/3)
		plus_row2=plus_row+1
		plus_row2=plus_row2%3+3*math.floor(row_num/3)
		plus_col2=plus_col+1
		plus_col2=plus_col2%3+3*math.floor(col_num/3)
		for element in self.possibleCandidates[(row_num,col_num)]:
			if self.data[row_num,plus_col]==0 or self.data[row_num,plus_col2]==0:
				return False
			for row_value in self.data[plus_row,:]:
				if row_value==element:
					for row_value2 in self.data[plus_row2,:]:
						if row_value2==element:
							self.data[row_num,col_num]=element
							print "We have found {2} at position x={0},y={1} using scanning rows technique.".format(row_num,col_num,element)
							return True
		return False
		
	def scanColumns(self,row_num,col_num):
		"""Scans the other two remaining columns of the nonet containing (row_num,col_num) to see if the value being tested is present 
		in those columns. If present in both columns and the two neighboring column cells of (row_num,col_num) are occupied, the value has 
		to be in (row_num,col_num). scanColumns tests all possible candidates of (row_num,col_num) until a value is found. If no value is
		found, False is returned.
		"""
		plus_row=row_num+1
		plus_col=col_num+1
		plus_col=plus_col%3+3*math.floor(col_num/3)
		plus_row=plus_row%3+3*math.floor(row_num/3)
		plus_row2=plus_row+1
		plus_row2=plus_row2%3+3*math.floor(row_num/3)
		plus_col2=plus_col+1
		plus_col2=plus_col2%3+3*math.floor(col_num/3)
		for element in self.possibleCandidates[(row_num,col_num)]:
			if self.data[plus_row,col_num]==0 or self.data[plus_row2,col_num]==0:
				return False
			for col_value in self.data[:,plus_col]:
				if col_value==element:
					for col_value2 in self.data[:,plus_col2]:
						if col_value2==element:
							self.data[row_num,col_num]=element
							print "We have found {2} at position x={0},y={1} using scanning columns technique.".format(row_num,col_num,element)
							return True
		return False 
	
	
	def findHiddenRowCandidates(self,x,y):
		"""Finds if a number is "hiding" in the row x. If a number is "hiding" in a row, it only appears once in the possible values list 
		of an empty cell for that row. Since it only appears once, that cell must be the location of the number. If the number is found, the 
		value is updated in self.data and True is returned. If no number is found, False is returned."""
		for element in self.possibleCandidates[(x,y)]:
			elementPresent=False
			for (x_value,y_value) in self.possibleCandidates:
				if x==x_value and y!=y_value:
						listValues=self.possibleCandidates[(x_value,y_value)]
						if element in listValues:
						#If element is in the list of  possible values for another zero location in the row, it can not be a hidden element
							elementPresent=True
							break
			
			if elementPresent:
				continue
			else:
				print "We have found {2} at position x={0},y={1} using the hidden row pair technique.".format(x,y,element)
				self.data[x,y]=element
				self.dataChanged=True
				return True			
		return False
					
	def findHiddenColCandidates(self,x,y):
		"""Finds if a number is "hiding" in the column y. If a number is "hiding" in a column it only appears once in the possible values list 
		of an empty cell for that column. Since it only appears once, that cell must be the location of the number. If the number is found, the 
		value is updated in self.data and True is returned. If no number is found, False is returned."""
		for element in self.possibleCandidates[(x,y)]:
			elementPresent=False
			for (x_value,y_value) in self.possibleCandidates:
				if y==y_value and x!=x_value:
					listValues=self.possibleCandidates[(x_value,y_value)]
					if element in listValues:
						#If an element is in the list of possible values for another cell location in the row, it can not be a hidden element.
						elementPresent=True
						break
			if elementPresent:
				continue
			else:
				self.data[x,y]=element
				print "We have found {2} at position x={0},y={1} using the hidden column pair technique.".format(x,y,element)
				self.dataChanged=True
				return True	
			
		return False
		
	
	def findHiddenNonetCandidates(self,x,y):
		"""Finds if a number is "hiding" in the nonet containing (x,y). If a number is "hiding" in a nonet it only appears once in the possible 
		values list of an empty cell for that nonet. Since it only appears once, that cell must be the location of the number. If the number is
		found, the value is updated in self.data and True is returned. If no number is found, False is returned."""
		elementPresent=False
		for element in self.possibleCandidates[(x,y)]:
			for x1 in range(0,3):
				x_value=3*math.floor(x/3)+x1
				for y1 in range(0,3):
					y_value=3*math.floor(y/3)+y1
					if (x_value,y_value) in self.possibleCandidates:
						listValues=self.possibleCandidates[(x_value,y_value)]
						if element in listValues:
							elementPresent=True
							break
			if elementPresent:
				continue
			else:
				self.data[x,y]=element
				print "We have found {2} at position x={0},y={1} using hidden nonent pair technique.".format(x,y,element)
				self.dataChanged=True
				return True	
			
	def removeRowValues(self,x,y,x1,y1,element):
		"""Helper method for findNakedPair. Removes the element from the possible candidates list that are in the same row of x. 
		The element is not removed from the possible candidates of (x,y) or (x1,y1) as these two values are the naked pair."""
		for (x_index,y_index) in self.possibleCandidates:
				if x==x_index and y_index!=y and y_index!=y1:
				 #if (x,y_value) in self.possibleCandidates:
					for value in self.possibleCandidates[(x_index,y_index)]:
						if value==element:
							self.possibleCandidates[(x_index,y_index)]=[val for val in self.possibleCandidates[(x_index,y_index)] if val !=element]
							
	def removeColValues(self,x,y,x1,y1,element):	
		"""Helper method for findNakedPair. Removes the element from the possible candidates list that are in the same column of y. 
		The element is not removed from the possible candidates of (x,y) or (x1,y1) as these two values are the naked pair."""
		for (x_index,y_index) in self.possibleCandidates:
				if y==y_index and x_index!=x and x_index!=x1:
				 #if (x,y_value) in self.possibleCandidates:
					for value in self.possibleCandidates[(x_index,y_index)]:
						if value==element:
							self.possibleCandidates[(x_index,y_index)]=[val for val in self.possibleCandidates[(x_index,y_index)] if val !=element]
							
	def removeNonetValues(self,x,y,x1,y1,element):
		"""Helper method for findNakedPair. Removes the element from the possible candidates list that are in the same column of y. 
		The element is not removed from the possible candidates of (x,y) or (x1,y1) as these two values are the naked pair."""
		for x_index in [0,1,2]:
			x_value=3*math.floor(x/3)+x_index
			for y_index in range(0,3):
				y_value=3*math.floor(y/3)+y_index
				if (x_value,y_value) in self.possibleCandidates and x_value !=x1 and y_value!=y_value:
					for value in self.possibleCandidates[(x_value,y_value)]:
						if value==element:
							
							if self.i==0:
								print "FixingNonet:old list of candidates for {0},{1},{2}".format(x_value,y_value,self.possibleCandidates[(x_value,y_value)])
							self.possibleCandidates[(x_value,y_value)]=[val for val in self.possibleCandidates[(x_value,y_value)] if val !=element]
							if self.i==0:
								print "new possible candidates for {0},{1},{2}".format(x_value,y_value,self.possibleCandidates[(x_value,y_value)])
			
	
	def removeValues(self,x,y):
		"""Removes any instances of the value at (x,y) in self.data from the possible values candidates in the row, column, and nonent where (x,y)
		is located."""
		element=self.data[x,y]
		for (x_index,y_index) in self.possibleCandidates:
			if x==x_index:
				for value in self.possibleCandidates[(x_index,y_index)]:
					if value==element:
						self.possibleCandidates[(x_index,y_index)]=[val for val in self.possibleCandidates[(x_index,y_index)] if val !=element]
			if y==y_index:
				for value in self.possibleCandidates[(x_index,y_index)]:
					if value==element:
						self.possibleCandidates[(x_index,y_index)]=[val for val in self.possibleCandidates[(x_index,y_index)] if val !=element]
		for x_index in [0,1,2]:
			x_value=3*math.floor(x/3)+x_index
			for y_index in range(0,3):
				y_value=3*math.floor(y/3)+y_index
				if (x_value,y_value) in self.possibleCandidates:
					for value in self.possibleCandidates[(x_value,y_value)]:
						if value==element:
							self.possibleCandidates[(x_value,y_value)]=[val for val in self.possibleCandidates[(x_value,y_value)] if val !=element]
	
	
def main():
	"""Collects input csv, finds the starting possible candidates and applies the algorithms for finding a solution to the input Sudoku puzzle"""
	file=sys.argv[1]
	data=np.loadtxt(open(file,"rb"),delimiter=",").astype('int')
	if data.size==81:
		print "This is a valid Sudoku puzzle {0}".format(data.size)
	else:
		print "This is not a valid 9x9 Sudoku  puzzle {0}".format(data.size)
	print "Initial sudoku puzzle is:"
	print data
	
	sudoku=solveSudoku(data)
	sudoku.initialize()
	solution=sudoku.runAlgorithms()
	
		
	
if __name__=="__main__":
	main()

		
		
		
		
