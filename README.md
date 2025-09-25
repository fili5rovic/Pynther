# Pynther

**Pynther** is a graphical simulation written in Python that visualizes the fundamental algorithms of sequential game theory. The simulation takes place on a map of fields in space where spaceships move, conquer, and color the fields in their color. The goal of the game is to have the most colored fields once all fields are colored or the maximum number of rounds has been reached.

## Features

- Visualization of sequential games with multiple agent spaceships
- Configurable number of rounds, agents, map, move timeout, and search depth
- Support for various agent types and algorithms
- Easily extensible architecture for adding new agent types

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/fili5rovic/Pynther.git
    cd Pynther
    ```

2. Install dependencies (the `pygame` package is required):

    ```bash
    pip install pygame
    ```

## Running the Simulation

Start the program from the terminal with the command:

```bash
python main.py agents map rounds timeout max_depth
```

Where the parameters are:

- `agents` — agent names to use, separated by commas (default: RandomAgent,RandomAgent,...)
- `map` — map file name (default: example_map.txt)
- `rounds` — maximum number of rounds (default: 5)
- `timeout` — maximum time per move in seconds (default: 0; unlimited)
- `max_depth` — maximum search tree depth (default: 5)

Example usage with two RandomAgents and the example map:

```bash
python main.py RandomAgent,RandomAgent example_map.txt 10 0 5
```

## Application Controls

- Press **SPACE** to start or pause the simulation
- Press **ESC** to exit and close the application

## Map Format

The map is a text file containing a matrix of fields:

| Symbol | Description                       |
|--------|-----------------------------------|
| 0      | Pit (impassable field)            |
| _      | Free field                        |
| a-d    | Colored field                     |
| A-D    | Spaceship                         |

Each line in the map file must have the same number of characters.

**Example map file:**
```
0__A_
___B_
a_b0_
```
