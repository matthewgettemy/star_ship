import kivy

#kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, Rotate, PushMatrix, PopMatrix
from kivy.vector import Vector
from kivy.utils import platform
from kivy.core.audio import SoundLoader

import random
import time

from kivy.config import Config
Config.set('graphics','resizable',0) #don't make the app re-sizeable
#Config.set('graphics', 'fullscreen', 1)
#Graphics fix
 #this fixes drawing issues on some phones
Window.clearcolor = (0,0,0,1.)
if platform == 'android':
    Window.fullscreen = True
else:
    Window.size = (600,800)

class WidgetDrawer(Widget):
    # This widget is used to draw all of the objects on the screen
    # it handles the following:
    # widget movement, size, positioning
    # whever a WidgetDrawer object is created, an image string needs to be specified
    # example:    wid - WidgetDrawer('./image.png')

    # objects of this class must be initiated with an image string
    # ;You can use **kwargs to let your functions take an arbitrary number of keyword arguments
    # kwargs ; keyword arguments
    def __init__(self, imageStr, size=(Window.width * .002 * 25, Window.width * .002 * 25), **kwargs):
        super(WidgetDrawer, self).__init__(**kwargs)  # this is part of the **kwargs notation
        # if you haven't seen with before, here's a link http://effbot.org/zone/python-with-statement.html
        #if 'background' in kwargs:
        #    with self.canvas.before:
        #        texture = CoreImage(imageStr).texture
        #        texture.wrap = 'repeat'
        #        rect_1 = Rectangle(texture=texture, size=(Window.width, Window.height), pos=self.pos)
        with self.canvas:
            # setup a default size for the object
            self.size = size
            #size = (Window.width * .002 * 25, Window.width * .002 * 25)
            # this line creates a rectangle with the image drawn on top
            self.rect_bg = Rectangle(source=imageStr, pos=self.pos, size=self.size)
            # this line calls the update_graphics_pos function every time the position variable is modified
            self.bind(pos=self.update_graphics_pos)
            self.x = self.center_x
            self.y = self.center_y
            # center the widget
            self.pos = (self.x, self.y)
            # center the rectangle on the widget
            self.rect_bg.pos = self.pos

    def update_graphics_pos(self, instance, value):
        # if the widgets position moves, the rectangle that contains the image is also moved
        self.rect_bg.pos = value
        self.angle = random.randint(0, 360)

    # use this function to change widget size
    def setSize(self, width, height):
        self.size = (width, height)

    # use this function to change widget position
    def setPos(xpos, ypos):
        self.x = xpos
        self.y = ypos



class Asteroid(WidgetDrawer):
    #Asteroid class. The flappy ship will dodge these
    velocity_x = NumericProperty(0) #initialize velocity_x and velocity_y
    velocity_y = NumericProperty(0) #declaring variables is not necessary in python
    #update the position using the velocity defined here. every time move is called we change the position by velocity_x
    #size_list = []
    #for i, size in enumerate(range(30, 100)):
    #    size_list += [size] * round(size/((i+1)**1.02))

    #size_range = list(range(30, 100))
    #weights = size_range[::-1]
    #weights = list(range(30, 100))
    #for i in size_range:
    #    weights.append(i)
    #    pass

    def __init__(self, imageStr):

        #tmp_size = random.choices(self.size_range, self.weights, k=1)[0]
        #tmp_size = random.choices(self.size_range, self.size_range, k=1)[0]
        #size_list = []
        #for i, size in enumerate(range(30, 100)):
           #num = round(size / ((i + 1) ** 1.02))
           #tmp_sizes = [size] * num
           #size_list += tmp_sizes
           #for item in tmp_sizes:
           #    size_list = size_list + item
           #    size_list.append(item)
        #size_list += [size] * num
        #size_list += [size] * round(size/((i+1)**1.02))

        tmp_size = random.randint(20, 100)
        self.size = (tmp_size, tmp_size)

        #tmp_size = random.choice(size_list)
        #self.size = (tmp_size, tmp_size)
        super(Asteroid, self).__init__(imageStr, size=self.size)
    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y
    def update(self):
