import numpy as np
import time
import random
import copy


class unsolved_sudoku:
    
    def __init__(self, sudoku_array):
        self.sudoku = sudoku_array
        self.possible_values_for_square = [[[1,2,3,4,5,6,7,8,9] for _ in range(1,9+1)] for _ in range(1, 9+1)]
        self.empty_cells = [[i, j] for i in range(0, 9) for j in range(0, 9) if self.sudoku[i][j] == 0]
        self.possible_values_for_square = self.get_possible_values() 
        self.naked_pairs()  
        
        
    def get_possible_values(self):
        # if value isn't in empty cells 
        for i in range (0,9):
            for j in range (0, 9):
                if [i, j] not in self.empty_cells:
                    self.possible_values_for_square[i][j] = []
                else:
                    self.possible_values_for_square[i][j] = self.possible_values(i, j)
        return(self.possible_values_for_square)
    
    def get_possible_values_for_square(self, row, collumn):
        return (self.possible_values_for_square[row][collumn])
    
    def get_three_by_three_from_row(self, row, collumn):
        if row < 3: 
            rows_lower = 0
            rows_upper = 3
        elif row >= 3 and row < 6:
            rows_lower = 3
            rows_upper = 6
        else:
            rows_lower = 6
            rows_upper = 9

        if collumn < 3: 
            collumns_lower = 0
            collumns_upper = 3
        elif collumn >= 3 and collumn < 6:
            collumns_lower = 3
            collumns_upper = 6
        else:
            collumns_lower = 6
            collumns_upper = 9

        return((np.array(self.sudoku)[rows_lower:rows_upper, collumns_lower:collumns_upper]))
    
    
    def get_three_by_three_from_square(self, square, values=False):
        if (square == 0) or (square == 1) or (square == 2):
            rows_lower = 0
            rows_upper = 3
        elif (square == 3) or (square == 4) or (square == 5):
            rows_lower = 3
            rows_upper = 6
        elif (square == 6) or (square == 7) or (square == 8):
            rows_lower = 6
            rows_upper = 9
    
        if (square == 0) or (square == 3) or (square == 6):
            collumns_lower = 0
            collumns_upper = 3
        elif (square == 1) or (square == 4) or (square == 7):
            collumns_lower = 3
            collumns_upper = 6
        elif (square == 2) or (square == 5) or (square == 8):
            collumns_lower = 6
            collumns_upper = 9

        if values == True:
            return((self.sudoku)[rows_lower:rows_upper, collumns_lower:collumns_upper])
        else:
            return([rows_lower, rows_upper, collumns_lower, collumns_upper])
    
    def get_three_by_three_possible_values(self, square):
        if (square == 0) or (square == 1) or (square == 2):
            rows_lower = 0
            rows_upper = 3
        elif (square == 3) or (square == 4) or (square == 5):
            rows_lower = 3
            rows_upper = 6
        elif (square == 6) or (square == 7) or (square == 8):
            rows_lower = 6
            rows_upper = 9
    
        if (square == 0) or (square == 3) or (square == 6):
            collumns_lower = 0
            collumns_upper = 3
        elif (square == 1) or (square == 4) or (square == 7):
            collumns_lower = 3
            collumns_upper = 6
        elif (square == 2) or (square == 5) or (square == 8):
            collumns_lower = 6
            collumns_upper = 9
        
        possible_values = []
        for i in range (rows_lower, rows_upper):
            for j in range (collumns_lower, collumns_upper):
                possible_values.append(self.possible_values_for_square[i][j])

        return(possible_values)
    
    #returns array of possible values for that square (indicated by the row and collumn)
    def possible_values(self, row, collumn):
        possible_values = self.possible_values_for_square[row][collumn]
        ## possible values looking at the row
        row_values = [value for value in self.sudoku[row] if value != 0]
        possible_values = (set(possible_values).difference(row_values))
        ## possible values looking at the collumn
        collumn_values = []
        for i in range(9):
            if self.sudoku[i][collumn] != 0:
                collumn_values.append(self.sudoku[i][collumn])
        possible_values = (set(possible_values).difference(collumn_values)) 
        three_by_three = self.get_three_by_three_from_row(row, collumn)
        three_by_three_values = [value for value in (three_by_three.flatten()) if value != 0]
        possible_values = (set(possible_values).difference(three_by_three_values))
        return(list(possible_values))
            
    
    def is_row_solved(self, row):
        if sorted(self.sudoku[row]) == list(range(1, 10)):
            return True
        return False 
    
    def is_collumn_solved(self, collumn):
        collumn_values = []
        for i in range(9):
            collumn_values.append(self.sudoku[i][collumn])
        if sorted(collumn_values) == list(range(1, 10)):
            return True
        return False 
    
    def is_three_by_three_solved(self, square):
        three_by_three = self.get_three_by_three_from_square(square, True)
        if sorted(three_by_three.flatten()) == list(range(1, 10)):
            return True
        return False
    
    def is_invalid(self):
        # print("check invalid")
        dictionary = self.get_possible()
        for key in dictionary:
            if dictionary[key] == []:
                return True
        ## check if each row is invalid 
        for i in range(9):
            if self.is_row_solved(i):
                continue
            else:
                row_values = [value for value in self.sudoku[i] if value != 0]
                if (len(row_values) != len(set(row_values))):
                    return True
                
                
        for i in range(9):
            if self.is_collumn_solved(i):
                continue
            else:
                collumn_values = []
                for j in range(9):
                    if self.sudoku[j][i] != 0:
                        collumn_values.append(self.sudoku[j][i])
                if (len(collumn_values) != len(set(collumn_values))):
                    return True
                
        for i in range(9):
            if self.is_three_by_three_solved(i):
                continue
            else:
                three_by_three = self.get_three_by_three_from_square(i, True)
                three_by_three_values = [value for value in (three_by_three.flatten()) if value != 0]
                if (len(three_by_three_values) != len(set(three_by_three_values))):
                    return True
                
        return False
    
    def set_value(self, row, collumn, number):
