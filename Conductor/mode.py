from machine import Pin
def var():
    button = Pin(12, Pin.IN, Pin.PULL_UP)
    if button.value() == 0:
        return True
    else:
        return False