MicroPython Matrix8x8 Driver
============================

MicroPython driver for AdaFruit 8x8 LED Matrix display with HT16K33 backpack.

Installation
------------

Copy `matrix8x8.py` file to your pyboard.

Usage
-----

```
from matrix8x8 import Matrix8x8
display = Matrix8x8()
display.set_row(2, 0xFF)      # turn on all LEDs in row 2
display.set_column(3, 0xFF)   # turn on all LEDs in column 3
display.set_pixel(7, 6)             # turn on LED at row 7, column 6
...
```

**Device controll methods:**

```
__init__(i2c_bus=1, addr=0x70, brightness=15, i2c=None)
    Params:
    * i2c_bus = I2C bus ID (1 or 2) or None (if param 'i2c' is provided)
    * addr = I2C address of connected display
    * brightness = display brightness (0 - 15)
    * i2c = initialised instance of pyb.I2C object

on()
    Turn on display.

off()
    Turn off display. You can controll display when it's off (change image,
    brightness, blinking, ...).

set_brightness(value)
    Set display brightness. Value from 0 (min) to 15 (max).

set_blinking(mode)
    Set blinking. Modes:
        0 - blinking off
        1 - blinking at 2Hz
        2 - blinking at 1Hz
        3 - blinking at 0.5Hz
```

**Image maipulation methods:**

```
set(bitmap)
    Show bitmap on display. Bitmap should be 8 bytes/bytearray object or any
    iterable object containing 8 bytes (one byte per row).

set_row(row, byte)
    Set row by byte.

set_column(column, byte)
    Set column by byte.

set_pixel(row, column)
    Set (turn on) pixel.

clear()
    Clear display.

clear_row(row)
    Clear row.

clear_column(column)
    Clear column.

clear_pixel(row, column)
    Clear pixel.
```

Notes:
* Rows a columns are numbered from 0 to 7.

Examples
--------

`examples/test_features.py` - Simple demo of display/driver fetures and usage.
`examples/game_of_life.py` - Conway's Game of Life. In action video:
http://youtu.be/XZgU1wqZMic

You can copy one of the examples to your pyboard as `main.py` and if you connect
display to I2C bus 1, they will instantly work.

Wiring
------

LED Matrix display is using I2C bus. You can connect and controll more displays
with one I2C bus if you change I2C address of display.

Example of wiring to I2C bus 1 on breadboard:

![](https://github.com/JanBednarik/micropython-matrix8x8/blob/master/docs/pyboard-matrix-wiring.jpg)

More info & Help
----------------

You can check more about the MicroPython project here: http://micropython.org
