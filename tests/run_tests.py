from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
EXAMPLES = ROOT / "examples"
GENERATED = ROOT / "generated"


def compile_examples():
    import achillesferse_compiler as afc

    GENERATED.mkdir(exist_ok=True)
    compiled = {}
    for src in sorted(EXAMPLES.glob("*.af")):
        out = GENERATED / f"{src.stem}.py"
        afc.compile_file(src, out)
        compiled[src.stem] = out
    return compiled


def load_program(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_calculator(compiled):
    from achillesferse_runtime import AchillesferseApp

    mod = load_program(compiled["calculator"])
    app = AchillesferseApp(mod.PROGRAM)
    app.root.update()
    app.call_function("append_token", "1")
    app.call_function("append_token", "2")
    app.call_function("append_token", "+")
    app.call_function("append_token", "3")
    app.call_function("append_token", "0")
    app.call_function("calculate")
    app.root.update()
    assert app.widget_text("display") == "42"
    app.app_exit()


def test_eliza(compiled):
    from achillesferse_runtime import AchillesferseApp

    mod = load_program(compiled["eliza"])
    app = AchillesferseApp(mod.PROGRAM)
    app.root.update()
    app.set_widget_text("user_input", "I feel sad")
    app.call_function("send")
    app.root.update()
    transcript = app.widget_text("conversation")
    assert "You: I feel sad" in transcript
    assert "How long have you felt sad?" in transcript
    app.app_exit()


def test_starfield(compiled):
    from achillesferse_runtime import AchillesferseApp

    mod = load_program(compiled["starfield"])
    app = AchillesferseApp(mod.PROGRAM)
    app.execute_block(mod.PROGRAM["on_start"])
    app.root.update()
    stars_before = [dict(s) for s in app.state["stars"]]
    app.execute_block(mod.PROGRAM["on_tick"]["body"])
    app.root.update()
    stars_after = app.state["stars"]
    assert len(stars_after) == len(stars_before)
    assert stars_after != stars_before
    app.app_exit()


def test_breakout(compiled):
    from achillesferse_runtime import AchillesferseApp

    mod = load_program(compiled["breakout"])
    app = AchillesferseApp(mod.PROGRAM)
    app.execute_block(mod.PROGRAM["on_start"])
    app.root.update()
    score_before = app.state["game"]["score"]
    for _ in range(5):
        app.execute_block(mod.PROGRAM["on_tick"]["body"])
    app.root.update()
    assert app.state["game"]["lives"] >= 1
    assert app.state["game"]["score"] >= score_before
    app.app_exit()


def test_todo_list(compiled):
    from achillesferse_runtime import AchillesferseApp

    mod = load_program(compiled["todo_list"])
    app = AchillesferseApp(mod.PROGRAM)
    app.root.update()
    app.set_widget_text("input", "Buy milk")
    app.call_function("add_item")
    app.root.update()
    assert "Buy milk" in app.widget_text("tasks")
    app.app_exit()


def test_startup_scripts(compiled):
    env = os.environ.copy()
    env["AF_TEST_AUTOCLOSE_MS"] = "250"
    for path in compiled.values():
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(ROOT),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
        )
        assert proc.returncode == 0, proc.stderr


def main():
    compiled = compile_examples()
    test_calculator(compiled)
    test_eliza(compiled)
    test_starfield(compiled)
    test_breakout(compiled)
    test_todo_list(compiled)
    test_startup_scripts(compiled)
    print(f"All Achillesferse tests passed for {len(compiled)} examples.")


if __name__ == "__main__":
    main()
