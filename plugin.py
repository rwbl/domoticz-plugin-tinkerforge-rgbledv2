# Domoticz Home Automation - Plugin Tinkerforge RGB LED Bricklet 2.0
# @author Robert W.B. Linn
# @version 1.0.0 (Build 20200206)
#
# NOTE: after every change run
# sudo chmod +x *.*                      
# sudo systemctl restart domoticz.service OR sudo service domoticz.sh restart
#
# Domoticz Python Plugin Development Documentation:
# https://www.domoticz.com/wiki/Developing_a_Python_plugin
# Tinkerforge RGB LED Bricklet 2.0 Documentation:
# Hardware:
# https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED_V2.html#rgb-led-v2-bricklet
# API Python Documentation:
# https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDV2_Bricklet_Python.html#rgb-led-v2-bricklet-python-api

"""
<plugin key="TFRGBLEDV2" name="Tinkerforge RGB LED Bricklet 2.0" author="rwbL" version="1.0.0">
    <description>
        <h2>Tinkerforge RGB LED Bricklet 2.0</h2><br/>
        This bricklet enables to control an RGB LED. Each of the three channels (Red, Green, Blue) can be set.<br/>
        For each of the channels, a Domoticz device is created from Type: Light/Switch, SubType: Switch, Switch Type: Dimmer.<br/>
        The Domoticz device slider for a color, has a range 0-100% which is mapped to a color value 0-255 used by the bricklet.<br/>
        The status light of the bricklet is turned off during start of the plugin.<br/>
        <br/>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>Address: IP address of the host connected to. Default: 127.0.0.1 (for USB connection)</li>
            <li>Port: Port used by the host. Default: 4223</li>
            <li>UID: Unique identifier of RGB LED Bricklet 2.0. Obtain the UID via the Brick Viewer. Default: Jng</li>
        </ul>
        <h3>Notes</h3>
        <ul style="list-style-type:square">
            <li>If the Master Brick has been disconnected from the Raspberry Pi (i.e. plugged out) and connected again, the hardware must be updated (using Setup > Hardware > select the plugin > Update) or restart Domoticz.</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="Host" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="75px" required="true" default="4223"/>
        <param field="Mode1" label="UID" width="200px" required="true" default="Jng"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug" default="true"/>
                <option label="False" value="Normal"/>
            </options>
        </param>
    </params>
</plugin>
""" 

## Imports
import Domoticz
import urllib
import urllib.request

# Amend the import path to enable using the Tinkerforge libraries
# Alternate (ensure to update in case newer Python API bindings):
# create folder tinkerforge and copy the binding content, i.e.
# /home/pi/domoticz/plugins/TFRGBLEDV2
from os import path
import sys
sys.path
sys.path.append('/usr/local/lib/python3.7/dist-packages')

import tinkerforge
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rgb_led_v2 import BrickletRGBLEDV2

# Number of channels = must match number of index defined below
CHANNELS = 3
UNITCHANNELR = 1
UNITCHANNELG = 2
UNITCHANNELB = 3
# Device Status Level & Text
STATUSLEVELOK = 1
STATUSLEVELERROR = 5
STATUSTEXTOK = "OK"
STATUSTEXTERROR = "ERROR"

