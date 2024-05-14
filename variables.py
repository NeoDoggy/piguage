

'''                        Dash Variables                        '''

#   Gauge State Variables --> fed from local MQTT Server
rpm_status = 1
coolant_status = 1
egt_status = 1
oilpressure_status = 1
boost_status = 1
fuel_status = 1
outside_temp_status = 666
speed_status = 1

#   MQTT Variables
broker_address = "localhost"  # Broker address
port = 1883  # Broker port


'''GPIO State Variables'''
#
# 0 is off, 1 is active -- Fed from the MQTT Server
illumination_state = 1
foglight_state = 1
highbeam_state = 1
defog_state = 1
leftturn_state = 1
rightturn_state = 1
brakewarn_state = 1
oillight_state = 1
alt_state = 1
glow_state = 1
fuelres_state = 1

# For the TestingStatus gauge change feature with the up/down arrows
gauge_change = 1
