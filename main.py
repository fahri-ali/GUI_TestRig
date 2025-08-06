from pathlib import Path

from tkinter import ttk, Tk, Canvas, Entry, Text, Button, PhotoImage, Label, Menu, messagebox, StringVar, OptionMenu

import os  # For handling directories
from datetime import datetime  # For generating unique filenames
import RPi.GPIO as GPIO
from PIL import Image, ImageTk  # Used to handle images in Tkinter
import time

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

import cv2

#====================================================================================
# Initial position of the drone within the map area
drone_x, drone_y = 212.0, 361.0  # Starting coordinates for image_drone
map_left, map_top = 195.0, 42.0  # Map's left and top boundaries
map_right, map_bottom = 525.0, 380.0  # Map's right and bottom boundaries
move_distance = 19  # Distance the drone moves per button press
circle_radius = 10
clicked_points = []
markers = []
step_delay = 0.05
is_drawing = False

# Setup GPIO pins for stepper motors
# Stepper motor 1
DIR1 = 20  # Direction pin for stepper 1
STEP1 = 21  # Step pin for stepper 1

# Stepper motor 2
DIR2 = 16  # Direction pin for stepper 2
STEP2 = 26  # Step pin for stepper 2

# Stepper motor 3
DIR3 = 25  # Direction pin for stepper 3
STEP3 = 24  # Step pin for stepper 3

#Stepper motor 4 Z axis
DIR4 = 5
STEP4 = 6

#Stepper motor 5 Z Axis
DIR5 = 13
STEP5 = 19

## Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([DIR1, STEP1, DIR2, STEP2, DIR3, STEP3, DIR4, STEP4, DIR5, STEP5], GPIO.OUT)

# Define step delay (speed of stepper motor)
STEP_DELAY = 0.001

def stepper_move_up_down(direction4, direction5, steps, motor4, motor5):
    # Set direction for motor4
    if motor4 == 1:
        GPIO.output(DIR4, GPIO.HIGH if direction4 == 'cw' else GPIO.LOW)
    elif motor4 == 2:
        GPIO.output(DIR5, GPIO.HIGH if direction4 == 'cw' else GPIO.LOW)
    
    # Set direction for motor5
    if motor5 == 1:
        GPIO.output(DIR4, GPIO.HIGH if direction5 == 'cw' else GPIO.LOW)
    elif motor5 == 2:
        GPIO.output(DIR5, GPIO.HIGH if direction5 == 'cw' else GPIO.LOW)

    # Move both motors simultaneously
    for _ in range(steps):
        if motor4 == 1 or motor5 == 1:
            GPIO.output(STEP4, GPIO.HIGH)
        if motor5 == 2 or motor4 == 2:
            GPIO.output(STEP5, GPIO.HIGH)

        time.sleep(STEP_DELAY)

        if motor4 == 1 or motor5 == 1:
            GPIO.output(STEP4, GPIO.LOW)
        if motor5 == 2 or motor4 == 2:
            GPIO.output(STEP5, GPIO.LOW)

        time.sleep(STEP_DELAY)
#================================================================================

current_frame = None

#cap = cv2.VideoCapture(0)

# Function to capture and display webcam stream without face detection
#def update_frame():
#    global current_frame
#    _, frame = cap.read()
#    frame = cv2.resize(frame, (170, 120))  # Resize jika frame valid

    # Convert the frame back to RGB and display it in the Tkinter window
#    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB format
#    img = Image.fromarray(cv2image)  # Convert image to PIL format
#    imgtk = ImageTk.PhotoImage(image=img)  # Convert image to ImageTk format
#
#    video_label.imgtk = imgtk  # Set the label's image
#    video_label.configure(image=imgtk)  # Update the image in the label

    # Store the current frame for capturing
#    current_frame = frame

#    video_label.after(10, update_frame)  # Update frame every 10ms
# Function to capture the current frame and display it in image_2
    
def clear_focus(event):
    window.focus()

window = Tk()

window.geometry("720x405")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 405,
    width = 720,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    90.0,
    320.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    90.0,
    299.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    89.0,
    341.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    111.0,
    320.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    69.0,
    319.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    360.0,
    215.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    360.0,
    19.0,
    image=image_image_7
)

