# domoticz-plugin-tinkerforge-rgbledv2
[Domoticz](https://www.domoticz.com/) plugin to interact with the [Tinkerforge RGB LED Bricklet 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED_V2.html#rgb-led-v2-bricklet).

# Objectives
* To set the color for each of the 3 RGB (Red, Green, Blue) channels of the Tinkerforge RGB LED Bricklet 2.0.
* To control the RGB LED bricklet via various Domoticz devices and dzVents Lua automation events
* To learn how to write generic Python plugin(s) for the Domoticz Home Automation system communicating with [Tinkerforge](http://www.tinkerforge.com) Building Blocks. This plugin espcially focus on defining own functions..

_Abbreviations_: TF=Tinkerforge, Bricklet=Tinkerforge RGB LED Bricklet 2.0, GUI=Domoticz Web UI.

## Solution
A Domoticz Python plugin named "Tinkerforge RGB LED Bricklet 2.0" with the three color channels RGB, which can be set individually.
For each of the three channels, a Domoticz device is created from Type: Light/Switch, SubType: Switch, Switch Type: Dimmer.
In the GUI, the dimmer widget uses a slider per color, which has a range 0-100% which is mapped to a color value 0-255 used by the bricklet.
The status light of the bricklet is turned off during start of the plugin.
The bricklet is connected to a Tinkerforge Master Brick which is direct connected via USB with the Domoticz Home Automation system.
The Domoticz Home Automation system is running on a Raspberry Pi 3B+.

### Logic
The only function of the plugin is to set the color of the bricklet.
This is triggered by receiving a command resulting in actions: IP connection > Create device object > perform function to set the color > IP disconnect.
The Domoticz heartbeat (default every 10s) is not used.

Any additional logic to be defined in Domoticz. Either by additional devices or scripts. Examples
* Selector switch to set a selectd color, i.e red, yellow or green
* Color switch to set the color picked from a color wheel
More see section "dzVents Lua Automation Script Examples".

### Plugin Concept Setting Color
The plugin uses the function _onCommand_ to set the color of a color channel of the bricklet.
This is handled by function _SetBrickletColor(self, Unit, Command, Level)_.
* The unit is the selected R,G or B color device from Domoticz (Integer).
* The command is the switch function to perform, i.e. "Set Level", "Off", "On" (String). 
* The level is the color level to set (Integer).
The Domoticz device is updated depending the unit (i.e. selected color) by settig nValue to 0 (=Off) or 1 (=On) and sValue to the level (0-255 as string!).
The bricklet device object is set by executing the API function set_rgb_value with the color parameter r,g,b - which are set prior this function.

Additional info **domoticz-plugin-tinkerforge-rgbledv2.pdf**.

## Hardware Parts
* Raspberry Pi 3B+ [(Info)](https://www.raspberrypi.org)
* Tinkerforge Master Brick 2.1 FW 2.4.10 [(Info)](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html#master-brick)
* Tinkerforge RGB LED Bricklet 2.0 FW 2.0.1 [(Info)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED_V2.html#)

## Software
* Raspberry Pi Raspian Debian Linux Buster 4.19.93-v7+ #1290
* Domoticz Home Automation System V4.11717 (beta) 
* Tinkerforge Brick Daemon 2.4.1, Brick Viewer 2.4.11
* Tinkerforge Python API-Binding 2.1.24 [(Info)](https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDV2_Bricklet_Python.html#rgb-led-v2-bricklet-python-api)
* Python 3.7.3, GCC 8.2.0
* The versions for developing this plugin are subject to change.

## Quick Steps
For implementing the Plugin on the Domoticz Server running on the Raspberry Pi.
See also Python Plugin Code (well documented) **plugin.py**.

## Test Setup
For testing this plugin, the test setup has a Master Brick with RGB LED Bricklet 2.0 connected to port D.

On the Raspberry Pi, it is mandatory to install the Tinkerforge Brick Daemon and Brick Viewer following [these](https://www.tinkerforge.com/en/doc/Embedded/Raspberry_Pi.html) installation instructions (for Raspian armhf).

Build the test setup by connecting the Tinkerforge Building Blocks and the LED & Push-button to the IO-4 pins (channels):
* RGB LED Bricklet 2.0 > Master Brick using bricklet cable 7p-10p (because using a Master Brick with 10p connectors and the RGB LED Bricklet 2.0 has the newer 7p connector).
* Master Brick > USB cable to Raspberry Pi

Start the Brick Viewer and action:
* Update the devices firmware
* Obtain the UID of the RGB LED Bricklet 2.0 as required by the plugin (i.e. Jng).

## Domoticz Web GUI
Open windows GUI Setup > Hardware, GUI Setup > Log, GUI Setup > Devices
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.
It is imporant, that the GUI > Setup > Hardware accepts new devices!

## Create folder
The folder name is the same as the key property of the plugin (i.e. plugin key="TFRGBLEDV2").
```
cd /home/pi/domoticz/plugins/TFRGBLEDV2
```

## Create the plugin
The plugin has a mandatory filename **plugin.py** located in the created plugin folder.
Domoticz Python Plugin Source Code: see file **plugin.py**.

## Install the Tinkerforge Python API
There are two options.

### 1) sudo pip3 install tinkerforge
Advantage: in case of binding updates, only a single folder must be updated.
Check if a subfolder tinkerforge is created in folder /usr/lib/python3/dist-packages.
**Note**
Check the version of "python3" in the folder path. This could also be python 3.7 or other = see below.

**If for some reason the bindings are not installed**
Unzip the Tinkerforge Python Binding into the folder /usr/lib/python3/dist-packages.
_Example_
Create subfolder Tinkerforge holding the Tinkerforge Python Library
```
cd /home/pi/tinkerforge
```
Unpack the latest python bindings into folder /home/pi/tinkerforge
Copy /home/pi/tinkerforge to the Python3 dist-packges
```
sudo cp -r /home/pi/tinkerforge /usr/lib/python3/dist-packages/
```

In the Python Plugin code amend the import path to enable using the Tinkerforge libraries
```
from os import path
import sys
sys.path
sys.path.append('/usr/local/lib/python3.7/dist-packages')
```

### 2) Install the Tinkerforge Python Bindings in a subfolder of the plugin and copy the binding content.
Disadvantage: Every Python plugin using the Tinkerforge bindings must have a subfolder tinkerforge.
In case of binding updates,each of the tinkerforge plugin folders must be updated.
/home/pi/domoticz/plugins/soilmoisturemonitor/tinkerforge

There is no need to amend the path as for option 1.

For either ways, the bindings are used like:
```
import tinkerforge
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rgb_led_v2 import BrickletRGBLEDV2
```
**Note**
Add more bindings depending Tinkerforge bricks & bricklets used.

Ensure to update the files in case of newer Tinkerforge Python Bindings.

## Make plugin.py executable
```
cd /home/pi/domoticz/plugins/TFRGBLEDV2
chmod +x plugin.py
```

## Restart Domoticz
Restart Domoticz to find the plugin:
```
sudo systemctl restart domoticz.service
```

**Note**
When making changes to the Python plugin code, ensure to restart Domoticz and refresh any of the Domoticz Web GUI's.

## Domoticz Add Hardware Tinkerforge IO-4 Bricklet 2.0
**IMPORTANT**
Prior adding, set GUI Stup > Settings > Hardware the option to allow new hardware.
If this option is not enabled, no new devices are created assigned to this hardware.
Check in the Domoticz log as error message Python script at the line where the new device is used
(i.e. Domoticz.Debug("Device created: "+Devices[1].Name))

In the GUI Setup > Hardware add the new hardware "Tinkerforge IO-4 Bricklet 2.0".

## Add Hardware - Check the Domoticz Log
After adding,ensure to check the Domoticz Log (GUI Setup > Log)

## Example Domoticz Log Entry Adding Hardware with Debug=True
```
2020-02-05 19:01:38.581 (RGBLED) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL 
2020-02-05 19:01:38.581 (RGBLED) 'HardwareID':'7' 
2020-02-05 19:01:38.581 (RGBLED) 'HomeFolder':'/home/pi/domoticz/plugins/TFRGBLEDV2/' 
2020-02-05 19:01:38.581 (RGBLED) 'StartupFolder':'/home/pi/domoticz/' 
2020-02-05 19:01:38.581 (RGBLED) 'UserDataFolder':'/home/pi/domoticz/' 
2020-02-05 19:01:38.581 (RGBLED) 'Database':'/home/pi/domoticz/domoticz.db' 
2020-02-05 19:01:38.581 (RGBLED) 'Language':'en' 
2020-02-05 19:01:38.581 (RGBLED) 'Version':'0.1.0' 
2020-02-05 19:01:38.581 (RGBLED) 'Author':'rwbL' 
2020-02-05 19:01:38.581 (RGBLED) 'Name':'RGBLED' 
2020-02-05 19:01:38.581 (RGBLED) 'Address':'127.0.0.1' 
2020-02-05 19:01:38.581 (RGBLED) 'Port':'4223' 
2020-02-05 19:01:38.581 (RGBLED) 'Key':'TFRGBLEDV2' 
2020-02-05 19:01:38.581 (RGBLED) 'Mode1':'Jng' 
2020-02-05 19:01:38.581 (RGBLED) 'Mode6':'Debug' 
2020-02-05 19:01:38.581 (RGBLED) 'DomoticzVersion':'4.11670' 
2020-02-05 19:01:38.581 (RGBLED) 'DomoticzHash':'f6af0fa0c' 
2020-02-05 19:01:38.581 (RGBLED) 'DomoticzBuildTime':'2020-02-02 12:21:53' 
2020-02-05 19:01:38.581 (RGBLED) Device count: 0 
2020-02-05 19:01:38.581 (RGBLED) Creating new Devices 
2020-02-05 19:01:38.582 (RGBLED) Creating device 'RGB Switch Red'. 
2020-02-05 19:01:38.583 (RGBLED) Device created: RGBLED - RGB Switch Red 
2020-02-05 19:01:38.583 (RGBLED) Creating device 'RGB Switch Green'. 
2020-02-05 19:01:38.584 (RGBLED) Device created: RGBLED - RGB Switch Green 
2020-02-05 19:01:38.584 (RGBLED) Creating device 'RGB Switch Blue'. 
2020-02-05 19:01:38.588 (RGBLED) Device created: RGBLED - RGB Switch Blue 
2020-02-05 19:01:38.588 (RGBLED) SetBrickletConfiguration 
2020-02-05 19:01:38.592 (RGBLED) Set Status LED OFF 
2020-02-05 19:01:38.693 (RGBLED) SetBrickletConfiguration OK 
2020-02-05 19:01:38.182 Status: (RGBLED) Started. 
2020-02-05 19:01:38.579 Status: (RGBLED) Initialized version 0.1.0, author 'rwbL' 
2020-02-05 19:01:38.578 Status: (RGBLED) Entering work loop. 
```

## Notes

### Master Brick Disconnected & Re-connected
If the Master Brick has been disconnected from the Raspberry Pi (i.e. plugged out) and re-connected again, the hardware must be updated (using Setup > Hardware > select the plugin > Update) or restart Domoticz.

## dzVents Lua Automation Script Examples

### RGB LED Blink Color Red Every Minute (dzVents Lua Automation Script)
```
-- Tinkerforge RGB LED Bricklet 2.0 Plugin - Test Script 
-- dzVents Automation Script: tfrgbledv2_blink_red
-- Turn every minute the LED RED ON | OFF.
-- The color level is set by the slider widget and not in this script.
-- The slider has a range 0-100% which is mapped to a RGB value 0-255 used by the Bricklet (see plugin.py).
--
-- The plugin "Tinkerforge RGB LED Bricklet 2.0" is used with 3 devices:
-- (Idx,Name,Type,SubType,SwitchType)
-- 76,RGBLED - RGB Switch Red,Light/Switch,Switch,Dimmer
-- 77,RGBLED - RGB Switch Green,Light/Switch,Switch,Dimmer
-- 78,RGBLED - RGB Switch Blue,Light/Switch,Switch,Dimmer

IDXRGBLEDRED = 76
IDXRGBLEDGREEN = 77
IDXRGBLEDBLUE = 78

return {
	on = {
		timer = {
			'every minute',              
	   },
    },
	execute = function(domoticz, timer)
		domoticz.log('Timer event was triggered by ' .. timer.trigger, domoticz.LOG_INFO)
        if (domoticz.devices(IDXRGBLEDRED).state == 'On') then
            domoticz.devices(IDXRGBLEDRED).switchOff()
        else
            domoticz.devices(IDXRGBLEDRED).switchOn()
		end
		
		-- Ensure colors green and blue are switched off
        domoticz.devices(IDXRGBLEDGREEN).switchOff()
        domoticz.devices(IDXRGBLEDBLUE).switchOff()
	end
}
```

### Traffic Light Changing Color Every Minute (dzVents Lua Automation Script)
```
-- Tinkerforge RGB LED Bricklet 2.0 Plugin - Test Script 
-- dzVents Automation Script: tfrgbledv2_trafficlight
-- Change the color of the RGB LED bricklet every miniute from RED > YELLOW > GREEN.
-- If ON, the selected color level is set to 100% (check the sliders) resulting in Bricklet RGB 255.
-- The slider has a range 0-100% which is mapped to a RGB value 0-255 used by the Bricklet (see plugin.py).
-- Color yellow = R=100% (255),G=100% (255),B=0%
-- Color blue is not used.
-- 
-- The plugin "Tinkerforge RGB LED Bricklet 2.0" is used with 3 devices:
-- (Idx,Name,Type,SubType,SwitchType)
-- 76,RGBLED - RGB Switch Red,Light/Switch,Switch,Dimmer
-- 77,RGBLED - RGB Switch Green,Light/Switch,Switch,Dimmer
-- 78,RGBLED - RGB Switch Blue,Light/Switch,Switch,Dimmer

IDXRGBLEDRED = 76
IDXRGBLEDGREEN = 77
IDXRGBLEDBLUE = 78

STATERED = 0
STATEYELLOW = 1
STATEGREEN = 2

return {
	on = {
	    timer = { 'every minute' },
    },
    data = {
        trafficlightState = { initial = STATERED }
    },
	execute = function(domoticz, timer)
	    local msg = string.format("Trafficlight triggered to state %d", domoticz.data.trafficlightState)
		domoticz.log(msg, domoticz.LOG_INFO)

		if (domoticz.data.trafficlightState == STATERED) then
            domoticz.devices(IDXRGBLEDRED).setLevel(100)
            domoticz.devices(IDXRGBLEDGREEN).switchOff()
		end

		if (domoticz.data.trafficlightState == STATEYELLOW) then
            domoticz.devices(IDXRGBLEDRED).setLevel(100)
            domoticz.devices(IDXRGBLEDGREEN).setLevel(100)
		end
		if (domoticz.data.trafficlightState == STATEGREEN) then
            domoticz.devices(IDXRGBLEDRED).switchOff()
            domoticz.devices(IDXRGBLEDGREEN).setLevel(100)
		end

        -- Blue is not used = switch off
        domoticz.devices(IDXRGBLEDBLUE).switchOff()

        -- Set the new state		
        domoticz.data.trafficlightState = domoticz.data.trafficlightState + 1
        if (domoticz.data.trafficlightState > STATEGREEN) then
            domoticz.data.trafficlightState = STATERED
        end

	end
}
```

### Traffic Light Switch (dzVents Lua Automation Script)
```
-- Tinkerforge RGB LED Bricklet 2.0 Plugin - Test Script 
-- dzVents Automation Script: tfrgbledv2_trafficlight_switch
-- Selector switch (Light/Switch,Switch,Selector) with 3 colors R-G-B to set the color of the bricklet.
-- Selector Level & Level Name: 10 (RED), 20 (YELLOW), 30 (GREEN). Level 0(=OFF) is hidden.
-- The selected color level is set to 100% mapped to a color value 255 used by the Bricklet (see plugin.py).
-- Color yellow = R=100% (255),G=100% (255),B=0%
-- Color blue is not used.
-- 
-- The plugin "Tinkerforge RGB LED Bricklet 2.0" is used with 3 devices:
-- (Idx,Name,Type,SubType,SwitchType)
-- 76,RGBLED - RGB Switch Red,Light/Switch,Switch,Dimmer
-- 77,RGBLED - RGB Switch Green,Light/Switch,Switch,Dimmer
-- 78,RGBLED - RGB Switch Blue,Light/Switch,Switch,Dimmer
--
-- 20200106 by rwbL

local IDXRGBLEDTRAFFICLIGHTSWITCH = 12
local IDXRGBLEDRED = 76
local IDXRGBLEDGREEN = 77
local IDXRGBLEDBLUE = 78

-- Seector switch levels
local LEVELRED = 10
local LEVELYELLOW = 20
local LEVELGREEN = 30

return {
	on = {
	    devices = {
	        IDXRGBLEDTRAFFICLIGHTSWITCH 
	    }
    },
	execute = function(domoticz, device)
	    local msg = string.format("Trafficlight set color %s (%d)", device.levelName, device.level)
        domoticz.log(msg, domoticz.LOG_INFO)

		if (device.level == LEVELRED) then
            domoticz.devices(IDXRGBLEDRED).setLevel(100)
            domoticz.devices(IDXRGBLEDGREEN).switchOff()
		end

		if (device.level == LEVELYELLOW) then
            domoticz.devices(IDXRGBLEDRED).setLevel(100)
            domoticz.devices(IDXRGBLEDGREEN).setLevel(100)
		end

		if (device.level == LEVELGREEN) then
            domoticz.devices(IDXRGBLEDRED).switchOff()
            domoticz.devices(IDXRGBLEDGREEN).setLevel(100)
		end

        -- Blue is not used = switch off
        domoticz.devices(IDXRGBLEDBLUE).switchOff()

    end
}
```

### Color Switch (dzVents Lua Automation Script)
```
-- Tinkerforge RGB LED Bricklet 2.0 Plugin - Test Script 
-- dzVents Automation Script: tfrgbledv2_colorswitch
-- Domoticz device Color Switch with a color wheel to set the color (via widget > edit).
-- The selected color level is set to 100% mapped to a color value 255 used by the Bricklet (see plugin.py).
-- 
-- The plugin "Tinkerforge RGB LED Bricklet 2.0" is used with 3 devices:
-- (Idx,Name,Type,SubType,SwitchType)
-- 76,RGBLED - RGB Switch Red,Light/Switch,Switch,Dimmer
-- 77,RGBLED - RGB Switch Green,Light/Switch,Switch,Dimmer
-- 78,RGBLED - RGB Switch Blue,Light/Switch,Switch,Dimmer
-- In addition a Color Switch:
-- (Idx,Name,Type,SubType,SwitchType)
-- 79,RGBLED - Color switch, Color Switch,RGB,Dimmer

local IDXRGBLEDCOLORSWITCH = 79
local IDXRGBLEDRED = 76
local IDXRGBLEDGREEN = 77
local IDXRGBLEDBLUE = 78

-- Seector switch levels
local LEVELRED = 0
local LEVELYELLOW = 10
local LEVELGREEN = 20

return {
	on = {
	    devices = {
	        IDXRGBLEDCOLORSWITCH
	    }
    },
	execute = function(domoticz, device)
	    domoticz.log('Device ' .. device.name .. ' was changed:' .. device.state, domoticz.LOG_INFO)
        local red = 0
        local green = 0
        local blue = 0
        -- Get the color as lua table
        color = device.getColor()
		-- For exploring the table key value pairs. Commment out if not required
	    for key,value in pairs(color) do 
	        domoticz.log('K:' .. key .. ', V:' .. tostring(value), domoticz.LOG_INFO) 
        end
	    -- Get the color if the state is not "Off", "Set Color" or "On"
		-- The color is obtained from the color table color["red"] ...
        if (device.state ~= "Off") then
            red = tonumber(color["red"])
            green = tonumber(color["green"])
            blue = tonumber(color["blue"])
        end
    
        domoticz.devices(IDXRGBLEDRED).setLevel(red)
        domoticz.devices(IDXRGBLEDGREEN).setLevel(green)
        domoticz.devices(IDXRGBLEDBLUE).setLevel(blue)

        local msg = string.format("Color set to %d-%d-%d", red,green,blue)
		domoticz.log(msg, domoticz.LOG_INFO)

    end
}
```
