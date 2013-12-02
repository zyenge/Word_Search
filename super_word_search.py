__author__= 'Z.GE'


"""
super_word_search.py contains two classes: puzzle_board, puzzle_solver

"""
import sys
from utility_function import *
import datetime



class puzzle_board:
  
  """puzzle_board defines class and methods to read and store puzzle properties as described in the input file.
  such as board, words to search, wrap condition """

  def __init__(self,inputfile=None):
    
    self.inputfile=inputfile
    
    try:
        with open(self.inputfile,'r') as f:
            self.puzzle= [i.rstrip('\n') for i in f.readlines()]
    except Exception as readerror:
        print readerror
        sys.exit(0)
    
    """read first line to get board dimension"""
    try:
        self.row=int(self.puzzle[0].split()[0])
        self.column=int(self.puzzle[0].split()[1])
    except Exception as griderror:
        print "grid coordinates format not correct"
        print griderror
        sys.exit(0)
    

  def get_board(self):
   
    self.board=[]
    for count in range(self.row):
      if len(self.puzzle[1+count])==self.column:
        self.board.append([board_row for board_row in self.puzzle[1+count]])
      else:
        print "column counts doen't match column number at line %s" %self.puzzle[1+count]
        system.exit(0)
    return self.board

  def get_wrap(self):
    #get wrap condition:
    if self.puzzle[self.row+1]=='NO_WRAP':
        self.wrap=False
    elif self.puzzle[self.row+1]=='WRAP':
        self.wrap=True
    else:
      print "wrap condition not specified or the number of rows doens't match the given row count at line %s" %str(self.row+1)
      sys.exit(0)
    return self.wrap
    
      
  def get_words(self):
    self.word_count=int(self.puzzle[self.row+2])
    self.words=[]
    for count in range(self.word_count):
        try:
          self.words.append(self.puzzle[self.row+3+count])
        except Exception:
          print "specified %s words, NOT enough words listed" %self.word_count
          sys.exit(0)
    try:
      if len(self.puzzle[self.row+3+self.word_count])!=0:
        print "specified %s words, too many words listed" %self.word_count
        sys.exit(0)
    except Exception:
      pass   
    
    return self.words
    
    


class puzzle_solver:
  
  """
  given board, word list, wrap condiction, contains methods to solve puzzle without multi-processing
  """
  
  eight_directions=get_directions()
  
  def __init__(self,board, wordlist,wrap):
    self.board=board
    self.words=wordlist
    self.wrap=wrap
    self.row=len(self.board)
    self.column=len(self.board[0])
  
  def __call__(self,word_list):
    puzzle_solver.find_word_list(self,word_list)
    
  def word_match(self,word,current_pos,direction,index_list):
      """
      This is a recursive function used to search a given word leter by letter in one direction (dx,dy)
    
      The function returns the position of the last letter and end recursion if reach the end of the word, else return False
        
      **parameters:
      word -> the rest of the word without the first letter
      current_pos -> position of the first letter
      direction -> one of the eight directions
      index_list -> a list of position that are already visited, used to check one position is not used more than once,
      index_list is initiated with current_pos
      board -> wordboard
      """
      
      index_loc=index_cleaner(current_pos[0]+direction[0],current_pos[1]+direction[1],self.row,self.column)
      pos_loc=positive_loc(index_loc[0],index_loc[1],self.row,self.column)
      if len(word)==0:
          return current_pos
      elif pos_loc in index_list:  #if the index is already visited, return False
          return False
      elif word[0]==self.board[index_loc[0]][index_loc[1]]:
          index_list.append(pos_loc)
          return self.word_match(word[1:], index_loc,direction,index_list)
      else:
          return False
  
  def find_word_list(self,word_list):
    
    
    """
    find words in seqence and return a string to write to the file (this methos use single process)
    **parameters:
    word_list -> entire word list
    """
    self.word_list=word_list
    self.output=''
    for word in self.word_list:
        init_index=[]  # if the first letter of word is found, add index into init_index
        for row_ix,row_item in enumerate(self.board):
            for col_ix,col_item in enumerate(row_item):
                if col_item==word[0]:
                    init_index.append((row_ix, col_ix))
        for xy in init_index:
            index_list=[xy]  # a list of position that are already visited, used to check one position is not used more than once
            find_match=False
            for direction in puzzle_solver.eight_directions: # for each direction, use the recusive word_match to search for the word
                find_match = find_match or puzzle_solver.word_match(self, word[1:],xy,direction,index_list)  # if match is found, word_match returns an ending position, else it returns False
            
                # check wrap condition:
                if find_match != False and self.wrap:
                    self.output=self.output+str(xy)+' '+str(positive_loc(find_match[0],find_match[1],self.row,self.column))+'\n'
                    break
                elif find_match != False and (not self.wrap):
                    if check_wrap(xy,positive_loc(find_match[0],find_match[1],self.row,self.column),direction):
                        find_match=False
                    else:
                        self.output=self.output+str(xy)+' '+str(positive_loc(find_match[0],find_match[1],self.row,self.column))+'\n'
                        break
            
        
            if find_match!= False: # if a word is already found, break the loop
                break
    
        if find_match == False:
            self.output=self.output+'Not Found'+'\n'

    with open("Output_file.txt","w") as write_file:
      write_file.write(self.output)
    return self.output