#dropdown mode
mode_dropdown = ttk.Combobox(window, values=["manual", "otomatis"], font=("Montserrat Regular", 10), width=6, state="readonly")
mode_dropdown.place(x=33.0, y=10.0)
mode_dropdown.set("manual")

# Bind the selection event to clear focus after selecting an item
mode_dropdown.bind("<<ComboboxSelected>>", clear_focus)

#dropdown wahana
wahana_dropdown = ttk.Combobox(window, values=["Phantom 3 Pro", "mavic 2 pro"], font=("Montserrat Regular", 10), width=12, state="readonly")
wahana_dropdown.place(x=1090.0, y=27.0)
wahana_dropdown.set("Phantom 3 Pro")

# Bind the selection event to clear focus after selecting an item
wahana_dropdown.bind("<<ComboboxSelected>>", clear_focus)
#=======================================================


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=94.5,
    y=18.0,
    width=3.9375,
    height=4.5
)

video_label = Label(window)
video_label.place(
    x=10.0,
    y=50.0,
    width=170.0,
    height=120.0
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    625.0,
    109.625,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    625.3125,
    294.40625,
    image=image_image_10
)

canvas.create_text(
    66.0,
    173.0,
    anchor="nw",
    text="Camera View",
    fill="#000000",
    font=("Montserrat Bold", 8 * -1)
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    23.9375,
    19.4375,
    image=image_image_11
)

#drone
image_image_drone = PhotoImage(
    file=relative_to_assets("image_drone.png"))
image_drone = canvas.create_image(
    212.0,
    361.0,
    image=image_image_drone
)

canvas.create_text(
    597.0,
    175.0,
    anchor="nw",
    text="Capture View",
    fill="#000000",
    font=("Montserrat Bold", 8 * -1)
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    26.0,
    272.0,
    image=image_image_13
)

canvas.create_text(
    49.0,
    267.0,
    anchor="nw",
    text="10",
    fill="#000000",
    font=("Montserrat Regular", 12 * -1)
)

canvas.create_text(
    61.0,
    266.0,
    anchor="nw",
    text="(m/s)",
    fill="#000000",
    font=("Montserrat Regular", 12 * -1)
)

canvas.create_text(
    61.0,
    213.0,
    anchor="nw",
    text="(m)",
    fill="#000000",
    font=("Montserrat Regular", 12 * -1)
)

canvas.create_text(
    16.0,
    249.0,
    anchor="nw",
    text="SPEED",
    fill="#000000",
    font=("Montserrat Bold", 10 * -1)
)

canvas.create_text(
    16.0,
    196.0,
    anchor="nw",
    text="ALTITUDE",
    fill="#000000",
    font=("Montserrat Bold", 10 * -1)
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    26.0,
    217.0,
    image=image_image_14
)

#Tombol Capture
button_image_capture = PhotoImage(
    file=relative_to_assets("button_capture.png"))
button_capture = Button(
    image=button_image_capture,
    borderwidth=0,
    highlightthickness=0,
    # command=capture_image,
    relief="flat"
)
button_capture.place(
    x=73.0,
    y=372.0,
    width=42.1875,
    height=14.062499046325684
)

#Tombol Landing
button_image_landing = PhotoImage(
    file=relative_to_assets("button_landing.png"))
button_landing = Button(
    image=button_image_landing,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_altitude(0),  # ← ubah di sini
    relief="flat"
)
button_landing.place(
    x=130.0,
    y=372.0,
    width=42.1875,
    height=14.062499046325684
)

# Nilai awal altitude
altitude_value = 0

# Nilai Altitude 
altitude_text = canvas.create_text(
    49.0,
    213.0,
    anchor="nw",
    text=str(altitude_value),
    fill="#000000",
    font=("Montserrat Regular", 12 * -1)
)

def update_altitude(target, step=1, delay=500):
    global altitude_value
    if altitude_value < target:
        altitude_value += step
        if altitude_value > target:
            altitude_value = target
        canvas.itemconfig(altitude_text, text=str(altitude_value))
        canvas.after(delay, lambda: update_altitude(target, step, delay))
    elif altitude_value > target:
        altitude_value -= step
        if altitude_value < target:
            altitude_value = target
        canvas.itemconfig(altitude_text, text=str(altitude_value))
        canvas.after(delay, lambda: update_altitude(target, step, delay))

