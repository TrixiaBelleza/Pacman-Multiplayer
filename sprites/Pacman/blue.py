import tkinter
from PIL import Image, ImageTk, ImageSequence

class Blue:
	def __init__(self,parent,canvas,x,y,keysym):
		self.parent = parent
		self.canvas = canvas

		if keysym == "Left":
			self.sequence = [ImageTk.PhotoImage(img)
				for img in ImageSequence.Iterator(Image.open(r"sprites/blue/left_blue_pacman.gif")
				)]
		elif keysym == "Right":
			self.sequence = [ImageTk.PhotoImage(img)
				for img in ImageSequence.Iterator(Image.open(r"sprites/blue/right_blue_pacman.gif")
				)]
		elif keysym == "Up":
			self.sequence = [ImageTk.PhotoImage(img)
				for img in ImageSequence.Iterator(Image.open(r"sprites/blue/up_blue_pacman.gif")
				)]
		elif keysym == "Down":
			self.sequence = [ImageTk.PhotoImage(img)
				for img in ImageSequence.Iterator(Image.open(r"sprites/blue/down_blue_pacman.gif")
				)]

		self.image = self.canvas.create_image(x,y, image = self.sequence[0])
		self.animate(1)

	def animate(self, counter):
		self.canvas.itemconfig(self.image, image = self.sequence[counter])
		self.parent.after(300, lambda: self.animate((counter+1) % len(self.sequence)))