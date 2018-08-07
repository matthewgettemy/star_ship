











class Application(App):
    """
    pass
    """
    def build(self):
        parent = Widget()
        return parent

"""
class ClientApp(App):

    def build(self):
        # this is where the root widget goes
        # should be a canvas
        parent = Widget()  # this is an empty holder for buttons, etc
        #with parent.canvas.before:
        #    texture = CoreImage('starry_night_background.jpg').texture
        #    texture.wrap = 'repeat'
        #    parent.rect_1 = Rectangle(texture=texture, size=Window.size, pos=(0,0))
        app = GUI()
        # Start the game clock (runs update function once every (1/60) seconds
        Clock.schedule_interval(app.update, 1.0 / 60.0)
        parent.add_widget(app)  # use this hierarchy to make it easy to deal w/buttons
        return parent
"""
if __name__ == '__main__' :
    ClientApp().run()