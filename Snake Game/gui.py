import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.resizable(0, 0)
root.title("Snake")
root.iconbitmap(r"icons\root_icon.ico")

frame = tk.Frame(root, width=500, height=130)
frame.grid_propagate(0)
frame.grid(row=0, column=0)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

grid_canvas = tk.Canvas(root, width=500, height=500, highlightthickness=0, bg="black")
grid_canvas.grid(row=1, column=0)

img1_og = Image.open(r"icons\settings_icon.png").resize((27, 27))
img1_tk = ImageTk.PhotoImage(img1_og)
settings_button = tk.Button(frame, image=img1_tk, state="disabled")
settings_button.grid(row=0, column=0)

img2_og = Image.open(r"icons\pause_icon.png").resize((27, 27))
img2_tk = ImageTk.PhotoImage(img2_og)
pause_button = tk.Button(frame, image=img2_tk)
pause_button.grid(row=0, column=1)

restart_button = tk.Button(frame, width=12, font=("Arial", 13, "bold"), text="Restart", state="disabled")
restart_button.grid(row=0, column=2, sticky="NW")

label = tk.Label(frame, text="0", font=("Arial", 23, "bold"), height=4)
label.grid(row=1, column=0, columnspan=3, sticky="ESW")

root.update()