#the update function moves the astreoid. Other things could happen here as well (speed changes for example)
        self.move()

    def collide_widget(self, widget_to_test_against):
        collide_vector = Vector((self.rect_bg.pos[0] + self.rect_bg.size[0]/2), (self.rect_bg.pos[1] + self.rect_bg.size[1]/2) ) - \
                         Vector((widget_to_test_against.rect_bg.pos[0] + widget_to_test_against.rect_bg.size[0]/2), (widget_to_test_against.rect_bg.pos[1] + widget_to_test_against.rect_bg.size[1]/2))
        collide_vector_length = collide_vector.length()
        #assume approximately sqare or spherical widgets...this won't look right for oblong widgets
        collision_length = (self.rect_bg.size[0]/2) + (widget_to_test_against.rect_bg.size[0]/2)
        if collide_vector_length < collision_length:
            #print('asteroid.size: {}'.format(self.rect_bg.size))
            #print('ship.size: {}'.format(widget_to_test_against.rect_bg.size))
            #print('collide_vector_length: {}'.format(collide_vector_length))
            #print('collision_length: {}'.format(collision_length))
            return True

class Flame(WidgetDrawer):

    def __init__(self, imageStr):
        super(Flame, self).__init__(imageStr)
        #self.rocket_takeoff_sound = SoundLoader.load(filename='./rocket_takeoff.mp3')
        #self.rocket_takeoff_sound.volume = 1
        #self.rocket_takeoff_sound.play()
        #self.rocket_takeoff_sound.seek(7)

    def move(self):
        pass

class Ship(WidgetDrawer):
    # Ship class. This is for the main ship object.
    # velocity of ship on x/y axis


    impulse = 0  # this variable will be used to move the ship up
    grav = 0 # this variable will be used to pull the ship down

    velocity_x = NumericProperty(0)  # we wont actually use x movement
    velocity_y = NumericProperty(0)
    def __init__(self, imageStr):
        #self.explosion_sound = SoundLoader.load(filename='explosion2.mp3')
        #self.explosion_sound.seek(0)
        self.size = (Window.width * .002 * 25, Window.width * .002 * 25)
        super(Ship, self).__init__(imageStr, size=self.size)
    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y

        # don't let the ship go too far
        if self.y > Window.height * 0.95:  # don't let the ship go up too high
            self.impulse = -3

    def determineVelocity(self):
        # move the ship up and down
        # we need to take into account our acceleration
        # also want to look at gravity
        self.grav = self.grav * 1.05  # the gravitational velocity should increase
        # set a grav limit
        if self.grav < -4:  # set a maximum falling down speed (terminal velocity)
            self.grav = -4
        # the ship has a propety called self.impulse which is updated
        # whenever the player touches, pushing the ship up
        # use this impulse to determine the ship velocity
        # also decrease the magnitude of the impulse each time its used
        self.velocity_y = self.impulse + self.grav
        self.impulse = 0.95 * self.impulse  # make the upward velocity decay

    def update(self):
        self.determineVelocity()  # first figure out the new velocity
        self.move()  # now move the ship

    def load_explosion_gif(self):
        self.explosion_gif_filename = 'ship_explosion.gif'
        self.explosion_gif = Image(source=self.explosion_gif_filename)
        self.explosion_gif.anim_loop = 1
        self.explosion_gif.anim_delay = 0.2
        self.explosion_gif._coreimage.anim_reset(False)
        #myimage._coreimage.anim_reset(False)


    def explode(self):

        #self.explosion_sound.play()
        self.explosion_gif._coreimage.anim_reset(True)
        self.explosion_gif.size = (self.size[0]*3, self.size[0]*3)
        self.explosion_gif.pos = (self.pos[0] - self.width, self.pos[1] - self.height)
        self.add_widget(self.explosion_gif)

    #def load_explosion_gif(self):
    #    self.explosion_gif_filename = 'ship_explosion.gif'
    #    self.explosion_gif = Image(source=self.explosion_gif_filename)
    #    #self.explosion_gif.anim_delay = 0.2
    #    #self.explosion_gif.anim_loop = 1

    #def explode(self):
    #    #self.explosion_gif_filename = 'ship_explosion.gif'
    #    #self.explosion_gif = Image(source=self.explosion_gif_filename)
    #    self.explosion_gif.anim_loop = 5
    #    self.explosion_gif.anim_delay = 0.2
    #    self.explosion_gif.pos = (self.pos[0], self.pos[1])
    #    self.explosion_gif.size = self.size

    #    print(self.explosion_gif.source)
    #    self.add_widget(self.explosion_gif)



