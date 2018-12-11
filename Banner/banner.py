import tkinter
from PIL import Image, ImageTk, ImageSequence

class Banner:
	def __init__(self,parent):
		self.parent = parent

		self.canvas = tkinter.Canvas(parent, width=500, height=200)
		self.canvas.pack()

		self.sequence = [ImageTk.PhotoImage(img)
			for img in ImageSequence.Iterator(
				Image.open(r"Banner/pacmen_title.gif"))] 

		self.image = self.canvas.create_image(250,100, image = self.sequence[0])
		self.animate(1)

	def animate(self, counter):
		self.canvas.itemconfig(self.image, image = self.sequence[counter])
		self.parent.after(300, lambda: self.animate((counter+1) % len(self.sequence)))
		