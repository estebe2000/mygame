import pygame
import pytmx
import pyscroll

from player import Player


class Game:
    def __init__(self):
        pygame.mixer.init()
        file = 'epic.mp3'
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # If the loops is -1 then the music will repeat indefinitely.
        # definir si le jeux a commencer
        self.is_menu = True


        # generation fenetre
        pygame.display.set_caption("Mon moteur de jeux")
        self.screen = pygame.display.set_mode((1080,720))

        # definir touche action
        self.action = False
        self.map = "carte.tmx"
        self.spawn = "player"
        self.next_map = ""

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(self.map)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # generer un joueur
        player_position = tmx_data.get_object_by_name(self.spawn)
        self.player = Player(player_position.x, player_position.y, self.spawn)

        # definir une liste de collisions
        self.walls = []

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        # definir une liste zone switch house
        self.zone_switch = []

        self.switch_map(self.map, self.spawn)




    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
        elif pressed[pygame.K_x]:
            self.is_menu = False
            print("enter")
        elif pressed[pygame.K_SPACE]:
            self.action = True
        else: self.action = False


    def switch_map(self, map_choice, p_position):
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(map_choice)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        if map_choice == "titre.tmx":
            map_layer.zoom = 1.7
        else:
            map_layer.zoom = 3

        # generer un joueur
        player_position = tmx_data.get_object_by_name(p_position)
        self.player = Player(player_position.x, player_position.y, "marioyoshi")

        # definir une liste de collisions
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # definir une liste zone switch house
        self.zone_switch = []
        for obj in tmx_data.objects:
            if obj.type == "zone_switch":
                self.zone_switch.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

    def update(self):

        self.group.update()

        # verification des zone switch
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.zone_switch) > -1:
                for obj in pytmx.util_pygame.load_pygame(self.map).objects:
                    if (self.zone_switch[sprite.feet.collidelist(self.zone_switch)]) == (pygame.Rect(obj.x, obj.y, obj.width, obj.height)):
                        self.next_map = obj.name

                # verifier si zone de switch cartes
                if self.action:
                    self.switch_map(self.next_map, self.map+"_spawn")
                    self.map = self.next_map

     # verification des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        # Boucle du Jeux
        clock = pygame.time.Clock()
        running  = True
        while running :
            self.player.sav_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)
        self.game.run()
        pygame.QUIT()