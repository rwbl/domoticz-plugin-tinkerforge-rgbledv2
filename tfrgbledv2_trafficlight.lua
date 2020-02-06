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
--
-- 20200104 by rwbL

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
