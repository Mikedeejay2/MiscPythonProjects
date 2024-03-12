# a121_catch_a_turtle.py
#-----import statements-----
import turtle as trtl
import random as rand

#-----game configuration-----
spot_color = "pink"
spot_size = 2
spot_shape = "circle"
score = 0
font_setup = ("Arial", 20, "normal")
timer = 30
counter_interval = 1000
timer_up = False
background_color = "aliceblue"
colors = ["red", "blue", "green", "yellow", "orange", "purple"]
sizes = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 1.1, 1.2, 1.3, 1.4, 1.5]

#-----initialize turtle-----
spot = trtl.Turtle()
spot.fillcolor(spot_color)
spot.shape(spot_shape)
spot.shapesize(spot_size)

score_writer = trtl.Turtle()
score_writer.penup()
score_writer.hideturtle()
score_writer.goto(-400, 300)

counter = trtl.Turtle()
counter.penup()
counter.hideturtle()
counter.goto(400, 300)

#-----game functions-----
def spot_clicked(x, y):
    if timer_up is False:
        add_color()
        change_size()
        change_position()
        update_score()
    else:
        spot.hideturtle()

def change_position():
    new_xpos = rand.randint(-400, 400)
    new_ypos = rand.randint(-300, 300)
    spot.penup()
    spot.goto(new_xpos, new_ypos)
    spot.pendown()

def update_score():
    global score
    score += 1
    score_writer.clear()
    score_writer.write(score, font=font_setup)

def countdown():
    global timer, timer_up
    counter.clear()
    if timer <= 0:
        counter.write("Time's up", font=font_setup)
        timer_up = True
    else:
        counter.write("Timer: " + str(timer), font=font_setup)
        timer -= 1
        counter.getscreen().ontimer(countdown, counter_interval)

def add_color():
    rand_color = rand.choice(colors)
    spot.fillcolor(rand_color)
    spot.stamp()
    spot.fillcolor(spot_color)

def change_size():
    rand_size = rand.choice(sizes)
    spot.shapesize(rand_size)

def start_game():
    spot.onclick(spot_clicked)
    countdown()

#-----events-----
start_game()

wn = trtl.Screen()
wn.bgcolor(background_color)
wn.mainloop()
