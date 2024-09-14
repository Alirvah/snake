#!/usr/bin/env python3

import curses
import time
import random

def main(stdscr):
    # Initialize the screen
    curses.curs_set(0)            # Hide the cursor
    stdscr.nodelay(1)             # Don't block I/O calls
    stdscr.timeout(100)           # Refresh every 100 milliseconds

    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()

    # Create initial snake and food
    snake = [
        [sh // 2, sw // 4 + 1],
        [sh // 2, sw // 4],
        [sh // 2, sw // 4 - 1]
    ]
    direction = curses.KEY_RIGHT

    food = [sh // 2, sw // 2]
    stdscr.addch(food[0], food[1], curses.ACS_PI)

    # Game loop
    while True:
        # Get user input
        key = stdscr.getch()
        if key != -1:
            direction = key

        # Calculate new head position
        head = [snake[0][0], snake[0][1]]

        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1
        elif direction == 27:  # ESC key to exit
            break

        # Insert new head position
        snake.insert(0, head)

        # Check for collision with walls
        if (head[0] in [0, sh] or head[1] in [0, sw] or head in snake[1:]):
            msg = "Game Over!"
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.refresh()
            time.sleep(2)
            break

        # Check if snake eats the food
        if head == food:
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                if nf not in snake:
                    food = nf
            stdscr.addch(food[0], food[1], curses.ACS_PI)
        else:
            # Remove tail segment
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        # Draw the head
        stdscr.addch(head[0], head[1], curses.ACS_CKBOARD)

        # Refresh the screen
        stdscr.refresh()

    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
