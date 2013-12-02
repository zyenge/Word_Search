import sys
from utility_function import *
import datetime
from super_word_search import puzzle_board,puzzle_solver


start_time=datetime.datetime.now()

board=puzzle_board("Input_file_for_parallel.txt")
word_search=puzzle_solver(board.get_board(),board.get_words(),board.get_wrap())
wordcount=len(board.get_words())
word_search.find_word_list(board.get_words())
print "time took to process %s words is "%wordcount, datetime.datetime.now()-start_time