class BasePlugin:

    def __init__(self):
        self.Debug = False
        
        # RGB Device Colors with initial values
        self.r = 9
        self.g = 8
        self.b = 58

        # NOT USED = PLACEHOLDER
        # The Domoticz heartbeat is set to every 10 seconds. Do not use a higher value than 30 as Domoticz message "Error: hardware (N) thread seems to have ended unexpectedly"
        # The plugin heartbeat is set in Parameter.Mode5 (seconds). This is determined by using a hearbeatcounter which is triggered by:
        # (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameter.Mode5) = 0
        # Example: trigger action every 60s = (6 * 10) mod 60 = 0
        """
        self.HeartbeatInterval = 10
        self.HeartbeatCounter = 0
        """

    def onStart(self):
        Domoticz.Debug("onStart called")
        Domoticz.Debug("Debug Mode:" + Parameters["Mode6"])
        if Parameters["Mode6"] == "Debug":
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()

        # Get the UID of the bricklet
        if len(Parameters["Mode1"]) == 0:
            StatusToLog(STATUSLEVELERROR, "[ERROR] Device UID not set. Get the UID using the Brick Viewer.")
            return

        # Create new devices for the Hardware = each channel is a dimmer switch; set the initial color
        if (len(Devices) == 0):
            Domoticz.Debug("Creating new Devices")
            # Parameter Type 244=Light/Switch, Subtype 73=Switch, Switchtype 7=Dimmer

            Domoticz.Device(Name="Switch Red", Unit=UNITCHANNELR, Type=244, Subtype=73, Switchtype=7, Used=1).Create()
            Devices[UNITCHANNELR].Update(nValue=1,sValue=str(self.r))
            Domoticz.Debug("Device created: "+Devices[UNITCHANNELR].Name)

            Domoticz.Device(Name="Switch Green", Unit=UNITCHANNELG, Type=244, Subtype=73, Switchtype=7, Used=1).Create()
            Devices[UNITCHANNELG].Update(nValue=1,sValue=str(self.g))
            Domoticz.Debug("Device created: "+Devices[UNITCHANNELG].Name)

            Domoticz.Device(Name="Switch Blue", Unit=UNITCHANNELB, Type=244, Subtype=73, Switchtype=7, Used=1).Create()
            Devices[UNITCHANNELB].Update(nValue=1,sValue=str(self.b))
            Domoticz.Debug("Device created: "+Devices[UNITCHANNELB].Name)

        # Set the bricklet configuration
        SetBrickletConfiguration(self)
        # Set the color at start - either with inital value or from the current dimmer switches set
        SetBrickletRGB(self, int(Devices[UNITCHANNELR].sValue), int(Devices[UNITCHANNELG].sValue), int(Devices[UNITCHANNELB].sValue) )
        
    def onStop(self):
        Domoticz.Debug("Plugin is stopping.")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + "', Hue: " + str(Hue))
        # Change the color of the RGB LED bricklet
        SetBrickletColor(self, Unit, Command, Level)

    def onDeviceModified(self, Unit):
        Domoticz.Debug("onDeviceModified called: Unit " + str(Unit))
        # Domoticz.Debug("nValue="+str(Devices[Unit].nValue) + ",sValue="+Devices[Unit].sValue + ", Color RGB="+Devices[Unit].Color)

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        """
        # NOT USED = PLACEHOLDER
        self.HeartbeatCounter = self.HeartbeatCounter + 1
        Domoticz.Debug("onHeartbeat called. Counter=" + str(self.HeartbeatCounter * self.HeartbeatInterval) + " (Heartbeat=" + Parameters["Mode5"] + ")")
        # check the heartbeatcounter against the heartbeatinterval
        if (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameters["Mode5"]) == 0:
            try:
                #Action
                return
            except:
                #Domoticz.Error("[ERROR] ...")
                return
        """

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onDeviceModified(Unit):
    global _plugin
    _plugin.onDeviceModified(Unit)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Tinkerforge Bricklet

# Set the bricklet configuration
# Status LED = OFF
def SetBrickletConfiguration(self):
    Domoticz.Debug("SetBrickletConfiguration")
    try:
        # Create IP connection
        ipConn = IPConnection()
        # Create device object
        rgbDev = BrickletRGBLEDV2(Parameters["Mode1"], ipConn)
        # Connect to brickd using Host and Port
        ipConn.connect(Parameters["Address"], int(Parameters["Port"]))
        # Update the configuration
        rgbDev.set_status_led_config(rgbDev.STATUS_LED_CONFIG_OFF )
        Domoticz.Debug("Set Status LED OFF" )
        # Disconnect
        ipConn.disconnect()
        Domoticz.Debug("SetBrickletConfiguration OK")
    except:
        Domoticz.Error("[ERROR] SetBrickletConfiguration failed. Check bricklet.")
    return

