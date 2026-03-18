from __future__ import annotations

import json
import math
import os
import random
import re
import sys
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from typing import Any, Callable


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def parse_font(value: Any):
    if value is None:
        return None
    if isinstance(value, (tuple, list)):
        return tuple(value)
    text = str(value).strip()
    if not text:
        return None
    parts = text.rsplit(" ", 1)
    if len(parts) == 2 and parts[1].lstrip("-").isdigit():
        return (parts[0], int(parts[1]))
    return text


def init_starfield(count: int, width: int, height: int):
    stars = []
    for _ in range(int(count)):
        stars.append({
            "x": random.uniform(-width / 2, width / 2),
            "y": random.uniform(-height / 2, height / 2),
            "z": random.uniform(0.2, 1.0),
        })
    return stars


def step_starfield(stars, speed: float, width: int, height: int):
    out = []
    speed = float(speed)
    for star in stars:
        z = float(star["z"]) - speed / 1000.0
        if z <= 0.02:
            out.append({
                "x": random.uniform(-width / 2, width / 2),
                "y": random.uniform(-height / 2, height / 2),
                "z": random.uniform(0.8, 1.0),
            })
            continue
        out.append({"x": star["x"], "y": star["y"], "z": z})
    return out


def eliza_reply(text: str) -> str:
    cleaned = " ".join(str(text).strip().split())
    if not cleaned:
        return "Please say a little more."
    if cleaned.endswith("?"):
        return "What do you think?"
    reflections = [
        (r"\bI need (.*)", "Why do you need {0}?"),
        (r"\bI feel (.*)", "How long have you felt {0}?"),
        (r"\bI am (.*)", "How does being {0} make you feel?"),
        (r"\bI'm (.*)", "How does being {0} make you feel?"),
        (r"\bI can't (.*)", "What makes you think you can't {0}?"),
        (r"\bI remember (.*)", "What does remembering {0} bring up for you?"),
        (r"\bmy (.*)", "Tell me more about your {0}."),
        (r"\bbecause (.*)", "Is that the real reason?"),
        (r"\bmother\b", "Tell me more about your family."),
        (r"\bfather\b", "How was your relationship with your father?"),
        (r"\bfriend\b", "Why do you mention your friends right now?"),
        (r"\byes\b", "You sound quite certain."),
        (r"\bno\b", "Why not?"),
    ]
    for pattern, reply in reflections:
        match = re.search(pattern, cleaned, re.IGNORECASE)
        if match:
            groups = [g.strip() for g in match.groups()]
            return reply.format(*groups)
    fallback = [
        "Please go on.",
        "Can you elaborate on that?",
        "How does that make you feel?",
        "Why do you say that?",
        "That is interesting. Tell me more.",
    ]
    return random.choice(fallback)


def calculate_expression(expr: str) -> str:
    try:
        return safe_eval(expr)
    except Exception:
        return "Error"


def safe_eval(expr: str) -> str:
    expr = expr.strip()
    if not expr:
        return ""
    allowed = set("0123456789+-*/().% ")
    if any(ch not in allowed for ch in expr):
        raise ValueError("Only digits and + - * / % ( ) . are allowed.")
    return str(eval(expr, {"__builtins__": {}}, {}))


def now_text(fmt: str = "%H:%M:%S") -> str:
    return datetime.now().strftime(fmt)