class MyButton(Button):
    #class used to get uniform button styles
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
 #all we're doing is setting the font size. more can be done later
        self.font_size = Window.width*0.018

class Background(Widget):
    def __init__(self, gui, image, **kwargs):
        super(Background, self).__init__(**kwargs)
        with gui.canvas.before:
            self.texture = CoreImage(image).texture
            self.texture.wrap = 'repeat'
            self.rect = Rectangle(texture=self.texture, size=Window.size, pos=self.pos)

    def update(self):
        t = Clock.get_boottime()
        u = 0
        v = t * 0.02
        w = 1
        h = 1
        # self.background.rect.tex_coords = u, -v, u + w, -v, u + w, -(v + h), u, -(v + h)
        #self.rect.tex_coords = u, v, u + w, v, u + w, (v + h), u, (v + h)

class Title(WidgetDrawer):
    def __init__(self, imageStr):
        self.size = (Window.size[0]/2, Window.size[1]/2)
        self.imageStr = imageStr
        super(Title, self).__init__(self.imageStr, self.size)
        #with gui.canvas.before:
        #    self.image = './star_ship_title.png'
        #    self.texture = CoreImage(self.image).texture
        #    self.rect = Rectangle(texture = self.texture,
        #                          size = (Window.size[0]/2, Window.size[1]/2),
        #                          pos=(Window.width/2 - self.width, Window.height/2 - self.height/2))