#         if [row, collumn] not in self.empty_cells:
#             raise ValueError(f"{row} {collumn} is not empty so you cannot set a value there")    
        state = copy.deepcopy(self)
        state.empty_cells.remove([row, collumn])
        state.possible_values_for_square[row][collumn].remove(number)
        state.sudoku[row][collumn] = number
        state.possible_values_for_square = state.get_possible_values() 
        state.naked_pairs()
        # print(state.possible_values_for_square)
        singleton_squares = state.get_singletons()
        if (len(singleton_squares) != 0):
            row = singleton_squares[0][0]
            collumn = singleton_squares[0][1]
            number = state.possible_values_for_square[row][collumn][0]
            state = state.set_value(singleton_squares[0][0], singleton_squares[0][1], state.possible_values_for_square[row][collumn][0])
        return state
                
    def is_goal(self):
        for i in range(0, 9):
            row_solved = self.is_row_solved(i)
            collumn_solved = self.is_collumn_solved(i)
            square_solved = self.is_three_by_three_solved(i)
            
            if (row_solved == False or collumn_solved == False or square_solved == False):
                return False
        return True
        
    
            
    def get_possible(self):
        my_dict = {}
        for i in range(len(self.empty_cells)):
            row = self.empty_cells[i][0]
            collumn = self.empty_cells[i][1]
            key = (row, collumn)
            value = self.possible_values_for_square[row][collumn]
            my_dict[key] = value
        return my_dict
        
    def get_final_state(self):
        if self.is_goal():
            return self.sudoku
        else:
            return [[-1 for _ in range(1,9+1)] for _ in range(1, 9+1)]
        
                
    #returns squares that have no final values and only one possible value
    def get_singletons(self):
        singletons = [] 
        for i in range (len(self.empty_cells)):
            list = []
            row = self.empty_cells[i][0]
            collumn = self.empty_cells[i][1]
            if ((len(self.possible_values_for_square[row][collumn]))==1):
                singletons.append(self.empty_cells[i])
        return(singletons)
    

    def naked_pairs(self):
        ## check if any two squares in the same box, row , collumn have the same two values
        ## if they do that means those two values can only be in those two square in that box/row/collumn so remove it from other possible values

        for i in range(0,9):
            row_possible_values = self.possible_values_for_square[i]
            row_values = {}
            row_naked_pairs = {}
            for j in range(len(row_possible_values)):
                if len(row_possible_values[j]) == 2:
                    row_values[j] = row_possible_values[j]

            for key1 in row_values:
                for key2 in row_values:
                    if key1 != key2:
                        if row_values[key1] == row_values[key2]:
                            row_naked_pairs[(key1,key2)] = row_values[key1]

            for key in row_naked_pairs:
                location1 = key[0]
                location2 = key[1]
                values = row_naked_pairs[key]
                if len(values) > 1:
                    value1 = values[0]
                    value2 = values[1]
                    for index in range (0,9):
                        if ((index != location1) and (index != location2)):
                            if value1 in row_possible_values[index]:
                                if (len(row_possible_values[index]) > 1) and (row_possible_values[index] != [value1, value2]):
                                    row_possible_values[index].remove(value1)
                            if value2 in row_possible_values[index]:
                                if (len(row_possible_values[index]) > 1) and (row_possible_values[index] != [value1, value2]):
                                    row_possible_values[index].remove(value2)
            
            self.possible_values_for_square[i] = row_possible_values
            
            collumn_possible_values = []

            for row in range(9):
                collumn_possible_values.append(self.possible_values_for_square[row][i])
            collumn_values = {}
            collumn_naked_pairs = {}
            for j in range(len(collumn_possible_values)):
                if len(collumn_possible_values[j]) == 2:
                    collumn_values[j] = collumn_possible_values[j]
            for key1 in collumn_values:
                for key2 in collumn_values:
                    if key1 != key2:
                        if collumn_values[key1] == collumn_values[key2]:
                            collumn_naked_pairs[(key1,key2)] = collumn_values[key1]
            
            for key in collumn_naked_pairs:
                pair1 = key[0]
                pair2 = key[1]
                values = collumn_naked_pairs[key]
                if len(values) > 1:
                    value1 = values[0]
                    value2 = values[1]
                    for index in range (0,9):
                        if ((index != pair1) and (index != pair2)):
                            if value1 in collumn_possible_values[index]:
                                if (len(collumn_possible_values[index]) > 1) and (collumn_possible_values[index] != [value1, value2]):
                                    collumn_possible_values[index].remove(value1)
                            if value2 in collumn_possible_values[index]:
                                if (len(collumn_possible_values[index]) > 1) and (collumn_possible_values[index] != [value1, value2]):
                                    collumn_possible_values[index].remove(value2)
            
            for row in range(9):
                self.possible_values_for_square[row][i] = collumn_possible_values[row]
        

            square_possible_values = self.get_three_by_three_possible_values(i)
            square_values = {}
            square_naked_pairs = {}
            for j in range(len(square_possible_values)):
                if len(square_possible_values[j]) == 2:
                    square_values[j] = square_possible_values[j]
            for key1 in square_values:
                for key2 in square_values:
                    if key1 != key2:
                        if square_values[key1] == square_values[key2]:
                            square_naked_pairs[(key1,key2)] = square_values[key1]
            
            for key in square_naked_pairs:
                pair1 = key[0]
                pair2 = key[1]
                values = square_naked_pairs[key]
                if len(values) > 1:
                    value1 = values[0]
                    value2 = values[1]
                    for index in range (0,9):
                        if ((index != pair1) and (index != pair2)):
                            if value1 in square_possible_values[index]:
                                if (len(square_possible_values[index]) > 1) and (square_possible_values[index] != [value1, value2]):
                                    square_possible_values[index].remove(value1)
                            if value2 in square_possible_values[index]:
                                if (len(square_possible_values[index]) > 1) and (square_possible_values[index] != [value1, value2]):
                                    square_possible_values[index].remove(value2)

            rows_lower = self.get_three_by_three_from_square(i)[0]
            rows_upper = self.get_three_by_three_from_square(i)[1]
            collumns_lower = self.get_three_by_three_from_square(i)[2]
            collumns_upper = self.get_three_by_three_from_square(i)[3]
            count = 0
            for row in range (rows_lower, rows_upper):
                for collumn in range (collumns_lower, collumns_upper):
                    self.possible_values_for_square[row][collumn] = square_possible_values[count]
                    count += 1

            
           


            



