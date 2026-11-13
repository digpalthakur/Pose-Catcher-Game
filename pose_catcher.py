"""
Pose Catcher - a yoga learning arcade game (Pygame)
---------------------------------------------------
A yoga pose name is shown at the top. Stick-figure poses fall down.
Move the mat to catch the CORRECT pose. After each correct catch the game
pauses and shows the pose's benefits and a fun fact.

Run:  python pose_catcher.py
Needs: pip install pygame
"""
import array
import math
import os
import random
import sys

import pygame

W, H, FPS = 800, 600, 60
TEXT_COLOR = (0, 0, 0)          # colour of all on-screen text
SHADOW_COLOR = (255, 255, 255)  # small shadow so text stays readable

# Arcade pixel font (Press Start 2P, free OFL licence) kept in the assets folder.
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "assets", "PressStart2P-Regular.ttf")


def load_font(size):
    """Use the arcade font; fall back to a normal font if the file is missing."""
    try:
        return pygame.font.Font(FONT_PATH, size)
    except (FileNotFoundError, pygame.error):
        return pygame.font.SysFont("arial", int(size * 1.6), bold=True)

# ----------------------------------------------------------------------
# POSE DATA  (stick figures are drawn on a 100 x 100 grid, y goes down)
# ----------------------------------------------------------------------
POSES = {
    "mountain": {
        "name": "Mountain Pose", "sanskrit": "Tadasana",
        "head": (50, 12),
        "lines": [[(50, 20), (50, 60)], [(50, 60), (44, 95)], [(50, 60), (56, 95)],
                  [(50, 28), (38, 55)], [(50, 28), (62, 55)]],
        "benefits": ["Improves posture", "Strengthens thighs and ankles",
                     "Builds body awareness"],
        "fact": "Tadasana is the foundation of almost every standing pose.",
    },
    "tree": {
        "name": "Tree Pose", "sanskrit": "Vrikshasana",
        "head": (50, 16),
        "lines": [[(50, 23), (50, 58)], [(50, 58), (50, 95)],
                  [(50, 58), (70, 68), (51, 78)],
                  [(50, 28), (36, 16), (48, 2)], [(50, 28), (64, 16), (52, 2)]],
        "benefits": ["Improves balance and focus", "Strengthens legs and core",
                     "Calms the mind"],
        "fact": "Vriksha means 'tree'. Stare at one fixed spot to stay steady.",
    },
    "warrior": {
        "name": "Warrior II", "sanskrit": "Virabhadrasana II",
        "head": (50, 12),
        "lines": [[(50, 20), (50, 60)], [(10, 30), (90, 30)],
                  [(50, 60), (78, 72), (78, 95)], [(50, 60), (20, 95)]],
        "benefits": ["Builds leg and shoulder strength", "Opens hips and chest",
                     "Boosts stamina"],
        "fact": "Named after Virabhadra, a fierce warrior from Hindu mythology.",
    },
    "triangle": {
        "name": "Triangle Pose", "sanskrit": "Trikonasana",
        "head": (84, 22),
        "lines": [[(50, 50), (74, 32)], [(50, 50), (20, 95)], [(50, 50), (80, 95)],
                  [(72, 34), (80, 92)], [(72, 34), (68, 2)]],
        "benefits": ["Stretches hamstrings, hips and spine", "Strengthens legs",
                     "Eases mild back stiffness"],
        "fact": "Trikona means 'three angles' - legs and torso form triangles.",
    },
    "cobra": {
        "name": "Cobra Pose", "sanskrit": "Bhujangasana",
        "head": (72, 48),
        "lines": [[(5, 92), (45, 92)], [(45, 92), (66, 60)], [(62, 66), (62, 92)]],
        "benefits": ["Strengthens the back and spine", "Opens chest and lungs",
                     "Stretches the abdomen"],
        "fact": "Bhujanga means 'serpent'. Cobra is part of Surya Namaskar.",
    },
    "chair": {
        "name": "Chair Pose", "sanskrit": "Utkatasana",
        "head": (40, 18),
        "lines": [[(30, 60), (38, 28)], [(30, 60), (62, 62), (58, 95)],
                  [(38, 30), (64, 12)]],
        "benefits": ["Strengthens thighs and calves", "Engages the core",
                     "Builds endurance"],
        "fact": "Utkata means 'fierce', so it is also called Fierce Pose.",
    },
    "dog": {
        "name": "Downward Dog", "sanskrit": "Adho Mukha Svanasana",
        "head": (20, 48),
        "lines": [[(10, 92), (30, 54), (50, 28), (88, 92)]],
        "benefits": ["Stretches hamstrings, calves and shoulders",
                     "Strengthens arms and legs", "Energizes the whole body"],
        "fact": "It looks like a dog stretching, which is how it got its name.",
    },
    "child": {
        "name": "Child's Pose", "sanskrit": "Balasana",
        "head": (24, 84),
        "lines": [[(46, 92), (74, 92)], [(74, 92), (66, 70)], [(66, 70), (32, 78)],
                  [(32, 80), (6, 92)]],
        "benefits": ["Gently stretches back and hips", "Relaxes the mind and eases stress",
                     "A perfect resting pose"],
        "fact": "Bala means 'child'. Rest here between harder poses.",
    },
    "boat": {
        "name": "Boat Pose", "sanskrit": "Navasana",
        "head": (27, 30),
        "lines": [[(50, 82), (32, 44)], [(50, 82), (88, 48)], [(34, 52), (62, 58)]],
        "benefits": ["Strengthens the core and hip flexors", "Improves balance",
                     "Builds back strength"],
        "fact": "Your body forms a 'V' like a boat. Nava means 'boat'.",
    },
    "bridge": {
        "name": "Bridge Pose", "sanskrit": "Setu Bandhasana",
        "head": (8, 84),
        "lines": [[(18, 88), (50, 56), (74, 64), (78, 92)], [(18, 91), (50, 92)]],
        "benefits": ["Strengthens back, glutes and legs", "Opens chest and shoulders",
                     "Gently stretches the spine"],
        "fact": "Setu Bandha means 'bridge construction' in Sanskrit.",
    },
    "easy": {
        "name": "Easy Pose", "sanskrit": "Sukhasana",
        "head": (50, 20),
        "lines": [[(50, 28), (50, 68)], [(18, 82), (50, 72), (82, 82)],
                  [(22, 90), (78, 90)], [(50, 38), (24, 70)], [(50, 38), (76, 70)]],
        "benefits": ["Calms the mind", "Improves sitting posture", "Gently opens the hips"],
        "fact": "Sukha means 'joy' or 'ease'. It is popular for breathing and meditation.",
    },
    "plank": {
        "name": "Plank Pose", "sanskrit": "Phalakasana",
        "head": (11, 54),
        "lines": [[(20, 62), (90, 88)], [(20, 62), (20, 92)]],
        "benefits": ["Strengthens core, arms and shoulders", "Builds endurance",
                     "Improves posture"],
        "fact": "Plank is often used as a step in sun salutation flows.",
    },
}
POSE_KEYS = list(POSES)

