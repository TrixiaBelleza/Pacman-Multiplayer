import tkinter
from PIL import Image, ImageTk, ImageSequence

class Green:
	def __init__(self,parent,canvas,x,y,keysym):
		self.parent = parent
		self.canvas = canvas

		if keysym == "Left":
			self.sequence = [ImageTk.PhotoImage(img)
				for img in ImageSequence.Iterator(Image.open(r"sprites/green/left_green_pacman.gif")
				)]
		elif keysym == "Right":
			self.sequence = [ImageTk.PhotoImage(img)
				for img in ImageSequence.Iterator(Image.open(r"sprites/green/right_green_pacman.gif")
				)]
		elif keysym == "Up":
			self.sequence = [ImageTk.PhotoImage(img)
				for img in ImageSequence.Iterator(Image.open(r"sprites/green/up_green_pacman.gif")
				)]
		elif keysym == "Down":
			self.sequence = [ImageTk.PhotoImage(img)
				for img in ImageSequence.Iterator(Image.open(r"sprites/green/down_green_pacman.gif")
				)]

		self.image = self.canvas.create_image(x,y, image = self.sequence[0])
		self.animate(1)

	def animate(self, counter):
		self.canvas.itemconfig(self.image, image = self.sequence[counter])
		self.parent.after(300, lambda: self.animate((counter+1) % len(self.sequence)))