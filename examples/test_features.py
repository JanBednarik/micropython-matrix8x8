import pyb

from matrix8x8 import Matrix8x8


display = Matrix8x8(brightness=0)

while True:
    # test set() and clear()
    display.set(b'\xFF' * 8)
    pyb.delay(500)
    display.clear()
    pyb.delay(500)
    display.set(b'\x55\xAA' * 4)
    pyb.delay(500)
    display.set(b'\xAA\x55' * 4)
    pyb.delay(500)
    display.clear()

    # test set_row(), clear_row()
    for i in range(8):
        display.set_row(i, 0xFF)
        pyb.delay(100)
    for i in range(8):
        display.clear_row(i)
        pyb.delay(100)
    display.clear()

    # test set_column(), clear_column()
    for i in range(8):
        display.set_column(i, 0xFF)
        pyb.delay(100)
    for i in range(8):
        display.clear_column(i)
        pyb.delay(100)
    display.clear()

    # test set_pixel(), clear_pixel()
    for row in range(8):
        for column in range(8):
            display.set_pixel(row, column)
            pyb.delay(40)
    for row in range(8):
        for column in range(8):
            display.clear_pixel(row, column)
            pyb.delay(40)
    display.clear()

    # test set_brightness()
    display.set(b'\xFF' * 8)
    for i in range(16):
        display.set_brightness(i)
        pyb.delay(100)
    for i in range(16):
        display.set_brightness(16-i)
        pyb.delay(100)

    # test on(), off()
    display.set(b'\xAA' * 8)
    pyb.delay(500)
    display.off()
    pyb.delay(500)
    display.on()

    # test set_blinking()
    display.set_blinking(3)
    pyb.delay(5000)
    display.set_blinking(2)
    pyb.delay(5000)
    display.set_blinking(1)
    pyb.delay(5000)
    display.set_blinking(0)
    pyb.delay(2000)

    # test changes when display is in off state
    display.off()
    pyb.delay(500)
    display.set(b'\x33' * 8)
    display.set_blinking(1)
    display.on()
    pyb.delay(2000)
    display.set_blinking(0)
