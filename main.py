import tkinter as tk
import random
from tkinter import messagebox
#Salah Eldin Qeadan - 211411368

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for x in range(9):
        if board[x][col] == num:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + startRow][j + startCol] == num:
                return False
    return True


def validate_input(P):
    # Allow empty input to enable clearing the cell
    if P == "":
        return True
    # Check if the input is a single digit between 1 and 9
    elif P.isdigit() and 1 <= int(P) <= 9:
        return True
    else:
        return False
def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def generate_puzzle(board, holes=40):
    solve_sudoku(board)  # First solve a complete board
    while holes > 0:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if board[i][j] != 0:
            board[i][j] = 0
            holes -= 1
    return board


root = tk.Tk()
root.title("Sudoku Puzzle")
root.configure(bg='#f0f0f0')  # Global background color

# Register the validation command
vcmd = (root.register(validate_input), '%P')

def create_grid(frame):
    entries = {}
    for row in range(9):
        for col in range(9):
            entry = tk.Entry(frame, width=2, font=('Courier', 24, 'bold'), justify='center',
                             borderwidth=2, relief='ridge', validate='key', validatecommand=vcmd)
            entry.grid(row=row, column=col, sticky='nsew', padx=1, pady=1, ipady=5)
            if (row // 3 + col // 3) % 2 == 0:
                entry.config(bg='#dddddd')  # Alternate subgrid color
            else:
                entry.config(bg='light grey')  # Default cell color
            entries[(row, col)] = entry
    return entries

def populate_grid(puzzle, entries):
    for row in range(9):
        for col in range(9):
            entries[(row, col)].delete(0, tk.END)
            entries[(row, col)].config(state='normal')
            if puzzle[row][col] != 0:
                entries[(row, col)].insert(0, puzzle[row][col])
                entries[(row, col)].config(state='readonly', readonlybackground='#e0e0e0', fg='black')

def clear_entries(entries):
    for entry in entries.values():
        entry.delete(0, tk.END)
        entry.config(state='normal', bg='light grey')

def get_board_from_entries(entries):
    board = []
    for row in range(9):
        current_row = []
        for col in range(9):
            entry_value = entries[(row, col)].get()
            if entry_value.isdigit():
                current_row.append(int(entry_value))
            else:
                current_row.append(0)
        board.append(current_row)
    return board


def check_no_duplicates(section):
    """Check if a section (row, column, or subgrid) contains no duplicates, excluding zeros."""
    numbers = [num for num in section if num != 0]
    return len(numbers) == len(set(numbers))

def simulate_zkp_verify(entries):
    board = get_board_from_entries(entries)
    packets = []

    for i in range(9):
        row_packet = [board[i][j] for j in range(9) if board[i][j] != 0]
        packets.append(row_packet)
        col_packet = [board[j][i] for j in range(9) if board[j][i] != 0]
        packets.append(col_packet)

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid_packet = [board[x][y] for x in range(i, i+3) for y in range(j, j+3) if board[x][y] != 0]
            packets.append(subgrid_packet)

    for i, packet in enumerate(packets):
        print(f"Packet {i+1}: {packet}")
        if not check_no_duplicates(packet):
            messagebox.showerror("ZKP Verification", "The puzzle does not adhere to Sudoku rules.")
            return

    messagebox.showinfo("ZKP Verification", "The puzzle adheres to Sudoku rules.")

def generate_and_populate(entries):
    new_board = [[0 for _ in range(9)] for _ in range(9)]
    puzzle = generate_puzzle(new_board)
    populate_grid(puzzle, entries)

frame = tk.Frame(root, bg='#f0f0f0')
frame.pack(pady=10, expand=True, fill='both')

entries = create_grid(frame)

# Buttons
clear_button = tk.Button(root, text='Clear', command=lambda: clear_entries(entries), bg='#ffcccc', fg='black')
clear_button.pack(side='left', padx=(10, 5))

check_button = tk.Button(root, text='Verify (ZKP)', command=lambda: simulate_zkp_verify(entries), bg='#ccffcc', fg='black')
check_button.pack(side='right', padx=(5, 10))

generate_button = tk.Button(root, text="Generate New Puzzle", command=lambda: generate_and_populate(entries), bg='#ccccff', fg='black')
generate_button.pack(side='bottom', pady=(10, 0))

# Generate the initial puzzle
generate_and_populate(entries)

root.mainloop()