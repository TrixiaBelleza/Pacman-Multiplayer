import backend_chat
import tkinter
from tkinter import *
from tkinter import messagebox

# MAIN WINDOW FUNCTIONS =============================================================================================

def pacman_window():
	tk_window = tkinter.Tk()
	tk_window.title("PROJECT")
	tk_window.geometry("500x500") 
	tk_window.configure(bg="BLACK",padx=50, pady=50)
	return tk_window

def main():
	window = pacman_window()
	main_chat()
	return window

def show_About():
	messagebox.showinfo("ABOUT", "This game is brought to you by:\nTrixia, Jesi, Mark, and Kianne")

def show_Instructions():
	messagebox.showinfo("INSTRUCTIONS", "To play the game, ...")

def exit_Game():
	prompt = messagebox.askyesno("EXIT", "Are you sure you want to exit? No data will be saved.")
	if prompt == True:
		window.destroy()

# GAME ENVIRONMENT ==================================================================================================

def game_map(chosen_map):
	global frame
	frame = Frame(window, bg="BLACK", pady=50)
	
	map_template = None
	if chosen_map == 1:
		map_template = open("map1.txt", "r")
		map_name = "Map 1"
	if chosen_map == 2:
		map_name = "Map 3"
	if chosen_map == 3:
		map_name = "Easy 3"

	if map_template == None:
		messagebox.showerror("ERROR", "File not found.")
		return

	global map_matrix
	map_matrix = []
	
	for lines in map_template:
		line = []
		line[0:len(lines)] = iter(lines)
		map_matrix.append(line)	

	main_frame.pack_forget()
	create_Map()
	
	global optionsFrm
	optionsFrm = Frame(window, bg="BLACK", pady=5)

	map_name_lbl = Label(optionsFrm, text=map_name, bg="#80dba6", padx=15)
	map_name_lbl.grid(column=0, row=0, padx=40)	
	
	global Back_btn
	Back_btn = Button(optionsFrm, text="MAIN MENU",bg="sky blue", padx=15, command=back)
	Back_btn.grid(column=1, row=0, padx=40)	
	
	optionsFrm.pack()
	frame.pack()
	map_template.close()

def get_Player_pos():
	global player_xpos
	global player_ypos
	for row in range(len(map_matrix)):
		for col in range(len(map_matrix[row])):
			if map_matrix[row][col] == "P":	# PLAYER
				player_xpos = row
				player_ypos = col

def create_Map():
	block_height = 20 * len(map_matrix)
	block_width = 20 * len(map_matrix[0])
	global canvas
	canvas = tkinter.Canvas(frame, bg="BLACK", height=block_height, width=block_width)
	
	y_pos = 0 # starting pixel in canvas
	increment = 20 # to determine next position
	for row in range(len(map_matrix)):
		x_pos = 0
		for col in range(len(map_matrix[row])):
			if map_matrix[row][col] == "D":		# PAC-DOT
				block = canvas.create_oval(x_pos+8, y_pos+8, x_pos-8+increment, y_pos-8+increment, fill="WHITE", outline="")
			elif map_matrix[row][col] == "s":	# STAR
				ax = x_pos+(increment/2), 
				ay = y_pos
				bx = x_pos+1
				by = y_pos+(increment/3)
				cx = x_pos+(increment/5)
				cy = y_pos+increment
				dx = x_pos+(increment/5)*4
				dy = y_pos+increment
				ex = x_pos+increment
				ey = y_pos+(increment/3)
				block = canvas.create_polygon(ax, ay, cx, cy, ex, ey, bx, by, dx, dy, fill="YELLOW", outline="")
			elif map_matrix[row][col] == "w":	# WALL
				block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLUE", outline="")
			elif map_matrix[row][col] == "e":	# EMPTY FLOOR
				block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLACK", outline="")
			elif map_matrix[row][col] == "P":	# PLAYER
				block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="RED", outline="")
			x_pos += increment
		y_pos += increment
	
	canvas.bind_all("<KeyPress>", key_listeners) # binds event listener to whole canvas
	canvas.pack()

