## utility functions

def get_directions():
    dir_list=[]
    for i in range(-1,2):
        for j in range(-1,2):
            dir_list.append((i,j))
    dir_list.pop(dir_list.index((0,0)))
    return dir_list

def index_cleaner(i,j,row,column):
    if i>=row:
        i=i-row
    if j>=column:
        j=j-column
    return (i,j)

def positive_loc(i,j,row,column):
    if i<0:
        i=i+row
    if j<0:
        j=j+column
    return (i,j)

def check_wrap(begin,end,arrow):
    if (arrow[0]<0 and end[0]>begin[0]) or (arrow[0]>0 and end[0]<begin[0]):
        return True
    elif (arrow[1]<0 and end[1]>begin[1]) or (arrow[1]>0 and end[1]<begin[1]):
        return True
    else:
        return False