#Take Off Button
button_take_off = PhotoImage(
    file=relative_to_assets("button_take off.png"))
button_Takeoff = Button(
    image=button_take_off,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_altitude(target_altitude), # ← ubah di sini
    relief="flat"
)
button_Takeoff.place(
    x=18.000030517578125,
    y=372.0,
    width=42.1875,
    height=14.062499046325684
)

# Variabel untuk menyimpan target altitude
target_altitude = 5  # default

# Variable untuk dropdown
selected_value = StringVar()
selected_value.set("1")  # default dropdown value

# Dropdown menu angka 1–10
dropdown = OptionMenu(window, selected_value, *[str(i) for i in range(1, 11)])
dropdown.place(x=85, y=210, width=50, height=25)

def altitude_to_steps(meter):
    return int(meter * 63000)

# Tombol Set di samping dropdown
def set_target():
    global target_altitude
    target_altitude = int(selected_value.get())
    print(f"Target altitude set to {target_altitude} m")

    current_altitude = 0  # Bisa dibuat global jika perlu dilacak dinamis
    delta = target_altitude - current_altitude
    steps = altitude_to_steps(abs(delta))

    if delta > 0:
        stepper_move_up_down('cw', 'ccw', steps, 1, 2)
    elif delta < 0:
        stepper_move_up_down('ccw', 'cw', steps, 1, 2)

#Tombol Set
button_image_set = PhotoImage(
    file=relative_to_assets("button_set.png"))
button_set = Button(
    image=button_image_set,
    borderwidth=0,
    highlightthickness=0,
    command=set_target,
    relief="flat"
)
button_set.place(
    x=135.0,
    y=210.0,
    width=42.1875,
    height=14.062499046325684
)

canvas.create_text(
    565.1875,
    212.0,
    anchor="nw",
    text="RESULT",
    fill="#000000",
    font=("Montserrat Bold", 8 * -1)
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    555.0,
    217.0,
    image=image_image_15
)

button_image_up = PhotoImage(
    file=relative_to_assets("button_up.png"))
button_up = Button(
    image=button_image_up,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_up clicked"),
    relief="flat"
)
button_up.place(
    x=82.9375,
    y=290.0,
    width=14.0625,
    height=14.062499046325684
)

button_image_right = PhotoImage(
    file=relative_to_assets("button_right.png"))
button_right = Button(
    image=button_image_right,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_right clicked"),
    relief="flat"
)
button_right.place(
    x=105.87496948242188,
    y=313.5000009536743,
    width=14.0625,
    height=14.062499046325684
)

#Tombol Bawah
button_image_down = PhotoImage(
    file=relative_to_assets("button_down.png"))
button_down = Button(
    image=button_image_down,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_down clicked"),
    relief="flat"
)
button_down.place(
    x=81.9375,
    y=336.5625009536743,
    width=14.0625,
    height=14.062499046325684
)

#Tombol Kiri
button_image_left = PhotoImage(
    file=relative_to_assets("button_left.png"))
button_left = Button(
    image=button_image_left,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_left clicked"),
    relief="flat"
)
button_left.place(
    x=60.0,
    y=312.5000009536743,
    width=14.0625,
    height=14.062499046325684
)

canvas.create_text(
    109.0,
    11.0,
    anchor="nw",
    text="Rice-Field Health Monitoring Drone using Vision-Based Deep  Learning",
    fill="#000000",
    font=("Montserrat Bold", 14 * -1)
)

#====================================================================================

