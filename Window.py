import random
import sys
import time
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self,width,height):
        self.root = Tk()
        self.root.title("Maze")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(height=height,width=width)
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()


    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()



    def close(self):
        self.running = False



class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y



class Line:
    def __init__(self,point1,point2):
        self.start = point1
        self.end = point2
    
    def draw(self,canvas, color):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill = color, width = 2)




class cell:
    def __init__(self, win =None, has_left_wall:bool = True, has_right_wall:bool = True , has_top_wall:bool = True , has_bottom_wall:bool = True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._Win = win
        self.visited = False

    def break_entrance(self):
        self.has_top_wall = False
    
    def break_exit(self):
        self.has_bottom_wall = False

    def draw(self, x1, y1, x2, y2):
        if self._Win is None:
            return
        
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        if self.has_left_wall:
            self._Win.canvas.create_line(self._x1, self._y1, self._x1, self._y2)
        else:
            self._Win.canvas.create_line(self._x1, self._y1, self._x1, self._y2,fill = "white")

        if self.has_right_wall:
            self._Win.canvas.create_line(self._x2, self._y1, self._x2, self._y2)
        else:
             self._Win.canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill = "white")

        if self.has_top_wall:
            self._Win.canvas.create_line(self._x1, self._y1, self._x2, self._y1)
        else:
            self._Win.canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill = "white")

        if self.has_bottom_wall:
             self._Win.canvas.create_line(self._x1, self._y2, self._x2, self._y2)
        else:
            self._Win.canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill = "white")
        

    def draw_move(self, to_cell, undo = False):
        color = "red"
        if undo:
            color = "grey"
        center_x= (self._x2 - self._x1)/2
        center_y = (self._y2 - self._y1)/2
        to_center_x = (to_cell._x2 - to_cell._x1)/2
        to_center_y = (to_cell._y2 - to_cell._y1)/2
        self._Win.canvas.create_line(self._x1 + center_x, self._y1 + center_y, 
                                     to_cell._x1 + to_center_x, to_cell._y1 + to_center_y, 
                                     fill = color, width = 2)
        


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed = None
    ):
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._Break_walls_R(0,0)
        self._reset_cells_visited()


    def _create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(cell(self.win))
            self._cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cells(i,j)

    def _draw_cells(self,i,j):
        if self.win is None:
            return
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw(x1,y1,x2,y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        if self._cells[0][0].has_top_wall == True:
            self._cells[0][0].break_entrance()
            self._draw_cells(0,0)
        if self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall == True:
            self._cells[self.num_cols -1][self.num_rows -1].break_exit()
            self._draw_cells(self.num_cols -1,self.num_rows -1)


    def _Break_walls_R(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            if i > 0 and not self._cells[i-1][j].visited:
                next_index_list.append((i-1,j))
            if i < self.num_cols -1 and not self._cells[i+1][j].visited:
                next_index_list.append((i+1,j))
            if j > 0 and not self._cells[i][j-1].visited:
                next_index_list.append((i,j-1))
            if j < self.num_rows -1 and not self._cells[i][j+1].visited:
                next_index_list.append((i,j+1))

            if len(next_index_list) == 0:
                self._draw_cells(i,j)
                return
            
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            if next_index[0] == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False


            if next_index[0] == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False


            if next_index[1] == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False

            if next_index[0] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i+1][j].has_bottom_wall = False

            self._Break_walls_R(next_index[0],next_index[1])

        


    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self,i,j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[self.num_cols-1][self.num_rows-1]:
            return True
    
        if j > 0 and self._cells[i][j].has_top_wall == False and not self._cells[i][j-1].visited:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i,j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1],undo = True)

        if i < self.num_cols-1 and self._cells[i][j].has_right_wall == False and not self._cells[i+1][j].visited:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1,j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j],undo = True)

        if j < self.num_rows-1 and self._cells[i][j].has_bottom_wall == False and not self._cells[i][j+1].visited:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i,j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1],undo = True)

        if i > 0 and self._cells[i][j].has_left_wall == False and not self._cells[i-1][j].visited:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1,j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j],undo = True)
        
        return False
               

                



def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)
    print("maze created")
    is_solveable = maze.solve()
    if not is_solveable:
        print("maze can not be solved!")
    else:
        print("maze solved!")
    win.wait_for_close()


main()