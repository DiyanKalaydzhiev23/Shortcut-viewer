from pynput import keyboard
from plyer import notification


current = []
comb = []
is_possible = False


def execute():
    global comb
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
    print(new_key)
    new_key = new_key.replace("Key.", "")
    new_key = new_key.replace("_l", "")
    new_key = new_key.replace("_r", "")
    current.append(key)
    if new_key == "ctrl" or new_key == "shift" or new_key == "alt" or new_key == "cmd":
        comb.append(new_key)
        is_possible = True
    elif is_possible:
        comb.append(new_key)
        if not (comb[-1] == "ctrl" or comb[-1] == "shift" or comb[-1] == "alt" or comb[-1] == "cmd"):
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
    current.pop(0)


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