def key_listeners(event):
	get_Player_pos()
	# PWEDE PA ATA MAPAIKLI PA HAHA
	if event.keysym == "Left":
		if map_matrix[player_xpos][player_ypos-1] == "D" or map_matrix[player_xpos][player_ypos-1] == "s" or map_matrix[player_xpos][player_ypos-1] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos][player_ypos-1] = "P"
	elif event.keysym == "Right": # Right
		if map_matrix[player_xpos][player_ypos+1] == "D" or map_matrix[player_xpos][player_ypos+1] == "s" or map_matrix[player_xpos][player_ypos+1] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos][player_ypos+1] = "P"
	elif event.keysym == "Up":
		if map_matrix[player_xpos-1][player_ypos] == "D" or map_matrix[player_xpos-1][player_ypos] == "s" or map_matrix[player_xpos-1][player_ypos] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos-1][player_ypos] = "P"
	elif event.keysym == "Down":
		if map_matrix[player_xpos+1][player_ypos] == "D" or map_matrix[player_xpos+1][player_ypos] == "s" or map_matrix[player_xpos+1][player_ypos] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos+1][player_ypos] = "P"
	
	# BAD IMPLEMENTATION PA TO BC BUONG MAP YUNG BINABAGO HAHAHA
	canvas.pack_forget()
	create_Map()

def back():
	prompt = messagebox.askyesno("ARE YOU SURE YOU WANT TO GO BACK?", "Once you go back to the main menu, \n your game will be lost.")
	if prompt == True:
		frame.destroy()
		optionsFrm.destroy()
		main_frame.pack()

# MAIN ==============================================================================================================

window = main()
window.resizable(width=FALSE, height=FALSE)
main_frame = Frame(window, bg="BLACK", padx=50, pady=50, )
main_frame.pack_propagate(False)
main_frame.pack()

# MAIN WINDOW WIDGETS ===============================================================================================

PickLbl = Label(main_frame, text="Please choose\na game map", bg="BLACK", fg="#e07b6a", font=("Arial Bold",14))
PickLbl.grid(column=0, row=0, padx=10, pady=10, ipadx=30, ipady=10, columnspan=3)
game_map1btn = Button(main_frame, bg='#80dba6', fg="#302727", text="Map 1", command=lambda main_frame=1:game_map(main_frame))
game_map2btn = Button(main_frame, bg='#80dba6', fg="#302727", text="Map 2", command=lambda main_frame=2:game_map(main_frame))
game_map3btn = Button(main_frame, bg='#80dba6', fg="#302727", text="Map 3", command=lambda main_frame=3:game_map(main_frame))
game_map1btn.grid(column=0, row=2, padx=1, pady=10, ipadx=9, ipady=10)
game_map2btn.grid(column=1, row=2, padx=1, pady=10, ipadx=9, ipady=10)
game_map3btn.grid(column=2, row=2, padx=1, pady=10, ipadx=9, ipady=10)

about_btn = Button(main_frame, text="About", command=show_About)
about_btn.grid(column=0, row=3, padx=10, ipadx=5, pady=25, ipady=6, sticky=SE)
how_btn = Button(main_frame, text="Instructions", command=show_Instructions)
how_btn.grid(column=1, row=3, padx=10, ipadx=5, pady=25, ipady=6, sticky=SE)
exit_btn = Button(main_frame, text="Exit", command=exit_Game)
exit_btn.grid(column=2, row=3, padx=10, ipadx=10, pady=25, ipady=6, sticky=SE)

#====================================================================================================================

window.mainloop()

# FOR REFERENCE, PLEASE READ:
# Shipman, John W. "Tkinter 8.5 reference: a GUI for." 31 December 2013. New Mexico Tech Computer Center. Web / PDF.
