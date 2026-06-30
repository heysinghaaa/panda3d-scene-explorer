# panda3d-scene-explorer

A compact Panda3D practice project for exploring Python-driven 3D scene setup, camera movement, model loading, task-manager update loops, and simple interaction logic.

This repository is intentionally small: it focuses on readable Panda3D fundamentals rather than custom art or a full game loop framework.

## Features

- Panda3D `ShowBase` application structure
- Scene graph setup with parented models and lights
- Built-in Panda3D model loading (`models/environment`, `models/panda`)
- Keyboard-driven camera movement
- Task-manager update loop for frame-based interaction
- Simple distance-based object highlighting
- On-screen control/status text
- Pure-Python movement helpers with tests

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Controls

| Key | Action |
| --- | --- |
| `W` / `S` | Move camera forward / backward |
| `A` / `D` | Strafe left / right |
| `Q` / `E` | Move down / up |
| Arrow keys | Rotate camera |
| `R` | Reset camera |
| `Esc` | Exit |

## Project Layout

```text
.
├── run.py
├── src/scene_explorer/
│   ├── app.py
│   └── movement.py
├── tests/
│   └── test_movement.py
└── docs/
    ├── controls.md
    └── implementation-notes.md
```

## Notes

The app uses Panda3D's built-in sample models so it can run without downloading separate assets. The code is written to make the scene graph, update loop, and input handling easy to inspect for learning, review, or AI-training style code evaluation.

