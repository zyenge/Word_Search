from multiprocessing import Pool
import datetime
from utility_function import *
import sys
from super_word_search import puzzle_board



def chunk(wordlist,n, board_dict):
  """split the word list into n chucks for parallel processing """
  for i in xrange(0, len(wordlist), n):
    sublist=wordlist[i:i+n]
    sublist.append(board_dict)
    yield sublist


def word_match(word,current_pos,direction,index_list,board):
    """
    This is a recursive function used to search a given word leter by letter in one direction (dx,dy)
    
    The function returns the position of the last letter and end recursion if reach the end of the word, else return False
        
    **parameters:
    word -> the rest of the word without the first letter
    (dx,dy) -> one of the eight directions
    (x,y) -> position of the first letter
    index_list -> a list of position that are already visited, used to check one position is not used more than once,
    index_list is initiated with current_pos
    """
    
    row=len(board) 
    column=len(board[0])
    index_loc=index_cleaner(current_pos[0]+direction[0],current_pos[1]+direction[1],row, column)
    pos_loc=positive_loc(index_loc[0],index_loc[1],row, column)
    if len(word)==0:
        return current_pos
    elif pos_loc in index_list:
        #print index_list
        return False
    elif word[0]==board[index_loc[0]][index_loc[1]]:
        index_list.append(pos_loc)
        return word_match(word[1:], index_loc,direction,index_list,board)
    else:
        return False


"""----------------------map function----------------------------"""
def find_word_list(para_dict):
    
    """
    for each sub word list, it returns a dictionary with each word as keys and postions (start, end) or 'not found' as values. 
    The reason for returning a dictionary instead of a string with only positions (like I did with the non_parallel case) is that 
    each process works at it's own speed and may return output at a different sequence than the given word sequence. 
    So if I need to produce an output like:
    
    (1,2) (1,6)
    (0,4) (4,4)
    NOT FOUND
    
    I need to output dictionaries on each processors, combine them in the reducing stage (see line 156 ), and match up with the 
    original word list sequence then return a string for final output
    """
    
    output={}
    
    
    wrap=para_dict[-1]['wrap']
    words=para_dict[-1]['words']
    board=para_dict[-1]['board']
    (row,column)=(len(board),len(board[0]))
    sub_words=para_dict[:-1]
    
    for word in sub_words:
        init_index=[]
        for row_ix,row_item in enumerate(board):
            for col_ix,col_item in enumerate(row_item):
                if col_item==word[0]:
                    init_index.append((row_ix, col_ix))
        for xy in init_index:
            index_list=[xy]
            find_match=False
            for direction in get_directions():
                find_match = find_match or word_match(word[1:],xy,direction,index_list,board)
                if find_match != False and wrap:
                    output[word]=str(xy)+' '+str(positive_loc(find_match[0],find_match[1],row,column))+'\n'
                    break
                elif find_match != False and (not wrap):
                    if check_wrap(xy,positive_loc(find_match[0],find_match[1],row,column),direction):
                        find_match=False
                    else:
                        output[word]=str(xy)+' '+str(positive_loc(find_match[0],find_match[1],row,column))+'\n'
                        break
            if find_match!= False:
                break
        
        if find_match == False:
            #print word,'Not Found'
            output[word]='Not Found'+'\n'
    return output
"""------------------------------------------------------------------"""




"""------------------------------Reducer-----------------------------""" 
def Reduce(words, words_search_result):
  """combine result from different processors"""
  output_dict={}
  for item in words_search_result:
      output_dict=dict(output_dict.items()+item.items())
  
  # match dict key words with the sequence of the given words
  output_string=''
  for eachword in words:
    output_string=output_string+output_dict[eachword]
  return output_string
"""------------------------------------------------------------------"""






if __name__ == '__main__':
  board=puzzle_board("Input_file_for_parallel.txt")
  words=board.get_words()
  wrap=board.get_wrap()

  pool = Pool(processes=4,)
  start_time=datetime.datetime.now()
   
  board_dict = {'board':board.get_board(),'words':words,'wrap': wrap}
  
  partitioned_text = list(chunk(words, len(words) / 4,board_dict))
    
  parallel_process= pool.map(find_word_list, partitioned_text)
  
  writeout=Reduce(words,parallel_process)
  
  """The required output file will save to file, the time took to run is printed to the screen"""
  
  with open("Output_file_by_parallel.txt","w") as write_multi:
      write_multi.write(writeout)
  
  print "time took to process %s words in parallel is " %len(words), datetime.datetime.now()-start_time