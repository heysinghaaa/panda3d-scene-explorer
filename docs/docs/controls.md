# Controls

The app keeps keyboard state in a small dictionary and converts pairs of keys into axis values each frame.

| Key | Action |
| --- | --- |
| `W` / `S` | Move forward and backward relative to the camera |
| `A` / `D` | Strafe left and right relative to the camera |
| `Q` / `E` | Move vertically down and up |
| Left / Right arrows | Rotate camera heading |
| Up / Down arrows | Adjust camera pitch |
| `R` | Reset camera to the starting view |
| `Esc` | Close the app |

The movement logic is intentionally separated into `src/scene_explorer/movement.py` so frame-rate math and input conversion can be tested without opening a Panda3D window.

