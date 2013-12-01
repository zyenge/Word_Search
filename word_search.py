import sys
from utility_function import *

class word_puzzle:
    
    eight_directions=get_directions()
    
    def __init__(self,inputfile=None):
        """
        read input file, check the format of the input file,
        get the board of letters: self.board
        get the list of words to search for: self.words
        get "Wrap" condition
        """
        self.inputfile=inputfile
        self.output=''
    
    def get_puzzle(self):
        # readfile
        try:
            with open(self.inputfile,'r') as f:
                self.puzzle= [i.rstrip('\n') for i in f.readlines()]
        except Exception as readerror:
            print readerror
            sys.exit(0)
        
        #read grid cord
        try:
            self.row=int(self.puzzle[0].split()[0])
            self.column=int(self.puzzle[0].split()[1])
        except Exception as griderror:
            print "grid coordinates format not correct"
            print griderror
            sys.exit(0)
        
        # read puzzle board
        self.board=[]
        for count in range(self.row):
            self.board.append([board_row for board_row in self.puzzle[1+count]])

        #words to search
        self.word_count=int(self.puzzle[self.row+2])
        self.words=[]
        for count in range(self.word_count):
            self.words.append(self.puzzle[self.row+3+count])
        
        #get wrap condition:
        if self.puzzle[self.row+1]=='NO_WRAP':
            self.wrap=False
        else:
            self.wrap=True
        return (self.board,self.words,self.wrap)
    
    def word_match(self,word,current_pos,direction,index_list):
        """
        for one word in the word list:
        Recursively matching the word letter by letter in one direction (dx,dy).
        The function returns the position of the last letter and end recursion if reach the end of the word, else return False
            
        **parameters:
        word -> the rest of the word without the first letter
        (dx,dy) -> one of the eight directions
        (x,y) -> position of the first letter
        index_list -> a list of position that are already visited, used to check one position is not used more than once,
        index_list is initiated with current_pos
        """
        #self.word=word
        #self.current_pos=corrent_pos
        #self.direction=direction
        #self.index_list=index_list
        index_loc=index_cleaner(current_pos[0]+direction[0],current_pos[1]+direction[1],self.row,self.column)
        pos_loc=positive_loc(index_loc[0],index_loc[1],self.row,self.column)
        if len(word)==0:
            return current_pos
        elif pos_loc in index_list:
            #print index_list
            return False
        elif word[0]==self.board[index_loc[0]][index_loc[1]]:
            index_list.append(pos_loc)
            return self.word_match(word[1:], index_loc,direction,index_list)
        else:
            return False
    
    def find_word_list(self,board,words,wrap):
        self.row=len(board)
        self.column=len(board[0])
        self.board=board
        for word in words:
            init_index=[]
            for row_ix,row_item in enumerate(board):
                for col_ix,col_item in enumerate(row_item):
                    if col_item==word[0]:
                        init_index.append((row_ix, col_ix))
            for xy in init_index:
                index_list=[xy]
                find_match=False
                for direction in word_puzzle.eight_directions:
                    find_match = find_match or word_puzzle.word_match(self, word[1:],xy,direction,index_list)
                    
                    # check wrap condition:
                    if find_match != False and wrap:
                        #print word, xy,positive_loc(find_match[0],find_match[1],self.row,self.column),direction
                        self.output=self.output+str(xy)+' '+str(positive_loc(find_match[0],find_match[1],self.row,self.column))+'\n'
                        break
                    elif find_match != False and (not wrap):
                        if check_wrap(xy,positive_loc(find_match[0],find_match[1],self.row,self.column),direction):
                            find_match=False
                        else:
                            #print word, xy,positive_loc(find_match[0],find_match[1],self.row,self.column),direction
                            self.output=self.output+str(xy)+' '+str(positive_loc(find_match[0],find_match[1],self.row,self.column))+'\n'
                            break
                    
                # if the word 
                if find_match!= False:
                    break
            
            if find_match == False:
                #print word,'Not Found'
                self.output=self.output+'Not Found'+'\n'
        
        with open("Output_file.txt","w") as write_file:
                    write_file.write(self.output)
        return self.output
        

class1=word_puzzle("Input_file.txt")
class1.get_puzzle()
print class1.find_word_list(*class1.get_puzzle())
