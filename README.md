# IRControl for ESP8266

Starting environment:
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

Using the generator to build a web interface
```sh
$ python3 ControlBuilder.py
> There are only two options:
> -g  Generate web interface
> -b  Build arduino header
```

Building Web UI 
```sh
$ python3 ControlBuilder.py -g
:: Basic client json builder
number of devices to configure? 1
Device name: Samsung TV
Type of device: 7
> Adding button
Button name: On/Off
Button style(optional): is-primary
IR codes(separated by comma): 34346897,410e21d
Add more buttons (y/n)? n
```
       
Validating the UI and modifying if necessary
```sh
$ chmod 700 run.sh
$ ./run.sh
```
Open http://127.0.0.1:5000/

Building arduino header
```sh
$ python3 ControlBuilder.py -b
SSID Name: myssidname
SSID Password: 
>> Header generated: arduino/IRControl.h
```

Copy header to Arduino libraries
```sh
$ mkdir [Arduino_Home_library]/IRControl
$ cp arduino/IRControl.h [Arduino_Home_library]/IRControl/
```

I've used an [ESP8266 D1 mini](https://www.amazon.com/dp/B01N3P763C/ref=cm_sw_r_tw_dp_4HT73YEQX2YWXFPVJCHS)

Finally, load the IRCtrl.ino program
```c
#include <IRControl.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>

ESP8266WebServer server(80);
IRsend irsend(14); //D5
...
```

The result:
![Sample Web Interface](sampleui.png?raw=true)

Related projects:
[NES.css](https://nostalgic-css.github.io/NES.css/)
