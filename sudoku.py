"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys


ROW = "ABCDEFGHI"
COL = "123456789"
grids = [r + c for r in ROW for c in COL]


def get_group(row, col):
    """Get the group of grids in the same row, col, and 3x3 box"""
    col_group = [r + col for r in ROW if r != row]
    row_group = [row + c for c in COL if c != col]
    for rows in ("ABC", "DEF", "GHI"):
        for cols in ("123", "456", "789"):
            if row in rows and col in cols:
                return (
                    col_group
                    + row_group
                    + [r + c for r in rows for c in cols if r + c != row + col]
                )


# key: each grid
# value: the group of grids that cannot share the same value
# as the key grid
groups = dict((rc, get_group(rc[0], rc[1])) for rc in grids)


def update_legal_values(grid, val, domain):
    """Updates the legal values of the grid group (deleting val)."""
    domain[grid] = val
    for rc in groups[grid]:
        if val in domain[rc]:
            # delete assigned value from other valid lists
            domain[rc] = domain[rc].replace(val, "")
            if len(domain[rc]) == 0:  # invalid delete -- last value
                return False
            elif len(domain[rc]) == 1:  # forward check
                if not update_legal_values(rc, domain[rc], domain):
                    return False
    return domain


def get_domain(board):
    """Get lists of legal values for each grid"""
    # initialize each grid with all 1-9 legal values
    domain = dict((rc, COL) for rc in grids)
    # delete illegal values
    for key, val in board.items():
        if val != "0":
            update_legal_values(key, val, domain)
    return domain


def is_complete(board):
    """Helper function to check if board is complete."""
    return all(len(board[rc]) == 1 for rc in grids)


def select_unassigned_variable(board):
    """Helper function to select the unassigned variable with minimum remaining value"""
    min_len, min_var = float("inf"), None
    for rc in grids:
        if len(board[rc]) > 1:
            if len(board[rc]) < min_len:
                min_len, min_var = len(board[rc]), rc

    return min_var


def backtracking(board):
    """Takes a board and returns solved board."""
    # check if assignment is complete
    if is_complete(board):
        return board

    # pick the minimum remaining variable from domain
    var = select_unassigned_variable(board)

    for val in board[var]:
        new_board = board.copy()
        # forward checking to reduce variables
        new_board = update_legal_values(var, val, new_board)
        if new_board:
            result = backtracking(new_board)
            if result:
                return result
    return False


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ""
        for j in COL:
            row += board[i + j] + " "
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for rc in grids:
        ordered_vals.append(board[rc])
    return "".join(ordered_vals)


if __name__ == "__main__":
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {
            ROW[r] + COL[c]: sys.argv[1][9 * r + c] for r in range(9) for c in range(9)
        }

        solved_board = backtracking(get_domain(board))

        # Write board to file
        out_filename = "output.txt"
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write("\n")

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = "sudokus_start.txt"
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = "output.txt"
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {
                ROW[r] + COL[c]: line[9 * r + c] for r in range(9) for c in range(9)
            }

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(get_domain(board))

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write("\n")

        print("Finishing all boards in file.")