def stepper_move_parallel(direction1, direction2, steps, motor1, motor2):
    # Set direction for motor1
    if motor1 == 1:
        GPIO.output(DIR1, GPIO.HIGH if direction1 == 'cw' else GPIO.LOW)
    elif motor1 == 2:
        GPIO.output(DIR2, GPIO.HIGH if direction1 == 'cw' else GPIO.LOW)
    
    # Set direction for motor2
    if motor2 == 1:
        GPIO.output(DIR1, GPIO.HIGH if direction2 == 'cw' else GPIO.LOW)
    elif motor2 == 2:
        GPIO.output(DIR2, GPIO.HIGH if direction2 == 'cw' else GPIO.LOW)

    # Move both motors simultaneously
    for _ in range(steps):
        if motor1 == 1 or motor2 == 1:
            GPIO.output(STEP1, GPIO.HIGH)
        if motor2 == 2 or motor1 == 2:
            GPIO.output(STEP2, GPIO.HIGH)

        time.sleep(STEP_DELAY)

        if motor1 == 1 or motor2 == 1:
            GPIO.output(STEP1, GPIO.LOW)
        if motor2 == 2 or motor1 == 2:
            GPIO.output(STEP2, GPIO.LOW)

        time.sleep(STEP_DELAY)

# Function to control stepper motors
def stepper_move(direction, motor):
    """Moves a stepper motor in the specified direction."""
    if motor == 1:
        GPIO.output(DIR1, GPIO.HIGH if direction == 'cw' else GPIO.LOW)
        for _ in range(315):  # Adjust the range for desired movement
            GPIO.output(STEP1, GPIO.HIGH)
            time.sleep(STEP_DELAY)
            GPIO.output(STEP1, GPIO.LOW)
            time.sleep(STEP_DELAY)
    elif motor == 2:
        GPIO.output(DIR2, GPIO.HIGH if direction == 'cw' else GPIO.LOW)
        for _ in range(315):
            GPIO.output(STEP2, GPIO.HIGH)
            time.sleep(STEP_DELAY)
            GPIO.output(STEP2, GPIO.LOW)
            time.sleep(STEP_DELAY)
    elif motor == 3:
        GPIO.output(DIR3, GPIO.HIGH if direction == 'cw' else GPIO.LOW)
        for _ in range(315):
            GPIO.output(STEP3, GPIO.HIGH)
            time.sleep(STEP_DELAY)
            GPIO.output(STEP3, GPIO.LOW)
            time.sleep(STEP_DELAY)


# Function to move the drone in a specified direction, constrained by the map boundaries
def move_drone(direction):
    global drone_x, drone_y
    if direction == 'up' and drone_y - move_distance > map_top:
        drone_y -= move_distance
        stepper_move_parallel('cw', 'ccw', 315, 1, 2)
    elif direction == 'down' and drone_y + move_distance < map_bottom:
        drone_y += move_distance
        stepper_move_parallel('ccw', 'cw', 315, 1, 2)
    elif direction == 'left' and drone_x - move_distance > map_left:
        drone_x -= move_distance
        stepper_move('cw', 3)
    elif direction == 'right' and drone_x + move_distance < map_right:
        drone_x += move_distance
        stepper_move('ccw', 3)

    # Update the drone's position on the canvas
    canvas.coords(image_drone, drone_x, drone_y)

def draw_marker(event):
    """Draws a 20px marker at the right-click position within the map bounds and records the point."""
    if is_drawing and map_left <= event.x <= map_right and map_top <= event.y <= map_bottom:
        # Draw marker on canvas
        marker = canvas.create_oval(
            event.x - circle_radius, event.y - circle_radius, 
            event.x + circle_radius, event.y + circle_radius, 
            outline="red", width=2
        )
        markers.append(marker)
        # Record the point
        clicked_points.append((event.x, event.y))

def start_drawing():
    """Enables drawing mode when 'Draw' menu item is selected."""
    global is_drawing
    is_drawing = True
    messagebox.showinfo("Drawing Mode", "You can now left-click to draw markers on the map.")

def clear_markers():
    """Clears all markers and resets points list."""
    global clicked_points, markers
    for marker in markers:
        canvas.delete(marker)
    markers.clear()
    clicked_points.clear()
    messagebox.showinfo("Clear Markers", "All markers have been removed.")

def move_image_drone():
    """Move the image_drone along the recorded points sequentially."""
    for x, y in clicked_points:
        current_x, current_y = canvas.coords(image_drone)[:2]  # Get current position of image_drone
        # Move gradually to the next point
        while abs(current_x - x) > 1 or abs(current_y - y) > 1:
            # Calculate the incremental step
            step_x = (x - current_x) * 0.1
            step_y = (y - current_y) * 0.1
            current_x += step_x
            current_y += step_y
            
            # Update image_drone position
            canvas.coords(image_drone, current_x, current_y)
            
            # Update canvas and pause for smooth movement
            window.update()
            time.sleep(step_delay)

