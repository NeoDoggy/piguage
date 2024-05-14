# Constants for the Digifiz Dash
import pygame


#   Currently enables RPM to rise and fall with keyboard up and down presses.
#   Will potentially change this in future to have full gauge functionality.
#   testingStatus = False

testingStatus = True
oFY = 100
scale=2.4

#   Screen Size
WIDTH, HEIGHT = 800, 480  # use your screens display information
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)# pygame.FULLSCREEN
WIN.fill((26,28,26))
FPS = 60

# Title and Icon
ICON = "./images/speedometer.png"
BG = "./images/background.png"
programIcon = pygame.image.load(ICON)
project_name = "piguage - "
digifiz_ver = "v. 0.1"

#   Colours
NEON_YELLOW = (236, 253, 147)   #   Speedo Colour
NEON_GREEN = (145, 213, 89)     #   Lower gauge colours, clock, odo etc
DARK_GREY = (9, 52, 50)         #   background of the digits (for the 7segment appearance)

#   Font Details
FONT_PATH = "./fonts/DSEG7Classic-Bold.ttf"
FONT_LARGE = int(174/scale)    #   Speedo size
FONT_MEDIUM = int(94/scale)    #   Clock, MFA, Fuel size
FONT_SMALL = int(67/scale)     #   Odo Size


#   Locations for gauge graphics, each has the same start XY but builds upon it, check images folder
RPM_XY = (135/scale, 5/scale+oFY)
COOLANT_XY = (1481/scale, 105/scale+oFY)
EGT_XY = (1599/scale, 105/scale+oFY)
OILPRESSURE_XY = (1711/scale, 105/scale+oFY)
BOOST_XY = (1822/scale, 105/scale+oFY)
CLOCK_XY = (555/scale, 620/scale+1+oFY)
FUEL_XY = (1560/scale, 620/scale+oFY)
ODO_XY = (60/scale, 644/scale+oFY)
ODO_L_XY = (395/scale, 678/scale+oFY)
MFA_XY = (1435/scale, 668/scale+oFY)
MFABG_XY = (1021/scale, 563/scale+oFY)
SPEEDO_XY = (1247/scale, 305/scale+oFY)



'''                         LOAD IMAGES                         '''

BACKGROUND = pygame.image.load(BG).convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (BACKGROUND.get_size()[0]/scale, BACKGROUND.get_size()[1]/scale))
MFA = pygame.image.load("./images/indicators/MFA_temp.png").convert_alpha()
MFA = pygame.transform.scale(MFA,(MFA.get_size()[0]/scale,MFA.get_size()[1]/scale))
fuelresOn = pygame.image.load("./images/indicators/fuelResOn.png").convert_alpha()
fuelresOn = pygame.transform.scale(fuelresOn,(fuelresOn.get_size()[0]/scale,fuelresOn.get_size()[1]/scale))
fuelresOff = pygame.image.load("./images/indicators/fuelResOff.png").convert_alpha()
fuelresOff = pygame.transform.scale(fuelresOff,(fuelresOff.get_size()[0]/scale,fuelresOff.get_size()[1]/scale))
