import tkinter

import pytest

from effort_leveling_support import GELS


@pytest.fixture
def app():
    root = tkinter.Tk()
    app = GELS(root)
    app.pack()
    yield app
    root.destroy()


def find_widgets(widget, widget_class):
    found = []
    for child in widget.winfo_children():
        if isinstance(child, widget_class):
            found.append(child)
        found.extend(find_widgets(child, widget_class))
    return found


def press_calculate(app, ev, num):
    ev_entry, num_entry = find_widgets(app, tkinter.Entry)
    for entry, value in ((ev_entry, ev), (num_entry, num)):
        entry.delete(0, tkinter.END)
        entry.insert(0, value)
    (button,) = find_widgets(app, tkinter.Button)
    button.invoke()
    return app.result_text.get()


def test_initial_values(app):
    assert app.ev_value.get() == 252
    assert app.num_value.get() == 1
    assert app.result_text.get() == "The result's gonna be written here."


def test_shows_result(app):
    assert press_calculate(app, "252", "3") == (
        "Give power-item each of them\n"
        "7 times in flock battle.\n"
        "And then kick 7 pokemons' ass"
    )


def test_shows_result_for_large_ev(app):
    assert press_calculate(app, "5000", "1") == (
        "Give power-item each of them\n"
        "200 times in flock battle.\n"
        "And then kick 0 pokemons' ass"
    )


@pytest.mark.parametrize(("ev", "num"), [("0", "1"), ("abc", "1"), ("252", "")])
def test_shows_error_for_invalid_input(app, ev, num):
    press_calculate(app, "252", "1")
    assert press_calculate(app, ev, num) == "Please input valid numbers."
