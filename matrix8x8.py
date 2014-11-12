import pyb


class Matrix8x8:
    """
    Driver for AdaFruit 8x8 LED Matrix display with HT16K33 backpack.
    Example of use:

    display = Matrix8x8()
    display.set(b'\xFF' * 8)    # turn on all LEDs
    display.clear()             # turn off all LEDs
    display.set_row(2, 0xFF)    # turn on all LEDs in row 2
    display.set_column(3, 0xFF) # turn on all LEDs in column 3
    display.set_pixel(7, 6)     # turn on LED at row 7, column 6
    """
    row_addr = (0x00, 0x02, 0x04, 0x06, 0x08, 0x0A, 0x0C, 0x0E)

    def __init__(self, i2c_bus=1, addr=0x70, brightness=15, i2c=None):
        """
        Params:
        * i2c_bus = I2C bus ID (1 or 2) or None (if param 'i2c' is provided)
        * addr = I2C address of connected display
        * brightness = display brightness (0 - 15)
        * i2c = initialised instance of pyb.I2C object
        """
        self._blinking = 0
        self.addr = addr
        self.buf = bytearray(8)

        # I2C init
        if i2c:
            self.i2c = i2c
        else:
            self.i2c = pyb.I2C(i2c_bus, pyb.I2C.MASTER, baudrate=400000)

        # set HT16K33 oscillator on
        self._send(0x21)

        self.set_brightness(brightness)
        self.clear()
        self.on()

    def _send(self, data):
        """
        Send data over I2C.
        """
        self.i2c.send(data, self.addr)

    def _send_row(self, row):
        """
        Send single row over I2C.
        """
        data = bytes((self.row_addr[row], rotate_right(self.buf[row])))
        self._send(data)

    def _send_buf(self):
        """
        Send buffer over I2C.
        """
        data = bytearray(16)
        i = 1
        for byte in self.buf:
            data[i] = rotate_right(byte)
            i += 2
        self._send(data)

    def _clear_column(self, column):
        """
        Clear column in buffer (set it to 0).
        """
        mask = 0x80 >> column
        for row in range(8):
            if self.buf[row] & mask:
                self.buf[row] ^= mask

    def _set_column(self, column, byte):
        """
        Set column in buffer by byte.
        """
        self._clear_column(column)
        if byte == 0:
            return
        mask = 0x80
        for row in range(8):
            shift = column - row
            if shift >= 0:
                self.buf[row] |= (byte & mask) >> shift
            else:
                self.buf[row] |= (byte & mask) << abs(shift)
            mask >>= 1

    def on(self):
        """
        Turn on display.
        """
        self.is_on = True
        self._send(0x81 | self._blinking << 1)

    def off(self):
        """
        Turn off display. You can controll display when it's off (change image,
        brightness, blinking, ...).
        """
        self.is_on = False
        self._send(0x80)

    def set_brightness(self, value):
        """
        Set display brightness. Value from 0 (min) to 15 (max).
        """
        self._send(0xE0 | value)

    def set_blinking(self, mode):
        """
        Set blinking. Modes:
            0 - blinking off
            1 - blinking at 2Hz
            2 - blinking at 1Hz
            3 - blinking at 0.5Hz
        """
        self._blinking = mode
        if self.is_on:
            self.on()

    def set(self, bitmap):
        """
        Show bitmap on display. Bitmap should be 8 bytes/bytearray object or any
        iterable object containing 8 bytes (one byte per row).
        """
        self.buf = bytearray(bitmap)
        self._send_buf()

    def clear(self):
        """
        Clear display.
        """
        for i in range(8):
            self.buf[i] = 0
        self._send_buf()

    def set_row(self, row, byte):
        """
        Set row by byte.
        """
        self.buf[row] = byte
        self._send_row(row)

    def clear_row(self, row):
        """
        Clear row.
        """
        self.set_row(row, 0)

    def set_column(self, column, byte):
        """
        Set column by byte.
        """
        self._set_column(column, byte)
        self._send_buf()

    def clear_column(self, column):
        """
        Clear column.
        """
        self._clear_column(column)
        self._send_buf()

    def set_pixel(self, row, column):
        """
        Set (turn on) pixel.
        """
        self.buf[row] |= (0x80 >> column)
        self._send_row(row)

    def clear_pixel(self, row, column):
        """
        Clear pixel.
        """
        self.buf[row] &= ~(0x80 >> column)
        self._send_row(row)


def rotate_right(byte):
    """
    Rotate bits right.
    """
    byte &= 0xFF
    bit = byte & 0x01
    byte >>= 1
    if(bit):
        byte |= 0x80
    return byte
