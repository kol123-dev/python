import curses
import random
import time

# --- Game Configuration ---
# Set the desired speed (lower is faster)
GAME_SPEED = 0.1 
SCORE = 0

def draw_info(screen):
    """Draws the score and instructions at the top."""
    h, w = screen.getmaxyx()
    info_text = f"Score: {SCORE} | Use WASD or Arrow Keys | Press 'q' to Quit"
    screen.addstr(0, w // 2 - len(info_text) // 2, info_text, curses.A_BOLD)
    screen.hline(1, 0, curses.ACS_HLINE, w) # Draw a horizontal line

def generate_food(snake, screen):
    """Generates a piece of food at a random position, not on the snake."""
    h, w = screen.getmaxyx()
    while True:
        # Note: We avoid row 0 and 1 because they are used for the score/info display
        food_y = random.randint(2, h - 2)
        food_x = random.randint(1, w - 2)
        if [food_y, food_x] not in snake:
            return [food_y, food_x]

def main(stdscr):
    global SCORE

    # --- Curses Setup ---
    curses.curs_set(0)        # Hide the cursor
    stdscr.nodelay(1)         # Make getch non-blocking (doesn't wait for input)
    stdscr.timeout(int(GAME_SPEED * 1000))  # Set the refresh rate

    # --- Window and Dimensions ---
    sh, sw = stdscr.getmaxyx()
    # Define the play area borders
    stdscr.border(0) 

    # --- Initial State ---
    # Initial snake position (center of screen, length 3)
    snake_y = sh // 2
    snake_x = sw // 4
    # Snake is a list of [y, x] coordinates
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    # Initial direction (RIGHT)
    current_direction = curses.KEY_RIGHT
    
    # Generate initial food
    food = generate_food(snake, stdscr)

    while True:
        stdscr.clear()
        draw_info(stdscr) # Always draw the info bar first
        stdscr.border(0) # Redraw the border

        # --- Draw Food ---
        try:
            stdscr.addch(food[0], food[1], '@', curses.A_BOLD | curses.color_pair(1))
        except curses.error:
             # Handle error if food lands outside screen edge during resize
            food = generate_food(snake, stdscr)
            continue
            
        # --- Handle User Input ---
        key = stdscr.getch()

        # Input mapping for both WASD and Arrow Keys
        if key in [curses.KEY_RIGHT, ord('d')] and current_direction != curses.KEY_LEFT:
            current_direction = curses.KEY_RIGHT
        elif key in [curses.KEY_LEFT, ord('a')] and current_direction != curses.KEY_RIGHT:
            current_direction = curses.KEY_LEFT
        elif key in [curses.KEY_UP, ord('w')] and current_direction != curses.KEY_DOWN:
            current_direction = curses.KEY_UP
        elif key in [curses.KEY_DOWN, ord('s')] and current_direction != curses.KEY_UP:
            current_direction = curses.KEY_DOWN
        elif key == ord('q'):
            break # Exit the loop and end the game

        # --- Calculate New Head Position ---
        new_head = [snake[0][0], snake[0][1]]

        if current_direction == curses.KEY_RIGHT:
            new_head[1] += 1
        elif current_direction == curses.KEY_LEFT:
            new_head[1] -= 1
        elif current_direction == curses.KEY_UP:
            new_head[0] -= 1
        elif current_direction == curses.KEY_DOWN:
            new_head[0] += 1

        # Insert new head at the beginning of the snake list
        snake.insert(0, new_head)

        # --- Game Over Conditions ---
        head_y, head_x = snake[0]
        
        # 1. Hit the border (or the info bar at row 1)
        if (head_y <= 1 or head_y >= sh - 1 or 
            head_x <= 0 or head_x >= sw - 1):
            break 
            
        # 2. Hit itself (excluding the new head, which is snake[0])
        if snake[0] in snake[1:]:
            break

        # --- Check for Food Collision ---
        if snake[0] == food:
            SCORE += 10
            # Generate new food and DON'T pop the tail (snake grows)
            food = generate_food(snake, stdscr)
            stdscr.timeout(int(GAME_SPEED * 1000 * 0.95)) # Speed up slightly
        else:
            # Pop the tail (snake moves, length remains same)
            snake.pop()

        # --- Draw Snake ---
        for i, segment in enumerate(snake):
            # Head uses a different character/style
            char = 'O' if i == 0 else '#'
            stdscr.addch(segment[0], segment[1], char)

        stdscr.refresh()
        
    # --- Game Over Screen ---
    stdscr.nodelay(0) # Wait for input to close
    stdscr.clear()
    
    game_over_text = "GAME OVER"
    final_score_text = f"Your Final Score: {SCORE}"
    exit_text = "Press any key to exit..."

    stdscr.addstr(sh // 2 - 2, sw // 2 - len(game_over_text) // 2, 
                  game_over_text, curses.A_BOLD | curses.A_REVERSE)
    stdscr.addstr(sh // 2, sw // 2 - len(final_score_text) // 2, 
                  final_score_text)
    stdscr.addstr(sh // 2 + 2, sw // 2 - len(exit_text) // 2, 
                  exit_text)
    stdscr.refresh()
    stdscr.getch() # Wait for user input before final exit

if __name__ == '__main__':
    try:
        # curses.wrapper handles initialization and safe shutdown
        curses.wrapper(main)
    except curses.error as e:
        print("\n--- Error ---")
        print("There was an issue initializing the terminal display.")
        print("Possible reasons:")
        print("1. Terminal window is too small.")
        print("2. 'curses' library is not properly configured on your system (common on Windows).")
        print("Please ensure your terminal window is maximized or wide enough.")
        print("---")

    print(f"\nGame Ended. Final Score: {SCORE}")