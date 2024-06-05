from geopy.geocoders import Nominatim
import serial
import pygame
from datetime import datetime
from rpm.rpm import RpmGauge
from aux_gauge.AuxGauge import AuxGauge
from constants import *
from variables import *
from draw import *
import obd
from micropyGPS import MicropyGPS

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
    i=0
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    my_gps = MicropyGPS()
    conn=obd.OBD() #connect to BT or TTL
    run = True
    while run:
        clock.tick(FPS/3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_ESCAPE]:
        #     pygame.quit()
        # if keys[pygame.K_UP]:
        #     i=(i+1)%51
        # if keys[pygame.K_DOWN]:
        #     i=0 if i-1<0 else i-1
        nmea=ser.readline().decode().strip()
        if(nmea.startswith("$GPVTG")):
            speed=nmea.split(',')[7]
            global speed_status
            speed_status=int(speed)
        cmd=obd.commands.RPM
        res=conn.query(cmd)
        rpm.set_frame(max(50,int(res.value)))
        # boost.set_frame(i%20)
        # oilpressure.set_frame(i%20)
        # egt.set_frame(i%20)
        # coolant.set_frame(i%20)
        # global fuel_status
        # fuel_status=i
        draw_digifiz()
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
