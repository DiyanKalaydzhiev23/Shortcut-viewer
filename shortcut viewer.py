from pynput import keyboard
from plyer import notification
from time import sleep


current = []
comb = []
is_possible = False

notification.notify(title="Shortcut viewer is on.",
                    message="To stop it press shift + esc.",
                    app_icon="shortcut-logo.ico")


def execute():
    global comb
    if "shift" in comb and "esc" in comb and len(comb) == 2:
        notification.notify(title="Shortcut viewer is closing",
                            message="Thank you for using the app.",
                            app_icon="shortcut-logo.ico",
                            timeout=1)
        sleep(5)
        raise SystemExit
    comb = list(set(comb))
    comb.sort(key=len, reverse=True)
    title = ' + '.join(comb)
    notification.notify(app_name="Shortcut viewer",
                        title=title,
                        message="was used.",
                        app_icon="shortcut-logo.ico",
                        timeout=1)
    comb.clear()


def on_press(key):
    global is_possible
    new_key = str(key)
    new_key = new_key.replace("Key.", "")
    new_key = new_key.replace("_l", "")
    new_key = new_key.replace("_r", "")
    current.append(key)
    if new_key == "ctrl" or new_key == "shift" or new_key == "alt" or new_key == "cmd":
        comb.append(new_key)
        is_possible = True
    elif is_possible:
        comb.append(new_key)
        comb[-1] = str(comb[-1]).replace("\\", "0", 1)
        comb[-1] = str(comb[-1]).replace("'", "")
        if comb[-1] == "<191>":
            comb[-1] = "/"
        elif len(comb[-1]) > 1 and not str(comb[-1]).isalpha() and "f" not in str(comb[-1]):
            if comb[-1] == "0t":
                comb[-1] = "0x09"
            comb[-1] = chr(int(comb[-1], 16) + 64)
        is_possible = False
        execute()


def on_release(key):
    global is_possible
    if not current:
        execute()
        is_possible = False
    else:
        current.pop(0)


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
