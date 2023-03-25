# Pi-OLED Display

![IMG_0041](https://user-images.githubusercontent.com/218876/227703075-8b00399f-497e-4344-afce-029e1e7bdb54.jpeg)

This repository contains the code and instructions for setting up an OLED display on a Raspberry Pi using Python and a virtual environment. The OLED display is a 0.96 inch, 128x64 pixel SSD1331 display connected via SPI. The display shows system information, including date, time, CPU usage, and temperature.

## Prerequisites

* Raspberry Pi (tested on Raspberry Pi 3)
* SSD1331 OLED display
* Python 3.9 or higher
* SPI interface enabled on Raspberry Pi

## Hardware Setup

Connect the SSD1331 OLED display to the Raspberry Pi via SPI using the following pin connections:

```
OLED -> Raspberry Pi
VCC  -> 3.3V
GND  -> GND
DIN  -> MOSI (GPIO10)
CLK  -> SCLK (GPIO11)
CS   -> CE0 (GPIO8)
DC   -> GPIO24
RST  -> GPIO25
```

## Software Setup

1. Clone this repository:

```bash
git clone https://github.com/johnboiles/pi-oled.git
cd pi-oled
```

2. Create a Python virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Test the OLED display:

```bash
python main.py
```

Your OLED display should show system information. Press `Ctrl+C` to stop the script.

4. Set up a systemd service to run the script at startup:

```bash
sudo bash -c 'cat << EOF > /etc/systemd/system/pi-oled.service
[Unit]
Description=Pi-OLED Display Service
After=multi-user.target

[Service]
User=pi
WorkingDirectory=/home/pi/pi-oled
ExecStart=/home/pi/pi-oled/venv/bin/python /home/pi/pi-oled/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl enable pi-oled.service
sudo systemctl start pi-oled.service
```

Your OLED display should now show system information on startup. To check the service status, run:

```bash
sudo systemctl status pi-oled.service
```

## Troubleshooting

If you encounter any issues, please check the following:

1. Ensure that SPI is enabled on your Raspberry Pi. You can enable it via `raspi-config` or by adding `dtparam=spi=on` to `/boot/config.txt` and rebooting.
2. Verify that the display is correctly wired to the Raspberry Pi.
3. Check the Python script for any errors or configuration issues.
4. Verify that the virtual environment is set up correctly and all dependencies are installed.

## License

This project is released under the MIT License.
