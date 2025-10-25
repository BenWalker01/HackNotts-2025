import pygame
import os

SPEED = 2


class Player:
    def __init__(self, window):
        self.x, self.y = (100, 100)
        self.window = window

        self.frames_walk = self._load_sheets()
        self.walking = False
        self.direction = "u"
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.current_frame = self.frames_walk[self.direction][0]

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
                frames_per_direction[order[i]].append(frame)
        return frames_per_direction

    def animate(self):
        self.animation_frame += self.animation_speed
        self.animation_frame = self.animation_frame % len(
            self.frames_walk[self.direction])
        self.current_frame = self.frames_walk[self.direction][int(
            self.animation_frame)]

    def draw(self):
        if self.walking:
            self.animate()
        self.window.screen.blit(self.current_frame, (self.x, self.y))

    def move_up(self):
        self.direction = "u"
        self.y -= SPEED
        self.walking = True

    def move_down(self):
        self.direction = "d"
        self.walking = True
        self.y += SPEED

    def move_left(self):
        self.direction = "l"
        self.x -= SPEED
        self.walking = True

    def move_right(self):
        self.direction = "r"
        self.x += SPEED
        self.walking = True
