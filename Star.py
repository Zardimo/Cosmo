import os
import time
import curses
import asyncio
import random
from curses_tools import draw_frame, read_controls, get_frame_size


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    
    row, column = start_row, start_column
    for _ in range(3):
        canvas.addstr(round(row), round(column), '*')
        await asyncio.sleep(0)

        canvas.addstr(round(row), round(column), 'O')
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def get_frame(frame_path):
    with open (frame_path, 'r') as frame:
        return frame.read()


async def blink(canvas, row, column, symbol):
    curses.curs_set(False)
    canvas.border()
    canvas.refresh()

    for _ in range(3):
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(random.randint(0, 5)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(0, 2)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(random.randint(0, 3)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(0, 2)):
            await asyncio.sleep(0)


async def animate_spaceship(canvas, row_lenght, column_lenght, both_edge):
    rocket_frame_1 = get_frame(os.path.join(os.getcwd(), 'GitHub/Cosmo/Rocket_animation/rocket_frame_1.txt'))
    rocket_frame_2 = get_frame(os.path.join(os.getcwd(), 'GitHub/Cosmo/Rocket_animation/rocket_frame_2.txt'))
    row =  row_lenght/2      #center_row_for_rocket
    column = column_lenght/2    #center_column_for_rocket
    frame_row, frame_column = get_frame_size(rocket_frame_1)
    frames = [rocket_frame_1, rocket_frame_2]
    for _ in range(100):
        for frame in frames:
            row_drection, column_direction, space_direction = read_controls(canvas)
            
            if row > both_edge and row < row_lenght-frame_row-both_edge:
                row += row_drection
            elif row > row_lenght-frame_row-both_edge:
                row -= 1
            elif row < both_edge:
                row += 1

            if column > both_edge and column < column_lenght-both_edge-frame_column:
                column += column_direction
            elif column < both_edge:
                column += 1
            elif column > column_lenght-both_edge-frame_column:
                column -=1

            draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)


def main(canvas):
    coroutines = []
    row_lenght, column_lenght = canvas.getmaxyx()
    symbols = '+*.:'
    edge = 1
    both_edge = 2
    coroutines.append(fire(canvas, start_row=random.randint(edge, row_lenght-both_edge), start_column=random.randint(edge, column_lenght-both_edge)))
    coroutines.append(animate_spaceship(canvas, row_lenght, column_lenght, both_edge))
    canvas.nodelay(1)
    for _ in range(1000):
        random_row = random.randint(edge, row_lenght-both_edge)
        random_column = random.randint(edge, column_lenght-both_edge)
        random_symbol = random.choice(symbols)
        coroutines.append(blink(canvas, random_row, random_column, random_symbol))
    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine1)
        if len(coroutines) == 0:
            break
        time.sleep(0.1)


if __name__=='__main__':
    curses.update_lines_cols()
    curses.wrapper(main)