from spriteEntity import *
from random import randint, random

# subclass of AnimatedSprite and represents a generic non-player character (NPC) in the game.
class NPC(spriteAnimator):
    def __init__(self, game, path='resources/sprites/npc/rangeNPC/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_pics = self.get_images(self.path + '/attack')
        self.death_pics = self.get_images(self.path + '/death')
        self.idle_pics = self.get_images(self.path + '/idle')
        self.pain_pics = self.get_images(self.path + '/pain')
        self.walk_pics = self.get_images(self.path + '/walk')

        # defines various attributes for NPC behavior
        self.attackDistance = randint(3, 6)
        self.speed = 0.02
        self.size = 20
        self.health = 100
        self.attackDamage = 6
        self.accuracy = 0.15
        self.isAlive = True
        self.isPain = False
        self.raycastValue = False
        self.numFrames = 0
        self.playerSearch = False

    # Updates the state of the NPC by checking the animation time, getting the current sprite, and running the logic.
    def update(self):
        self.checkAnimationTime()
        self.getSprite()
        self.runLogic()
        # self.draw_ray_cast()

    # Checks if a given position (x, y) is a wall based on the game's world map
    def checkWall(self, x, y):
        return (x, y) not in self.game.map.world_map

    # Checks for collision with walls and adjusts the NPC's position accordingly.
    def checkWallCollision(self, dx, dy):
        if self.checkWall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.checkWall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    # Calculates the next position for the NPC using a pathfinding algorithm and moves the NPC towards that position.
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        # pg.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.entity_manager.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.checkWallCollision(dx, dy)

    # Triggers an attack action for the NPC.
    # Plays a sound effect and calculates whether the attack hits the player based on the NPC's accuracy.
    # Inflicts damage to the player if the attack is successful.
    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attackDamage)

    # Animates the NPC's death sequence if it is no longer alive.
    def animateDeath(self):
        if not self.isAlive:
            if self.game.global_trigger and self.numFrames < len(self.death_pics) - 1:
                self.death_pics.rotate(-1)
                self.image = self.death_pics[0]
                self.numFrames += 1

    # Animates the NPC's pain sequence if it has been damaged.
    def animatePain(self):
        self.animate(self.pain_pics)
        if self.animation_trigger:
            self.isPain = False

    # Checks if the player's shot intersects with the NPC's sprite.
    # Plays a sound effect and updates the NPC's health and pain status accordingly.
    def check_hit_in_npc(self):
        if self.raycastValue and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.isPain = True
                self.health -= self.game.weapon.damage
                self.checkHealth()

    # Checks if the NPC's health has reached zero.
    # Sets the NPC as not alive and plays a death sound effect
    def checkHealth(self):
        if self.health < 1:
            self.isAlive = False
            self.game.sound.npc_death.play()

    # Executes the main logic for the NPC's behavior.
    # Checks for player-NPC interaction, such as ray casting to detect the player's presence.
    # Animates the NPC based on its state and executes the appropriate actions.
    def runLogic(self):
        if self.isAlive:
            self.raycastValue = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if self.isPain:
                self.animatePain()

            elif self.raycastValue:
                self.playerSearch = True

                if self.dist < self.attackDistance:
                    self.animate(self.attack_pics)
                    self.attack()
                else:
                    self.animate(self.walk_pics)
                    self.movement()

            elif self.playerSearch:
                self.animate(self.walk_pics)
                self.movement()

            else:
                self.animate(self.idle_pics)
        else:
            self.animateDeath()

    # Returns the current map position of the NPC as a tuple (x, y).
    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    # Performs ray casting to check if there is a line of sight between the NPC and the player.
    # Determines the distances to the player and to walls in both horizontal and vertical directions.
    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wallDist_v, wallDist_h = 0, 0
        playerDist_v, playerDist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                playerDist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wallDist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                playerDist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wallDist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(playerDist_v, playerDist_h)
        wall_dist = max(wallDist_v, wallDist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    # Draws visual indicators of the ray casting process
    # Draws a circle at the NPC's position and a line to the player's position if line of sight is detected.
    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)

#  represents a range shooter NPC
class RangeNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/rangeNPC/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

#  represents a melee NPC
class MeleeNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/meleeNPC/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attackDistance = 1
        self.health = 150
        self.attack_damage = 15
        self.speed = 0.028
        self.accuracy = 0.50

#  represents a specific type of boss NPC
class BossNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/bossNPC/0.png', pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 300
        self.attack_damage = 18
        self.speed = 0.032
        self.accuracy = 0.30
