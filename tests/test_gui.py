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
    assert app.ev_value.get() == "252"
    assert app.num_value.get() == "1"
    assert app.result_text.get() == "The result's gonna be written here."


RESULT_252_3 = (
    "Give power-item each of them\n"
    "7 times in flock battle.\n"
    "Then take it away, 1 flock battles\n"
    "and kick 2 pokemons' ass one by one.\n"
    "24 battles in total."
)


def test_shows_result(app):
    assert press_calculate(app, "252", "3") == RESULT_252_3


@pytest.mark.parametrize("key", ["<Return>", "<KP_Enter>"])
def test_enter_key_calculates(app, key):
    _, num_entry = find_widgets(app, tkinter.Entry)
    num_entry.delete(0, tkinter.END)
    num_entry.insert(0, "3")
    num_entry.focus_force()
    app.update()
    num_entry.event_generate(key)
    assert app.result_text.get() == RESULT_252_3


@pytest.mark.parametrize(
    ("ev", "num"),
    [
        ("0", "1"),
        ("253", "1"),
        ("252", "7"),
        ("abc", "1"),
        ("252", ""),
        ("2.5", "1"),
        ("252", "1.9"),
        ("1e2", "1"),
    ],
)
def test_shows_error_for_invalid_input(app, ev, num):
    press_calculate(app, "252", "1")
    assert press_calculate(app, ev, num) == "Please input EV 1-252 and pokemons 1-6."


def test_accepts_full_width_digits_and_spaces(app):
    assert press_calculate(app, "２５２", " 3 ") == RESULT_252_3  # noqa: RUF001
