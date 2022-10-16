"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"


# for testing
test_input = (
    "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
)

test_board = {
    ROW[r] + COL[c]: test_input[9 * r + c] for r in range(9) for c in range(9)
}


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


# dict stores each grid and the group of grids that cannot share the same value
groups = dict((r + c, get_group(r, c)) for r in ROW for c in COL)


def update_legal_values(grid, val, domain):
    """Updates the legal values of the grid group (deleting val)."""
    for rc in groups[grid]:
        if val in domain[rc]:
            domain[rc] = domain[rc].replace(val, "")
    return


def get_domain(board):
    """Get all the legal values of each grid"""
    domain = dict((r + c, COL) for r in ROW for c in COL)
    print(domain)
    for key, val in board.items():
        if val != "0":
            if val not in domain[key] or len(domain[key]) == 0:
                print("invalid board")
                return False
            update_legal_values(key, val, domain)
    return domain


# print(get_domain(test_input))


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
    for r in ROW:
        for c in COL:
            ordered_vals.append(board[r + c])
    return "".join(ordered_vals)


def is_complete(board):
    """Helper function to check if board is complete."""
    for val in board.values():
        if len(val) > 1:
            return False
        return True


def select_unassigned_variable(board):
    """Helper function to select the unassigned variable with minimum remaining value"""
    return sorted(board, key=lambda k: len(board[k]), reverse=True)[0]


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this

    # check if assignment is comlete
    if is_complete(board):
        return board

    var = select_unassigned_variable(board)

    for var in order_domain_values(var, board):
        pass

    return solved_board


if __name__ == "__main__":
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {
            ROW[r] + COL[c]: sys.argv[1][9 * r + c]
            for r in range(9)
            for c in range(9)
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
