import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename

# The background color everywhere
global_bg_color = "#21252b"
# The color used for buttons and text boxes
lighter_color = "#282c34"
# The color of all text
text_color = "#cccccc"
# The color of a pressed button
pressed_button_color = "#404859"
# The size of the padding between buttons
pad_size = 5
# The font used on all sidebar elements
sidebar_font = ("Segoe UI", 12)
# The configuration for all buttons
button_config = {
    "compound": "center",
    "font": sidebar_font, 
    "bd": 2, 
    "relief": tk.FLAT,
    "cursor": "hand2",
    "bg": lighter_color,
    "fg": text_color,
    "activebackground": pressed_button_color,
    "activeforeground": text_color,
    "width": 40}

# Runs a provided command using subprocess and outputs it to the text box
def do_command(command):
    global command_textbox, url_entry
    
    command_textbox.config(state=tk.NORMAL)
    command_textbox.delete(1.0, tk.END)
    command_textbox.insert(tk.END, command + " working....\n")
    command_textbox.update()

    # If url_entry is blank, use localhost IP address 
    url_val = url_entry.get()
    if (len(url_val) == 0):
        # url_val = "127.0.0.1"
        url_val = "::1"
    
    # use url_val 
    p = subprocess.Popen(command + ' ' + url_val, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #v2
    
    cmd_results, cmd_errors = p.communicate()
    command_textbox.insert(tk.END, cmd_results)
    command_textbox.insert(tk.END, cmd_errors)
    command_textbox.config(state=tk.DISABLED)

# Saves text currently in the command textbox to a file
def save_command_text():
    filename = asksaveasfilename(defaultextension='.txt', filetypes = (
        ('Text files', '*.txt'),
        ('Python files', '*.py *.pyw'),
        ('All files', '*.*')))
    if filename is None:
        return
    file = open (filename, mode = 'w')
    text_to_save = command_textbox.get("1.0", tk.END)
  
    file.write(text_to_save)
    file.close()

root = tk.Tk()
root.configure(background=global_bg_color) # Change the global background color
root.title("Networking Utilities") # Set the title of the window
sidebar_frame = tk.Frame(root, bg=global_bg_color, padx=pad_size)
sidebar_frame.pack(fill=tk.Y, side=tk.LEFT, expand=False)

# Makes a button that runs the ping command
ping_btn = tk.Button(sidebar_frame, button_config, 
    text="Check to see if a URL is up and active", 
    command=lambda:do_command("ping"))
ping_btn.pack(side=tk.TOP, pady=pad_size)

# Makes a button that runs the tracert command
tracert_btn = tk.Button(sidebar_frame, button_config,
    text="Trace the path of a packet to the host", 
    command=lambda:do_command("tracert"))
tracert_btn.pack(side=tk.TOP)

# Makes a button that runs the nslookup command
nslookup_btn = tk.Button(sidebar_frame, button_config, 
    text="Query nameserver for the host IP addresses", 
    command=lambda:do_command("nslookup"))
nslookup_btn.pack(side=tk.TOP, pady=pad_size)

# Makes a button that runs the save function
save_btn = tk.Button(sidebar_frame, button_config, 
    text="Save results", 
    command=save_command_text)
save_btn.pack(side=tk.BOTTOM, pady=pad_size)

 # creates the frame with label for the text box
frame_URL = tk.Frame(sidebar_frame, pady=pad_size * 2, width=50, bg=global_bg_color)
frame_URL.pack()

# Decorative label for entering a URL
url_label = tk.Label(frame_URL, text="Enter a URL: ", 
    compound="center",
    font=sidebar_font,
    relief=tk.FLAT, 
    fg=text_color,
    bg=global_bg_color)
url_label.pack(side=tk.LEFT)

# URL entry box for specifying a URL to use in commands
url_entry= tk.Entry(frame_URL, 
    width=25, 
    font=sidebar_font, 
    background=lighter_color, 
    foreground=text_color, 
    relief=tk.FLAT)
url_entry.pack(side=tk.LEFT)

# Adds an output box to GUI
command_textbox = tksc.Text(root, 
    width=70, 
    height=30, 
    background=lighter_color, 
    foreground=text_color, 
    relief=tk.FLAT, 
    padx=pad_size)
command_textbox.insert(tk.END, "Waiting for input...")
command_textbox.config(state=tk.DISABLED)
command_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop() 