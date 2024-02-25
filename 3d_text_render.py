import turtle as trtl
import string
import math

# --- Configuration Variables ---

# Starting (preview) quality
quality = 10
# Quality for rendering (Enter key)
good_quality = 1
# Font size of the text (bigger will be slower)
font_size = 200
# Font settings
font = ("Arial", font_size, "bold")
# The depth (perspective) of the text
# Larger values will be slower, and could have visual issues
text_depth = 1.0
# The color of light. Will not affect highlights
light_color = (250, 250, 240)
# The radius (size) of the light
light_radius = 500
# The color of the text
text_color = (80, 0, 0)
# The color of text at base depth
text_color_dark = (10, 0, 0)
# White color. Used with highlights
white = (255, 255, 255)
# Gray color. Used with highlights
gray = (100, 100, 100)
# Black color. Used with shadows
black = (0, 0, 0)
# The center of the perspective view
perspective_center = (0, -800)

# --- Internal Variables ---

# The location of the cursor, location of the light and new text
cursor_location = (0, 0)
# The list of typed letters and their locations on screen
letter_list = []
# A sorted version of the letter list, sorted by distance away from perspective center
sorted_letter_list = []

# --- Turtle Setup ---

wn = trtl.Screen()
wn.bgcolor("black")

turtle = trtl.Turtle()
turtle.speed(0)
trtl.colormode(255)
turtle.penup()
trtl.tracer(0, 0)
turtle.hideturtle()

# --- Helper Functions ---

# Add the values of two lists together, lists should be the same length
def add_lists(list1, list2):
    return [list1[i] + list2[i] for i in range(len(list1))]

# Subtract the values of two lists together, lists should be the same length
def subtract_lists(list1, list2):
    return [list1[i] - list2[i] for i in range(len(list1))]

# Get the difference of values between two lists. Lists should be the same length.
def get_offset(location1, location2, multiplier=1):
    difference = subtract_lists(location1, location2)
    return [difference[0] * multiplier, difference[1] * multiplier]

# Get the distance between two locations
def get_distance(location1, location2, multiplier=1):
    return math.sqrt((location2[0]-location1[0])**2 + (location2[1]-location1[1])**2) * multiplier

# Normalize a list of an unknown range of values to a range between -1 and 1
def normalize(list, multiplier=1):
    max_value = max([abs(i) for i in list])
    # Edge case, lists of only zeros will cause a division by zero error
    if max_value == 0:
        return list
    return [i / max_value * multiplier for i in list]

# Linear interpolation between two lists given a current and end index, returns a list of floats
def lerp_float(start_list, end_list, current_index, end_index):
    percent = current_index / end_index

    return [end_list[i] * percent + start_list[i] * (1 - percent) for i in range(len(start_list))]

# Linear interpolation between two lists given a current and end index, returns a list of ints
def lerp_int(start_list, end_list, current_index, end_index):
    percent = current_index / end_index

    return [math.floor(end_list[i] * percent + start_list[i] * (1 - percent)) for i in range(len(start_list))]

# Get the base depth location from a starting location, generates the perspective effect
def get_depth_end_location(location):
    offset = get_offset(perspective_center, location, 0.05*(font_size / 150)*text_depth)
    return add_lists(location, offset)

# Sort the letter list by distance away from perspective center
# Sorting the list this way mostly solves the issue of text rendering out of order and causing visual issues
def create_sorted_list():
    global sorted_letter_list
    sorted_letter_list = letter_list.copy()
    sorted_letter_list.sort(key=lambda x: (abs(x[1][0]) + abs(cursor_location[0])) + (abs(x[1][1]) + abs(cursor_location[1])), reverse=True)

# --- Drawing Functions ---

# Draws the background light based off of selected quality and light radius
def draw_background_light():
    # Modified based on current quality, higher number quality (lower quality) will be less iterations
    light_iterations = light_radius // quality
    # Difference in radius between each iteration
    radius_diff = light_radius / light_iterations
    color = light_color
    radius = light_radius
    for i in range(light_iterations):
        # Calculate radius in an exponential fashion to ramp up light to center
        radius = light_radius / ((i/light_iterations + 1)**7)
        # Calculate color linearly from light iterations
        color = [math.floor(light_color[c] * (i / light_iterations)) for c in range(3)]
        # Go to the circle start position (cursor location minus the current radius)
        turtle.goto(cursor_location[0], cursor_location[1] - math.floor(radius))
        turtle.pensize(radius * 2)
        turtle.pencolor(color)
        turtle.pendown()
        turtle.circle(math.floor(radius))
        turtle.penup()
    # Reset the turtle position
    turtle.goto(cursor_location)

# Draw all elements on the screen, erasing the previous elements
def draw_all():
    wn.tracer(False)
    turtle.clear()
    draw_background_light()
    draw_letters()
    wn.tracer(True)
    trtl.update()

