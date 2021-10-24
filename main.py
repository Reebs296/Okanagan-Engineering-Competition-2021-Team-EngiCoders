import random
#import gui library
import tkinter as tk

#create tile class that is either a stone or a bomb

class Tile:
    #initialize the tile
    def __init__(self, x, y, bomb):
        self.x = x
        self.y = y
        self.bomb = bomb
        self.bombnum = 0
        self.revealed = False
        self.flagged = False

#create board class that holds array of tiles 
class Board:
    #initialize the board with x and y size and number of bombs
    def __init__(self, x, y, bombs):
        self.x = x
        self.y = y
        self.bombs = bombs
        self.tiles = []
    #add Tile objects to the tiles array and randomly place bombs until the number of bombs is reached
    def add_tiles(self):
        for i in range(self.x):
            for j in range(self.y):
                self.tiles.append(Tile(i, j, False))
        for i in range(self.bombs):
            rand_x = random.randint(0, self.x - 1)
            rand_y = random.randint(0, self.y - 1)
            self.tiles[rand_x + rand_y * self.x].bomb = True

    #is valid checks if the tile is within the bounds of the board
    def is_valid(self, x, y):
        if x < 0 or x >= self.x:
            return False
        if y < 0 or y >= self.y:
            return False
        return True
    
    #count the number of bombs adjacent to the tile
    def count_adjacent_bombs(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.is_valid(x + i, y + j):
                    if self.tiles[(x + i) + (y + j) * self.x].bomb == True:
                        count += 1
        return count

    #loop through the tiles array and count the number of bombs adjacent to each tile
    def count_bombs(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.tiles[i + j * self.x].bomb == False:
                    #set bomnum equal to the amount of bombs around the tile 
                    self.tiles[i + j * self.x].bombnum = self.count_adjacent_bombs(i, j)
                else:
                    self.tiles[i + j * self.x].bombnum = -1

    def clicked_tile(self, x, y):
        #if the tile is a bomb, game over
        if self.tiles[x + y * self.x].bomb == True:
            return False
        #if the tile is not a bomb, reveal the tile
        else:
            self.tiles[x + y * self.x].revealed = True
            #if the tile is not a bomb and has no adjacent bombs, reveal all adjacent tiles
            if self.tiles[x + y * self.x].bombnum == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if self.is_valid(x + i, y + j):
                            if self.tiles[(x + i) + (y + j) * self.x].revealed == False:
                                self.clicked_tile(x + i, y + j)
            return True

    def print_board(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.tiles[i + j * self.x].revealed == False:
                    print("[ ]", end = "")

                #if the tile is a bomb and is revealed, print a bomb
                elif self.tiles[i + j * self.x].bomb == True and self.tiles[i + j * self.x].revealed == True:
                    print("[B]", end = "")

                #if the tile is flagged, print a flag
                elif self.tiles[i + j * self.x].flagged == True:
                    print("[F]", end = "")
                else:
                    print("[" + str(self.tiles[i + j * self.x].bombnum) + "]", end = "")

            
            print("")
        print("")

        #check if the game is over
        #if all unrevealed tiles are bombs, you win
    def check_win(self):
        count = 0
        for i in range(self.x):
            for j in range(self.y):
                if self.tiles[i + j * self.x].revealed == False:
                    count += 1
        if count == self.bombs:
            return True
        else:
            return False

#create board object
board = Board(10, 10, 10)

#difficulty buttons clicked function based on the bomb and size of the board
def difficulty_clicked(x, y, bombs, popup):
    board.x = x
    board.y = y
    board.bombs = bombs
    board.add_tiles()  
    board.count_bombs()
    board.print_board()
    popup.destroy()

def flag_tile(x, y):
    board.tiles[x + y * board.x].flagged = True

def clicked_tile(x, y, button):
    #if the tile is not revealed and not flagged, reveal the tile
    if board.tiles[x + y * board.x].revealed == False and board.tiles[x + y * board.x].flagged == False:
        #if the tile is a bomb, game over
        if board.tiles[x + y * board.x].bomb == True:  
            board.tiles[x + y * board.x].revealed = True
            board.print_board()
            print("Game over")
            #popup window to show game over
            popup = tk.Tk()
            popup.title("Game Over")
            popup.geometry("200x100")
            #create label to show game over
            label = tk.Label(popup, text = "Game Over")
            label.pack()
            #create button to restart the game
            button = tk.Button(popup, text = "Exit", command = lambda: exit())
            button.pack()
            popup.mainloop()

            return False
        #if the tile is not a bomb, reveal the tile
        else:
            board.tiles[x + y * board.x].revealed = True
            #if the tile is not a bomb and has no adjacent bombs, reveal all adjacent tiles and set the button to the number of adjacent bombs
            if board.tiles[x + y * board.x].bombnum == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if board.is_valid(x + i, y + j):
                            if board.tiles[(x + i) + (y + j) * board.x].revealed == False:
                                clicked_tile(x + i, y + j, button)
            board.print_board()
            return True

#create main function
def main():
    
    while True:      
        #create a popup window with a difficulty button for each difficulty
        popup = tk.Tk()
        popup.title("Difficulty")
        popup.geometry("200x200")
        #create a button for each difficulty
        easy_button = tk.Button(popup, text = "Easy", command = lambda: difficulty_clicked(9, 9, 10, popup))
        medium_button = tk.Button(popup, text = "Medium", command = lambda: difficulty_clicked(16, 16, 40, popup))
        hard_button = tk.Button(popup, text = "Hard", command = lambda: difficulty_clicked(16, 30, 99, popup))
        #add the buttons to the popup window
        easy_button.pack()
        medium_button.pack()
        hard_button.pack()
        #show the popup window
        popup.mainloop()
        #destroy the popup window

        #create a game window
        game_window = tk.Tk()
        #set the game window title to Minesweeper
        game_window.title("Minesweeper")
        #set the game window size to 500x500
        game_window.geometry("500x500")
        #create a grid of buttons based on the board size
        for i in range(board.x):
            for j in range(board.y):
                #create a button for each tile that you can right click on to flag the tile and left click to reveal the tile
                button = tk.Button(game_window, text = "", command = lambda x = i, y = j: clicked_tile(x, y, button))
                button.bind("<Button-1>", lambda event, x = i, y = j: clicked_tile(x, y, button))
                button.bind("<Button-3>", lambda event, x = i, y = j: flag_tile(x, y, button))
                #flag the tile by right clicking on it
                button.grid(row = i, column = j)

        #if all unreavealed tiles are bombs, you win
        if board.check_win() == True:
            print("You win")
            #popup window to show you win
            popup = tk.Tk()
            popup.title("You Win")
            popup.geometry("200x100")
            #create label to show you win
            label = tk.Label(popup, text = "You Win")
            label.pack()
            #create button to restart the game
            button = tk.Button(popup, text = "Exit", command = lambda: exit())
            button.pack()
            popup.mainloop()
            #destroy the popup window
            popup.destroy()
            #destroy the game window
            game_window.destroy()
            #restart the game
            main() 
        
        game_window.mainloop()

if __name__ == "__main__":
    main()


    