def draw_mandelbrot(canvas, center_x=-0.5, center_y=0.0, zoom=1.0, max_iter=40, block=4):
    width = max(1, int(canvas.winfo_width() or canvas.cget("width")))
    height = max(1, int(canvas.winfo_height() or canvas.cget("height")))
    canvas.delete("all")
    zoom = max(0.0001, float(zoom))
    max_iter = max(8, int(max_iter))
    block = max(1, int(block))
    scale = 3.0 / zoom

    def color_for(i):
        if i >= max_iter:
            return "#000000"
        t = i / max_iter
        r = int(9 * (1 - t) * t * t * t * 255)
        g = int(15 * (1 - t) * (1 - t) * t * t * 255)
        b = int(8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    for py in range(0, height, block):
        y0 = center_y + (py - height / 2) / (height / 2) * scale * (height / max(1, width))
        for px in range(0, width, block):
            x0 = center_x + (px - width / 2) / (width / 2) * scale
            x = 0.0
            y = 0.0
            iteration = 0
            while x * x + y * y <= 4.0 and iteration < max_iter:
                x, y = x * x - y * y + x0, 2 * x * y + y0
                iteration += 1
            color = color_for(iteration)
            canvas.create_rectangle(px, py, px + block, py + block, outline="", fill=color)


def breakout_new(width: int, height: int, brick_rows: int = 5, brick_cols: int = 9):
    width = int(width)
    height = int(height)
    bricks = []
    margin_x = 20
    top = 40
    gap = 6
    brick_w = (width - 2 * margin_x - gap * (brick_cols - 1)) / brick_cols
    brick_h = 18
    colors = ["#FF6B6B", "#FFD166", "#06D6A0", "#4CC9F0", "#B388EB"]
    for row in range(brick_rows):
        for col in range(brick_cols):
            x = margin_x + col * (brick_w + gap)
            y = top + row * (brick_h + gap)
            bricks.append({"x": x, "y": y, "w": brick_w, "h": brick_h, "color": colors[row % len(colors)], "alive": True})
    return {
        "ball_x": width / 2,
        "ball_y": height * 0.70,
        "ball_r": 8,
        "vx": 4.2,
        "vy": -4.2,
        "paddle_x": width / 2 - 55,
        "paddle_y": height - 32,
        "paddle_w": 110,
        "paddle_h": 12,
        "score": 0,
        "lives": 3,
        "game_over": False,
        "win": False,
        "bricks": bricks,
    }


def breakout_move_paddle(state, delta: float, width: int):
    state = dict(state)
    state["paddle_x"] = max(0, min(float(width) - state["paddle_w"], state["paddle_x"] + float(delta)))
    return state


def breakout_step(state, width: int, height: int):
    state = dict(state)
    if state.get("game_over") or state.get("win"):
        return state

    width = float(width)
    height = float(height)
    bx = state["ball_x"] + state["vx"]
    by = state["ball_y"] + state["vy"]
    r = state["ball_r"]

    if bx - r <= 0 or bx + r >= width:
        state["vx"] *= -1
        bx = max(r, min(width - r, bx))
    if by - r <= 0:
        state["vy"] *= -1
        by = r
    if by + r >= height:
        state["lives"] -= 1
        if state["lives"] <= 0:
            state["game_over"] = True
            return state
        state["ball_x"] = width / 2
        state["ball_y"] = height * 0.70
        state["vx"] = 4.2 * (-1 if random.random() < 0.5 else 1)
        state["vy"] = -4.2
        return state

    px = state["paddle_x"]
    py = state["paddle_y"]
    pw = state["paddle_w"]
    ph = state["paddle_h"]
    if (px - r) <= bx <= (px + pw + r) and (py - r) <= by <= (py + ph + r) and state["vy"] > 0:
        offset = (bx - (px + pw / 2)) / max(1, pw / 2)
        state["vx"] = 5.0 * offset
        state["vy"] = -abs(state["vy"])
        by = py - r - 1

    bricks = []
    hit_brick = False
    for brick in state["bricks"]:
        brick = dict(brick)
        if brick["alive"] and (brick["x"] - r) <= bx <= (brick["x"] + brick["w"] + r) and (brick["y"] - r) <= by <= (brick["y"] + brick["h"] + r):
            brick["alive"] = False
            state["vy"] *= -1
            state["score"] += 10
            hit_brick = True
        bricks.append(brick)
    state["bricks"] = bricks
    if hit_brick and all(not b["alive"] for b in bricks):
        state["win"] = True

    state["ball_x"] = bx
    state["ball_y"] = by
    return state


def breakout_draw(canvas, state):
    canvas.delete("all")
    width = max(1, int(canvas.winfo_width() or canvas.cget("width")))
    height = max(1, int(canvas.winfo_height() or canvas.cget("height")))
    canvas.create_rectangle(0, 0, width, height, outline="", fill="#10131A")
    for brick in state.get("bricks", []):
        if brick.get("alive"):
            canvas.create_rectangle(brick["x"], brick["y"], brick["x"] + brick["w"], brick["y"] + brick["h"], outline="", fill=brick["color"])
    canvas.create_rectangle(state["paddle_x"], state["paddle_y"], state["paddle_x"] + state["paddle_w"], state["paddle_y"] + state["paddle_h"], outline="", fill="#E6EAF0")
    r = state["ball_r"]
    canvas.create_oval(state["ball_x"] - r, state["ball_y"] - r, state["ball_x"] + r, state["ball_y"] + r, outline="", fill="#FFFFFF")
    canvas.create_text(70, height - 14, text=f"Score: {state['score']}", fill="#D8DEE9", font=("Segoe UI", 10, "bold"))
    canvas.create_text(width - 70, height - 14, text=f"Lives: {state['lives']}", fill="#D8DEE9", font=("Segoe UI", 10, "bold"))
    if state.get("game_over"):
        canvas.create_text(width / 2, height / 2, text="Game Over", fill="#FF6B6B", font=("Segoe UI", 22, "bold"))
    elif state.get("win"):
        canvas.create_text(width / 2, height / 2, text="You Win!", fill="#06D6A0", font=("Segoe UI", 22, "bold"))


class ReturnSignal(Exception):
    def __init__(self, value: Any = None):
        self.value = value
        super().__init__("return")


class AchillesferseApp:
    def __init__(self, program: dict[str, Any]):
        self.program = program
        app_meta = program.get("app", {})
        self.root = tk.Tk()
        self.root.title(app_meta.get("title", "Achillesferse App"))
        width = int(app_meta.get("width", 800))
        height = int(app_meta.get("height", 600))
        self.root.geometry(f"{width}x{height}")
        bg = app_meta.get("bg")
        if bg:
            self.root.configure(bg=bg)

        self.widgets: dict[str, Any] = {}
        self.state: dict[str, Any] = {}
        self.functions = program.get("functions", {})
        self._tick_after_id = None
        self._start_after_id = None
        self.last_event = None

        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self._init_state()
        self._build_widgets()
        self._bind_events()

        on_start = program.get("on_start", [])
        if on_start:
            self._start_after_id = self.root.after(30, lambda: self.execute_block(on_start))

        tick = program.get("on_tick")
        if tick:
            delay = int(tick.get("ms", 33))
            self._schedule_tick(delay, tick.get("body", []))

        autoclose_ms = os.environ.get("AF_TEST_AUTOCLOSE_MS")
        if autoclose_ms:
            try:
                self.root.after(int(autoclose_ms), self._close)
            except Exception:
                pass

    def _init_state(self):
        for name, expr in self.program.get("vars", {}).items():
            self.state[name] = self.eval_expr(expr)

    def _parent_for(self, parent_name: str | None):
        if parent_name and parent_name in self.widgets:
            return self.widgets[parent_name]
        return self.root

    def _coerce_opt(self, value: Any):
        if isinstance(value, str):
            lower = value.strip().lower()
            if lower in {"true", "false"}:
                return lower == "true"
            if lower.lstrip("-").isdigit():
                return int(lower)
            try:
                if "." in lower:
                    return float(lower)
            except Exception:
                pass
        return value

    def _build_widgets(self):
        for spec in self.program.get("widgets", []):
            name = spec["name"]
            wtype = spec["type"].upper()
            opts = dict(spec.get("options", {}))
            parent = self._parent_for(opts.pop("parent", None))

            common = {}
            for key in ("text", "bg", "fg", "width", "height", "wrap", "justify"):
                if key in opts:
                    common[key] = self._coerce_opt(opts.pop(key))
            if "font" in opts:
                common["font"] = parse_font(opts.pop("font"))

            if wtype == "LABEL":
                widget = tk.Label(parent, **common)
            elif wtype == "ENTRY":
                widget = tk.Entry(parent, **common)
                if parse_bool(spec.get("options", {}).get("readonly")):
                    widget.configure(state="readonly")
            elif wtype == "BUTTON":
                action = opts.pop("action", "")
                widget = tk.Button(parent, command=self.make_action(action), **common)
            elif wtype == "TEXT":
                widget = tk.Text(parent, **common)
                if parse_bool(spec.get("options", {}).get("readonly")):
                    widget.configure(state="disabled")
            elif wtype == "CANVAS":
                widget = tk.Canvas(parent, **common)
            elif wtype == "FRAME":
                widget = tk.Frame(parent, **{k: v for k, v in common.items() if k in {"bg"}})
            elif wtype == "LISTBOX":
                widget = tk.Listbox(parent, **common)
            else:
                raise ValueError(f"Unknown widget type: {wtype}")

            self.widgets[name] = widget
            self._place_widget(widget, spec.get("options", {}))

    def _place_widget(self, widget: Any, opts: dict[str, Any]):
        if "row" in opts or "column" in opts:
            grid_kwargs = {}
            for key in ("row", "column", "rowspan", "columnspan", "sticky", "padx", "pady", "ipadx", "ipady"):
                if key in opts:
                    grid_kwargs[key] = self._coerce_opt(opts[key])
            widget.grid(**grid_kwargs)
        else:
            pack_kwargs = {}
            for key in ("side", "fill", "padx", "pady"):
                if key in opts:
                    pack_kwargs[key] = self._coerce_opt(opts[key])
            if "expand" in opts:
                pack_kwargs["expand"] = parse_bool(opts["expand"])
            widget.pack(**pack_kwargs)

    def _run_bound_action(self, action: str, event: Any):
        self.last_event = event
        try:
            self.make_action(action)()
        finally:
            self.last_event = None

    def _bind_events(self):
        for spec in self.program.get("bindings", []):
            widget = self.widgets[spec["widget"]]
            event = spec["event"]
            action = spec["action"]
            widget.bind(event, lambda e, action=action: self._run_bound_action(action, e))

    def _schedule_tick(self, delay: int, body):
        def runner():
            try:
                self.execute_block(body)
            except tk.TclError:
                return
            finally:
                try:
                    if self.root.winfo_exists():
                        self._tick_after_id = self.root.after(delay, runner)
                except tk.TclError:
                    return
        self._tick_after_id = self.root.after(delay, runner)

    def _close(self):
        for after_id in (self._start_after_id, self._tick_after_id):
            if after_id:
                try:
                    self.root.after_cancel(after_id)
                except Exception:
                    pass
        self._start_after_id = None
        self._tick_after_id = None
        try:
            if self.root.winfo_exists():
                self.root.destroy()
        except Exception:
            pass

    def make_action(self, action: str) -> Callable[[], None]:
        action = (action or "").strip()
        if not action:
            return lambda: None
        def _runner():
            self.eval_expr(action)
        return _runner

    def get_widget(self, widget_ref: Any):
        if isinstance(widget_ref, str) and widget_ref in self.widgets:
            return self.widgets[widget_ref]
        return widget_ref

    def widget_text(self, widget_ref: Any) -> str:
        widget = self.get_widget(widget_ref)
        if isinstance(widget, tk.Entry):
            return widget.get()
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c")
        if isinstance(widget, tk.Label):
            return str(widget.cget("text"))
        if isinstance(widget, tk.Listbox):
            selected = widget.curselection()
            if selected:
                return str(widget.get(selected[0]))
            return "\n".join(str(widget.get(i)) for i in range(widget.size()))
        return ""

    def set_widget_text(self, widget_ref: Any, value: Any):
        widget = self.get_widget(widget_ref)
        text = "" if value is None else str(value)
        if isinstance(widget, tk.Entry):
            readonly = str(widget.cget("state")) == "readonly"
            if readonly:
                widget.configure(state="normal")
            widget.delete(0, tk.END)
            widget.insert(0, text)
            if readonly:
                widget.configure(state="readonly")
        elif isinstance(widget, tk.Text):
            disabled = str(widget.cget("state")) == "disabled"
            if disabled:
                widget.configure(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert("1.0", text)
            if disabled:
                widget.configure(state="disabled")
        elif isinstance(widget, tk.Label):
            widget.configure(text=text)
        elif isinstance(widget, tk.Listbox):
            widget.delete(0, tk.END)
            lines = text.splitlines() if text else []
            for line in lines:
                widget.insert(tk.END, line)
        else:
            raise TypeError("UISET supports Entry, Text, Label and Listbox widgets.")

    def append_widget_text(self, widget_ref: Any, value: Any):
        widget = self.get_widget(widget_ref)
        text = "" if value is None else str(value)
        if isinstance(widget, tk.Entry):
            widget.insert(tk.END, text)
        elif isinstance(widget, tk.Text):
            disabled = str(widget.cget("state")) == "disabled"
            if disabled:
                widget.configure(state="normal")
            widget.insert(tk.END, text)
            widget.see(tk.END)
            if disabled:
                widget.configure(state="disabled")
        elif isinstance(widget, tk.Label):
            current = widget.cget("text")
            widget.configure(text=f"{current}{text}")
        elif isinstance(widget, tk.Listbox):
            for line in text.splitlines() or [text]:
                if line != "":
                    widget.insert(tk.END, line)
        else:
            raise TypeError("APPEND supports Entry, Text, Label and Listbox widgets.")

    def clear_widget(self, widget_ref: Any):
        widget = self.get_widget(widget_ref)
        if isinstance(widget, tk.Listbox):
            widget.delete(0, tk.END)
            return
        self.set_widget_text(widget_ref, "")

    def focus_widget(self, widget_ref: Any):
        self.get_widget(widget_ref).focus_set()

    def clear_canvas(self, widget_ref: Any):
        self.get_widget(widget_ref).delete("all")

    def canvas_rect(self, widget_ref: Any, x1, y1, x2, y2, **kwargs):
        return self.get_widget(widget_ref).create_rectangle(x1, y1, x2, y2, **kwargs)

    def canvas_oval(self, widget_ref: Any, x1, y1, x2, y2, **kwargs):
        return self.get_widget(widget_ref).create_oval(x1, y1, x2, y2, **kwargs)

    def canvas_line(self, widget_ref: Any, x1, y1, x2, y2, **kwargs):
        return self.get_widget(widget_ref).create_line(x1, y1, x2, y2, **kwargs)

    def canvas_text(self, widget_ref: Any, x, y, text, **kwargs):
        return self.get_widget(widget_ref).create_text(x, y, text=text, **kwargs)

    def draw_starfield(self, widget_ref: Any, stars):
        canvas = self.get_widget(widget_ref)
        self.clear_canvas(canvas)
        width = max(1, int(canvas.winfo_width() or canvas.cget("width")))
        height = max(1, int(canvas.winfo_height() or canvas.cget("height")))
        cx = width / 2
        cy = height / 2
        for star in stars:
            z = max(0.02, float(star["z"]))
            x = cx + float(star["x"]) / z
            y = cy + float(star["y"]) / z
            size = max(1.0, 3.0 * (1.1 - z))
            if 0 <= x <= width and 0 <= y <= height:
                canvas.create_oval(x, y, x + size, y + size, fill="white", outline="")

    def sound_beep(self, frequency: int = 880, duration: int = 120):
        try:
            if sys.platform.startswith("win"):
                import winsound
                winsound.Beep(int(frequency), int(duration))
            else:
                self.root.bell()
        except Exception:
            try:
                self.root.bell()
            except Exception:
                pass

    def app_exit(self):
        self._close()

    def event_x(self) -> int:
        return int(getattr(self.last_event, "x", 0) or 0)

    def event_y(self) -> int:
        return int(getattr(self.last_event, "y", 0) or 0)

    def event_keysym(self) -> str:
        return str(getattr(self.last_event, "keysym", "") or "")

    def listbox_delete_selected(self, widget_ref: Any):
        widget = self.get_widget(widget_ref)
        if isinstance(widget, tk.Listbox):
            selected = list(widget.curselection())
            selected.reverse()
            for idx in selected:
                widget.delete(idx)

    def build_eval_env(self) -> dict[str, Any]:
        env: dict[str, Any] = {
            "math": math,
            "random": random,
            "json": json,
            "time": time,
            "messagebox": messagebox,
            "init_starfield": init_starfield,
            "step_starfield": step_starfield,
            "safe_eval": safe_eval,
            "calculate_expression": calculate_expression,
            "eliza_reply": eliza_reply,
            "now_text": now_text,
            "text": self.widget_text,
            "ui": self.get_widget,
            "state": self.state,
            "widgets": self.widgets,
            "canvas_rect": self.canvas_rect,
            "canvas_oval": self.canvas_oval,
            "canvas_line": self.canvas_line,
            "canvas_text": self.canvas_text,
            "canvas_clear": self.clear_canvas,
            "draw_starfield": self.draw_starfield,
            "draw_mandelbrot": lambda widget_ref, center_x=-0.5, center_y=0.0, zoom=1.0, max_iter=40, block=4: draw_mandelbrot(self.get_widget(widget_ref), center_x, center_y, zoom, max_iter, block),
            "breakout_new": breakout_new,
            "breakout_step": breakout_step,
            "breakout_move_paddle": breakout_move_paddle,
            "breakout_draw": lambda widget_ref, game_state: breakout_draw(self.get_widget(widget_ref), game_state),
            "sound_beep": self.sound_beep,
            "focus_widget": self.focus_widget,
            "app_exit": self.app_exit,
            "event_x": self.event_x,
            "event_y": self.event_y,
            "event_keysym": self.event_keysym,
            "listbox_delete_selected": self.listbox_delete_selected,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "len": len,
            "min": min,
            "max": max,
            "sum": sum,
            "range": range,
            "round": round,
            "abs": abs,
        }
        env.update(self.state)
        env.update(self.widgets)
        for name in self.functions.keys():
            env[name] = self._make_function_proxy(name)
        return env

    def _make_function_proxy(self, name: str):
        def _proxy(*args):
            return self.call_function(name, *args)
        return _proxy

    def eval_expr(self, expr: Any):
        if expr is None:
            return None
        if isinstance(expr, (int, float, bool, list, dict)):
            return expr
        text = str(expr).strip()
        if text == "":
            return ""
        env = self.build_eval_env()
        return eval(text, {"__builtins__": {}}, env)

    def execute_block(self, block):
        self._execute_statements(block)

    def _execute_statements(self, statements):
        for stmt in statements:
            stype = stmt["type"]
            if stype == "set":
                self.state[stmt["name"]] = self.eval_expr(stmt["expr"])
            elif stype == "uiset":
                self.set_widget_text(stmt["widget"], self.eval_expr(stmt["expr"]))
            elif stype == "append":
                self.append_widget_text(stmt["widget"], self.eval_expr(stmt["expr"]))
            elif stype == "clear":
                self.clear_widget(stmt["widget"])
            elif stype == "focus":
                self.focus_widget(stmt["widget"])
            elif stype == "canvas_clear":
                self.clear_canvas(stmt["widget"])
            elif stype == "draw_starfield":
                self.draw_starfield(stmt["widget"], self.eval_expr(stmt["expr"]))
            elif stype == "expr":
                self.eval_expr(stmt["expr"])
            elif stype == "return":
                value = self.eval_expr(stmt["expr"]) if stmt.get("expr") else None
                raise ReturnSignal(value)
            elif stype == "if":
                cond = self.eval_expr(stmt["cond"])
                if cond:
                    self._execute_statements(stmt["then"])
                else:
                    handled = False
                    for elif_branch in stmt.get("elifs", []):
                        if self.eval_expr(elif_branch["cond"]):
                            self._execute_statements(elif_branch["body"])
                            handled = True
                            break
                    if not handled and stmt.get("else"):
                        self._execute_statements(stmt["else"])
            elif stype == "for":
                iterable = self.eval_expr(stmt["iterable"])
                for item in iterable:
                    self.state[stmt["name"]] = item
                    self._execute_statements(stmt["body"])
            elif stype == "while":
                guard = 0
                while self.eval_expr(stmt["cond"]):
                    self._execute_statements(stmt["body"])
                    guard += 1
                    if guard > 100000:
                        raise RuntimeError("Loop guard triggered.")
            else:
                raise ValueError(f"Unknown statement type: {stype}")

    def call_function(self, name: str, *args):
        spec = self.functions[name]
        params = spec.get("params", [])
        missing = object()
        backup = {}
        for idx, param in enumerate(params):
            backup[param] = self.state.get(param, missing)
            self.state[param] = args[idx] if idx < len(args) else None
        try:
            try:
                self._execute_statements(spec.get("body", []))
            except ReturnSignal as signal:
                return signal.value
        finally:
            for param in params:
                previous = backup.get(param, missing)
                if previous is missing:
                    self.state.pop(param, None)
                else:
                    self.state[param] = previous
        return None

    def run(self):
        self.root.mainloop()
