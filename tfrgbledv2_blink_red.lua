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
--
-- 20200102 by rwbL

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
