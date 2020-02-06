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
--
-- 20200106 by rwbL

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
