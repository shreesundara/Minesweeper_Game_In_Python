#author : Shree Phani Sundara B N
#Python : Assignment.
#Branch : M.Tech 1st Semester.
#USN : 1PI14SWT14
#Version : 1.0
#Program : A simpler implementation of MinesWeeper program..

#import required modules..
#import pygame
from livewires import games, colour
import random

#Instantiate a SCREEN Dimensions CONSTANT as contents of tuple..
NO_OF_ROWS = 8;
NO_OF_COLS = 8;
IMAGE_WIDTH = 26;
IMAGE_HEIGHT = 26;
SCREEN_DIM = (IMAGE_WIDTH*NO_OF_ROWS , IMAGE_HEIGHT*NO_OF_COLS);#26*8 because the image sizes is 26X26 and we require only 8 cells..


MOUSE_BUTTON_LEFT = 0;
MOUSE_BUTTON_MIDDLE = 1;
MOUSE_BUTTON_RIGHT = 2;
MAX_NO_OF_BLAST_OBJECTS = 5;

CELL_EMPTY = 0;
BLAST_OBJ = 1;
CELL_CHECKED = 2;

	
# Defining MinesWeeper Class Definition...

class MinesWeeper(object):
	""" MinesWeeper Class Definition """
	def __init__(self):
		self.screenWidth = SCREEN_DIM[0];
		self.screenHeight = SCREEN_DIM[1];
		self.cell_contents_list = [];
		self.gameOver = False;
		self.userWins = False;
		self.noOfBlastObjectsInserted = 0;
		self.noOfCheckedCells = 0;
		self.initializeCellContents();
		self.drawScreen();
	
	
	def initializeCellContents(self):
		self.initializeCellList();
		self.insertBlastObjects();

	def initializeCellList(self):

		for i in range(NO_OF_ROWS * NO_OF_COLS):
			#print "index i is : " ;
			#print i
			##cell_contents_list[i] = CELL_EMPTY;
			self.cell_contents_list.append(CELL_EMPTY);
		
		#self.displayCellListContentsInConsole();
	
	
	def displayCellListContentsInConsole(self) :
		print "Cell List Contents are ";
		counter = 0;
		for i in self.cell_contents_list:
			print "cell_content [",counter,"] --> ", i;
			counter+=1;
	
	def displayIndexesOfBlastObjLocations(self):
		print "Cell Blast Object Locations are ";
		counter = 0;
		for i in self.cell_contents_list:
			if i == BLAST_OBJ:
				print "cell_content [",counter,"] --> ", i;
			
			counter+=1;
	
	def countNoOfBlastObjects(self):
		counter = 0;
		for i in self.cell_contents_list:
			if i == BLAST_OBJ:
				#print "cell_content [",counter,"] --> ", i;
				counter+=1;
			
		self.noOfBlastObjectsInserted = counter;
		self.noOfCheckedCells = counter;
		print "No of blast objects present are", counter;
	
	def insertBlastObjects(self):
		for i in range(MAX_NO_OF_BLAST_OBJECTS):
			rand_num = random.randrange(NO_OF_ROWS * NO_OF_COLS);
			self.cell_contents_list[rand_num] = BLAST_OBJ;
		
		#self.displayCellListContentsInConsole();
		
		#This is for debugging only... Change this later..
		self.displayIndexesOfBlastObjLocations();
		
		self.countNoOfBlastObjects();
	
	def drawScreen(self):
		self.my_screen = games.Screen(self.screenWidth,self.screenHeight);
		self.my_screen.mouse_down = self.mouse_down;
		
		self.danger_image = games.load_image("my_images/boom.png");
		self.normal_image = games.load_image("my_images/normal.png");
		#self.danger_image = games.load_image("my_images/danger.png");
		
		
		self.clock_sound = games.load_sound("my_sounds/clock_tick.wav");
		self.blast_sound = games.load_sound("my_sounds/burst.wav");		
		
		self.my_screen.set_background(self.normal_image);
		
		if(self.clock_sound != None):
			self.clock_sound.play();
		else:
			print "Some problem while playing sound";

		#This is only for debugging...
		#self.displayAllCellContents();
		
		self.my_screen.mainloop();
		
	
		
	def mouse_down(self, pos, button):
		if(self.gameOver or self.userWins):
			return;
			
		if(button == MOUSE_BUTTON_LEFT) :
			xPos = pos[0];
			yPos = pos[1];
			cell_col = xPos / IMAGE_WIDTH;#starting from cell_row count 0.
			cell_row = yPos / IMAGE_HEIGHT;#starting from cell_row count 1.
			#selected_cell_index = (cell_row*NO_OF_COLS) + (cell_col+1);#this starts from index 1, so it must subtracted by 1..
			selected_cell_index = self.return_1D_cell_index(cell_row,cell_col);
			print "**********************************************************"
			print "Selected Cell Row is ", cell_row;
			#print cell_row;
			print "Selected Cell Col is ", cell_col;
			#print cell_col;
			print "Selected cell in 1D array is ", selected_cell_index;
			print "**********************************************************"
			
			self.displaySingleCellContent(selected_cell_index,cell_row,cell_col);
			
	
	def displaySingleCellContent(self,indexOfCell,yPos_of_cell,xPos_of_cell):
		if(indexOfCell >= 0 and indexOfCell < NO_OF_ROWS*NO_OF_COLS):
			#display cell contents..
			
			if (self.cell_contents_list[indexOfCell] == CELL_CHECKED):
				#return without doing anything...
				return;
			
			
			elif(self.cell_contents_list[indexOfCell] == BLAST_OBJ):
				
				self.gameOver = True;
				
				#display all cell-contents
				self.displayAllCellContents();
				
				#display message to user "You Loose"..
				games.Text(screen = self.my_screen,
							x = (SCREEN_DIM[0]/2),
							y = (SCREEN_DIM[1]/2) - 10,
							text = "GAME OVER:",
							size = 40,
							colour = colour.blue
							);
				games.Text(screen = self.my_screen,
							x = SCREEN_DIM[0]/2,
							y = SCREEN_DIM[1]/2 + 25,
							text = "You Loose ",
							size = 40,
							colour = colour.blue
							);							
				self.noOfCheckedCells+=1;
				
			else:
				#display a numeric text in that cell position,
				#depending the no.. of neighbouring blast objects..
				noOfBombs = self.checkAndReturnCellNumericValue(indexOfCell,xPos_of_cell,yPos_of_cell);
				print "noOfBombs is ", noOfBombs;
				games.Text(screen = self.my_screen,
							x = (xPos_of_cell * IMAGE_WIDTH) + 13,
							y = (yPos_of_cell * IMAGE_HEIGHT) + 13,
							text = str(noOfBombs),
							size = 30,
							colour = colour.black
							);
				self.noOfCheckedCells+=1;
				self.cell_contents_list[indexOfCell] = CELL_CHECKED;
				
				
		else:
			print "Invalid index provided for displaying cell contents ";
		
		print "No.. of checked cells are ", self.noOfCheckedCells;
		
		if(self.noOfCheckedCells >= NO_OF_ROWS*NO_OF_COLS):
			self.userWins = True;
			#display all cell-contents
			self.displayAllCellContents();
			
			self.my_screen.clear();
			#display message to user "You Loose"..
			games.Text(screen = self.my_screen,
						x = (SCREEN_DIM[0]/2),
						y = (SCREEN_DIM[1]/2) - 10,
						text = "GAME OVER:",
						size = 30,
						colour = colour.dark_green
						);
			games.Text(screen = self.my_screen,
						x = SCREEN_DIM[0]/2,
						y = SCREEN_DIM[1]/2 + 25,
						text = "You \"WIN\" ",
						size = 30,
						colour = colour.dark_green
						);						
			
	
	def checkAndReturnCellNumericValue(self,indexOfCell,col,row):
		noOfBombs = 0;
		
		print "main row and column is ", (row)+1 ,", and column", (col)+1 , " and index is", indexOfCell; 
		
		#check if its previous col in same row has bomb...
		index = self.return_1D_cell_index(row,col-1);
		if(index >= 0 and index < NO_OF_ROWS*NO_OF_COLS):
			if(self.cell_contents_list[index] == BLAST_OBJ):
				print "checking row and column is ", (row)+1 ,", and column", (col-1)+1 , " and index is", index; 		
				noOfBombs+=1;
		
		#check if its next col in same row has bomb...
		index = self.return_1D_cell_index(row,col+1);
		if(index >= 0 and index < NO_OF_ROWS*NO_OF_COLS):		
			if(self.cell_contents_list[index] == BLAST_OBJ):
				print "checking row and column is ", (row)+1 ,", and column", (col+1)+1 , " and index is", index; 				
				noOfBombs+=1;
			
		#check if its previous row in same col has bomb...
		index = self.return_1D_cell_index(row-1,col);
		if(
			(index >= 0 and index < NO_OF_ROWS*NO_OF_COLS)
			and
			self.cell_contents_list[index] == BLAST_OBJ
		):
			print "checking row and column is ", (row-1)+1 ,", and column", (col)+1 , " and index is", index; 		
			noOfBombs+=1;
		
		#check if its next row in same col has bomb...		
		index = self.return_1D_cell_index(row+1,col);
		if(
			(index >= 0 and index < NO_OF_ROWS*NO_OF_COLS)
			and 
			self.cell_contents_list[index] == BLAST_OBJ
		   ):
			print "checking row and column is ", (row+1)+1 ,", and column", (col)+1 , " and index is", index; 		
			noOfBombs+=1;

		#check if its previous row in its previous col has bomb...
		index = self.return_1D_cell_index(row-1,col-1);
		if(
			(index >= 0 and index < NO_OF_ROWS*NO_OF_COLS)
			and
			self.cell_contents_list[index] == BLAST_OBJ
		):
			print "checking row and column is ", (row-1)+1 ,", and column", (col-1)+1 , " and index is", index; 		
			noOfBombs+=1;
		
		#check if its previous row in its next col has bomb...
		index = self.return_1D_cell_index(row-1,col+1);
		if(
			(index >= 0 and index < NO_OF_ROWS*NO_OF_COLS) 
			and
			self.cell_contents_list[index] == BLAST_OBJ
		):
			print "checking row and column is ", (row-1)+1 ,", and column", (col+1)+1 , " and index is", index; 				
			noOfBombs+=1;
		
		#check if its next row in its previous col has bomb...		
		index = self.return_1D_cell_index(row+1,col-1);
		if(
			(index >= 0 and index < NO_OF_COLS*NO_OF_ROWS)
			and
			self.cell_contents_list[index] == BLAST_OBJ
		):
			print "checking row and column is ", (row+1)+1 ,", and column", (col-1)+1 , " and index is", index; 		
			noOfBombs+=1;
		
		#check if its next row in its next col has bomb...				
		index = self.return_1D_cell_index(row+1,col+1);
		if(
			(index >= 0 and index < NO_OF_ROWS*NO_OF_COLS)
			and
			self.cell_contents_list[index] == BLAST_OBJ
		):
			print "checking row and column is ", (row+1)+1 ,", and column", (col+1)+1 , " and index is", index; 		
			noOfBombs+=1;
			
			
		return noOfBombs;
	
	
	def return_1D_cell_index(self,row,col):
		#this starts from index 1, so it must subtracted by 1 before being returned..
		if(row >= 0 and col >= 0 and row < NO_OF_ROWS and col < NO_OF_COLS):
			selected_cell_index = (row*NO_OF_COLS) + (col+1);
			return selected_cell_index-1;
		else:
			return -1;
	
	
	def displayAllCellContents(self):
		row = 0;
		col = 0;
		for i in self.cell_contents_list:
			
			if(i == BLAST_OBJ):
				CustomBlastObject(self.my_screen,
									(col*IMAGE_WIDTH) + 13 ,
									(row*IMAGE_HEIGHT) + 13,
									self.danger_image
									);
				print "row is : ", row , " and col is : ", col;
				#raw_input("Press any key");

			col+=1;
			
			if(col > NO_OF_COLS-1) :
				row +=1;
				col = 0;
			
		
		
#end of MinesWeeper Class Definition..


#Defining the Sprite Object Class...		
class CustomBlastObject(games.Sprite):
	""" The bomb image sprite object """
	
	def __init__(self,my_screen,xPos,yPos,my_image):
		self.init_sprite(screen = my_screen, x = xPos, y = yPos, image = my_image  );

#End of Sprite Class Definition..
		
#Main Execution Starts Here..
my_mines = MinesWeeper();