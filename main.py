import time
import subprocess
from typing import Tuple
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ssd1331 as ssd1331


import builtins
import inspect
import sys

original_print = builtins.print

# Define a custom print function
def custom_print(*args, **kwargs):
    # Get the caller's frame
    frame = inspect.currentframe().f_back

    # Get the source file name and line number of the print call
    source_file = frame.f_code.co_filename
    line_number = frame.f_lineno

    # Add the source file and line number to the output
    prefix = f"[{source_file}:{line_number}]"
    original_print(prefix, *args, **kwargs)

# Override the built-in print function
builtins.print = custom_print


def init_display() -> Tuple[int, int, ssd1331.SSD1331]:
    cs_pin = digitalio.DigitalInOut(board.D5)
    dc_pin = digitalio.DigitalInOut(board.D6)
    reset_pin = digitalio.DigitalInOut(board.D9)
    BAUDRATE = 24000000
    spi = board.SPI()
    disp = ssd1331.SSD1331(spi, rotation=0, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)

    if disp.rotation % 180 == 90:
        height = disp.width
        width = disp.height
    else:
        width = disp.width
        height = disp.height

    return width, height, disp


def get_ip() -> str:
    cmd = "hostname -I | cut -d' ' -f1"
    return f"IP: {subprocess.check_output(cmd, shell=True).decode('utf-8').strip()}"


def get_cpu_load() -> str:
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    return f"CPU Load: {subprocess.check_output(cmd, shell=True).decode('utf-8').strip()}"


def get_mem_usage() -> str:
    cmd = "free -m | awk 'NR==2{printf \"%s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    return f"Mem: {subprocess.check_output(cmd, shell=True).decode('utf-8').strip()}"


def get_disk_usage() -> str:
    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%d GB  %s\", $3,$2,$5}'"
    return f"Disk: {subprocess.check_output(cmd, shell=True).decode('utf-8').strip()}"


def get_cpu_temp() -> str:
    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"%.1f C\", $(NF-0) / 1000}'"
    return f"CPU Temp: {subprocess.check_output(cmd, shell=True).decode('utf-8').strip()}"


width, height, disp = init_display()
image = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(image)
padding = -2
x = 0
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)

while True:
    system_info = [
        get_ip(),
        get_cpu_load(),
        get_mem_usage(),
        get_disk_usage(),
        get_cpu_temp(),
    ]

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    y = padding
    for info in system_info:
        draw.text((x, y), info, font=font)
        bbox = font.getbbox(info)  # Get the bounding box
        y += bbox[3] + 2

    disp.image(image)
    time.sleep(1)
