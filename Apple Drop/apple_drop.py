#    a123_apple_1.py
import turtle as trtl
import random as rand

#-----setup-----
apple_image = "apple.gif"
pear_image = "pear.gif"

wn = trtl.Screen()
# wn.setup(width=1.0, height=1.0)
wn.addshape(apple_image)
wn.addshape(pear_image)
wn.bgpic("background.gif")

font_size = 30
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
number_of_apples = 5
apples = []
apple_letters = []

#-----functions-----
# given a turtle, set that turtle to be shaped by the image
def draw_apple(active_apple, letter):
    active_apple.shape(apple_image)
    active_apple.showturtle()
    write_letter(active_apple, letter)
    wn.update()

# Make the apple fall to the ground
def fall_to_ground(active_apple):
    active_apple.clear()
    active_apple.goto(active_apple.xcor(), -150)

# Write a letter on top of an apple given the apple and the letter
def write_letter(active_apple, letter):
    wn.tracer(False)
    active_apple.clear()
    active_apple.goto(active_apple.xcor(), active_apple.ycor() - font_size)
    active_apple.color("white")
    active_apple.write(letter, align="center", font=("Arial", font_size, "bold"))
    active_apple.goto(active_apple.xcor(), active_apple.ycor() + font_size)
    wn.tracer(True)

# Remove an apple and its corresponding letter
def remove_apple(active_apple, letter):
    active_apple.hideturtle()
    letters.append(letter)
    apples.remove(active_apple)
    apple_letters.remove(letter)

# Respawn an apple, assigning it a new letter as well
def respawn_apple(active_apple):
    if len(letters) == 0:
        return
    wn.tracer(False)
    active_apple.goto(rand.randint(-150, 150), rand.randint(-50, 150))
    wn.tracer(True)
    letter = letters.pop(rand.randint(0, len(letters)-1))
    apples.append(active_apple)
    apple_letters.append(letter)
    draw_apple(active_apple, letter)

# Receive a keypress of a specified letter
def press_letter(letter):
    if letter in apple_letters:
        active_apple = apples[apple_letters.index(letter)]
        fall_to_ground(active_apple)
        remove_apple(active_apple, letter)
        respawn_apple(active_apple)

# Keypress initialization function that uses closures to create a new function for a keypress
def keypress(letter):
    def fun():
        press_letter(letter)
    return fun

#-----function calls-----
# Generate keypress functions
for i in letters:
    wn.onkeypress(keypress(i), i.lower())

# Generate turtles for the number of apples and spawn them
for i in range(number_of_apples):
    apple = trtl.Turtle()
    apple.penup()
    respawn_apple(apple)

wn.listen()
wn.mainloop()