# Implementation Notes

## Scene Graph

`SceneExplorerApp` loads Panda3D's built-in `models/environment` and `models/panda` assets, then attaches both models to `render`. This keeps the scene graph simple and visible in the code:

- `environment` acts as the surrounding terrain
- `panda` acts as the object of interest
- lights are attached as scene nodes and enabled on `render`

## Task Manager Loop

The app registers `update_scene` with Panda3D's task manager:

```python
self.taskMgr.add(self.update_scene, "update-scene")
```

Each frame, the task reads keyboard state, applies time-scaled camera movement, updates pitch/heading, and refreshes the distance-based highlight state.

## Interaction Logic

The panda model changes color when the camera is close enough. This is a lightweight stand-in for gameplay proximity logic and keeps the sample easy to reason about during code review.

## Review Focus

Useful code-review questions for this project:

- Are movement values frame-rate independent?
- Are input bindings easy to extend?
- Is scene setup separated from per-frame update logic?
- Are hard-coded constants named clearly?
- Can logic be tested without launching the engine?

