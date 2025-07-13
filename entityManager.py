from spriteEntity import *
from npc import *
from random import choices, randrange

# manages the creation, update, and interactions of sprites and NPCs in the game.
class EntityManager:
    #  Initializes the object with the game instance and the chosen difficulty level.
    #  It sets up the paths for different types of sprites, initializes sprite and NPC lists, and spawns NPCs based on the chosen difficulty.
    def __init__(self,game, difficulty_choice):
        self.game = game
        self.sprite_list = []
        self.npc_list = []


        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        # spawn npc
        if(difficulty_choice==1):
            self.enemies = 10  # npc count
            self.npc_types = [RangeNPC, MeleeNPC, BossNPC]
            self.weights = [60, 30, 10]
            self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
            self.spawn_npc()
        if (difficulty_choice == 2):
            self.enemies = 20  # npc count
            self.npc_types = [RangeNPC, MeleeNPC, BossNPC]
            self.weights = [60, 30, 10]
            self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
            self.spawn_npc()

        # sprite map
        add_sprite(spriteAnimator(game))
        add_sprite(spriteAnimator(game, pos=(1.5, 1.5)))
        add_sprite(spriteAnimator(game, pos=(1.5, 7.5)))
        add_sprite(spriteAnimator(game, pos=(5.5, 3.25)))
        add_sprite(spriteAnimator(game, pos=(5.5, 4.75)))
        add_sprite(spriteAnimator(game, pos=(7.5, 2.5)))
        add_sprite(spriteAnimator(game, pos=(7.5, 5.5)))
        add_sprite(spriteAnimator(game, pos=(14.5, 1.5)))
        add_sprite(spriteAnimator(game, pos=(14.5, 4.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(spriteAnimator(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))
        add_sprite(spriteAnimator(game, pos=(14.5, 24.5)))
        add_sprite(spriteAnimator(game, pos=(14.5, 30.5)))
        add_sprite(spriteAnimator(game, pos=(1.5, 30.5)))
        add_sprite(spriteAnimator(game, pos=(1.5, 24.5)))

    # Spawns NPCs in the game world based on the chosen difficulty.
    # It randomly selects NPC types with weighted probabilities and assigns them to random positions on the game map, considering restricted areas.
    def spawn_npc(self):
        for i in range(self.enemies):
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    # Checks if all NPCs have been eliminated and declare a win state
    def check_win(self):
        if not len(self.npc_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game(self.game.map_choice, self.game.difficulty_choice)

    # updates NPCs positions, animations, and checks for win conditions.
    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.isAlive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.check_win()

    # Adds an NPC to the NPC list.
    def add_npc(self, npc):
        self.npc_list.append(npc)

    # Adds a sprite to the sprite list
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)