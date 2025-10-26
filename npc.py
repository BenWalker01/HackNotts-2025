import pygame
import random
import glob
import os
from player import Player


SPEED = 10
SCALE = 0.30
HITBOX_MARGIN = 5


class NPC(Player):
    def __init__(self, window, map_name="main"):
        super().__init__(window)

        self.map = window           # the Map object this NPC belongs to
        self.map_name = map_name    # string name of that map

        self.x, self.y = self._get_random_valid_position()
        self.home = (self.x, self.y)
        self.rect.topleft = (self.x, self.y)

        print(f"[NPC:{self.map_name}] Spawned at {self.x}, {self.y}")

        # Animation & facing
        self.direction = random.choice(["d", "l", "r"])
        self.image = self.frames_walk[self.direction][0]

        # Movement & cooldown
        self.cooldown = 0
        self.target = None
        self.last_move_time = pygame.time.get_ticks()
        self.pause_duration = 1000  # ms

        # Home movement logic
        self.last_home_update = pygame.time.get_ticks()
        self.home_move_chance = 0.01
        self.home_move_radius = 500

    def set_map(self, new_map, map_name=None):
        """Allows reassigning this NPC to another map if needed."""
        self.map = new_map
        if map_name:
            self.map_name = map_name

    def _load_sheets(self):
        frames_folder_root = "assets/character/models/sequences"
        walk_dirs = glob.glob(os.path.join(
            frames_folder_root, "**", "walk"), recursive=True)
        frames_folder_walk = random.choice(walk_dirs)
        frame_files = sorted(f for f in os.listdir(frames_folder_walk))

        frames_per_direction = {"l": [], "r": [], "u": [], "d": []}
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
                    frame, (int(width * SCALE), int(height * SCALE))
                )
                frames_per_direction[order[i]].append(frame)
        return frames_per_direction

    def _maybe_move_home(self):
        now = pygame.time.get_ticks()
        time_since_last = now - self.last_home_update
        if time_since_last < 1000:
            return

        self.last_home_update = now
        if random.random() < self.home_move_chance:
            self.home = self.choose_target(max_distance=self.home_move_radius)

    def _get_random_valid_position(self):
        """Find a random walkable tile within this map."""
        attempts = 0
        max_attempts = 10000

        while attempts < max_attempts:
            x = random.randint(0, self.map.screen.get_width() - 1)
            y = random.randint(0, self.map.screen.get_height() - 1)
            if self.map.can_move_to(x, y):
                return x, y
            attempts += 1

        return (600, 350)

    def choose_target(self, max_distance=50):
        """Pick a random walkable target near the NPC's home."""
        candidates = []
        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                x, y = self.home[0] + dx, self.home[1] + dy
                if self.map.can_move_to(x, y):
                    distance = ((x - self.home[0]) **
                                2 + (y - self.home[1]) ** 2) ** 0.5
                    weight = max_distance - distance
                    candidates.append((x, y, weight))

        if not candidates:
            return self.x, self.y

        total_weight = sum(w for _, _, w in candidates)
        r = random.uniform(0, total_weight)
        upto = 0
        for x, y, w in candidates:
            if upto + w >= r:
                return x, y
            upto += w

    def move_towards(self, target_x, target_y, dt):
        import math

        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)

        if dist < 1:
            self.x, self.y = target_x, target_y
            return True

        dx /= dist
        dy /= dist
        speed = 15
        step = speed * (dt / 1000.0)

        new_x = self.x + dx * step
        new_y = self.y + dy * step

        if self.map.can_move_to(new_x, new_y):
            self.x = new_x
            self.y = new_y

            # Direction
            if abs(dx) > abs(dy):
                self.direction = "r" if dx > 0 else "l"
            else:
                self.direction = "d" if dy > 0 else "u"

            self.walking = True
        else:
            self.walking = False
            return True

        return False

    def update(self):
        now = pygame.time.get_ticks()
        dt = now - self.last_move_time
        self.last_move_time = now

        if self.cooldown > 0:
            self.cooldown -= dt
            if self.cooldown > 0:
                return
            else:
                self.cooldown = 0

        self._maybe_move_home()

        if self.target is None:
            self.target = self.choose_target()

        reached = self.move_towards(*self.target, dt)

        if reached:
            self.cooldown = self.pause_duration + random.randint(0, 1000)
            self.target = None
            self.walking = False
        else:
            self.walking = True

        self.rect.topleft = (self.x, self.y)
        if self.walking:
            self.animate()
