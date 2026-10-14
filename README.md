# Connect Four – MinMax Algorithm in Python

## Project Description

This project implements a generalized version of the classic **Connect Four (Puissance 4)** game using Python and Object-Oriented Programming (OOP).

The main objective is to develop an Artificial Intelligence (AI) player using the **MinMax algorithm**, with optional **Alpha-Beta Pruning** to optimize decision-making.

The game supports different board sizes, multiple player types, two evaluation heuristics, and performance comparisons between AI strategies.

This project was developed as part of a Python practical assignment (TP) at **SUPINFO**.

## Features

* Customizable board dimensions (rows and columns)
* Configurable number of consecutive pieces required to win
* Console-based game interface
* Human vs Human
* Human vs Random Bot
* Human vs MinMax AI
* Random Bot vs MinMax AI
* MinMax AI vs MinMax AI
* MinMax algorithm with configurable search depth
* Optional Alpha-Beta Pruning
* Two heuristic evaluation functions
* Automatic win and draw detection
* Performance statistics (wins, losses, draws)

## Technologies Used

* **Language:** Python 3
* **Programming Paradigm:** Object-Oriented Programming (OOP)
* **Algorithms:** MinMax, Alpha-Beta Pruning
* **Libraries:** Python Standard Library

## Project Structure

```text
TP_Puissance4/
│
├── puissance4.py       # Board and game management
├── minMax.py           # MinMax AI and Alpha-Beta Pruning
├── stupidBot.py        # Random bot player
├── human.py            # Human player input
├── main.py             # Main application
├── statistiques.py     # Performance comparison
└── README.md           # Project documentation
```

## Game Rules

Connect Four is a two-player strategy game.

1. The game is played on a grid containing rows and columns.
2. Players take turns dropping their pieces into available columns.
3. Pieces fall to the lowest available position due to gravity.
4. The first player to connect the required number of pieces horizontally, vertically, or diagonally wins.
5. If the board becomes full without a winner, the game ends in a draw.

### Default Configuration

| Parameter              | Default Value |
| ---------------------- | ------------- |
| Rows                   | 6             |
| Columns                | 7             |
| Pieces required to win | 4             |
| Players                | 2             |
| Empty cell             | 0             |
| Player 1               | 1             |
| Player 2               | 2             |

## Artificial Intelligence – MinMax

The **MinMax algorithm** is a recursive decision-making algorithm used in two-player games.

It assumes that both players make optimal decisions.

* **MAX player:** Attempts to maximize the evaluation score.
* **MIN player:** Attempts to minimize the evaluation score.

The AI explores possible future moves up to a predefined depth and selects the move with the best expected outcome.

### Alpha-Beta Pruning

Alpha-Beta Pruning improves MinMax by eliminating branches that cannot influence the final decision.

* **Alpha (α):** Best score guaranteed to the maximizing player.
* **Beta (β):** Best score guaranteed to the minimizing player.

When `alpha >= beta`, the remaining branches can be skipped.

This optimization reduces the number of explored states without changing the theoretical MinMax result.

## Evaluation Heuristics

The project includes two heuristic evaluation methods.

### Heuristic 1 – Positional Evaluation

Each board position receives a score based on the number of possible winning alignments passing through that position.

The evaluation function calculates:

```text
Score = Sum of AI positional scores
      - Sum of opponent positional scores
```

This heuristic favors strategically important positions, particularly central positions.

### Heuristic 2 – Alignment Evaluation

The board is divided into possible winning sequences.

Each sequence receives a score depending on its contents:

* A sequence containing pieces from both players receives a score of zero.
* A sequence containing only one player's pieces receives a score based on the number of pieces.

The final evaluation is:

```text
Score = AI alignment scores
      - Opponent alignment scores
```

This heuristic helps the AI identify winning opportunities and potential threats.

## Installation

### Requirements

* Python 3.10 or newer (recommended)
* Visual Studio Code or another Python-compatible editor

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Navigate to the project directory:

```bash
cd TP_Puissance4
```

No external dependencies are required.

## Running the Game

Start the application:

```bash
python main.py
```

Depending on the operating system, you may need:

```bash
python3 main.py
```

The application allows players to select their strategies and play through the console.

### Example Board

```text
  0 1 2 3 4 5 6
+---------------+
| . . . . . . . |
| . . . . . . . |
| . . . . . . . |
| . . . X . . . |
| . . O X . . . |
| . O X X O . . |
+---------------+
```

Legend:

* `.` = Empty cell
* `X` = Player 1
* `O` = Player 2

## Performance Comparison

The project includes a statistics module to compare different strategies.

Run:

```bash
python statistiques.py
```

The goal is to organize multiple games between different player types while alternating the starting player.

Performance indicators include:

* Number of wins
* Number of losses
* Number of draws
* Win percentage

### Example Statistics

The following table is illustrative, not an actual benchmark result.

| Player     | Wins | Losses | Draws |
| ---------- | ---: | -----: | ----: |
| MinMax AI  |    8 |      1 |     1 |
| Random Bot |    1 |      8 |     1 |

These comparisons help evaluate the effectiveness of MinMax against random strategies.

## Object-Oriented Design

The project follows the principles of Object-Oriented Programming, including encapsulation.

### `puissance4`

Responsible for:

* Creating the game board
* Managing board dimensions
* Placing pieces
* Checking available columns
* Detecting winning combinations
* Managing game states

### `minMax`

Responsible for:

* Exploring possible moves recursively
* Evaluating game positions
* Selecting optimal moves
* Applying Alpha-Beta Pruning

### `stupidBot`

Responsible for:

* Selecting random valid moves

### `human`

Responsible for:

* Requesting user input
* Selecting a valid column

### `statistiques.py`

Responsible for:

* Running automated matches
* Tracking wins, losses, and draws
* Comparing different strategies

## Future Improvements

Possible extensions include:

* Graphical User Interface (GUI) using Tkinter or Pygame
* Adjustable AI difficulty
* Improved heuristic evaluation
* AI vs AI visualization
* Execution time comparison
* Number of explored MinMax nodes
* Tournament results exported to CSV
* Transposition tables to optimize AI search

## Learning Objectives

Through this project, we explore:

1. Python Object-Oriented Programming
2. Encapsulation and class design
3. Recursive algorithms
4. Adversarial search algorithms
5. MinMax decision-making
6. Alpha-Beta Pruning
7. Heuristic evaluation
8. Algorithm performance analysis

## Author

**4DCGD**

GitHub: https://github.com/4DCGD

## License

This project was developed for educational purposes as part of a Python programming assignment.

---

**SUPINFO – Python Practical Assignment**

*Connect Four AI using MinMax and Alpha-Beta Pruning*