class GUI(Widget):
    # this is the main widget that contains the game.
    asteroidList = []  # use this to keep track of asteroids
    minProb = 1700  # this variable used in spawning asteroids

    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.delt = 0
        self.opening_sequence = True
        self.number_of_asteroids_removed = 0
        self.max_number_of_asteroids = 18
        self.asteroid_probability_max = 1800
        self.max_asteroid_velocity = 70
        self.min_asteroid_velocity = 60
        #with self.canvas.before:
        #    texture = CoreImage('starry_night_background.jpg').texture
        #    texture.wrap = 'repeat'
        #    self.background = Rectangle(texture=texture, size=Window.size, pos=(0,0))
        self.background = Background(self, 'starry_night_background4.jpg')
        self.title = Title('./star_ship_title.png')
        self.title.x = Window.width/2 - self.title.width/2
        self.title.y = Window.height/2
        self.add_widget(self.title)
        #self.background_music = SoundLoader.load(filename='./background_music.mp3')
        #self.background_music.volume = 0.1
        #self.title_music_scifi = SoundLoader.load(filename='./title_song_scifi.mp3')
        #self.title_music_scifi.volume = 0.1
        #self.title_music_scifi.play()

        #self.rocket_takeoff_sound = SoundLoader.load(filename='./rocket_takeoff.mp3')
        #self.rocket_takeoff_sound.volume = 0.6
        #self.background_music.loop = True

        #self.explosion = Explosion(None)
        #self.explosion.load_gif()

        self.score = 0000
        self.score_label = Label(text='{}'.format(self.score), font_size='40sp')
        self.score_label.x = Window.width - (self.score_label.width * 3)
        self.score_label.y = Window.height - (self.score_label.height * 1.2)
        self.add_widget(self.score_label)

        self.debug_label = Label(text='{}'.format(self.number_of_asteroids_removed), font_size='20sp')
        self.debug_label.x = 100
        self.debug_label.y = Window.height - (self.debug_label.height * 1.2)
        self.add_widget(self.debug_label)



        #self.flame = Flame(imageStr='./flame.png')
        #self.ship = Ship(imageStr='./ship.png')
        #self.ship.x = Window.width / 2
        #self.flame.x = self.ship.x
        #self.ship.y = 0 - self.ship.height
        #self.flame.y = self.ship.y - self.flame.height
        #self.ship.load_explosion_gif()



        #l = Label(text='Block')  # give the game a title
        #l.x = Window.width / 2 - l.width / 2
        #l.y = Window.height * 0.8
        #self.add_widget(l)  # add the label to the screen

        # now we create a ship object
        # notice how we specify the ship image

        #self.ship = Ship(imageStr='./ship.png')
        #self.ship.x = Window.width / 2
        #self.ship.y = Window.height / 8
        #self.ship.load_explosion_gif()

        #self.add_widget(self.ship)

        #self.background = Background(background = './starry_night_background.jpg')



    def respawn_ship(self):
        print('creating objects')
        self.flame = Flame(imageStr='./flame.png')
        print('done with flame')
        self.ship = Ship(imageStr='./ship.png')
        print('created objects')
        self.ship.x = Window.width / 2
        self.flame.x = self.ship.x
        # self.ship.y = Window.height / 8

        self.ship.y = 0 - self.ship.height
        self.flame.y = self.ship.y - self.flame.height
        print('loading gif')
        self.ship.load_explosion_gif()
        print('loaded gif')
        self.add_widget(self.flame)
        self.add_widget(self.ship)
        print('added widgets')
        #self.rocket_takeoff_sound.stop()
        #self.rocket_takeoff_sound.play()
        #self.rocket_takeoff_sound.seek(8)


    def update_score(self):

        self.score += 1
        self.score_label.text = '{:05}'.format(self.score)

        #self.debug_label.text = '{:.5}'.format(self.delt)

    def add_asteroid(self):
        # add an asteroid to the screen
        # self.asteroid
        imageNumber = random.randint(1, 5)
        imageStr = './sandstone_' + str(imageNumber) + '.png'
        tmpAsteroid = Asteroid(imageStr)
        cube_width = Window.width * .002 * 25
        #tmpAsteroid.x = Window.width * random.random()#0.99
        num_spots = round(Window.width / cube_width)
        tmpAsteroid.x = random.randrange(num_spots)*cube_width

        # randomize y position
        ypos = Window.height

        #ypos = ypos * Window.height * .0625

        tmpAsteroid.y = ypos
        tmpAsteroid.velocity_y = 0
        vel = random.randint(self.min_asteroid_velocity, self.max_asteroid_velocity)
        #tmpAsteroid.velocity_x = -0.1 * vel
        tmpAsteroid.velocity_y = -0.1 * vel

        self.asteroidList.append(tmpAsteroid)
        self.add_widget(tmpAsteroid)
        #print(len(self.asteroidList))

    # handle input events
    # kivy has a great event handler. the on_touch_down function is already recognized
    # and doesn't need t obe setup. Every time the screen is touched, the on_touch_down function is called
    def on_touch_down(self, touch):
        print('got touch down')
        if self.title:
            #print('removing self.title.')
            self.remove_widget(self.title)
            print('removed title.')
            self.title = None
            #self.title_music_scifi.stop()
            #self.background_music.play()
            print('spawning ship')
            self.respawn_ship()
            print('spawned ship')


        touchx = touch.pos[0]
        touchy = touch.pos[1]

        if (touchx < self.ship.x + self.ship.size[0]/2) and (self.ship.x < Window.width - self.ship.size[0]*2):
            self.ship.x += self.ship.size[0]
            self.flame.x += self.ship.size[0]
        elif (touchx > self.ship.x + self.ship.size[0]/2) and (self.ship.x > self.ship.size[0]):
            self.ship.x -= self.ship.size[0]
            self.flame.x -= self.ship.size[0]
        self.ship.impulse = 0  # give the ship an impulse
        self.ship.grav = 0  # reset the gravitational velocity

    def gameOver(self):  # this function is called when the game ends
        # add a restart button
        restartButton = MyButton(text='Restart')

        # restartButton.background_color = (.5,.5,1,.2)
        def restart_button(obj):
            self.opening_sequence = True
            self.number_of_asteroids_removed = 0
            self.max_asteroid_velocity = 55
            self.min_asteroid_velocity = 50
            # this function will be called whenever the reset button is pushed
            'restart button pushed'
            self.remove_widget(self.ship.explosion_gif)
            self.remove_widget(self.ship)
            self.remove_widget(self.flame)
            #self.remove_widget(self.explosion)
            self.respawn_ship()
            # reset game
            for k in self.asteroidList:

                self.remove_widget(k)
                self.ship.xpos = Window.width * 0.25
                self.ship.ypos = Window.height * 0.5
                self.minProb = 1700

            self.asteroidList = []
            self.score = 0
            self.parent.remove_widget(restartButton)
            # stop the game clock in case it hasn't already been stopped
            Clock.unschedule(self.update)
            # start the game clock
            Clock.schedule_interval(self.update, 1.0 / 60.0)

        restartButton.size = (Window.width * .3, Window.height * .1)
        restartButton.pos = Window.width * 0.5 - restartButton.width / 2, Window.height * 0.5
        # bind the button using the built-in on_release event
        # whenever the button is released, the restart_button function is called
        restartButton.bind(on_release=restart_button)

        # *** It's important that the parent get the button so you can click on it
        # otherwise you can't click through the main game's canvas
        self.parent.add_widget(restartButton)
        #self.rocket_takeoff_sound.stop()

    def update(self, dt):
        t1 = time.clock()
        current_elapsed = Clock.get_boottime()
        current_elapsed_int = round(current_elapsed, 0)
        #print('CEI: {}'.format(current_elapsed_int))
        # This update function is the main update function for the game
        # All of the game logic has its origin here
        # events are setup here as well
        # update game objects
        # update ship

        #while self.ship.y < Window.height / 8:
        #    print(self.ship.y)
        #    self.ship.y += 0.002

        if self.title:
            return

        self.ship.update()
        if self.opening_sequence:
            if self.ship.y < Window.height / 8:

                self.ship.y += 2
                self.flame.y += 2.05
                return
            else:
                #self.rocket_takeoff_sound.stop()
                self.opening_sequence = False
                #self.flame.rocket_takeoff_sound.stop()
                #self.remove_widget(self.flame)

        #self.background.update()

        #self.update_score()
        # update asteroids
        # randomly add an asteroid
        tmpCount = random.randint(1, self.asteroid_probability_max)
        if tmpCount > self.minProb and len(self.asteroidList) <= self.max_number_of_asteroids:
            self.update_score()
            self.add_asteroid()
            self.max_asteroid_velocity += 1
            self.min_asteroid_velocity += 1
            if self.minProb < 1300:
                self.minProb = 1300
            self.minProb = self.minProb - 1

        #if current_elapsed_int % 2 == 0:
            #print(current_elapsed_int)
        asteroid_tmp = self.asteroidList[:]
        asteroids_removed = 0
        for i, asteroid in enumerate(asteroid_tmp):
            if asteroid.pos[1] + asteroid.size[1] < 0:
                actual_i = i - asteroids_removed
                target = self.asteroidList[actual_i]
                self.remove_widget(target)
                self.asteroidList.pop(actual_i)
                asteroids_removed += 1
        self.number_of_asteroids_removed += asteroids_removed

        for k in self.asteroidList:

            # check for collision with ship
            if k.collide_widget(self.ship):
                #self.ship.explode()
                #self.add_widget(self.explosion)
                #self.explosion.explode(self.ship.pos, self.ship.size)
                self.ship.explode()
                self.remove_widget(self.flame)
                #self.remove_widget(self.ship)
                'death'
                # game over routine
                self.gameOver()
                Clock.unschedule(self.update)

                # add reset button
            k.update()


        t2 = time.clock()
        self.delt = t2 - t1
        self.debug_label.text = '{:.5}'.format(self.delt)

class TitleScreen():



    
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

if __name__ == '__main__' :
    ClientApp().run()


