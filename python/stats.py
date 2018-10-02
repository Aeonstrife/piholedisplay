import epd2in13
import time
import Image
import ImageDraw
import ImageFont
import json
import subprocess
import time
import requests

api_url = 'http://pi.hole/admin/api.php'
bg_color = 0
fill_color = 255

epd = epd2in13.EPD()
epd.init(epd.lut_partial_update)

# For simplicity, the arguments are explicit numerical coordinates
image = Image.new('1', (epd2in13.EPD_WIDTH, epd2in13.EPD_HEIGHT), 255)  # 255: clear the frame
draw = ImageDraw.Draw(image)

width = epd2in13.EPD_WIDTH
height = epd2in13.EPD_HEIGHT

draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = -2
top = padding
bottom = height - padding

x = 0

epd.set_frame_memory(image, 0, 0)
epd.display_frame()
epd.set_frame_memory(image, 0, 0)
epd.display_frame()

while True:
	cmd = "hostname -I | cut -d\' \' -f1"
	IP = subprocess.check_output(cmd, shell=True)
	cmd = "hostname"
	HOST = subprocess.check_output(cmd, shell=True)
	cmd = "top -bn1 | grep load | awk " \
	"'{printf \"CPU Load: %.2f\", $(NF-2)}'"
	CPU = subprocess.check_output(cmd, shell=True)
	cmd = "free -m | awk 'NR==2{printf " \
	"\"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
	MemUsage = subprocess.check_output(cmd, shell=True)
	cmd = "df -h | awk '$NF==\"/\"{printf " \
	"\"Disk: %d/%dGB %s\", $3,$2,$5}'"
	Disk = subprocess.check_output(cmd, shell=True)
	
	try:
		r = requests.get(api_url)
		data = json.loads(r.text)
		DNSQUERIES = data['dns_queries_today']
		ADSBLOCKED = data['ads_blocked_today']
		CLIENTS = data['unique_clients']
	except KeyError:
		time.sleep(1)
		continue

	time_image = Image.new('1', (height, width), bg_color)  # 255: clear the frame
	draw = ImageDraw.Draw(time_image)
	font = ImageFont.truetype("/home/pi/slkscr.ttf", 15)
	
	draw.text((x, top), "HOST: " + HOST, font=font, fill=fill_color)
	draw.text((x, top + 15), "IP: " + str(IP), font=font, fill=fill_color)
	draw.text((x, top + 30),     str(CPU), font=font, fill=fill_color)
	draw.text((x, top + 45),    str(MemUsage),  font=font, fill=fill_color)
	draw.text((x, top + 60),    str(Disk),  font=font, fill=fill_color)
	draw.text((x, top + 75), "Ads Blocked: " + str(ADSBLOCKED), font=font, fill=fill_color)
	draw.text((x, top + 90), "Clients:     " + str(CLIENTS), font=font, fill=fill_color)
	draw.text((x, top + 105), "DNS Queries: " + str(DNSQUERIES), font=font, fill=fill_color)
	
	epd.set_frame_memory(time_image.transpose(Image.ROTATE_90), 0, 0)
	epd.display_frame()
	epd.set_frame_memory(time_image.transpose(Image.ROTATE_90), 0, 0)
	epd.display_frame()
	time.sleep(1)