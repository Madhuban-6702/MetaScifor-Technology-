import tkinter as tk

class TicTacToe:
    def __init__(self, window):
        self.window = window
        self.window.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
    
    def create_board(self):
        for r in range(3):
            for c in range(3):
                button = tk.Button(self.window, text="", width=5, height=2, command=lambda row=r, col=c: self.make_move(row, col))
                button.grid(row=r, column=c)
                self.board[r][c] = button
    
    def make_move(self, row, col):
        button = self.board[row][col]
        if button["text"] == "" and not self.check_winner():
            button["text"] = self.current_player  
            if not self.check_winner():
                self.current_player = "O" if self.current_player == "X" else "X"
            else:
                self.display_winner()
    
    def check_winner(self):
        lines = [# Row
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],

            # Column
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],

            # Diagonal
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[0][2], self.board[1][1], self.board[2][0]]
        ]

        for line in lines:
            if all(button["text"] == self.current_player and button["text"] != "" for button in line):
                return True
        return False
    
    def display_winner(self):
        winner_text = f"Player {self.current_player} wins!"
        winner_label = tk.Label(self.window, text=winner_text, font=("Arial", 16))
        winner_label.grid(row=3, column=0, columnspan=3)
        for r in range(3):
            for c in range(3):
                self.board[r][c]["state"] = "disabled" 

if __name__ == "__main__":
    window = tk.Tk()
    game = TicTacToe(window)
    window.mainloop()
