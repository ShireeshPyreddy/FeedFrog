import pygame
from random import randint
import math

# Initialize pygame and create a window
pygame.init()
WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.init()

frog_eat_sound = pygame.mixer.Sound("audio_files/Frog-Sound.mp3")
frog_idle_sound = pygame.mixer.Sound("audio_files/frog-eat-sound.mp3")
food_appear_sound = pygame.mixer.Sound("audio_files/fly-sound.mp3")
bee_sting_sound = pygame.mixer.Sound("audio_files/bee-buzzing-6254.mp3")

background_image = pygame.image.load("images/background.jpg")  # Replace with your background image
land_background_image = pygame.image.load("images/land_background.jpg")  # Replace with your background image
water_background_image = pygame.image.load("images/water-background.jpg")  # Replace with your background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
land_background_image = pygame.transform.scale(land_background_image, (WIDTH, HEIGHT))
water_background_image = pygame.transform.scale(water_background_image, (WIDTH, HEIGHT))

# Define colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define speed constants for each level
LEVEL_SPEEDS = {
    "easy": 1,
    "medium": 4,
    "hard": 7
}


class Frog:
    def __init__(self):
        self.x = WIDTH / 2
        self.size = 50
        self.y = HEIGHT - self.size  # this places the frog at the bottom of the window
        self.tongue_length = 0  # Initialize tongue length
        self.tongue_direction = 0, 0  # Tuple representing direction of the tongue
        self.tongue_out = False

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.size + 10, self.size + 10))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y - 20, self.size - 30, self.size - 30))
        pygame.draw.rect(win, (0, 255, 0), (self.x + 40, self.y - 20, self.size - 30, self.size - 30))
        pygame.draw.rect(win, BLACK, (self.x + 8, self.y - 10, self.size - 46, self.size - 46))
        pygame.draw.rect(win, BLACK, (self.x + 48, self.y - 10, self.size - 46, self.size - 46))
        # Check if the tongue is out
        if self.tongue_out:
            # If it is, reduce the length
            if self.tongue_length > 0:
                self.tongue_length -= 2
            # Once the tongue_length is zero, set tongue_out to False and play sound effect
            else:
                self.tongue_out = False

    def draw_tongue(self, win):
        # Set the starting point
        start_point = (self.x + (self.size + 9) // 2, self.y + (self.size + 5) // 2)

        # Calculate the ending point based on the direction and tongue length
        end_point = (
            start_point[0] + self.tongue_length * self.tongue_direction[0],
            start_point[1] + self.tongue_length * self.tongue_direction[1]
        )

        # Draw the tongue line
        pygame.draw.line(win, (255, 0, 0), start_point, end_point, 5)

        # Check if the tongue is out
        if self.tongue_out:
            # If it is, reduce the length
            if self.tongue_length > 0:
                self.tongue_length -= 2
            # Once the tongue_length is zero, set tongue_out to False
            else:
                self.tongue_out = False


class Food:
    def __init__(self, frog_y, level):
        self.width = randint(20, 40)
        self.height = randint(10, 20)
        self.x = randint(0, WIDTH - self.width)  # Random x-coordinate within the window
        # Random y-coordinate between the top of the screen and the top of the frog
        self.y = randint(0, int(frog_y - self.height))
        # self.speed = randint(1, 5)  # Random speed for food movement
        self.speed = LEVEL_SPEEDS[level.lower()]  # Speed based on the selected level
        self.direction = 1 if randint(0, 1) else -1  # Random direction (-1 for left, 1 for right)
        self.v_speed = LEVEL_SPEEDS[level.lower()]  # Vertical speed based on the selected level
        self.v_direction = 1 if randint(0, 1) else -1  # Random vertical direction (-1 for up, 1 for down)

    def update(self):
        self.x += self.speed * self.direction
        # Update vertical position
        self.y += self.v_speed * self.v_direction

    def draw(self, win):
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height))

        # Draw vertical black lines on top and bottom center
        line_length = 5
        line_width = 2
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        if self.direction == -1:
            pygame.draw.line(win, BLACK, (center_x - line_length // 2, self.y),
                             (center_x + line_length // 2, self.y - 10),
                             line_width)
            pygame.draw.line(win, BLACK, (center_x - line_length // 2, self.y + self.height),
                             (center_x + line_length // 2, self.y + self.height + 8), line_width)
            pygame.draw.line(win, BLACK, (center_x - line_length // 2, self.y + self.height),
                             (center_x + line_length // 2, self.y + self.height + 8), line_width)
            pygame.draw.line(win, (0, 0, 0), (self.x - line_length, center_y), (self.x, center_y), line_width)
        else:
            pygame.draw.line(win, (0, 0, 0), (center_x - line_length // 2, self.y),
                             (center_x - line_length // 2 - 5, self.y - line_length - 3), line_width)
            pygame.draw.line(win, (0, 0, 0), (center_x - line_length // 2, self.y + self.height),
                             (center_x - line_length // 2 - 5, self.y + self.height + line_length + 3), line_width)
            pygame.draw.line(win, (0, 0, 0), (self.x + self.width, center_y),
                             (self.x + self.width + line_length, center_y), line_width)

    def intersects_with_line(self, x1, y1, x2, y2):
        # Check if line intersects with any of the sides of the rectangle
        if self.line_intersects_rect_side(x1, y1, x2, y2, self.x, self.y, self.x + self.width, self.y) or \
                self.line_intersects_rect_side(x1, y1, x2, y2, self.x + self.width, self.y, self.x + self.width,
                                               self.y + self.height) or \
                self.line_intersects_rect_side(x1, y1, x2, y2, self.x + self.width, self.y + self.height, self.x,
                                               self.y + self.height) or \
                self.line_intersects_rect_side(x1, y1, x2, y2, self.x, self.y + self.height, self.x, self.y):
            return True
        return False

    @staticmethod
    def line_intersects_rect_side(x1, y1, x2, y2, x3, y3, x4, y4):
        # Calculate denominator
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return False

        # Calculate intersection point
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        # Check if intersection point is on both line segments
        if 0 <= t <= 1 and 0 <= u <= 1:
            return True
        return False


class Bug:
    def __init__(self, frog_y, level):
        self.radius = 10
        # Set initial x-coordinate to either 0 or WIDTH - self.radius * 2
        self.x = 0 if randint(0, 1) else WIDTH - self.radius * 2
        # Random y-coordinate between the top of the screen and the top of the frog
        self.y = randint(0, int(frog_y - self.radius * 2))
        self.speed = LEVEL_SPEEDS[level.lower()]  # Speed based on the selected level
        # Set direction based on initial x-coordinate
        self.direction = 1 if self.x == 0 else -1
        self.v_speed = LEVEL_SPEEDS[level.lower()]  # Vertical speed based on the selected level
        self.v_direction = 1 if randint(0, 1) else -1  # Random vertical direction (-1 for up, 1 for down)

    def update(self):
        self.x += self.speed * self.direction
        # Update vertical position
        self.y += self.v_speed * self.v_direction

    def draw(self, win):
        pygame.draw.circle(win, RED, (self.x + self.radius, self.y + self.radius), self.radius)

    def is_visible(self):
        return 0 <= self.x <= WIDTH - self.radius * 2 and 0 <= self.y <= HEIGHT - self.radius * 2

    def intersects_with_line(self, x1, y1, x2, y2):
        # Calculate the distance between the center of the circle and the line
        dx = x2 - x1
        dy = y2 - y1
        cx = self.x + self.radius
        cy = self.y + self.radius

        # Check if the line is actually a point
        if dx == 0 and dy == 0:
            # Calculate the distance between the point and the center of the circle
            d = math.sqrt((cx - x1) ** 2 + (cy - y1) ** 2)
        else:
            d = abs(dy * cx - dx * cy - x1 * y2 + x2 * y1) / math.sqrt(dx ** 2 + dy ** 2)

        # Check if the distance is less than or equal to the radius of the circle
        return d <= self.radius

    def draw_line(self, win, length):
        # Calculate the start and end points of the line based on the bug's position and direction
        start_x = self.x + self.radius
        start_y = self.y + self.radius
        end_x = start_x + length * self.direction
        end_y = start_y

        # Draw the line
        pygame.draw.line(win, RED, (start_x, start_y), (end_x, end_y), 2)


def main(level, mode):
    if level and mode is not None:
        clock = pygame.time.Clock()

        pygame.mixer.music.load(
            "audio_files/background_music.mp3")  # Replace with the path to your background music file
        pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
        pygame.mixer.music.set_volume(0.5)  # Set the volume between 0.0 and 1.0

        frog = Frog()
        foods = []  # List to store food instances
        bugs = []  # List to store bug instances
        food_counter = 0  # Counter for foods touching the tongue
        run = True

        actual_level = level

        idle_time = 0  # Time since last user input
        idle_threshold = 5000  # Time threshold for playing idle sound (in milliseconds)

        while run:
            clock.tick(60)

            if actual_level.lower() == 'progression':
                if food_counter < 25:
                    level = 'easy'
                elif 25 <= food_counter <= 100:
                    level = 'medium'
                elif food_counter > 100:
                    level = 'hard'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # If user clicked, calculate the direction and set the frog's tongue_length
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    frog.tongue_length = 40  # Here I'm using a fixed length. Update this as required.
                    frog.tongue_direction = (mouse_pos[0] - frog.x, mouse_pos[1] - frog.y)
                    frog.tongue_out = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    frog.tongue_length = max(frog.tongue_length, 0)  # Keep the tongue length if it's already longer
                    frog.tongue_out = frog.tongue_length > 0

                # Reset idle_time on any user input
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.KEYUP):
                    idle_time = 0

            # Update idle_time and play idle sound if threshold is exceeded
            idle_time += clock.tick(60)
            if idle_time > idle_threshold:
                frog_idle_sound.play()
                idle_time = 0

            if level.lower() == 'easy':
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    frog.x -= 5
                if keys[pygame.K_RIGHT]:
                    frog.x += 5

            # Drawing
            if mode.lower() == "land":
                win.blit(land_background_image, (0, 0))  # Draw the background
            else:
                win.blit(water_background_image, (0, 0))  # Draw the background

            # Update and draw foods
            for food in foods:
                food.update()
                if food.x > WIDTH or food.x + food.width < 0:
                    foods.remove(food)  # Remove food if it goes off-screen
                food.draw(win)

            for bug in bugs:
                bug.update()
                if bug.x > WIDTH or bug.x + bug.radius * 2 < 0:
                    bugs.remove(bug)  # Remove bug if it goes off-screen
                bug.draw(win)
                bug.draw_line(win, 20)

            # Generate new food if fewer than 2 on the screen
            if len(foods) < 2:
                new_food = Food(frog.y, level)  # Pass the y-coordinate of the top of the frog
                foods.append(new_food)
                food_appear_sound.play()

            if level.lower() in ['easy', 'medium']:
                bugs_count = 2
            else:
                bugs_count = randint(2, 4)

            if len(bugs) < bugs_count:
                new_bug = Bug(frog.y, level)  # Pass the y-coordinate of the top of the frog
                bugs.append(new_bug)

            # Update and draw bugs
            bug_count = min(len(bugs), 2)
            for i in range(bug_count):
                bugs[i].draw(win)

            frog.draw(win)
            frog.draw_tongue(win)
            # Calculate the start and end points of the frog's tongue
            tongue_start_x = frog.x + frog.size // 2
            tongue_start_y = frog.y + frog.size // 2
            tongue_end_x = tongue_start_x + frog.tongue_length * frog.tongue_direction[0]
            tongue_end_y = tongue_start_y + frog.tongue_length * frog.tongue_direction[1]

            # Check for collision with bugs
            if frog.tongue_out:
                for bug in bugs:
                    if bug.is_visible() and bug.intersects_with_line(tongue_start_x, tongue_start_y, tongue_end_x,
                                                                     tongue_end_y):
                        pygame.mixer.music.stop()
                        bee_sting_sound.play()
                        # Display "Game Over" message and exit game loop
                        font = pygame.font.Font(None, 60)
                        game_over_text = font.render("Game Over", True, RED)
                        game_over_text_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                        win.blit(game_over_text, game_over_text_rect)
                        pygame.display.flip()
                        pygame.time.wait(3000)  # Wait for 3 seconds before exiting
                        run = False

            # Check for collision with food
            for food in foods[:]:
                if food.intersects_with_line(tongue_start_x, tongue_start_y, tongue_end_x, tongue_end_y):
                    foods.remove(food)  # Remove food if it collides with the tongue
                    food_counter += 1
                    frog_eat_sound.play()

            # Display the food counter on the screen
            font = pygame.font.Font(None, 30)
            counter_text = font.render("Food Count: " + str(food_counter), True, BLACK)
            win.blit(counter_text, (10, 10))

            pygame.display.flip()

    else:
        if level is None:
            print("Please select level properly")
        else:
            print("Please select mode properly")

    pygame.quit()


def game_intro():
    intro = True
    clock = pygame.time.Clock()

    pygame.mixer.music.load("audio_files/music.mp3")  # Replace with the path to your background music file
    pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
    pygame.mixer.music.set_volume(0.5)  # Set the volume between 0.0 and 1.0

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                intro = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            intro = False

        win.blit(background_image, (0, 0))  # Draw the background
        font = pygame.font.Font(None, 60)
        text = font.render("Feed Frog", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 8))  # Adjust the y-coordinate here
        win.blit(text, text_rect)

        font = pygame.font.Font(None, 30)
        start_text = font.render("Press Enter to start", True, BLACK)
        start_text_rect = start_text.get_rect(center=(WIDTH / 2, HEIGHT / 8 + 70))
        win.blit(start_text, start_text_rect)

        pygame.display.flip()
        clock.tick(30)


def select_level():
    level_selection = True
    clock = pygame.time.Clock()
    level = None

    pygame.mixer.music.load("audio_files/music.mp3")  # Replace with the path to your background music file
    pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
    pygame.mixer.music.set_volume(0.5)  # Set the volume between 0.0 and 1.0

    while level_selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                level_selection = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            level_selection = False

        font = pygame.font.Font(None, 30)

        # Level selection
        level_text = font.render("Select a level:", True, BLACK)
        level_text_rect = level_text.get_rect(center=(WIDTH / 2, HEIGHT / 4 + 200))
        win.blit(level_text, level_text_rect)

        easy_text = font.render("Easy", True, BLACK)
        easy_text_rect = easy_text.get_rect(center=(WIDTH / 2, HEIGHT / 4 + 250))
        win.blit(easy_text, easy_text_rect)
        easy_rect = pygame.Rect(easy_text_rect.left - 10, easy_text_rect.top - 10, easy_text_rect.width + 20,
                                easy_text_rect.height + 20)

        medium_text = font.render("Medium", True, BLACK)
        medium_text_rect = medium_text.get_rect(center=(WIDTH / 2, HEIGHT / 4 + 300))
        win.blit(medium_text, medium_text_rect)
        medium_rect = pygame.Rect(medium_text_rect.left - 10, medium_text_rect.top - 10, medium_text_rect.width + 20,
                                  medium_text_rect.height + 20)

        hard_text = font.render("Hard", True, BLACK)
        hard_text_rect = hard_text.get_rect(center=(WIDTH / 2, HEIGHT / 4 + 350))
        win.blit(hard_text, hard_text_rect)
        hard_rect = pygame.Rect(hard_text_rect.left - 10, hard_text_rect.top - 10, hard_text_rect.width + 20,
                                hard_text_rect.height + 20)

        progression_text = font.render("Progression", True, BLACK)
        progression_text_rect = progression_text.get_rect(center=(WIDTH / 2, HEIGHT / 4 + 400))
        win.blit(progression_text, progression_text_rect)
        progression_rect = pygame.Rect(progression_text_rect.left - 10, progression_text_rect.top - 10,
                                       progression_text_rect.width + 20, progression_text_rect.height + 20)

        # Check for level selection
        mouse_pos = pygame.mouse.get_pos()
        if easy_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                level = "Easy"
                level_selection = False
        elif medium_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                level = "Medium"
                level_selection = False
        elif hard_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                level = "Hard"
                level_selection = False
        elif progression_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                level = "Progression"
                level_selection = False

        pygame.display.flip()
        clock.tick(30)

    return level


def select_mode():
    mode_selection = True
    clock = pygame.time.Clock()
    mode = None

    pygame.mixer.music.load("audio_files/music.mp3")  # Replace with the path to your background music file
    pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
    pygame.mixer.music.set_volume(0.5)  # Set the volume between 0.0 and 1.0

    while mode_selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mode_selection = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            mode_selection = False

        font = pygame.font.Font(None, 30)

        # Mode selection
        mode_text = font.render("Select a mode:", True, BLACK)
        mode_text_rect = mode_text.get_rect(center=(WIDTH / 2, HEIGHT / 8 + 140))
        win.blit(mode_text, mode_text_rect)

        land_text = font.render("Land Mode", True, BLACK)
        land_text_rect = land_text.get_rect(center=(WIDTH / 2, HEIGHT / 8 + 180))
        win.blit(land_text, land_text_rect)
        land_rect = pygame.Rect(land_text_rect.left - 10, land_text_rect.top - 10, land_text_rect.width + 20,
                                land_text_rect.height + 20)

        water_text = font.render("Water Mode", True, BLACK)
        water_text_rect = water_text.get_rect(center=(WIDTH / 2, HEIGHT / 8 + 220))
        win.blit(water_text, water_text_rect)
        water_rect = pygame.Rect(water_text_rect.left - 10, water_text_rect.top - 10, water_text_rect.width + 20,
                                 water_text_rect.height + 20)

        # Check for mode selection
        mouse_pos = pygame.mouse.get_pos()
        if land_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                mode = "Land"
                mode_selection = False
        elif water_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                mode = "Water"
                mode_selection = False

        pygame.display.flip()
        clock.tick(30)

    return mode


def show_rules(level):
    rules_shown = False
    clock = pygame.time.Clock()

    pygame.mixer.music.load("audio_files/music.mp3")  # Replace with the path to your background music file
    pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
    pygame.mixer.music.set_volume(0.5)  # Set the volume between 0.0 and 1.0

    while not rules_shown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                rules_shown = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            rules_shown = True

        win.blit(background_image, (0, 0))  # Draw the background

        font = pygame.font.Font(None, 30)

        # Display game rules
        if level.lower() == "easy":
            rules_text = [
                "Game Rules for Easy Level:",
                "",
                "- Use the mouse to control the frog's tongue.",
                "- Use the keyboard left and right direction to move the frog left or right",
                "- Catch flies (in black) with the tongue to increase your food count.",
                "- Avoid touching bees (in red) with the tongue, or the game is over.",
                "- As this is easy level, the game speed will be slow.",
                "- Good luck and have fun!",
                "",
                "Click or press enter to start the game."
            ]
        elif level.lower() == "medium":
            rules_text = [
                "Game Rules for Medium Level:",
                "",
                "- Use the mouse to control the frog's tongue.",
                "- Catch flies (in black) with the tongue to increase your food count.",
                "- Avoid touching bees (in red) with the tongue, or the game is over.",
                "- As this is medium level, the game speed will be little faster.",
                "- Good luck and have fun!",
                "",
                "Click or press enter to start the game."
            ]
        elif level.lower() == "hard":
            rules_text = [
                "Game Rules for Hard Level:",
                "",
                "- Use the mouse to control the frog's tongue.",
                "- Catch flies (in black) with the tongue to increase your food count.",
                "- Avoid touching bees (in red) with the tongue, or the game is over.",
                "- As this is hard level, the game speed will be very fast.",
                "- As this is hard level, the no. of bug will also be increased.",
                "It can be between 2 to 4",
                "- Good luck and have fun!",
                "",
                "Click or press enter to start the game."
            ]
        else:
            rules_text = [
                "Game Rules for Progression Level:",
                "",
                "- Use the mouse to control the frog's tongue.",
                "- Catch flies (in black) with the tongue to increase your food count.",
                "- Avoid touching bees (in red) with the tongue, or the game is over.",
                "- As this is progression level, the game speed will be gradually",
                "increased based on the food count.",
                "- As this is progression level, the no. of bug will also be increased",
                "when it reaches hard level. It can be between 2 to 4",
                "- Good luck and have fun!",
                "",
                "Click or press enter to start the game."
            ]

        y_offset = HEIGHT / 4
        for line in rules_text:
            if "(in red)" in line:
                parts = line.split("(in red)")
                for part in parts:
                    if part:
                        if part == " ":
                            continue
                        if part == parts[-1]:  # Last part of the line
                            text = font.render(part, True, BLACK)
                        else:
                            text = font.render(part, True, BLACK)
                        text_rect = text.get_rect(center=(WIDTH / 2, y_offset))
                        win.blit(text, text_rect)
                        y_offset += 30
                    if part != parts[-1]:
                        red_text = font.render("(in red)", True, RED)
                        red_text_rect = red_text.get_rect(center=(WIDTH / 2, y_offset))
                        win.blit(red_text, red_text_rect)
                        y_offset += 30
            else:
                text = font.render(line, True, BLACK)
                text_rect = text.get_rect(center=(WIDTH / 2, y_offset))
                win.blit(text, text_rect)
                y_offset += 30

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    game_intro()
    mode_selected = select_mode()
    level_selected = select_level()
    show_rules(level_selected)
    main(level_selected, mode_selected)
