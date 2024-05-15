"""
    Digifiz     v.03
    March 4th, 2021

    Attempting to code the Digifiz dash project cleaner
    Written by GFunkBus76 in 2021

    Opensource and designed from many online projects...
    Copy, paste, run, debug... repeat lol.

    Mainly inspired by ManxGauged and miata-dash on github.
    Redefined and cleaned up a bit.
    Use at your own discretion.

    Happy to help you if I can.

    https://github.com/gfunkbus76

"""

from geopy.geocoders import Nominatim
import serial
import time
import string
import pynmea2
import pygame
from datetime import datetime
# import paho.mqtt.client as mqttClient
from rpm.rpm import RpmGauge
from aux_gauge.AuxGauge import AuxGauge
from constants import *
from variables import *
from draw import *
import random
import time
import os

#   Import pygame, for main graphics functions
#   Date time is for the clock and perhaps MQTT
#   Paho to handle the MQTT subscription from Node-Red

# offset
oFY = 90

# Setup Display
pygame.init()

# Title and Icon
pygame.display.set_icon(programIcon)
pygame.display.set_caption(project_name + digifiz_ver)

# Font Information
odo_font = pygame.font.Font(FONT_PATH, FONT_SMALL)
digital_font = pygame.font.Font(FONT_PATH, FONT_MEDIUM)
font_speedunits = pygame.font.Font(FONT_PATH, FONT_LARGE)

# Setup Game Loop
clock = pygame.time.Clock()

#   Create gauge instances from classes.
boost = AuxGauge(BOOST_XY, 19)
egt = AuxGauge(EGT_XY, 19)
coolant = AuxGauge(COOLANT_XY, 19)
oilpressure = AuxGauge(OILPRESSURE_XY, 19)
rpm = RpmGauge(RPM_XY, 50)


#   Creating the list for the indicator gauges
indicator_images = []
for i in range(10):
    image = pygame.image.load(("./images/indicators/ind" + str(i) + ".png"))
    image = pygame.transform.scale(image, (image.get_size()[0]/2.4, image.get_size()[1]/2.4))
    indicator_images.append(image)


######
#       MQTT Connection Function
######


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else: print("Connection failed")


def on_message(client, userdata, message): print(message.topic + " " + message.payload.decode())


######
#       ENGINE TOPIC MQTT
######

def on_message_rpm(digi, obj, message):
    rpm_mqtt = int((message.payload.decode()))
    rpm.set_frame(rpm_mqtt)


def on_message_coolant(digi, obj, message):
    coolant_mqtt = int((message.payload.decode()))
    coolant.set_frame(coolant_mqtt)


def on_message_egt(digi, obj, message):
    egt_mqtt = int((message.payload.decode()))
    egt.set_frame(egt_mqtt)


def on_message_oilpressure(digi, obj, message):
    oilpressure_mqtt = int((message.payload.decode()))
    oilpressure.set_frame(oilpressure_mqtt)


def on_message_boost(digi, obj, message):
    boost_mqtt = int((message.payload.decode()))
    boost.set_frame(boost_mqtt)


######
#       CABIN TOPIC MQTT
######

def on_message_speed_cv(digi, obj, message):
    global speed_status
    speed_cv_mqtt = int((message.payload.decode()))
    # speed_status = 55
    speed_status = speed_cv_mqtt


def on_message_speed_gps(digi, obj, message):
    global speed_gps_status
    speed_gps_mqtt = int((message.payload.decode()))
    speed_gps_status = speed_gps_mqtt


def on_message_outside_temp(digi, obj, message):
    global outside_temp_status
    outside_temp_mqtt = int((message.payload.decode()))
    outside_temp_status = outside_temp_mqtt


def on_message_fuel(digi, obj, message):
    global fuel_status
    fuel_mqtt = int((message.payload.decode()))
    fuel_status = fuel_mqtt


######
#       INDICATOR TOPIC MQTT
######

def on_message_illumination(digi, obj, message):
    global illumination_state
    illumination_mqtt = int((message.payload.decode()))
    illumination_state = illumination_mqtt


def on_message_foglight(digi, obj, message):
    global foglight_state
    foglight_mqtt = int((message.payload.decode()))
    foglight_state = foglight_mqtt


def on_message_defog(digi, obj, message):
    global defog_state
    defog_mqtt = int((message.payload.decode()))
    defog_state = defog_mqtt


def on_message_highbeam(digi, obj, message):
    global highbeam_state
    highbeam_mqtt = int((message.payload.decode()))
    highbeam_state = highbeam_mqtt


def on_message_leftturn(digi, obj, message):
    global leftturn_state
    leftturn_mqtt = int((message.payload.decode()))
    leftturn_state = leftturn_mqtt


def on_message_rightturn(digi, obj, message):
    global rightturn_state
    rightturn_mqtt = int((message.payload.decode()))
    rightturn_state = rightturn_mqtt


def on_message_brakewarn(digi, obj, message):
    global brakewarn_state
    brakewarn_mqtt = int((message.payload.decode()))
    brakewarn_state = brakewarn_mqtt


def on_message_oillight(digi, obj, message):
    global oillight_state
    oillight_mqtt = int((message.payload.decode()))
    oillight_state = oillight_mqtt


def on_message_alt(digi, obj, message):
    global alt_state
    alt_mqtt = int((message.payload.decode()))
    alt_state = alt_mqtt


def on_message_glow(digi, obj, message):
    global glow_state
    glow_mqtt = int((message.payload.decode()))
    glow_state = glow_mqtt


######
#       Various Functions for Dash
######

