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
