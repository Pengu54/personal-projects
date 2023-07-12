import gui
import random

SNAKE_COLOUR = "#00FF00"
FRUIT_COLOUR = "#FF0000"
GRID_SIZE = [20, 20] #x, y
CELL_X = gui.grid_canvas.winfo_width() / GRID_SIZE[0]
CELL_Y = gui.grid_canvas.winfo_height() / GRID_SIZE[1]
INITIAL_SNAKE_SIZE = 3

class Snake():

    def __init__(self):
        self.DIR_OFFSETS = {
            "down": [0, 1],
            "up": [0, -1],
            "right": [1, 0],
            "left": [-1, 0]
        }
        
        self.direction = "down"
        self.grown = False
        self.moving = False
        self.cell_coords = list()

        #render the snake initially
        self.rendered_cells = list()
        for i in range(INITIAL_SNAKE_SIZE):
            self.cell_coords.append([0, i])
            cell = gui.grid_canvas.create_rectangle(0, CELL_Y * i, CELL_X, CELL_Y * (i+1), fill=SNAKE_COLOUR)
            self.rendered_cells.append(cell) 

        gui.root.bind("<Key>", self.change_direction)
    
    def change_direction(self, event):
        if not self.moving:
            if event.keysym == "s":
                self.direction = "down"
            elif event.keysym == "w":
                self.direction = "up"
            elif event.keysym == "d":
                self.direction = "right"
            elif event.keysym == "a":
                self.direction = "left"

    def render(self):
        if not self.grown:
            gui.grid_canvas.delete(self.rendered_cells[0]) #del last rendered cell
            del self.rendered_cells[0]
        else:
            self.grown = False

        head_x = self.cell_coords[-1][0]
        head_y = self.cell_coords[-1][1]
        new_head = gui.grid_canvas.create_rectangle(CELL_X * head_x, CELL_Y * head_y, CELL_X * (head_x+1), CELL_Y * (head_y+1), fill=SNAKE_COLOUR)
        self.rendered_cells.append(new_head)# ^ new rendered cell front of head pos
        
    def move(self):
        self.moving = True
        offset = self.DIR_OFFSETS[self.direction]
        head_coords = self.cell_coords[-1]
        head_x = head_coords[0] + offset[0]
        head_y = head_coords[1] + offset[1]

        self.cell_coords.append([head_x, head_y])
        del self.cell_coords[0]
        self.moving = False
    
    def grow(self):
        offset = self.DIR_OFFSETS[self.direction]
        tail_coords = self.cell_coords[0]
        new_tail_coords = [tail_coords[0] - offset[0], tail_coords[1] - offset[1]] #subtract since going back
        self.cell_coords.insert(0, new_tail_coords)

        self.grown = True

    def check_collisions(self, fruit_coords):
        #on fruit
        head_coords = self.cell_coords[-1]
        if head_coords == fruit_coords:
            return True, "fruit collision"
        #out of bounds
        elif (head_coords[0] > (GRID_SIZE[0]-1) or head_coords[0] < 0): #x
            return True, "out of bounds"
        elif  (head_coords[1] > (GRID_SIZE[1]-1) or head_coords[1] < 0): #y
            return True, "out of bounds"
        #on snake body
        elif head_coords in self.cell_coords[:-1]:
            return True, "snake collision" 
        else:
            return False


class Fruit():

    def __init__(self):
        self.coords = list()
        self.rendered_fruit = None

        self.spawn([[0, i] for i in range(INITIAL_SNAKE_SIZE)])
        self.render()

    def spawn(self, excluded_snake_coords):
        rand_x = random.randint(0, GRID_SIZE[0]-1)
        rand_y = random.randint(0, GRID_SIZE[1]-1)
        
        if [rand_x, rand_y] in excluded_snake_coords:
            while [rand_x, rand_y] in excluded_snake_coords:
                rand_x = random.randint(0, GRID_SIZE[0]-1)
                rand_y = random.randint(0, GRID_SIZE[1]-1)
        
        self.coords.insert(0, rand_x)
        self.coords.insert(1, rand_y)

    def render(self):
        fruit_x = self.coords[0]
        fruit_y = self.coords[1]
        self.rendered_fruit = gui.grid_canvas.create_oval(CELL_X * fruit_x, CELL_Y * fruit_y, CELL_X * (fruit_x+1), CELL_Y * (fruit_y+1), fill=FRUIT_COLOUR)
    
    def delete(self):
        self.coords.clear()

        gui.grid_canvas.delete(self.rendered_fruit)
        del self.rendered_fruit

class Game():

    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.game_state = "running"
        self.points = 0

    def pause(self):
        if self.game_state == "running":
            self.game_state = "paused"
            gui.label.configure(text="GAME PAUSED")
            gui.restart_button.configure(state="normal")
            gui.settings_button.configure(state="normal")
        
        elif self.game_state == "paused":
            self.game_state = "running"
            gui.label.configure(text=str(self.points))
            gui.restart_button.configure(state="disabled")
            gui.settings_button.configure(state="disabled")
            self.main()

    def restart(self):
        del self.snake
        del self.fruit
        gui.grid_canvas.delete("all")

        self.snake = Snake()
        self.fruit = Fruit()
        self.game_state = "running"
        self.points = 0
        
        gui.label.configure(text="0")
        gui.restart_button.configure(state="disabled")
        gui.pause_button.configure(state="normal")
        gui.settings_button.configure(state="disabled")

        self.main()

    def main(self):
            if self.game_state == "paused":
                return

            self.snake.move()
            collision = self.snake.check_collisions(self.fruit.coords)
            
            if collision == False:
                self.snake.render()
                gui.root.after(100, self.main)
            else:
                if collision[1] == "fruit collision":
                    self.fruit.delete()
                    self.snake.grow()
                    self.snake.render()
                    self.fruit.spawn(self.snake.cell_coords)
                    self.fruit.render()

                    self.points += 1
                    gui.label.configure(text=str(self.points))
                    gui.root.after(100, self.main)
                
                elif collision[1] == "out of bounds" or collision[1] == "snake collision":
                    self.game_state = "finished"
                    gui.label.configure(text="GAME OVER")
                    gui.restart_button.configure(state="normal")
                    gui.pause_button.configure(state="disabled")
                    gui.settings_button.configure(state="normal")

game = Game()

#button events
gui.restart_button.configure(command= game.restart)
gui.pause_button.configure(command= game.pause)

game.main()
gui.root.mainloop()