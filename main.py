import time
import subprocess
from typing import Tuple
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ssd1331 as ssd1331
import psutil


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
    return f"CPU Load: {psutil.cpu_percent():.2f}%"


def get_mem_usage() -> str:
    mem = psutil.virtual_memory()
    return f"RAM: {mem.used // (1024*1024)}/{mem.total // (1024*1024)}MB"


def get_disk_usage() -> str:
    disk = psutil.disk_usage('/')
    return f"DISK: {disk.used // (1024*1024*1024)}/{disk.total // (1024*1024*1024)}GB"


def get_cpu_temp() -> str:
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
        cpu_temp = float(temp_file.read()) / 1000
    return f"CPU Temp: {cpu_temp:.1f} C"


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
    time.sleep(5)
