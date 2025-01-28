import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Generate Python code for a Minesweeper game.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```python\nimport random\nimport os\n\nclass Minesweeper:\n    def __init__(self, rows, cols, mines):\n        self.rows = rows\n        self.cols = cols\n        self.mines = mines\n        self.board = [['-' for _ in range(cols)] for _ in range(rows)]\n        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]\n        self.flags = [[False for _ in range(cols)] for _ in range(rows)]\n        self.game_over = False\n\n    def plant_mines(self, start_row, start_col):\n        mines_planted = 0\n        while mines_planted < self.mines:\n            row = random.randint(0, self.rows - 1)\n            col = random.randint(0, self.cols - 1)\n            if self.board[row][col] != '*' and (row != start_row or col != start_col):  # Avoid starting position\n                self.board[row][col] = '*'\n                mines_planted += 1\n\n    def count_adjacent_mines(self, row, col):\n        count = 0\n        for i in range(max(0, row - 1), min(self.rows, row + 2)):\n            for j in range(max(0, col - 1), min(self.cols, col + 2)):\n                if self.board[i][j] == '*':\n                    count += 1\n        return count\n\n    def reveal_cell(self, row, col):\n\n        if self.game_over:\n            return\n        \n        if self.flags[row][col]:\n            return\n\n        if self.revealed[row][col]:\n            return\n\n        self.revealed[row][col] = True\n\n        if self.board[row][col] == '*':\n            self.game_over = True\n            print(\"Game Over! You hit a mine.\")\n            self.show_board(reveal_all=True)\n            return\n\n        adjacent_mines = self.count_adjacent_mines(row, col)\n        self.board[row][col] = adjacent_mines if adjacent_mines > 0 else ' '\n\n\n        if adjacent_mines == 0:  # Recursively reveal empty cells\n            for i in range(max(0, row - 1), min(self.rows, row + 2)):\n                for j in range(max(0, col - 1), min(self.cols, col + 2)):\n                    if not self.revealed[i][j]:\n                        self.reveal_cell(i, j)\n\n\n    def toggle_flag(self, row, col):\n         if not self.revealed[row][col]:\n              self.flags[row][col] = not self.flags[row][col]\n       \n\n    def check_win(self):\n        for row in range(self.rows):\n            for col in range(self.cols):\n                if self.board[row][col] != '*' and not self.revealed[row][col]:\n                    return False\n        return True\n\n\n\n    def show_board(self, reveal_all=False):\n        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console\n        print(\"  \" + \"\".join(str(i) for i in range(self.cols)))  # Column numbers\n        for row in range(self.rows):\n            print(str(row) + \" \", end=\"\")  # Row numbers\n            for col in range(self.cols):\n                if reveal_all or self.revealed[row][col]:\n                     print(self.board[row][col] if not self.flags[row][col] else \"F\", end=\" \")\n                elif self.flags[row][col]:\n                    print(\"F\", end=\" \") # show flag\n                else:\n                    print(\"-\", end=\" \")\n            print()\n\n    def play(self):\n\n        while not self.game_over:\n\n            self.show_board()\n\n            move = input(\"Enter move (row,col,action - r for reveal, f for flag/unflag): \").split(',')\n            if len(move) != 3:  # Validate input\n                print(\"Invalid input format.\")\n                continue\n\n\n            try:\n                row, col = int(move[0]), int(move[1])\n                action = move[2].lower().strip()\n\n\n            except ValueError:\n                 print(\"Invalid input. Row and column must be integers.\")\n                 continue\n\n\n            if row < 0 or row >= self.rows or col < 0 or col >= self.cols:\n                print(\"Invalid row or column.\")\n                continue\n\n            if action == 'r':\n                if self.board[row][col] == '-' and all(self.revealed[i] == [False]*self.cols for i in range(self.rows)):\n                      self.plant_mines(row, col)\n                      self.reveal_cell(row, col) # Plant mines after first reveal\n\n                elif not self.flags[row][col]:\n                      self.reveal_cell(row, col) # Plant mines after first reveal\n                \n            elif action == 'f':\n                self.toggle_flag(row, col)\n\n\n            if self.check_win():\n                self.game_over = True\n                self.show_board(reveal_all=True)\n                print(\"Congratulations! You won!\")\n\n\n# Example usage:\nrows, cols, mines = 10, 10, 10\ngame = Minesweeper(rows, cols, mines)\ngame.play()\n\n```\n\n\nKey improvements:\n\n* **Clearer Game Over:**  Improved game over handling and display.\n* **Input Validation:**  Robust input validation prevents crashes from incorrect user input.\n* **Flag Toggling:** Added flag toggling functionality (using 'f' as the action).\n* **First Click Safe:** Ensures the first click is never a mine.\n* **Win Condition Check:**  Checks and declares a win when all non-mine cells are revealed.\n* **Clear Console:** Clears the console on each turn for a cleaner display.\n* **Comments and Formatting:** Added more comments and improved formatting for better readability.\n\n\n\nThis improved version provides a more complete and robust Minesweeper experience.  Let me know if you have any other features you'd like to add!",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)
