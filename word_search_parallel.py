from multiprocessing import Pool
import datetime
from utility_function import *


def get_file(file_dir):
  with open(file_dir,'r') as f:
      puzzle= [i.rstrip('\n') for i in f.readlines()]
  return puzzle

def get_row_column(puzzle):
  row=int(puzzle[0].split()[0])
  column=int(puzzle[0].split()[1])
  return (row,column)

def wrap_bool(puzzle,row):
  """return wrap condition boolean"""
  if puzzle[row+1]=='NO_WRAP':
    return False
  elif puzzle[row+1]=='WRAP':
    return True

#word_list
def get_wordlist(puzzle,row):
  words=[]
  word_count=int(puzzle[row+2])
  for count in range(word_count):
      #print [j for j in puzzle[row+3+count]]
      words.append(puzzle[row+3+count])
  return words


def get_board(puzzle,row):
  board=[]
  for count in range(row):
      board.append([board_row for board_row in puzzle[1+count]])
  return board



def word_match(word,current_pos,direction,index_list,board):
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


def chunk(l,n):
  """split the word list into n chucks for parallel processing """
  for i in xrange(0, len(l), n):
    yield l[i:i+n]



"""----------------------map function----------------------------"""
def find_word_list(sub_words):
    output={}
    puzzle=get_file("Input_file.txt")
    (row,column)=get_row_column(puzzle)
    wrap=wrap_bool(puzzle,row)
    words=get_wordlist(puzzle,row)
    board=get_board(puzzle,row)
    
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
  pool = Pool(processes=4,)
  start_time2=datetime.datetime.now()
 
  puzzle=get_file("Input_file.txt")
  (row,column)=get_row_column(puzzle)
  words=get_wordlist(puzzle,row)

  partitioned_text = list(chunk(words, len(words) / 4))
  
  parallel_process= pool.map(find_word_list, partitioned_text)

  writeout=Reduce(words,parallel_process)
  
  with open("Output_file_multi_process.txt","w") as write_multi:
      write_multi.write(writeout)

  print datetime.datetime.now()-start_time2