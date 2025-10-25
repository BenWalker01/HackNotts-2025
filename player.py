import pygame
import os
from map import Map

SCALE = 0.30
SPEED = 3 * SCALE

HITBOX_MARGIN = 5


class Player(pygame.sprite.Sprite):
    def __init__(self, window):
        super().__init__()
        self.x, self.y = (100, 100)
        self.window: Map = window

        self.frames_walk = self._load_sheets()
        self.walking = False
        self.direction = "u"
        self.animation_frame = 0
        self.animation_speed = 0.15

        self.image = self.frames_walk[self.direction][0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def _load_sheets(self):
        frames_folder_root = "assets/character/models/sequences/leather_armor"
        frames_folder_walk = os.path.join(frames_folder_root, "walk")
        frame_files = sorted(f for f in os.listdir(frames_folder_walk))
        frames_per_direction = {
            "l": [],
            "r": [],
            "u": [],
            "d": []
        }
        order = ["u", "l", "d", "r"]
        for filename in frame_files:
            img = pygame.image.load(os.path.join(
                frames_folder_walk, filename)).convert_alpha()
            width = img.get_width()
            height = img.get_height() // 4

            for i in range(4):
                frame = img.subsurface(pygame.Rect(
                    0, i * height, width, height))
                frame = pygame.transform.scale(
                    frame, (int(width * SCALE), int(height * SCALE)))
                frames_per_direction[order[i]].append(frame)
        return frames_per_direction

    def animate(self):
        self.animation_frame += self.animation_speed
        self.animation_frame = self.animation_frame % len(
            self.frames_walk[self.direction])
        self.image = self.frames_walk[self.direction][int(
            self.animation_frame)]

    def update(self):
        if self.walking:
            self.animate()
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        self.window.screen.blit(self.image, self.rect)

    def move_up(self):
        self.direction = "u"
        new_y = self.y - SPEED
        mid_x = self.x + self.width // 2
        if self.window.can_move_to(mid_x, new_y + HITBOX_MARGIN):
            self.y = new_y
        self.walking = True
        self.rect.topleft = (self.x, self.y)

    def move_down(self):
        self.direction = "d"
        new_y = self.y + SPEED
        mid_x = self.x + self.width // 2
        if self.window.can_move_to(mid_x, new_y + self.height - HITBOX_MARGIN):
            self.y = new_y
        self.walking = True
        self.rect.topleft = (self.x, self.y)

    def move_left(self):
        self.direction = "l"
        new_x = self.x - SPEED
        mid_y = self.y + self.height // 2
        if self.window.can_move_to(new_x + HITBOX_MARGIN, mid_y):
            self.x = new_x
        self.walking = True
        self.rect.topleft = (self.x, self.y)

    def move_right(self):
        self.direction = "r"
        new_x = self.x + SPEED
        mid_y = self.y + self.height // 2
        if self.window.can_move_to(new_x + self.width - HITBOX_MARGIN, mid_y):
            self.x = new_x
        self.walking = True
        self.rect.topleft = (self.x, self.y)
