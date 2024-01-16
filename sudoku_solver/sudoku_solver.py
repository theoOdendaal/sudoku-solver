import numpy as np
from collections import Counter

SIZE = 3

class Matrix:
    
    def __init__(self, matrix : np.ndarray):
        self.matrix = matrix
        self.ix = 0
        self.iy = 0
        self.get_potential_numbers()
        self.iterations = 0
        
    def get_potential_numbers(self):
    # Determine all potential values for each unknown element.
    
        self.potential_array = np.empty((9, 9), dtype=object)
        for self.iy in range(0, SIZE**2):
            for self.ix in range(0, SIZE**2):
                temp = []
                for i in range(1, SIZE**2 + 1):        
                    if self.matrix[self.iy, self.ix] == 0:
                        self.matrix[self.iy, self.ix] = i
                        if self.check_matrix():
                            temp.append(i)
                        self.matrix[self.iy, self.ix] = 0
                #else:
                #    temp.append(self.matrix[self.iy, self.ix])

                self.potential_array[self.iy, self.ix] = temp
        self.yi = 0
        self.xi = 0

    def next_unknown(self, back_track : bool = False):
        # Finds the next unknown value
        self.iterations += 1
        
        if back_track:
            while True:
                self.xi -= 1
                if self.xi < 0:
                    self.yi -= 1
                    self.xi = SIZE**2 - 1
                
                if len(self.potential_array[self.yi, self.xi]) != 0 or (self.yi == 0 and self.xi == 0):
                    break
        
        else:
            while True:
                self.xi += 1
                if self.xi > SIZE**2 - 1:
                    self.yi += 1
                    self.xi = 0
                
                self.yi = min(self.yi, SIZE**2 - 1)
                self.xi = min(self.xi, SIZE**2 - 1)
                    
                if len(self.potential_array[self.yi, self.xi]) != 0 or (self.yi == SIZE**2 -1 and self.xi == SIZE**2 -1):
                    break

        print('#' * (self.xi + self.yi * 9))
        #print(f'{self.yi} : {self.xi}')
 
    def check_block(self):
        # Evaluate blocks.
        for iy, iiy in zip(range(0, SIZE**2 - SIZE + 1, SIZE), range(SIZE - 1, SIZE**2, SIZE)):
            for ix, iix in zip(range(0, SIZE **2, SIZE), range(SIZE - 1, SIZE**2, SIZE)):
                if max(Counter([k for k in self.matrix[iy : iiy + 1, ix : iix + 1].flatten() if k != 0]).values()) > 1:
                   return False
            
        return True

    def check_horizontal(self):
        # Evaluate rows.
        for y in self.matrix:
            if max(Counter([k for k in y if k != 0]).values()) > 1:
                return False
        
        return True

    def check_vertical(self):
        # Evaluate columns.
        for ix in range(0, SIZE**2):
            if max (Counter([k for k in [self.matrix[iy, ix] for iy in range(0, SIZE**2)] if k != 0]).values()) > 1:
                return False
        
        return True

    def check_matrix(self):
        # y = columns - first iteration.
        # x = rows - second iteration.
        if self.check_block() and self.check_horizontal() and self.check_vertical():
            return True
    
        return False

    def solve(self):
        
        self.yi = 0
        self.xi = -1
        self.next_unknown()
        
        while self.yi < (SIZE**2):
            while self.xi < (SIZE**2):
                
                # End condition
                if self.yi == SIZE**2-1 and self.xi == SIZE**2-1 and len(self.potential_array[self.yi, self.xi]) == 0:
                    return self.matrix

                # If only one potential value exist, update the matrix.
                if len(self.potential_array[self.yi, self.xi]) == 1:
                    self.matrix[self.yi, self.xi] = self.potential_array[self.yi, self.xi][0]
                    self.potential_array[self.yi, self.xi] = []
                    self.next_unknown()
                    continue
                
                # Finds index of current potential value.
                if self.matrix[self.yi, self.xi] == 0:
                    index = 0
                else:
                    index = (self.potential_array[self.yi, self.xi].index(self.matrix[self.yi, self.xi])) + 1

                # If index exceeds the length of potential values, reset index and backtrack.
                if index >= len(self.potential_array[self.yi, self.xi]):
                    self.matrix[self.yi, self.xi] = 0
                    self.next_unknown(True)
                    continue
                    
                
                for i in range(index, len(self.potential_array[self.yi, self.xi])):
                    self.matrix[self.yi, self.xi] = self.potential_array[self.yi, self.xi][index]
                    if self.check_matrix():
                        self.next_unknown()
                        break
                    else:
                        if i == (len(self.potential_array[self.yi, self.xi])):
                            self.matrix[self.yi, self.xi] = 0
                            self.next_unknown(True)
                            break

        return self.matrix
                

if __name__ == '__main__':
    
    matrix = np.array([ [0,0,0,8,0,0,0,0,9],
                        [0,1,9,0,0,5,8,3,0],
                        [0,4,3,0,1,0,0,0,7],
                        [4,0,0,1,5,0,0,0,3],
                        [0,0,2,7,0,4,0,1,0],
                        [0,8,0,0,9,0,6,0,0],
                        [0,7,0,0,0,6,3,0,0],
                        [0,3,0,0,7,0,0,8,0],
                        [9,0,4,5,0,0,0,0,1]])
    
    matrix = np.array([ [8,4,0,0,0,3,0,0,6],
                        [0,2,0,9,0,0,0,1,5],
                        [0,0,0,0,8,0,0,0,0],
                        [1,0,0,0,0,0,0,4,0],
                        [0,0,8,0,5,0,9,0,0],
                        [0,3,0,0,0,0,0,0,2],
                        [0,0,0,0,7,0,0,0,0],
                        [6,9,0,0,0,4,0,8,0],
                        [3,0,0,8,0,0,0,2,7]])
        

    
    #matrix[0,0] = 2
    #matrix[0,1] = 5
    print(matrix)
    print('\n')
    sudo = Matrix(matrix)
    print(sudo.solve())
    print(sudo.check_matrix())
    print(f'Solved in {sudo.iterations} iterations.')
