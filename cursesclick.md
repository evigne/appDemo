To integrate the `curses`-based terminal navigation with `click`, you can use `click` to call the `curses` function by wrapping the `curses.wrapper(main)` in a `click` command. Here's an example that demonstrates how to structure this:

```python
import click
import curses

def main(stdscr):
    # Disable cursor
    curses.curs_set(0)

    # List of items to display
    items = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
    current_row = 0

    def print_menu(stdscr, current_row):
        stdscr.clear()
        for idx, item in enumerate(items):
            if idx == current_row:
                stdscr.addstr(idx, 0, item, curses.A_REVERSE)  # Highlight selected item
            else:
                stdscr.addstr(idx, 0, item)
        stdscr.refresh()

    # Initial print of the menu
    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(items) - 1:
            current_row += 1
        elif key == ord('\n'):
            stdscr.addstr(len(items), 0, f"You selected: {items[current_row]}")
            stdscr.refresh()
            stdscr.getch()
            break

        print_menu(stdscr, current_row)

@click.command()
def select_option():
    """Invoke the curses menu."""
    curses.wrapper(main)

if __name__ == '__main__':
    select_option()
```

In this solution:

1. **`curses.wrapper(main)`** is wrapped in the `click` command.
2. **`click.command()`** defines a command-line interface command that calls the `main` function using `curses`.

This approach combines both libraries and allows you to invoke the interactive `curses` menu via the command-line interface built with `click`.