"""
Solves a Sudoku puzzle and returns its unique solution.

Input
    sudoku : 9x9 numpy array
        Empty cells are designated by 0.

Output
    9x9 numpy array of integers
        It contains the solution, if there is one. If there is no solution, all array entries should be -1.
"""    
    

    ### YOUR CODE HERE
    
#     return solved_sudoku
# # YOUR CODE HERE


def check_validity(sudoku):
    dictionary = sudoku.get_possible()
    for key in dictionary:
        if dictionary[key] == []:
            return False
    return True

def pick_next_square(sudoku):

    dictionary = sudoku.get_possible()
    length = 10
    short_key = ()
    for key in dictionary:
        if len(dictionary[key]) < length:
            length = len(dictionary[key])
            short_key = key
    return([short_key[0],short_key[1]])



def order_values(sudoku, cell):
    values = sudoku.get_possible_values_for_square(cell[0], cell[1])
    value_dict = {}
    for value in values:
        count = 0
        for row in range (9):
            for collumn in range (9):
                for item in (sudoku.get_possible_values_for_square(row, collumn)):
                    if item == value:
                        count += 1
        value_dict[value] = count
    lst = []
    value_dict = dict(sorted(value_dict.items(), key=lambda item: item[1]))
    for key in value_dict:
        lst.append(key)
    
    return lst


def depth_first_search(sudoku_board):
        square = pick_next_square(sudoku_board)
        values = order_values(sudoku_board, square)
        for value in values:
            new_state = sudoku_board.set_value(square[0], square[1], value)
            if new_state.is_goal():
                return new_state
            if not new_state.is_invalid():
                deep_state = depth_first_search(new_state)
                if not deep_state.is_invalid() and deep_state.is_goal():
                    return deep_state
        return sudoku_board
            



def sudoku_solver(sudoku):
    UnsolvedSudoku = unsolved_sudoku(sudoku)
    solved_sudoku = depth_first_search(UnsolvedSudoku)
    return(np.array(solved_sudoku.get_final_state()))


sudokus = np.load(f"/Users/simranbarve/Documents/UNI/Y1/AI/sudoku/data/hard_puzzle.npy")
solutions = np.load(f"/Users/simranbarve/Documents/UNI/Y1/AI/sudoku/data/hard_solution.npy")


SKIP_TESTS = False

def tests():
    import time
    difficulties = ['hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")
        
        sudokus = np.load(f"/Users/simranbarve/Documents/UNI/Y1/AI/sudoku/data/{difficulty}_puzzle.npy")
        solutions = np.load(f"/Users/simranbarve/Documents/UNI/Y1/AI/sudoku/data/{difficulty}_solution.npy")
        
        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)
            
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()
            
            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)
            
            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])
            
            print("This sudoku took", end_time-start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break
            
if not SKIP_TESTS:
    tests()

