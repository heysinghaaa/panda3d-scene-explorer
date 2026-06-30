from __future__ import annotations

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import AmbientLight, DirectionalLight, TextNode, Vec3, WindowProperties

from .movement import AxisInput, bool_axis, pitch_with_limits, scaled_delta


class SceneExplorerApp(ShowBase):
    """Small Panda3D scene explorer focused on readable engine basics."""

    MOVE_SPEED = 18.0
    TURN_SPEED = 75.0
    HIGHLIGHT_DISTANCE = 13.0

    def __init__(self) -> None:
        super().__init__()
        self.disableMouse()
        self.key_state = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "turn_left": False,
            "turn_right": False,
            "look_up": False,
            "look_down": False,
        }
        self.panda = None
        self.status_text = None

        self._configure_window()
        self._bind_input()
        self._build_scene()
        self._build_overlay()
        self.reset_camera()
        self.taskMgr.add(self.update_scene, "update-scene")

    def _configure_window(self) -> None:
        props = WindowProperties()
        props.setTitle("Panda3D Scene Explorer")
        if hasattr(self.win, "requestProperties"):
            self.win.requestProperties(props)
        self.setBackgroundColor(0.08, 0.1, 0.12, 1)

    def _bind_input(self) -> None:
        bindings = {
            "w": ("forward", True),
            "w-up": ("forward", False),
            "s": ("backward", True),
            "s-up": ("backward", False),
            "a": ("left", True),
            "a-up": ("left", False),
            "d": ("right", True),
            "d-up": ("right", False),
            "e": ("up", True),
            "e-up": ("up", False),
            "q": ("down", True),
            "q-up": ("down", False),
            "arrow_left": ("turn_left", True),
            "arrow_left-up": ("turn_left", False),
            "arrow_right": ("turn_right", True),
            "arrow_right-up": ("turn_right", False),
            "arrow_up": ("look_up", True),
            "arrow_up-up": ("look_up", False),
            "arrow_down": ("look_down", True),
            "arrow_down-up": ("look_down", False),
        }
        for event, (key, value) in bindings.items():
            self.accept(event, self._set_key, [key, value])
        self.accept("r", self.reset_camera)
        self.accept("escape", self.userExit)

    def _set_key(self, key: str, value: bool) -> None:
        self.key_state[key] = value

    def _build_scene(self) -> None:
        environment = self.loader.loadModel("models/environment")
        environment.reparentTo(self.render)
        environment.setScale(0.25)
        environment.setPos(-8, 42, 0)

        self.panda = self.loader.loadModel("models/panda")
        self.panda.reparentTo(self.render)
        self.panda.setScale(0.006)
        self.panda.setPos(0, 18, 0)
        self.panda.setH(180)

        self._add_lighting()

    def _add_lighting(self) -> None:
        ambient = AmbientLight("ambient-light")
        ambient.setColor((0.35, 0.35, 0.38, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        sun = DirectionalLight("key-light")
        sun.setColor((0.85, 0.82, 0.76, 1))
        sun_np = self.render.attachNewNode(sun)
        sun_np.setHpr(-35, -55, 0)
        self.render.setLight(sun_np)

    def _build_overlay(self) -> None:
        OnscreenText(
            text="WASD move | Q/E height | Arrows look | R reset | Esc quit",
            pos=(0, 0.92),
            scale=0.045,
            fg=(0.92, 0.94, 0.96, 1),
            align=TextNode.ACenter,
            mayChange=False,
        )
        self.status_text = OnscreenText(
            text="",
            pos=(-1.28, -0.92),
            scale=0.04,
            fg=(0.74, 0.86, 1, 1),
            align=TextNode.ALeft,
            mayChange=True,
        )

    def reset_camera(self) -> None:
        self.camera.setPos(0, -28, 7)
        self.camera.setHpr(0, -12, 0)

    def _read_axis_input(self) -> AxisInput:
        return AxisInput(
            forward=bool_axis(self.key_state["forward"], self.key_state["backward"]),
            strafe=bool_axis(self.key_state["right"], self.key_state["left"]),
            vertical=bool_axis(self.key_state["up"], self.key_state["down"]),
            turn=bool_axis(self.key_state["turn_right"], self.key_state["turn_left"]),
            pitch=bool_axis(self.key_state["look_up"], self.key_state["look_down"]),
        )

    def update_scene(self, task):
        dt = globalClock.getDt()
        axis = self._read_axis_input()

        self.camera.setH(self.camera.getH() - scaled_delta(axis.turn, self.TURN_SPEED, dt))
        next_pitch = pitch_with_limits(
            self.camera.getP(),
            scaled_delta(axis.pitch, self.TURN_SPEED, dt),
        )
        self.camera.setP(next_pitch)

        self.camera.setY(self.camera, scaled_delta(axis.forward, self.MOVE_SPEED, dt))
        self.camera.setX(self.camera, scaled_delta(axis.strafe, self.MOVE_SPEED, dt))
        self.camera.setZ(self.camera.getZ() + scaled_delta(axis.vertical, self.MOVE_SPEED, dt))

        self._update_panda_focus()
        return task.cont

    def _update_panda_focus(self) -> None:
        if self.panda is None or self.status_text is None:
            return

        distance = (self.camera.getPos(self.render) - self.panda.getPos(self.render)).length()
        is_near = distance <= self.HIGHLIGHT_DISTANCE
        self.panda.setColor((1.0, 0.82, 0.28, 1) if is_near else (1, 1, 1, 1))
        self.status_text.setText(
            f"Camera: {self._format_vec(self.camera.getPos())} | Panda distance: {distance:.1f}"
        )

    @staticmethod
    def _format_vec(value: Vec3) -> str:
        return f"x={value.x:.1f}, y={value.y:.1f}, z={value.z:.1f}"