TIPS = [
    "Slow, deep breathing can help reduce stress.",
    "Even 10 minutes of yoga a day can improve flexibility.",
    "Never force a pose - stretch only until it feels comfortable.",
    "Yoga is best learned with a qualified teacher, too.",
]


def draw_pose(surf, key, rect, color, width=3):
    """Draw a stick figure inside rect by scaling the 100x100 grid."""
    p = POSES[key]

    def sx(x): return rect.x + x * rect.w / 100

    def sy(y): return rect.y + y * rect.h / 100

    for line in p["lines"]:
        pts = [(sx(x), sy(y)) for x, y in line]
        pygame.draw.lines(surf, color, False, pts, width)
    pygame.draw.circle(surf, color, (int(sx(p["head"][0])), int(sy(p["head"][1]))),
                       max(3, int(7 * rect.w / 100)))


def wrap_text(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_sound(freqs, ms=120, vol=0.3):
    """Create a simple beep sequence (no sound files needed)."""
    rate, buf = 44100, array.array("h")
    for f in freqs:
        n = int(rate * ms / 1000)
        for i in range(n):
            env = 1 - i / n
            buf.append(int(math.sin(2 * math.pi * f * i / rate) * env * vol * 32767))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_drone():
    """Peaceful, soft and playful background ambience."""

    rate, secs = 44100, 4
    buf = array.array("h")

    for i in range(rate * secs):
        t = i / rate

        # Soft musical chord
        music = (
            0.50 * math.sin(2 * math.pi * 262 * t) +
            0.30 * math.sin(2 * math.pi * 330 * t) +
            0.20 * math.sin(2 * math.pi * 392 * t) +
            0.10 * math.sin(2 * math.pi * 523 * t)
        )

        # Gentle breathing-like volume movement
        pulse = 0.85 + 0.15 * math.sin(2 * math.pi * 0.25 * t)

        sample = music * pulse * 0.045

        buf.append(int(sample * 32767))

    return pygame.mixer.Sound(buffer=buf.tobytes())

def gradient(top, bottom):
    s = pygame.Surface((W, H))
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        pygame.draw.line(s, c, (0, y), (W, y))
    pygame.draw.circle(s, (255, 235, 130), (640, H - 150), 60)       # sun
    pygame.draw.ellipse(s, (120, 200, 140), (-120, H - 110, 520, 200))  # hills
    pygame.draw.ellipse(s, (90, 180, 120), (280, H - 90, 650, 180))
    return s


class Item:
    def __init__(self, key, x):
        self.key = key
        self.y = -80.0
        self.rect = pygame.Rect(x, -80, 70, 70)

    def move(self, speed):
        self.y += speed
        self.rect.y = int(self.y)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption("Pose Catcher - Learn Yoga Poses")
        self.screen = pygame.display.set_mode((W, H))
        self.clock = pygame.time.Clock()
        self.f_title = load_font(48)
        self.f_big = load_font(32)
        self.f_mid = load_font(16)
        self.f_txt = load_font(12)
        self.f_small = load_font(10)

        self.sound_ok = True
        try:
            self.s_good = make_sound([392, 523, 659], 180)
            self.s_bad = make_sound([392, 330], 140, 0.22)
            self.s_bonus = make_sound([523, 659, 784, 1047, 1319], 90)
            self.drone = make_drone()
            self.drone.set_volume(0.15)
            self.drone.play(loops=-1)
        except pygame.error:
            self.sound_ok = False

        self.bg_normal = gradient((110, 190, 255), (255, 225, 170))
        self.bg_calm = gradient((150, 230, 215), (255, 245, 190))
        self.stars = [(random.randint(0, W), random.randint(0, 300),
                       random.random() * 6) for _ in range(60)]
        self.high = 0
        self.state = "START"
        self.t = 0
        self.reset()

    # ------------------------------------------------------------------
    def reset(self):
        self.score, self.balance, self.streak = 0, 5, 0
        self.level, self.correct = 1, 0
        self.items, self.particles = [], []
        self.mat = pygame.Rect(W // 2 - 60, H - 50, 120, 16)
        self.target = random.choice(POSE_KEYS)
        self.spawn_timer = 0
        self.bonus_frames = 0
        self.info_key = None
        self.flash = 0
        self.msg, self.msg_t, self.msg_color = "", 0, (255, 255, 255)
        self.learned = set()
        self.tip = random.choice(TIPS)
        self.praise = "Great catch!"

    def play(self, snd):
        if self.sound_ok:
            snd.play()

    def say(self, text, color=(255, 255, 255)):
        self.msg, self.msg_t, self.msg_color = text, 70, color

    def burst(self, x, y, color):
        for _ in range(22):
            a = random.random() * math.tau
            sp = random.uniform(1, 4)
            col = random.choice([(255, 210, 80), (255, 140, 170), (120, 220, 150), (150, 200, 255)])
            self.particles.append([x, y, math.cos(a) * sp, math.sin(a) * sp, 35, col])

    # ------------------------------------------------------------------
    # difficulty
    def speed(self):
        s = min(2.0 + 0.5 * (self.level - 1), 7.0)
        return s * 0.5 if self.bonus_frames > 0 else s

    def spawn_gap(self):
        gap = max(35, 90 - 8 * (self.level - 1))
        return int(gap * 1.3) if self.bonus_frames > 0 else gap

    def spawn(self):
        on_screen = any(i.key == self.target for i in self.items)
        if not on_screen or random.random() < 0.35:
            key = self.target
        else:
            key = random.choice(POSE_KEYS)
        self.items.append(Item(key, random.randint(10, W - 80)))

    # ------------------------------------------------------------------
    def catch(self, item):
        """Called when the mat touches a falling pose (collision)."""
        if item.key == self.target:
            pts = 20 if self.bonus_frames > 0 else 10
            self.score += pts
            self.streak += 1
            self.correct += 1
            self.learned.add(item.key)
            self.burst(item.rect.centerx, item.rect.centery, (255, 230, 120))
            self.play(self.s_good)
            if self.correct % 5 == 0:
                self.level += 1
            if self.streak == 3:               # 3 correct in a row -> calm bonus
                self.streak = 0
                self.bonus_frames = 10 * FPS
                self.play(self.s_bonus)
            self.info_key = item.key
            self.praise = random.choice(["Great catch!", "Wonderful!", "Namaste!", "Beautiful balance!"])
            self.items.clear()
            self.state = "INFO"
        else:
            self.balance -= 1
            self.streak = 0
            self.flash = 15
            self.play(self.s_bad)
            self.say("NOT QUITE - KEEP GOING! -1", (255, 245, 200))
            if self.balance <= 0:
                self.high = max(self.high, self.score)
                self.tip = random.choice(TIPS)
                self.state = "GAME_OVER"

    def next_target(self):
        self.target = random.choice([k for k in POSE_KEYS if k != self.target])
        self.state = "PLAYING"

    # ------------------------------------------------------------------
    def update(self):
        self.t += 1
        for p in self.particles:
            p[0] += p[2]; p[1] += p[3]; p[4] -= 1
        self.particles = [p for p in self.particles if p[4] > 0]
        if self.flash > 0:
            self.flash -= 1
        if self.msg_t > 0:
            self.msg_t -= 1

        if self.state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.mat.x -= 9
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.mat.x += 9
        self.mat.clamp_ip(self.screen.get_rect())

        if self.bonus_frames > 0:
            self.bonus_frames -= 1
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_gap():
            self.spawn_timer = 0
            self.spawn()

        for item in self.items[:]:
            item.move(self.speed())
            if self.mat.colliderect(item.rect):
                self.items.remove(item)
                self.catch(item)
                if self.state != "PLAYING":
                    break
            elif item.rect.top > H:
                self.items.remove(item)

    # ------------------------------------------------------------------
    def text(self, s, font, color, center=None, topleft=None):
        # All on-screen text is black, with a small white arcade-style shadow.
        img = font.render(s, True, TEXT_COLOR)
        r = img.get_rect()
        if center: r.center = center
        if topleft: r.topleft = topleft
        self.screen.blit(font.render(s, True, SHADOW_COLOR), r.move(2, 2))
        self.screen.blit(img, r)

    def overlay(self, alpha=170):
        o = pygame.Surface((W, H), pygame.SRCALPHA)
        o.fill((255, 255, 255, alpha))
        self.screen.blit(o, (0, 0))

    def draw_background(self):
        calm = self.bonus_frames > 0 and self.state in ("PLAYING", "PAUSED", "INFO")
        self.screen.blit(self.bg_calm if calm else self.bg_normal, (0, 0))
        for x, y, ph in self.stars:
            r = 2 if math.sin(self.t * 0.05 + ph) > 0.3 else 1
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), r)

    def draw_hud(self):
        bar = pygame.Surface((W, 90), pygame.SRCALPHA)
        bar.fill((255, 255, 255, 170))
        self.screen.blit(bar, (0, 0))
        self.text("CATCH: " + POSES[self.target]["name"].upper(), self.f_mid,
                  (255, 240, 180), center=(W // 2, 26))
        self.text(f"SCORE {self.score}", self.f_txt, (255, 255, 255), topleft=(15, 14))
        self.text(f"LEVEL {self.level}", self.f_txt, (255, 255, 255), topleft=(15, 44))
        self.text("BALANCE", self.f_small, (255, 255, 255), topleft=(590, 14))
        for i in range(5):
            c = (120, 230, 160) if i < self.balance else (90, 90, 90)
            pygame.draw.circle(self.screen, c, (690 + i * 22, 20), 8)
        self.text("STREAK", self.f_small, (255, 255, 255), topleft=(590, 44))
        for i in range(3):
            c = (255, 220, 90) if i < self.streak else (90, 90, 90)
            pygame.draw.circle(self.screen, c, (690 + i * 22, 50), 8)
        if self.bonus_frames > 0:
            secs = self.bonus_frames // FPS + 1
            self.text(f"CALM BONUS {secs}s - SLOW FALL, 2X POINTS",
                      self.f_txt, (190, 255, 220), center=(W // 2, 72))

    def draw_play(self):
        self.draw_background()
        for item in self.items:
            pygame.draw.rect(self.screen, (245, 238, 225), item.rect, border_radius=12)
            draw_pose(self.screen, item.key, item.rect.inflate(-14, -14), (60, 40, 90))
        glow = pygame.Surface((220, 60), pygame.SRCALPHA)
        a = int(60 + 40 * math.sin(self.t * 0.1))
        pygame.draw.ellipse(glow, (255, 230, 150, a), glow.get_rect())
        self.screen.blit(glow, glow.get_rect(center=self.mat.center))
        pygame.draw.rect(self.screen, (120, 80, 170), self.mat, border_radius=8)
        for x, y, dx, dy, life, col in self.particles:
            pygame.draw.circle(self.screen, col, (int(x), int(y)), max(1, life // 10))
        if self.flash > 0:
            r = pygame.Surface((W, H), pygame.SRCALPHA)
            r.fill((255, 200, 120, self.flash * 5))
            self.screen.blit(r, (0, 0))
        self.draw_hud()
        if self.msg_t > 0:
            self.text(self.msg, self.f_txt, self.msg_color, center=(W // 2, 120))

    def draw_info(self):
        self.draw_play()
        self.overlay(190)
        p = POSES[self.info_key]
        panel = pygame.Rect(40, 40, 720, 520)
        pygame.draw.rect(self.screen, (250, 244, 232), panel, border_radius=20)
        pygame.draw.rect(self.screen, (255, 190, 90), panel, 5, border_radius=20)
        self.text(self.praise.upper(), self.f_mid, (230, 120, 40), center=(W // 2, 82))
        self.text(p["name"].upper(), self.f_big, (60, 40, 90), center=(W // 2, 128))
        self.text(p["sanskrit"], self.f_txt, (120, 100, 140), center=(W // 2, 168))
        fig = pygame.Rect(65, 205, 200, 200)
        pygame.draw.rect(self.screen, (230, 220, 245), fig, border_radius=16)
        draw_pose(self.screen, self.info_key, fig.inflate(-30, -30), (60, 40, 90), 5)
        x, y = 300, 205
        self.text("BENEFITS", self.f_mid, (230, 120, 40), topleft=(x, y))
        y += 34
        for b in p["benefits"]:
            for ln in wrap_text("- " + b, self.f_txt, 430):
                self.text(ln, self.f_txt, (40, 40, 60), topleft=(x, y))
                y += 22
            y += 4
        y += 14
        self.text("DID YOU KNOW?", self.f_mid, (230, 120, 40), topleft=(x, y))
        y += 34
        for ln in wrap_text(p["fact"], self.f_txt, 430):
            self.text(ln, self.f_txt, (40, 40, 60), topleft=(x, y))
            y += 22
        if self.bonus_frames > 0:
            self.text("CALM BONUS! POSES FALL SLOWER", self.f_txt, (30, 130, 100),
                      center=(W // 2, 495))
        if (self.t // 30) % 2 == 0:
            self.text("PRESS SPACE TO CONTINUE", self.f_txt, (120, 100, 140),
                      center=(W // 2, 535))

    def draw_start(self):
        self.draw_background()
        self.overlay(110)
        self.text("POSE", self.f_title, (255, 240, 180), center=(W // 2, 85))
        self.text("CATCHER", self.f_title, (255, 200, 120), center=(W // 2, 150))
        self.text("LEARN YOGA ASANAS AS YOU PLAY", self.f_txt, (255, 255, 255),
                  center=(W // 2, 205))
        lines = ["LEFT/RIGHT, A/D OR MOUSE: MOVE THE MAT",
                 "CATCH THE POSE NAMED AT THE TOP",
                 "RIGHT POSE: +10 AND LEARN ABOUT IT",
                 "WRONG POSE: LOSE 1 BALANCE (YOU HAVE 5)",
                 "3 RIGHT IN A ROW: CALM BONUS ROUND",
                 "P: PAUSE"]
        for i, ln in enumerate(lines):
            self.text(ln, self.f_txt, (255, 255, 255), center=(W // 2, 265 + i * 32))
        if (self.t // 30) % 2 == 0:
            self.text("PRESS SPACE TO START", self.f_mid, (190, 255, 220),
                      center=(W // 2, 495))
        self.text("G: POSE GUIDE", self.f_txt, (255, 240, 180), center=(W // 2, 545))

    def draw_guide(self):
        self.draw_background()
        self.overlay(120)
        self.text("POSE GUIDE", self.f_big, (255, 240, 180), center=(W // 2, 42))
        for i, k in enumerate(POSE_KEYS):
            cx, top = 100 + (i % 4) * 200, 85 + (i // 4) * 165
            r = pygame.Rect(cx - 55, top, 110, 110)
            pygame.draw.rect(self.screen, (245, 238, 225), r, border_radius=14)
            draw_pose(self.screen, k, r.inflate(-20, -20), (60, 40, 90), 4)
            self.text(POSES[k]["name"].upper(), self.f_small, (255, 255, 255),
                      center=(cx, top + 130))
        self.text("PRESS ANY KEY TO GO BACK", self.f_small, (255, 255, 255),
                  center=(W // 2, 578))

    def draw_over(self):
        self.draw_background()
        self.overlay(150)
        self.text("GAME OVER", self.f_title, (255, 235, 150), center=(W // 2, 90))
        self.text("WELL DONE!", self.f_mid, (190, 255, 220), center=(W // 2, 145))
        self.text(f"SCORE {self.score}    BEST {self.high}", self.f_mid,
                  (255, 255, 255), center=(W // 2, 195))
        names = ", ".join(POSES[k]["name"] for k in sorted(self.learned)) or "none yet"
        self.text(f"POSES YOU LEARNED: {len(self.learned)}", self.f_txt, (255, 240, 180),
                  center=(W // 2, 250))
        for i, ln in enumerate(wrap_text(names, self.f_txt, 720)):
            self.text(ln, self.f_txt, (255, 255, 255), center=(W // 2, 280 + i * 22))
        for i, ln in enumerate(wrap_text("TIP: " + self.tip, self.f_txt, 720)):
            self.text(ln, self.f_txt, (190, 255, 220), center=(W // 2, 385 + i * 22))
        if (self.t // 30) % 2 == 0:
            self.text("PRESS R TO PLAY AGAIN", self.f_mid, (255, 255, 255),
                      center=(W // 2, 490))

    def draw(self):
        if self.state == "START": self.draw_start()
        elif self.state == "GUIDE": self.draw_guide()
        elif self.state == "INFO": self.draw_info()
        elif self.state == "GAME_OVER": self.draw_over()
        else:
            self.draw_play()
            if self.state == "PAUSED":
                self.overlay(150)
                self.text("PAUSED", self.f_big, (255, 255, 255),
                          center=(W // 2, H // 2))
        pygame.display.flip()

    # ------------------------------------------------------------------
    def handle(self, e):
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.MOUSEMOTION and self.state == "PLAYING":
            self.mat.centerx = e.pos[0]
            self.mat.clamp_ip(self.screen.get_rect())
        if e.type != pygame.KEYDOWN:
            return
        if self.state == "START":
            if e.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.reset(); self.state = "PLAYING"
            elif e.key == pygame.K_g:
                self.state = "GUIDE"
        elif self.state == "GUIDE":
            self.state = "START"
        elif self.state == "PLAYING" and e.key == pygame.K_p:
            self.state = "PAUSED"
        elif self.state == "PAUSED" and e.key == pygame.K_p:
            self.state = "PLAYING"
        elif self.state == "INFO" and e.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.next_target()
        elif self.state == "GAME_OVER" and e.key == pygame.K_r:
            self.reset(); self.state = "PLAYING"

    def run(self):
        while True:
            for e in pygame.event.get():
                self.handle(e)
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()