# Draw a single letter on the screen. Called many times.
def draw_letter_single(letter, location, color):
    turtle.goto((location[0], location[1] - font_size/1.5))
    turtle.color(color)
    turtle.write(letter, align="center", font=font)

# Draw the a highlight version of the shadow, opposite of the highlight, for contrast
def draw_shadow_highlight(letter, location):
    offset = normalize(get_offset(cursor_location, location), 2)
    shadow_location = subtract_lists(location, offset)
    draw_letter_single(letter, shadow_location, black)

# Draw a highlight to make the edge of text white towards the light source
def draw_highlight(letter, location):
    offset = normalize(get_offset(cursor_location, location), 2)
    highlight_location = add_lists(location, offset)
    draw_letter_single(letter, highlight_location, white)

# Draw highlights down the side of the 3D perspective. Draws both shadow and highlight
def draw_highlights_perspective(letter, location):
    offset = normalize(get_offset(cursor_location, location), 2)
    highlight_location = add_lists(location, offset)
    draw_perspective(letter, highlight_location, get_depth_end_location(location), white, gray, 1)
    shadow_location = subtract_lists(location, offset)
    draw_perspective(letter, shadow_location, get_depth_end_location(location), black, black, 1)

# Draws the shadow on the ground that cascades away from the light source
def draw_shadow(letter, location):
    start_location = get_depth_end_location(location)
    offset = get_offset(start_location, cursor_location, 0.2)
    end_location = add_lists(start_location, offset)
    draw_perspective(letter, start_location, end_location, black, black)

# Draw a perspective from the start location to the end location.
# Cut distance is to prevent color seeping at the edge of overlapping perspective draws by skipping the first n draws
def draw_perspective(letter, location, end_location, start_color=text_color, end_color=text_color_dark, cut_distance=0):
    # Quality modifier, modifies the distance (iterations) for faster performance
    quality_mod = (quality*2) - 1
    distance = math.floor(get_distance(location, end_location, 0.6/quality_mod))
    for i in range(1 + cut_distance, distance + 1):
        # Lerp between the start and end locations to get the current location
        current_location = lerp_float(end_location, location, i, distance)
        # Lerp between the start and end colors to get hte current color
        color = lerp_int(end_color, start_color, i, distance)
        # Draw the current location
        draw_letter_single(letter, current_location, color)

# Draw all the letters on the screen
# This function will draw more or less details based on current quality
def draw_letters():
    # Draw the shadow of text first so that no overlapping occurs with other text
    if quality < 5:
        for letter, location in sorted_letter_list:
            draw_shadow(letter, location)
    
    for letter, location in sorted_letter_list:
        if quality < 3:
            # Draw the highlights and shadows of the perspective letter
            draw_highlights_perspective(letter, location)
        
        if quality < 11:
            # Draw the shadow highlight (black contrast) below the perspective
            draw_shadow_highlight(letter, location)

        if quality < 8:
            # Draw the perspective of the letter
            draw_perspective(letter, location, get_depth_end_location(location))
        
        # Finally, draw the highlight and top letter
        draw_highlight(letter, location)
        draw_letter_single(letter, location, text_color)

# --- Input Functions ---

# Change the cursor location and re-draw everything
def move_cursor(x, y):
    global cursor_location
    cursor_location = (x, y)
    draw_all()

# Write a letter, add it to the letters list
def write_letter(letter):
    letter_list.append([letter, cursor_location])
    create_sorted_list()
    move_cursor(cursor_location[0] + font_size/1.2, cursor_location[1])

# Undo a letter by deleting the last added letter from the letters list
def undo():
    # If letter list is empty, return
    if not letter_list:
        return
    # Store location in a variable for later to move cursor back to it
    location = letter_list[-1][1]
    del letter_list[-1]
    # Recreate the sorted list to update the text on screen
    create_sorted_list()
    # Move the cursor to the old location
    move_cursor(location[0], location[1])

# Returns a function that calls write_letter() with the letter parameter
# This is called a closure, as it stores the letter parameter in the nested function when returned
def keypress(letter):
    def fun():
        write_letter(letter)
    return fun

# Set the quality to the good quality to render the screen in full quality
def set_quality():
    global quality
    quality = good_quality
    draw_all()

# Called when the mouse is clicked. Calls move_cursor
def click_mouse(x, y):
    move_cursor(x, y)

# Initialize all key press events. 
# There is no good way to initialize a key press for all keys, so a loop must be used
# to initialize all printable characters. 
# Slice characters from string.printable that aren't wanted. (Enter, backspace, etc)
for key in string.printable[:74] + string.printable[75:94]:
    wn.onkeypress(keypress(key), key)

#Initialize the mouse click event
trtl.onscreenclick(click_mouse)

# Initialize key press events for return (render) and backspace (undo)
wn.onkeypress(set_quality, "Return")
wn.onkeypress(undo, "BackSpace")

# Draw the screen
draw_all()

# Listen for the registered events, start the program
wn.listen()
wn.mainloop()