def mileage():
    #   Text File or Odometer and Tripometer Information (pulled from ManxGauged project, just reads from text file
    #   Need to incorporate writing to the file after I figure out how to tabulate the mileage based on GPS or CV
    global odo_font
    odometer = 114514
    tripometer = 0
    # odofile = open("./odo.txt", "r")
    # odo_from_file_text_line1 = odofile.readline()
    # response = odo_from_file_text_line1.replace('\n', "")
    # response2 = response.replace('\r', "")
    # response3 = response2.replace("./odo:", "")
    # try:
    #     odometer = int(response3)
    # except:
    #     print("Error: ODO read from file is not an int")
    #     error_reading_odo_from_file = 1
    # odometer_arduino = odometer

    # odo_from_file_text_line2 = odofile.readline()
    # response = odo_from_file_text_line2.replace('\n', "")
    # response2 = response.replace('\r', "")
    # response3 = response2.replace("trip:", "")
    # try:
    #     tripometer = int(response3)
    # except:
    #     print
    #     "Error: Trip read from file is not an int"
    #     error_reading_odo_from_file = 1
    # odofile.close()

    digital_odo = odometer
    odo_text = odo_font.render(str(digital_odo), True, NEON_GREEN)
    text_rect = odo_text.get_rect()
    text_rect.midright = ODO_L_XY
    WIN.blit(odo_text, text_rect)

#####
#       Functions for Drawing onto the screen
#####

def draw_fuel_text():
    #global digital_font
    digital_fuel = fuel_status
    fuel_text = digital_font.render(str(int(digital_fuel)), True, NEON_GREEN)
    text_rect = fuel_text.get_rect()
    text_rect.midright = (1717/scale, 667/scale+oFY)
    WIN.blit(fuel_text, text_rect)


def draw_speedometer_text():
    '''
    Speedometer text and write
    '''
    #global speed_status
    #global font_speedunits
    speedtext = font_speedunits.render(str(speed_status), True, NEON_YELLOW)
    text_rect = speedtext.get_rect()
    text_rect.midright = SPEEDO_XY
    WIN.blit(speedtext, text_rect)

def draw_mfa():
    '''
    Drawing the interior temp only currently - the MFA will eventually evolve.
    '''
    #global outside_temp_status

    WIN.blit(MFA, MFABG_XY)
    #   Draw MFA display
    text = digital_font.render(str(outside_temp_status), True, NEON_GREEN)
    #   Enables the text to be right center aligned
    text_rect = text.get_rect()
    text_rect.midright = MFA_XY
    WIN.blit(text, text_rect)




def draw_indicators():
    '''
    The area where I blit or draw the indicators/idiot lights and turn signals/low fuel etc.
    '''

    if illumination_state == 1:
        WIN.blit(indicator_images[0], (45/2.4, 460/2.4+oFY))
    if foglight_state == 1:
        WIN.blit(indicator_images[1], (185/2.4, 460/2.4+oFY))
    if defog_state == 1:
        WIN.blit(indicator_images[2], (325/2.4, 460/2.4+oFY))
    if highbeam_state == 1:
        WIN.blit(indicator_images[3], (465/2.4, 460/2.4+oFY))
    if leftturn_state == 1:
        WIN.blit(indicator_images[4], (605/2.4, 460/2.4+oFY))
    if rightturn_state == 1:
        WIN.blit(indicator_images[5], (1220/2.4, 460/2.4+oFY))
    if brakewarn_state == 1:
        WIN.blit(indicator_images[6], (1360/2.4, 460/2.4+oFY))
    if oillight_state == 1:
        WIN.blit(indicator_images[7], (1500/2.4, 460/2.4+oFY))
    if alt_state == 1:
        WIN.blit(indicator_images[8], (1640/2.4, 460/2.4+oFY))
    if glow_state == 1:
        WIN.blit(indicator_images[9], (1780/2.4, 460/2.4+oFY))

    #   To highlight the fuel reserve indicator (factory is at 7 litres
    if fuel_status <= 7:
        WIN.blit(fuelresOn, (1795/2.4, 616/2.4+oFY))
    else:
        WIN.blit(fuelresOff, (1795/2.4, 616/2.4+oFY))

#   Main Drawings for the program - Background + Gauges
def draw_digifiz():
    WIN.blit(BACKGROUND, (0, 0+oFY))
    rpm.show(WIN)
    coolant.show(WIN)
    boost.show(WIN)
    oilpressure.show(WIN)
    egt.show(WIN)
    mileage()
    draw_indicators()
    draw_clock()
    draw_mfa()
    draw_fuel_text()
    draw_speedometer_text()

#####
#       Main Function for the Pygame Program
#####

def main():
    #   MQTT Variables
    # broker_address = "localhost"  # Broker address
    # port = 1880  # Broker port
    # client = mqttClient.Client("pytest")  # create new instance
    # client.on_connect = on_connect  # attach function to callback
    # client.on_message = on_message  # attach function to callback
    # client.connect(broker_address, port=port)  # connect to broker
    # client.loop_start()  # start the loop
    i=0

    # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    #   The main loop, clock setting and click x for quit etc.
    run = True
    while run:
        clock.tick(FPS/3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        if keys[pygame.K_UP]:
            i=(i+1)%51
        if keys[pygame.K_DOWN]:
            i=0 if i-1<0 else i-1
        rpm.set_frame(i)
        boost.set_frame(i%20)
        oilpressure.set_frame(i%20)
        egt.set_frame(i%20)
        coolant.set_frame(i%20)
        global speed_status
        speed_status=i*3
        global fuel_status
        fuel_status=i
        draw_digifiz()
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
