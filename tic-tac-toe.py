import random


class Node:
    def __init__(self, board_state=None, turn=None):
        self.board_state = board_state if board_state is not None else []   # list[9]  'X' for user, 'O' for bot,  'B' for blank
        self.children   = []                                                # list that stores all the children nodes (not children board list)
        self.turn = turn                                                    # node player turn ('O for bot' or 'X for user')
        self.rating = None                                                  # -1 = user wins, 0 = draw, +1 = bot wins


# The list all possible win conditions
WINS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],   # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],   # columns
    [0, 4, 8], [2, 4, 6],              # diagonals
]


# Function that prints the full tic tac toe board for played moves
def printBoard(board):
    printList = []
    for index in board:                                         # replaces b with a blank space on the displayed game board
        if index.lower() == 'b':
            printList.append(' ')
        else:
            printList.append(index)

    print("\n")
    print(f" {printList[0]} | {printList[1]} | {printList[2]} ")
    print("---|---|---")
    print(f" {printList[3]} | {printList[4]} | {printList[5]} ")
    print("---|---|---")
    print(f" {printList[6]} | {printList[7]} | {printList[8]} ")
    print("\n")


# function that checks if a board has a winner, draw or still has empty slots left
def game_state(board):
    for a, b, c in WINS:
        if board[a] == board[b] == board[c] != 'B':
            return 1 if board[a] == 'O' else -1
    if 'B' not in board:
        return 0
    else:
        return 'B'


# Function to generate a tree of all possible future moves for the current board. It creates a node for each move. 
def game_tree(board, turn):
    root = Node(board.copy(), turn)

    state = game_state(board)

    # base case that assigns rating to the leaves of the tree
    if state == 1:
        root.rating = 1
        return root
    if state == -1:
        root.rating = -1
        return root
    if state == 0:
        root.rating = 0
        return root

    for i in range(9):
        if board[i] == 'B':                 # next move in a blank space. Add the new move node to the tree recursively
            childBoard = board.copy()
            childBoard[i] = turn
            if turn == 'X':
                child = game_tree(childBoard, 'O')
                root.children.append(child)
            else:
                child = game_tree(childBoard, 'X')
                root.children.append(child)

    return root


# Function that assigns rating for each node.
def minimax(root):
    if not root.children:
        return

    for child in root.children:
        minimax(child)

    ratings = [node.rating for node in root.children]
    root.rating = max(ratings) if root.turn == 'O' else min(ratings)


# The bot move function
def bot_move(board):
    tree = game_tree(board, 'O')
    minimax(tree)
    favourable_moves = []
    ratings = [node.rating for node in tree.children]
    highest_ratings = max(ratings)
    for child in tree.children:
        if child.rating == highest_ratings:
            favourable_moves.append(child)
    next_move = random.choice(favourable_moves)

    return next_move.board_state


# Main function
def main():
    board = ['B'] * 9
    example_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

    print("\nWelcome to the Tic Tac Toe game!")
    print("You will be playing against the computer.")
    print("\nTo pick a position you can pick a number from 0 - 8.")
    print("You will play as X and the computer will play O.")
    print("The positions you pick correspond to the example below:")
    printBoard(example_arr)

    print("If you would like to start enter 'x'.")
    print("If you would like the computer to start enter 'o'.")
    print()

    # Starting choice
    while True:
        turn = input("Enter 'x' or 'o': ").strip().lower()
        if turn in ('x', 'o'):
            break
        print("Invalid input. Please enter 'x' or 'o'.")

    # Play as long as there are blank slots and win condition not met
    while game_state(board) == 'B':

        if turn == 'x':
            while True:
                raw = input("Your turn. Which position would you like to place (0-8): ").strip()
                if not raw.isdigit():
                    print("Invalid input. Please enter a number.")
                    continue

                move = int(raw)
                if move < 0 or move > 8:
                    print("Please pick a position between 0 and 8.")
                    continue

                if board[move] != 'B':
                    print("Position already taken! Choose an empty spot.")
                    continue

                break

            board[move] = 'X'
            turn = 'o'
            print(f"You placed X at position {move}")
            printBoard(board)

        else:
            print("The computer will now play.")
            new_board = bot_move(board)

            # find which position changed so we can report it
            move = next(i for i in range(9) if board[i] != new_board[i])
            board = new_board

            turn = 'x'
            print(f"Computer placed O at position {move}")
            printBoard(board)

    result = game_state(board)
    if result == 1:
        print("The computer won!")
    elif result == -1:
        print("Congratulations, you won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()