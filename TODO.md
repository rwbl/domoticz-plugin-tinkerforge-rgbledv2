# ToDo domoticz-plugin-tinkerforge-rgbledv2
  
### NEW: Recognise disconnecting the Master brick
If the master brick is disconnected from the USB port, the plugin does not recognize that.

**Workaround (not tested yet)**
In the function onCommand, check the bricklet chip temperature.
If the bricklet is not reachable, an error is set.

_Status_
Not started.
