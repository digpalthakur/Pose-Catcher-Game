# Pose Catcher - Learn Yoga While You Play

A 2D arcade game made with Python + Pygame. Stick-figure yoga poses fall from the sky and you catch the one named at the top of the screen. After every correct catch the game shows the pose's benefits and a fun fact.

**Helping angle:** teaches yoga pose names, shapes and benefits in a relaxed, game-like way. (Educational only, not medical advice.)

## Run
```
pip install pygame
python pose_catcher.py
```
No image or sound files are needed. Graphics are drawn with `pygame.draw` and sounds are generated in code.

## Controls
| Key | Action |
|---|---|
| LEFT / RIGHT or A / D | Move the mat |
| Mouse movement | Move the mat |
| SPACE | Start / continue after the info card |
| G | Pose Guide (start screen) |
| P | Pause / resume |
| R | Restart after game over |

## Rules
- Catch the pose named at the top: **+10 points** and an info card (benefits + fact).
- Catch a wrong pose: **-1 balance point** (you start with 5). At 0 the game ends.
- **3 correct in a row** starts a **Calm Bonus** (10 s): poses fall slower and points are doubled, with a calm green background.
- **Difficulty:** every 5 correct catches the level rises, poses fall faster and spawn more often.

## Customization (unique mechanics)
1. Educational info card after each correct catch (changes game flow: a new INFO state).
2. Balance-point lives instead of a timer.
3. Streak-triggered Calm Bonus round that changes speed, scoring and visuals.

## Multimedia
Stick-figure sprites, sunrise background with twinkling stars, pulsing mat glow, particle bursts, sound effects (catch, wrong, bonus) and a soft looping background drone.

## Game states
`START -> PLAYING <-> PAUSED`, `PLAYING -> INFO -> PLAYING`, `PLAYING -> GAME_OVER -> PLAYING` (restart with R). `GUIDE` is reachable from START.

## Algorithm and collision detection
```
loop every frame (60 FPS):
    handle events (keys, mouse, state changes)
    if PLAYING:
        move mat
        spawn a falling pose every N frames (N shrinks with level)
        for each falling pose:
            y += speed
            if mat_rect.colliderect(pose_rect):   # collision
                correct -> score, streak, info card (INFO state)
                wrong   -> lose balance, reset streak
            elif pose is below the screen: remove it
    draw background, poses, mat, particles, HUD
```
Collision detection uses axis-aligned rectangles: both the mat and each falling pose have a `pygame.Rect`, and `colliderect` returns True when the rectangles overlap.

## Screenshots
Add your own: start screen, gameplay, info card, game-over screen.