#Klik kanan pada area map
def show_context_menu(event):
    """Displays a context menu at the right-click position."""
    context_menu.post(event.x_root, event.y_root)

# Set up the context menu
context_menu = Menu(window, tearoff=0)
context_menu.add_command(label="Draw", command=start_drawing)

# Bind right-click to show the context menu
canvas.bind("<Button-3>", show_context_menu)

# Bind left-click to draw marker if in drawing mode
canvas.bind("<Button-1>", draw_marker)

# Buttons for movement and clearing markers
move_button = Button(window, text="Start Movement", command=move_image_drone)
move_button.pack()

clear_button = Button(window, text="Clear Markers", command=clear_markers)
clear_button.pack()

# Key press event handler
def on_key_press(event):
    if event.keysym == 'Up':
        move_drone('up')
    elif event.keysym == 'Down':
        move_drone('down')
    elif event.keysym == 'Left':
        move_drone('left')
    elif event.keysym == 'Right':
        move_drone('right')

# Configure the navigation buttons to control the drone's movement
button_up.config(command=lambda: move_drone('up'))
button_down.config(command=lambda: move_drone('down'))
button_left.config(command=lambda: move_drone('left'))
button_right.config(command=lambda: move_drone('right'))

# Bind the tanda panah untuk pergerakan
window.bind('<Up>', on_key_press)
window.bind('<Down>', on_key_press)
window.bind('<Left>', on_key_press)
window.bind('<Right>', on_key_press)
# window.bind('<c>', lambda event: capture_image())
#====================================================================================

# Variables for zigzag movement control
zigzag_direction = 'right'  # Initial zigzag direction
is_zigzag_active = False  # Flag to control the start and stop of automatic movement

# Zigzag movement function
def zigzag_move():
    global drone_x, drone_y, zigzag_direction, is_zigzag_active

    if not is_zigzag_active:
        return  # Stop movement if zigzag is not active

    # Move right or left based on the current zigzag direction
    if zigzag_direction == 'right':
        if drone_x + move_distance < map_right:
            drone_x += move_distance
            stepper_move('ccw', 3)
        else:
            zigzag_direction = 'left'  # Switch direction when hitting the right boundary
            drone_y -= move_distance  # Move up after reaching the boundary
            stepper_move_parallel('cw', 'ccw', 315, 1, 2)
    elif zigzag_direction == 'left':
        if drone_x - move_distance > map_left:
            drone_x -= move_distance
            stepper_move('cw', 3)
        else: 
            zigzag_direction = 'right'  # Switch direction when hitting the left boundary
            drone_y -= move_distance  # Move up after reaching the boundary
            stepper_move_parallel('cw', 'ccw', 315, 1, 2)

    # Update drone position on the canvas
    canvas.coords(image_drone, drone_x, drone_y)

    if drone_y - move_distance <= map_top:
        is_zigzag_active = False
    elif is_zigzag_active == True:
        window.after(int(step_delay * 10000), zigzag_move)

# Button to start and stop zigzag movement
def toggle_zigzag():
    global is_zigzag_active
    is_zigzag_active = not is_zigzag_active  # Toggle the zigzag flag
    if is_zigzag_active:
        window.after(100, zigzag_move)

# Button for starting zigzag movement
zigzag_button = Button(window, text="Start Zigzag", command=toggle_zigzag)
zigzag_button.pack()

# Bind the 'S' key to start the zigzag movement
# window.bind('<s>', start_zigzag)

import threading

def start_zigzag_thread():
    zigzag_thread = threading.Thread(target=zigzag_move)
    zigzag_thread.start()

def clear_markers():
    global clicked_points
    clicked_points.clear()
    canvas.delete("all")  # Clears all markers

def cleanup_gpio():
    GPIO.cleanup()
    window.destroy()

#update_frame()

window.resizable(False, False)
window.mainloop()
