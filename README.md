# Sudoku

#### Introduction

The aim of this task was to create an agent which was able that was able to solve 9x9 sudoku puzzles. I did this using a backtracking depth first search and constraint propagation. This initial algorithm worked but struggled to solve the hard puzzles within the 20 second time limit, so I added a naked pairs function which is a technique used in sudoku solving. 

#### Initial Algorithm

I used the eight queens revisited algorithm to help me when implementing my depth first search as well as the constraint propagation. The backtracking algorithm recursively tries every possible value for each square in the sudoku. 
I used constraint propagation by having a list of all the possible values for each square in the sudoku which then got updated each time a value was set this helped reduce the number of values the algorithm tried. 
When I tested this basic algorithm it struggled to complete any of the hard sudokus within 60 seconds. Therefore, I implemented more functions to decrease the time th ealgorithm took. I did this by changing the order_values function so that it chose th esquare with the least poccible values and ordered them based on how many other squares it was a possible value for. 

When this had been implemented the algorithm solved the hard sudokus between 20 to 40 seconds however this wasn't efficient enough so I did some research on techniques used to incresae speed and efficiency in sudoku solving and came across naked pairs which is a sudoku solving technique. 

#### Naked Pairs

Naked Pairs refers to when two squares in a row, collumn or block have the exact same two numbers as possible values 

![Alt text](https://www.learn-sudoku.com/images/naked_pair1.gif)

In the image you can see that two squares just have "2" and "3" as possible values, they are nake pairs. This means that two and three have to go in either of those square so they aren't possible values for any otehr square in that block so it can be removed from the other squares' possible values. 

![Alt text](https://www.learn-sudoku.com/images/naked_pair2.gif)

This can also be done with rows and collumns, reducing the number of possible values and therefore reducing the time taken. 

I implemented this so that the other possible values were removed when a naked pairs was identified and then when the possible values were set the naked pairs were identified and other possible valeus were removed and this process was repeated everytime a new value was set. 

#### References 

Sudoku - Naked Pairs n.d., www.learn-sudoku.com, viewed 3 January 2023, <https://www.learn-sudoku.com/naked-pairs.html>.