# Set the color of the RGB LED bricklet
# The self parameter is used to ensure all 3 RGB colors are captured and used to set the color
# The Level is given via the Domoticz Switch Type Dimmer in a range 0-100%. The RGB LED has a range 0-255. 
# The level is adjusted accordingly.
def SetBrickletColor(self, Unit, Command, Level):
    Domoticz.Debug("SetBrickletColor: Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + ", ID="+str(Devices[Unit].ID) )
    SetCommand = str(Command)
    try:
        # Create IP connection
        ipConn = IPConnection()
        # Create device object
        rgbDev = BrickletRGBLEDV2(Parameters["Mode1"], ipConn)
        # Connect to brickd using Host and Port
        ipConn.connect(Parameters["Address"], int(Parameters["Port"]))
        # Assign the color and update the domoticz dimmerswitches
        state = 1
        if SetCommand == "Off":
            state = 0
            Level = 0
        if Unit == UNITCHANNELR:
            self.r = Level
            Devices[UNITCHANNELR].Update(nValue=state,sValue=str(self.r))
        if Unit == UNITCHANNELG:
            self.g = Level
            Devices[UNITCHANNELG].Update(nValue=state,sValue=str(self.g))
        if Unit == UNITCHANNELB:
            self.b = Level
            Devices[UNITCHANNELB].Update(nValue=state,sValue=str(self.b))
        # Update the tinkerforge rgbled device with mapped values
        rm = MapRange(self.r,0,100,0,255)
        gm = MapRange(self.g,0,100,0,255)
        bm = MapRange(self.b,0,100,0,255)
        rgbDev.set_rgb_value(rm,gm,bm)
        Domoticz.Debug("Bricklet Update: R=%d,G=%d,B=%d" % (rm,gm,bm))
        # Disconnect
        ipConn.disconnect()
        Domoticz.Debug("SetBrickletColor: OK")
    except:
        Domoticz.Error("[ERROR] SetBrickletColor failed. Check bricklet.")
    return

# Set the color of the RGB LED bricklet
# The self parameter is used to ensure all 3 RGB colors are captured and used to set the color.
# The color level is given via the Domoticz Switch Type Dimmer in a range 0-100%. The RGB LED has a range 0-255. 
def SetBrickletRGB(self, r, g, b):
    Domoticz.Debug("SetBrickletRGB: R=%d,G=%d,B=%d" % (r,g,b))
    try:
        # Create IP connection
        ipConn = IPConnection()
        # Create device object
        rgbDev = BrickletRGBLEDV2(Parameters["Mode1"], ipConn)
        # Connect to brickd using Host and Port
        ipConn.connect(Parameters["Address"], int(Parameters["Port"]))
        # Assign the color and update the domoticz dimmer switches
        state = 1
        self.r = r
        Devices[UNITCHANNELR].Update(nValue=state,sValue=str(self.r))
        self.g = g
        Devices[UNITCHANNELG].Update(nValue=state,sValue=str(self.g))
        self.b = b
        Devices[UNITCHANNELB].Update(nValue=state,sValue=str(self.b))
        # Update the tinkerforge rgbled device with mapped values
        rm = MapRange(self.r,0,100,0,255)
        gm = MapRange(self.g,0,100,0,255)
        bm = MapRange(self.b,0,100,0,255)
        Domoticz.Debug("Bricklet Update: R=%d,G=%d,B=%d" % (rm,gm,bm))
        rgbDev.set_rgb_value(rm,gm,bm)
        # Disconnect
        ipConn.disconnect()
        Domoticz.Debug("SetBrickletRGB: OK")
    except:
        Domoticz.Error("[ERROR] SetBrickletRGB failed. Check bricklet.")
    return

# Generic helper functions

# Dump the plugin parameter & device information to the domoticz debug log
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

# Log a status message, either to the domoticz log or error
# Alert Level: 1=OK, 4=ERROR
def StatusToLog(level,text):
    if level == STATUSLEVELOK:
        Domoticz.Log(text)
    if level == STATUSLEVELERROR:
        Domoticz.Error(text)
    return

# Map a range from to.
# Example mapping 0-100% to 0-255: MapRange(255,0,100,0,255) gives 255.
def MapRange(x,a,b,c,d):
    try:
        y=(x-a)/(b-a)*(d-c)+c
    except:
        y=-1
    return round(y)
   
