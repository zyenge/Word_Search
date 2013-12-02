__author__= 'Z.GE'

"""
contains main and associated methods to solve word puzzle using multiple processing techniques.
"""


from multiprocessing import Pool
import datetime
from utility_function import *
import sys
from super_word_search import puzzle_board



def chunk(wordlist, n, board_dict):
  """split the word list into n chucks for parallel processing 
  **parameters:
  wordlist -> the entire wordlist
  n -> number of the processors
  board_dict -> a dictionary that desribes the puzzle board that is specified in the input file
  
  """
  for i in xrange(0, len(wordlist), n):
    sublist=wordlist[i:i+n]
    sublist.append(board_dict)
    yield sublist


def word_match(word,current_pos,direction,index_list,board):
    """
    This is a recursive function used to search a given word leter by letter in one direction (dx,dy)
    This function is called by the map function: find_word_list
    
    
    It returns the position of the last letter and end recursion if reach the end of the word, else return False
        
    **parameters:
    word -> the rest of the word without the first letter
    current_pos -> position of the first letter
    direction -> one of the eight directions
    index_list -> a list of position that are already visited, used to check one position is not used more than once,
    index_list is initiated with current_pos
    board -> wordboard
    """
    
    row=len(board) 
    column=len(board[0])
    index_loc=index_cleaner(current_pos[0]+direction[0],current_pos[1]+direction[1],row, column)
    pos_loc=positive_loc(index_loc[0],index_loc[1],row, column)
    if len(word)==0:
        return current_pos
    elif pos_loc in index_list:  #if the index is already visited, return False
        return False
    elif word[0]==board[index_loc[0]][index_loc[1]]:
        index_list.append(pos_loc)
        return word_match(word[1:], index_loc,direction,index_list,board)
    else:
        return False


"""----------------------map function----------------------------"""
def find_word_list(sub_list):
    
    """
    for each sub word list, it returns a dictionary with each word as keys and postions (start, end) or 'not found' as values. 
    The reason for returning a dictionary instead of a string with only positions (like I did with the non_parallel case) is that 
    each process works at it's own speed and may return output at a different sequence than the given word sequence. 
    So if I need to produce an output like:
    
    (1,2) (1,6)
    (0,4) (4,4)
    NOT FOUND
    
    I need to output dictionaries on each processors, combine them in the reducing stage (see line 127 ), and match up with the 
    original word list sequence then return a string for final output
    
    
    **parameters:
    sub_list -> a list containing a sublist of the words, and the properties of the puzzle board as specified in the input file.
    These properties are the last item in the sub_list list, and are stored in a dictionary,
    
    """
    
    output={}
    
    
    wrap=sub_list[-1]['wrap']
    words=sub_list[-1]['words']
    board=sub_list[-1]['board']
    (row,column)=(len(board),len(board[0]))
    
    sub_words=sub_list[:-1]
    for word in sub_words:
        init_index=[]  # if the first letter of word is found, add index into init_index
        for row_ix,row_item in enumerate(board):
            for col_ix,col_item in enumerate(row_item):
                if col_item==word[0]: 
                    init_index.append((row_ix, col_ix))
        for xy in init_index:
            index_list=[xy] # a list of position that are already visited, used to check one position is not used more than once
            find_match=False
            for direction in get_directions(): # for each direction, use the recusive word_match to search for the word
                find_match = find_match or word_match(word[1:],xy,direction,index_list,board)  # if match is found, word_match returns an ending position, else it returns False
            
                # check wrap condition and write output file
                if find_match != False and wrap:
                    output[word]=str(xy)+' '+str(positive_loc(find_match[0],find_match[1],row,column))+'\n'
                    break
                elif find_match != False and (not wrap):
                    if check_wrap(xy,positive_loc(find_match[0],find_match[1],row,column),direction):
                        find_match=False
                    else:
                        output[word]=str(xy)+' '+str(positive_loc(find_match[0],find_match[1],row,column))+'\n'
                        break
            if find_match!= False: # if a word is already found, break the loop
                break
        
        if find_match == False:
            output[word]='Not Found'+'\n'
    return output
"""------------------------------------------------------------------"""




"""------------------------------Reducer-----------------------------""" 
def Reduce(words, words_search_result):
  """combine result from different processors and write to file
  ** parameters:
  words -> entire list of words from input file
  words_search_result -> a list of dictionaries resulted from differet processors.
                         Each contains words as keys, and their start & end positions or 'NOT FOUND' as values
  
  
  """
  
  output_dict={}
  for item in words_search_result:
      output_dict=dict(output_dict.items()+item.items())
  
  # match dict key words with the sequence of the given words
  output_string=''
  for eachword in words:
    output_string=output_string+output_dict[eachword]
  
  with open("Output_file_by_parallel.txt","w") as write_multi:
      write_multi.write(output_string)
  return "Multi-processing output written to file SUCCESSFULLY!! \n :) "
"""------------------------------------------------------------------"""






if __name__ == '__main__':
  
  board=puzzle_board("Input_file_for_parallel.txt")
  words=board.get_words()
  wrap=board.get_wrap() # get wrap condition (bool)
  pool = Pool(processes=4,) # set process pool to 4
  
  start_time=datetime.datetime.now() 
  
  board_dict = {'board':board.get_board(),'words':words,'wrap': wrap} #puzzle properties to pass to each processsors
  
  partitioned_text = list(chunk(words, len(words) / 4, board_dict)) # contains subset of words and puzzle properties as input to map function below (find_word_list), to be distributed across the process pool
    
  parallel_process= pool.map(find_word_list, partitioned_text)
  
  print Reduce(words,parallel_process) #reduce the multi-processing outputs to a string to write to the file
  
  """The required output file will save to file, the time took to run is printed to the screen"""
  
  
  print "time took to process %s words in parallel is " %len(words), datetime.datetime.now()-start_time