# TetrisCurses

# Core project
Notions: curses library and terminals
## Introduction
The game tetris is pretty popular, I bet you have played it many times in versions that had nice graphics, nice sounds, nice effects… well, today, you will code your own version of tetris, and it just won't be as beautiful!

Using the `curses` library (yep, the one you use for the command-line edition on the shell project), you will code a text-based, no-frills tetris game.

Excited yet?!

## Your mission
You will code a tetris.py program that allows the user to play a tetris game on the terminal.

For the core project, your tetris game will follow those guidelines:

- it will use a single character for the falling blocks (you can choose whatever character you like)
- the right & left keys should make the falling block move to the right or to the left
- you need to keep track of the score: every time a line is destroyed, the player gets one point. So you need an area with the score, and an area with the game
- if a falling block is stuck at the top, it's game over! There should be a message announcing the final score before the program exits cleanly.

 Additionally, resizing the terminal window shouldn't cause your program to crash. So you need to catch the signal SIGWINCH to take appropriate actions (which can be reducing the score area, or exiting cleanly the program if there's not enough space to display the game and the score area).

Note: don't hesitate to research a little what's a signal and how it interacts with the terminal, if you didn't do it already for the shell project. You might be asked about it during the staff review... 🙃

![example1](https://i.imgur.com/S7UFpM9.gif)

# BONUSES
## 1. Complex blocks
Having the blocks be single characters was simple enough, it made it easy to check for collisions and didn't allow for cascading line destruction. But a tetris game isn't as exciting without the possibility to misplace different-sized blocks! So let's add them.

For this bonus, you will turn the falling blocks into actual pieces.

![example2](https://i.imgur.com/nFCjibY.gif)

## 2. Piece rotation
You will make your tetris game complete with this last bonus, by implementing piece rotation. When the user strikes a specific key (the up key for example, though you can choose something else), the piece should rotate on itself. Be careful with the collusions, if there's not enough place for the piece to rotate, it shouldn't rotate.
