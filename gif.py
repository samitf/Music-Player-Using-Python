from tkinter import *
from PIL import Image, ImageTk

class GifLabel(Label):
    def __init__(self, master=None, gif_path=None, delay=50,width=None,height=None, **kwargs):
        super().__init__(master, **kwargs)
        self.height = height
        self.width = width
        self.gif = Image.open(gif_path)
        self.tk_image = ImageTk.PhotoImage(self.gif)
        self.config(image=self.tk_image,highlightcolor="#00ADB5")
        self.delay = delay
        self.frame_index = 0
        self.animate()

    def animate(self):
        self.frame_index += 1
        if self.frame_index >= self.gif.n_frames:
            self.frame_index = 0
        self.gif.seek(self.frame_index)
        self.tk_image = ImageTk.PhotoImage(self.gif)
        self.config(image=self.tk_image)
        self.after(self.delay, self.animate)

# Example usage
#root = Tk()

# Add the GIF label to the root window
#gif_label = GifLabel(root, gif_path='C:\\Users\\samit\\Downloads\\Untitled design.gif')
#gif_label.pack()

#root.mainloop()


