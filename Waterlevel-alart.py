from influxdb_client import InfluxDBClient
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
import sys

#initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

WIDTH = 128
HEIGHT = 64

oled1 = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)
oled2 = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3d)

# --- influxdb server settings ---
url = "<YOUR_INFLUXDB_URL>"
token = "<YOUR_INFLUXDB_TOKEN>"
org = "<YOUR_INFLUXDB_ORG>"

def get_waterlevel_data():

    # client initialization
    client = InfluxDBClient(url=url, token=token, org=org)

    # create query last 30m data
    waterlevel_query = 'from(bucket: "<WATERLEVEL_BUCKET>") |> range(start: -20m)  |> filter(fn: (r) => r["_measurement"] == "<YOUR_MEASUREMENT>")|> filter(fn: (r) => r["_field"] == "water_level")'
    wether_query = 'from(bucket: "<WEATHER_BUCKET>") |> range(start: -20m)  |> filter(fn: (r) => r["_measurement"] == "<YOUR_MEASUREMENT>")|> filter(fn: (r) => r["_field"] == "temperature")'


    # execute the query and get the results
    query_api = client.query_api()
    get_waterlevel_data = query_api.query(waterlevel_query)
    get_temperature_data = query_api.query(wether_query)

    latest_waterlevel = []
    for table in get_waterlevel_data:
        for record in table.records:
            latest_waterlevel.append((record.get_field(), record.get_value()))

    latest_temperature = []
    for table in get_temperature_data:
        for record in table.records:
            latest_temperature.append((record.get_field(), record.get_value()))

    client.close()
    return latest_waterlevel[0][1], latest_temperature[0][1]

def display_oled(waterlevel, temperature):

    #flush display area
    oled1.fill(0)
    oled2.fill(0)
    oled1.show()
    oled2.show()

    #load fonts with specified font size
    #font DejaVuSans is standard font in Raspberry Pi OS

    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    #load font

    try:
        font_small = ImageFont.truetype(FONT_PATH, 17) #title font size
        font_large = ImageFont.truetype(FONT_PATH, 48) #value font size
    except IOError:
        font_small = ImageFont.load_default()
        font_large = ImageFont.load_default()

    #functino to create image for display

    def create_display_image(line1_text, line2_text):
        
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)

        #line 1 (title) position calculation
        bbox1 = draw.textbbox((0, 0), line1_text, font=font_small)
        w1 = bbox1[2] - bbox1[0]
        x1 = 1
        y1 = 2

        #line 2 (value) position calculation
        bbox2 = draw.textbbox((0, 0), line2_text, font=font_large)
        w2 = bbox2[2] - bbox2[0]
        x2 = 1
        y2 = 18

        # Draw the text on the display(image)
        draw.text((x1, y1), line1_text, font=font_small, fill=255)
        draw.text((x2, y2), line2_text, font=font_large, fill=255)

        return image

    disp1_text1 = "Waterlevel"
    disp1_text2 = str(waterlevel)
    disp2_text1 = "Temperature"
    disp2_text2 = str(temperature)

    #create image for OLED1 (0x3c) and display
    img1 = create_display_image(disp1_text1, disp1_text2)
    oled1.image(img1)
    oled1.show()

    #create image for OLED2 (0x3d) and display
    img2 = create_display_image(disp2_text1, disp2_text2)
    oled2.image(img2)
    oled2.show()

#main routine

latest_data = get_waterlevel_data()
display_oled(latest_data[0], latest_data[1])

if latest_data[0] > 3.0:
    subprocess.call("aplay -D hw:0,0 01-ETWS.wav", shell=True)
    sys.exit()

if latest_data[0] > 2.9:
    subprocess.call("aplay -D hw:0,0 02-J-Alart.wav", shell=True)
    sys.exit()

if latest_data[0] > 2.8:
    subprocess.call("aplay -D hw:0,0 03-Tsunami.wav", shell=True)
