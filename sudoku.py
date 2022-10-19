"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"
grids = [r + c for r in ROW for c in COL]


def get_col(rc):
    """helper function to get all grids in the same column"""
    return [r + rc[1] for r in ROW if rc[0] != r]


def get_row(rc):
    """helper function to get all grids in the same row"""
    return [rc[0] + c for c in COL if rc[1] != c]


def get_box(rc):
    """helper function to get all grids in the same 3x3 box"""
    for rows in ("ABC", "DEF", "GHI"):
        for cols in ("123", "456", "789"):
            if rc[0] in rows and rc[1] in cols:
                return [r + c for r in rows for c in cols if r + c != rc]


def get_group(rc):
    """helper function to get all the related grids (column, row, box)"""
    return list(set(get_col(rc) + get_row(rc) + get_box(rc)))


# memoize function get_group
# key: each grid
# value: the group of grids that cannot share the same value as the key grid
groups = dict((rc, get_group(rc)) for rc in grids)


def inference(var, val, domains):
    """
    helper function to assign value and forward check to update the domains.
    """
    # assign value
    domains[var] = val
    # delete value from domains
    for v in groups[var]:
        if val in domains[v]:
            # check if domain will be valid after update
            if len(domains[v]) <= 1:
                return False
            domains[v] = domains[v].replace(val, "")
    return domains


def get_domains(board):
    """Get lists of legal values for each grid"""
    # initialize each grid with all 1-9 legal values
    domains = dict((rc, COL) for rc in grids)

    # delete illegal values
    for key, val in board.items():
        if val != "0":
            domains = inference(key, val, domains)

    return domains


def is_complete(board):
    """Helper function to check if board is complete."""
    if all(len(board[rc]) == 1 for rc in grids):
        for rc in grids:
            if (
                len(set([board[grid] for grid in get_col(rc)] + [board[rc]])) < 9
                or len(set([board[grid] for grid in get_row(rc)] + [board[rc]])) < 9
                or len(set([board[grid] for grid in get_box(rc)] + [board[rc]])) < 9
            ):
                return False
        return True
    return False


def select_unassigned_variable(board):
    """Helper function to select the unassigned variable with minimum remaining value"""
    min_len, min_var = float("inf"), None
    for rc in grids:
        if len(board[rc]) > 1 and len(board[rc]) < min_len:
            min_len, min_var = len(board[rc]), rc

    return min_var


def backtracking(board):
    """Takes a board and returns solved board."""
    # check if assignment is complete
    if is_complete(board):
        return board

    # pick the minimum remaining variable from domain
    var = select_unassigned_variable(board)

    # return failed if there are no valid mrv
    if not var:
        return False

    for val in board[var]:
        # assign value and then forward check
        new_board = inference(var, val, board.copy())
        if new_board:
            result = backtracking(new_board)
            if result:
                return result


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

        solved_board = backtracking(get_domains(board))
        # print_board(solved_board)

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
        outfile_readme = open("README.txt", "w")
        total_solved, runtime = 0, []
        print("Solving sudokus...")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {
                ROW[r] + COL[c]: line[9 * r + c] for r in range(9) for c in range(9)
            }

            # Print starting board.
            # print_board(board)

            # Solve with backtracking
            start_time = time.time()
            solved_board = backtracking(get_domains(board))
            runtime.append(time.time() - start_time)
            if solved_board:
                total_solved += 1

            # Print solved board.
            # print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write("\n")

        outfile_readme.write("Total boards solved: %.0f" % total_solved)
        outfile_readme.write("\n")
        outfile_readme.write("Total time taken: %.2fs" % sum(runtime))
        outfile_readme.write("\n")
        outfile_readme.write(
            "Average time taken: %.2fs" % (sum(runtime) / len(runtime))
        )
        outfile_readme.write("\n")
        outfile_readme.write("Minimum time taken: %.5fs" % (min(runtime)))
        outfile_readme.write("\n")
        outfile_readme.write("Maximum time taken: %.2fs" % (max(runtime)))
        outfile_readme.write("\n")
        outfile_readme.write(
            "Standard deviation of time taken: %.2f" % statistics.pstdev(runtime)
        )
        outfile_readme.write("\n")

        print("Finishing all boards in file.")
