from spriteEntity import *

# a subclass of AnimatedSprite and represents a weapon object in the game.
class Weapon(spriteAnimator):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time) #Initializes the Weapon object by calling the parent class constructor (AnimatedSprite).
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images]) #Creates a deque of images from the loaded image, and smoothscales each image based on the desired scale
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2+200 , HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50


    # Handles the animation of the weapon when the player shoots (left mouse click)
    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1     #The frame counter is incremented, and if it reaches the number of images, the reloading flag is set to False and the frame counter is reset.
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.checkAnimationTime()
        self.animate_shot()