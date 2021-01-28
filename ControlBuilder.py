import json, re, sys
from colorama import init
from termcolor import colored
from pathlib import Path
from jsmin import jsmin
from csscompressor import compress
import htmlmin
import getpass
init()

class Device:
    def __init__(self, deviceIndex, deviceName, typeProvider):
        self.deviceIndex = deviceIndex
        self.deviceName = deviceName
        self.typeProvider = typeProvider

class Button:
    def __init__(self, index, label, codes, style):
        self.index = index
        self.label = label
        self.codes = codes
        self.style = style

class SSID:
    def __init__(self,name,password):
        self.name = name
        self.password = password

class GettingConfig:
    "Used to define the structure of json object to build UI interface"

    def __init__(self, libraryName="IRCtrlPage.h"):
        self.libraryName = libraryName
        self.interface = []

    def buildDevice(self, deviceObj):
        device={}
        device['device']=deviceObj.deviceIndex
        device['lbl']=deviceObj.deviceName
        device['type']=deviceObj.typeProvider
        device['btns']=[]
        return device

    def buildButton(self, buttonObj):
        button={}
        button['cmd']=buttonObj.index
        button['lbl']=buttonObj.label
        button['codes']=buttonObj.codes
        if buttonObj.style.__len__() > 0:
            button['style']=buttonObj.style
        return button

    def addButtons(self):
        btns=[]
        btnIndex=1
        while True:
            print('> Adding button')
            button=self.buildButton(self.__getInputButton(btnIndex))
            btns.append(button)
            if input('Add more buttons (y/n)? ') != 'y':
                break
            btnIndex+=1
        return btns

    def clientBuilder(self):
        print(':: Basic client json builder')
        numberDevices=int(input('number of devices to configure? '))
        for deviceIndex in range(1,numberDevices+1):
            device = self.buildDevice(self.__getInputDevice(deviceIndex))
            device['btns'] = self.addButtons()
            self.interface.append(device)

    def __getInputDevice(self, deviceIndex):
        label=input(colored('Device name: ','red'))
        typeProvider=input(colored('Type of device: ','red'))
        return Device(deviceIndex,label,typeProvider)

    def __getInputButton(self, btnIndex):
        label=input(colored('Button name: ','red'))
        style=input(colored('Button style(optional): ','red'))
        codes=input(colored('IR codes(separated by comma): ')).split(',')
        return Button(btnIndex,label,codes,style)          

    def getCleanJson(self):
        jsonStr = str(json.dumps(self.interface, separators=(',',':')))
        return jsonStr

class LocalServer:

    def __init__(self):
        self.gaction = Path('./local-server/static/actions.js')
        self.taction = Path('./local-server/static/actions.js.j2')
        self.style = Path('./local-server/static/style.css')
        self.main = Path('./local-server/templates/index.html')
        self.lib = Path('./arduino/IRControl.h')

    def buildActionJS(self, configJson):
        try:
            self.gaction.unlink()
        except Exception:
            print("There is no action to clean")
        action = re.sub('InterfaceBuilder', configJson+';', self.taction.read_text())
        self.gaction.write_text(action)

    def generateServer(self):
        config = GettingConfig()
        config.clientBuilder()
        self.buildActionJS(config.getCleanJson())

    def buildLibrary(self):
        try:
            self.lib.unlink()
        except Exception:
            print("There is no lib to clean")
        jsminified = re.sub('"','\\"',jsmin(self.gaction.read_text()))
        cssminified =  re.sub('"','\\"',compress(self.style.read_text()))
        htmlminified = re.sub('"','\\"',htmlmin.minify(self.main.read_text(), remove_optional_attribute_quotes=False) )
        htmlminified = htmlminified.replace('{% raw %}', '').replace('{% endraw %}','')
        ssid = self.__getInputSSID()

        with self.lib.open('w') as f:
            f.write('#define %s "%s"' % ('html_page', htmlminified))
            f.write('\n')
            f.write('#define %s "%s"' % ('js_control', jsminified))
            f.write('\n')
            f.write('#define %s "%s"' % ('css_style', cssminified))
            f.write('\n')
            f.write('#define %s "%s"' % ('SSID_NAME', ssid.name))
            f.write('\n')
            f.write('#define %s "%s"' % ('SSID_PSWD', ssid.password))

    def __getInputSSID(self):
        name=input(colored('SSID Name: ','red'))
        password = getpass.getpass(colored('SSID Password: ','red'))
        return SSID(name, password)

def man():
    print('There are only two options:')
    print('-g  Generate web interface')
    print('-b  Build arduino header')
    exit()

def main(option):
    loc = LocalServer()
    if option == '-g':
        loc.generateServer()
    elif option == '-b':
        loc.buildLibrary()
    else:
        print("I don't know this option")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        man()
    main(sys.argv[1])



     