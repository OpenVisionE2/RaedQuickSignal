#!/usr/bin/python
# -*- coding: utf-8 -*-
#RAEDQuickSignal (c) RAED 07-02-2014
#Thank's mfaraj to help with some codes

from __future__ import print_function

from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry, ConfigText, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Screens.ChannelSelection import ChannelSelection
from Components.Sources.StaticText import StaticText
from Components.ConfigList import ConfigListScreen
from Components.Console import Console as iConsole
from Plugins.Plugin import PluginDescriptor
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from GlobalActions import globalActionMap
from Screens.MessageBox import MessageBox
from Tools.Directories import fileExists
from Components.Language import language
from Components.MenuList import MenuList
from enigma import eTimer, getDesktop
from Screens.InputBox import InputBox
from keymapparser import readKeymap
from Components.Label import Label
from Screens.Screen import Screen
from Tools.Directories import *
from Components.config import *
from datetime import datetime
from .screens.skin import *
import re
from six.moves.urllib.request import urlretrieve
from os import path as os_path, remove as os_remove
from sys import version_info
from six.moves.urllib.request import urlretrieve
if version_info[0] == 2:
        # Python 2
        from urllib2 import urlopen as compat_urlopen
        from urllib2 import Request as compat_Request
        from urllib2 import URLError as compat_URLError
else:
        # Python 3
        from urllib.request import urlopen as compat_urlopen
        from urllib.request import Request as compat_Request
        from urllib.error import URLError as compat_URLError

VER = "5.3"


def removeunicode(data):
    try:
        try:
                data = data.encode('utf', 'ignore')
        except:
                pass
        data = data.decode('unicode_escape').encode('ascii', 'replace').replace('?', '').strip()
    except:
        pass
    return data


def trace_error():
    import sys
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/RaedQuickSignal.log', 'a'))
    except:
        pass


def logdata(label_name='', data=None):
    try:
        data = str(data)
        fp = open('/tmp/RaedQuickSignal.log', 'a')
        fp.write(str(label_name) + ': ' + data + "\n")
        fp.close()
    except:
        trace_error()
        pass


def dellog(label_name='', data=None):
    try:
        if os_path.exists('/tmp/RaedQuickSignal.log'):
                os_remove('/tmp/RaedQuickSignal.log')
    except:
        pass


def getDesktopSize():
    s = getDesktop(0).size()
    return (s.width(), s.height())


def isHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] == 1280


##############################################################################
config.plugins.RaedQuickSignal = ConfigSubsection()
config.plugins.RaedQuickSignal.enabled = ConfigYesNo(default=True)
config.plugins.RaedQuickSignal.keyname = ConfigSelection(default="KEY_TEXT", choices=[
                ("KEY_TEXT", "TEXT"),
                ("KEY_TV", "TV"),
                ("KEY_RADIO", "RADIO"),
                ("KEY_OK", "OK"),
                ("KEY_HELP", "HELP"),
                ("KEY_INFO", "INFO"),
                ("KEY_RED", "RED"),
                ("KEY_GREEN", "GREEN"),
                ("KEY_BLUE", "BLUE"),
                ("KEY_PVR", "PVR"),
                ("KEY_0", "0"),
                ("KEY_1", "1"),
                ("KEY_2", "2"),
                ("KEY_3", "3"),
                ("KEY_F1", "f1"),
                ("KEY_F2", "f2"),
                ("KEY_F3", "f3"),
                ])
config.plugins.RaedQuickSignal.style = ConfigSelection(default="AGC1", choices=[
                ("AGC1", "AGC Progress + Picon"),
                ("AGC2", "AGC Progress + Event Description"),
                ("AGC3", "AGC Progress + Weather"),
                ("Event1", "Event Progress + Picon"),
                ("Event2", "Event Progress + Event Description"),
                ("Event3", "Event Progress + Weather"),
                ("Full", "Full Screen without any extra functions"),
                ])
config.plugins.RaedQuickSignal.enabledb = ConfigSelection(default="Enable", choices=[
                ("Enable", "Enable show db value"),
                ("Disable", "Disable show db value")
                ])
config.plugins.RaedQuickSignal.piconpath = ConfigSelection(default="PLUGIN", choices=[
                ("PLUGIN", "Set Picon Path from Plugin"),
                ("MEDIA", "Set Picon Path from /media"),
                ])
config.plugins.RaedQuickSignal.refreshInterval = ConfigNumber(default=30) #in minutes
##############################################################################
try:
        config.plugins.TSweather = ConfigSubsection()
        config.plugins.TSweather.city = ConfigText(default="manama", visible_width=250, fixed_size=False)
        config.plugins.TSweather.windtype = ConfigSelection(default="ms", choices=[
                ("ms", _("m/s")),
                ("fts", _("ft/s")),
                ("kmh", _("km/h")),
                ("mph", _("mp/h")),
                ("knots", _("knots"))])
        config.plugins.TSweather.degreetype = ConfigSelection(default="C", choices=[
                ("C", _("Celsius")),
                ("F", _("Fahrenheit"))])
        config.plugins.TSweather.weather_location = ConfigText(default="bh-BH", visible_width=250, fixed_size=False)
except:
        trace_error()
        pass

import gettext
REDC = '\033[31m'
ENDC = '\033[m'


def cprint(text):
    print(REDC + "[RaedQuickSignal] " + text + ENDC)


def downloadFile(url, filePath):
    try:
        # Download the file from `url` and save it locally under `file_name`:
        urlretrieve(url, filePath)
        return True
        req = compat_Request(url)
        response = compat_urlopen(req)
        print("response.read", response.read())
        output = open(filePath, 'wb')
        output.write(response.read())
        output.close()
        response.close()
        return True
    except compat_URLError as e:
        trace_error()
        if hasattr(e, 'code'):
            cprint('We failed with error code - %s.' % e.code)
        elif hasattr(e, 'reason'):
            cprint('We failed to reach a server.')
            cprint('Reason: %s' % e.reason)
    return False


def readurl(url):
    try:
        req = compat_Request(url)
        response = compat_urlopen(req)
        data = response.read()
        response.close()
        cprint("[data %s]" % data)
        return data
    except compat_URLError as e:
        if hasattr(e, 'code'):
            cprint('We failed with error code - %s.' % e.code)
        elif hasattr(e, 'reason'):
            cprint('We failed to reach a server.')
            cprint('Reason: %s' % e.reason)


def getcities(weather_location):
        url = (b"http://www.geonames.org/advanced-search.html?q=&country=%s&featureClass=P&continentCode=".decode("utf-8")) % str(weather_location.upper())
        logdata("xmlurl", url)
        data = readurl(url)
        if data == None:
                return []
        try:
                regx = '''<a href="(.*?)"><img src=".*?" border="0" alt=".*?"></a>'''
                match = re.findall(str(regx), str(data), re.M | re.I)
                cities = []
                for cityURL in match:
                    if 'wiki' in cityURL:
                            continue
                    cityName = os.path.split(cityURL)[1].replace(".html", "")
                    logdata('cityName', cityName)
                    if cityName in cities:
                        continue
                    cities.append(cityName)
                cities.sort()
                return cities
        except Exception as error:
                trace_error()


class WeatherLocationChoiceList(Screen):
        def __init__(self, session, country):
                self.skin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal")
                self.skin = SKIN_WeatherLocation
                self.session = session
                self.country = country
                list = []
                Screen.__init__(self, session)
                self.title = _(country)
                self["choicelist"] = MenuList(list)
                self["key_red"] = Label(_("Cancel"))
                self["key_green"] = Label(_("Add city"))
                self["myActionMap"] = ActionMap(["SetupActions", "ColorActions"],
                {
                        "ok": self.keyOk,
                        "green": self.add_city,
                        "cancel": self.keyCancel,
                        "red": self.keyCancel,
                }, -1)
                self.iConsole = iConsole()
                self.timer = eTimer()
                self.timer.callback.append(self.createChoiceList)
                self.timer.start(5, False)

        def createChoiceList(self):
                self.timer.stop()
                list = []
                list = getcities(self.country)
                self["choicelist"].l.setList(list)

        def control_xml(self, result, retval, extra_args):
                if retval != 0:
                        self.write_none()

        def write_none(self):
                with open('/tmp/weathermsn.xml', 'w') as noneweather:
                        noneweather.write('None')
                noneweather.close()

        def get_xmlfile(self, weather_city, weather_location):
                degreetype = config.plugins.TSweather.degreetype.value
                weather_city = weather_city.replace(" ", "+")
                url = 'http://weather.service.msn.com/data.aspx?weadegreetype=%s&culture=%s&weasearchstr=%s&src=outlook' % (degreetype, weather_location, weather_city)
                file_name = '/tmp/weathermsn.xml'
                try:
                       urlretrieve(url, file_name)
                       return True
                except Exception as error:
                       trace_error()

        def add_city(self):
                 self.session.openWithCallback(self.cityCallback, InputBox, title=_("Please enter a name of the city"), text="cityname", maxSize=False, visible_width=250)

        def cityCallback(self, city=None):
                try:
                        if os_path.exists('/tmp/weathermsn.xml'):
                                os_remove('/tmp/weathermsn.xml')
                        returnValue = self["choicelist"].l.getCurrentSelection()
                        countryCode = self.country.lower() + "-" + self.country.upper()
                        if self.get_xmlfile(returnValue, countryCode) == False:
                                self.session.open(MessageBox, _("Sorry, your city is not available."), MessageBox.TYPE_ERROR)
                                return
                        if not fileExists('/tmp/weathermsn.xml'):
                                self.write_none()
                                self.session.open(MessageBox, _("Sorry, your city is not available."), MessageBox.TYPE_ERROR)
                                return None
                        if returnValue != None:
                                self.close(returnValue)
                        else:
                                self.keyCancel()
                except Exception as error:
                        trace_error()

        def keyOk(self):
                try:
                        if os_path.exists('/tmp/weathermsn.xml'):
                                os_remove('/tmp/weathermsn.xml')
                        returnValue = self["choicelist"].l.getCurrentSelection()
                        countryCode = self.country.lower() + "-" + self.country.upper()
                        if self.get_xmlfile(returnValue, countryCode) == False:
                                self.session.open(MessageBox, _("Sorry, your city is not available."), MessageBox.TYPE_ERROR)
                                return
                        if not fileExists('/tmp/weathermsn.xml'):
                                self.write_none()
                                self.session.open(MessageBox, _("Sorry, your city is not available."), MessageBox.TYPE_ERROR)
                                return None
                        if returnValue != None:
                                self.close(returnValue)
                        else:
                                self.keyCancel()
                except Exception as error:
                        trace_error()

        def keyCancel(self):
                self.close(None)


class RaedQuickSignalScreen(Screen):
        def __init__(self, session):
                Screen.__init__(self, session)
                self.skin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal")
                dellog()
                if config.plugins.RaedQuickSignal.style.value == "AGC1":
                        if config.plugins.RaedQuickSignal.piconpath.value == "PLUGIN":
                             if config.plugins.RaedQuickSignal.enabledb.value == "Enable":
                                   if isHD():
                                         self.skin = SKIN_AGC_Picon_SNRdB
                                   else:
                                         self.skin = SKIN_AGC_Picon_SNRdB_FHD
                             else:
                                   if isHD():
                                         self.skin = SKIN_AGC_Picon_NOSNRdB
                                   else:
                                         self.skin = SKIN_AGC_Picon_NOSNRdB_FHD
                        elif config.plugins.RaedQuickSignal.piconpath.value == "MEDIA":
                             if config.plugins.RaedQuickSignal.enabledb.value == "Enable":
                                   if isHD():
                                         self.skin = SKIN_AGC_Picon_media_SNRdB
                                   else:
                                         self.skin = SKIN_AGC_Picon_media_SNRdB_FHD
                             else:
                                   if isHD():
                                         self.skin = SKIN_AGC_Picon_media_NOSNRdB
                                   else:
                                         self.skin = SKIN_AGC_Picon_media_NOSNRdB_FHD
                elif config.plugins.RaedQuickSignal.style.value == "AGC2":
                        if config.plugins.RaedQuickSignal.enabledb.value == "Enable":
                             if isHD():
                                   self.skin = SKIN_AGC_Event_Des_SNRdB
                             else:
                                   self.skin = SKIN_AGC_Event_Des_SNRdB_FHD
                        else:
                             if isHD():
                                   self.skin = SKIN_AGC_Event_Des_NOSNRdB
                             else:
                                   self.skin = SKIN_AGC_Event_Des_NOSNRdB_FHD
                elif config.plugins.RaedQuickSignal.style.value == "AGC3":
                        if config.plugins.RaedQuickSignal.enabledb.value == "Enable":
                             if isHD():
                                   self.skin = SKIN_AGC_Weather_SNRdB
                             else:
                                   self.skin = SKIN_AGC_Weather_SNRdB_FHD
                        else:
                             if isHD():
                                   self.skin = SKIN_AGC_Weather_NOSNRdB
                             else:
                                   self.skin = SKIN_AGC_Weather_NOSNRdB_FHD
                elif config.plugins.RaedQuickSignal.style.value == "Event1":
                        if config.plugins.RaedQuickSignal.piconpath.value == "PLUGIN":
                             if config.plugins.RaedQuickSignal.enabledb.value == "Enable":
                                   if isHD():
                                         self.skin = SKIN_Event_Progress_Picon_SNRdB
                                   else:
                                         self.skin = SKIN_Event_Progress_Picon_SNRdB_FHD
                             else:
                                   if isHD():
                                         self.skin = SKIN_Event_Progress_Picon_NOSNRdB
                                   else:
                                         self.skin = SKIN_Event_Progress_Picon_NOSNRdB_FHD
                        elif config.plugins.RaedQuickSignal.piconpath.value == "MEDIA":
                             if config.plugins.RaedQuickSignal.enabledb.value == "Enable":
                                   if isHD():
                                         self.skin = SKIN_Event_Progress_Picon_media_SNRdB
                                   else:
                                         self.skin = SKIN_Event_Progress_Picon_media_SNRdB_FHD
                             else:
                                   if isHD():
                                         self.skin = SKIN_Event_Progress_Picon_media_NOSNRdB
                                   else:
                                         self.skin = SKIN_Event_Progress_Picon_media_NOSNRdB_FHD
                elif config.plugins.RaedQuickSignal.style.value == "Event2":
                        if config.plugins.RaedQuickSignal.enabledb.value == "Enable":
                             if isHD():
                                   self.skin = SKIN_Event_Progress_Event_Des_SNRdB
                             else:
                                   self.skin = SKIN_Event_Progress_Event_Des_SNRdB_FHD
                        else:
                             if isHD():
                                   self.skin = SKIN_Event_Progress_Event_Des_NOSNRdB
                             else:
                                   self.skin = SKIN_Event_Progress_Event_Des_NOSNRdB_FHD
                elif config.plugins.RaedQuickSignal.style.value == "Event3":
                        if config.plugins.RaedQuickSignal.enabledb.value == "Enable":
                             if isHD():
                                   self.skin = SKIN_Event_Progress_Weather_SNRdB
                             else:
                                   self.skin = SKIN_Event_Progress_Weather_SNRdB_FHD
                        else:
                             if isHD():
                                   self.skin = SKIN_Event_Progress_Weather_NOSNRdB
                             else:
                                   self.skin = SKIN_Event_Progress_Weather_NOSNRdB_FHD
                elif config.plugins.RaedQuickSignal.style.value == "Full":
                       if isHD():
                             self.skin = SKIN_Full_Screen
                       else:
                             self.skin = SKIN_Full_Screen_FHD
                self.session = session
                self.startupservice = config.servicelist.startupservice.value
                logdata('self.startupservice', self.startupservice)
                sref = self.session.nav.getCurrentService()
                from ServiceReference import ServiceReference
                p = ServiceReference(str(sref))
                servicename = str(p.getServiceName())
                serviceurl = p.getPath()
                logdata('serviceurl', serviceurl)
                logdata('servicename', servicename)
                logdata('playeble-sref', sref)
                config.servicelist.startupservice.value = serviceurl
                config.servicelist.startupservice.save()
                self.servicelist = self.session.instantiateDialog(ChannelSelection)
                self["setupActions"] = ActionMap(["WizardActions", "SetupActions", "MenuActions"],
                    {
                         "cancel": self.exit,
                         "menu": self.showsetup,
                         "up": self.keyUp,
                         "down": self.keyDown,
                         "left": self.keyLeft,
                         "right": self.keyRight,
                    })
                shown = True
                self.onLayoutFinish.append(self.layoutFinished)

        def layoutFinished(self):
                self.instance.show()
                self.setTitle("RaedQuickSignal V %s" % VER)
                cfile = open("/tmp/.qsignal", "w")
                cfile.close()

        def keyLeft(self):
                self.servicelist.moveUp()
                self.servicelist.zap()

        def keyRight(self):
                self.servicelist.moveDown()
                self.servicelist.zap()

        def keyUp(self):
                self.session.execDialog(self.servicelist)

        def keyDown(self):
                self.session.execDialog(self.servicelist)

        def exit(self):
                if os_path.exists("/tmp/.qsignal"):
                        os_remove("/tmp/.qsignal")
                config.servicelist.startupservice.value = self.startupservice
                config.servicelist.startupservice.save()
                self.close()

        def setupback(self, answer=False):
                if answer:
                        self.exit()

        def showsetup(self):
                self.session.openWithCallback(self.setupback, RaedQuickSignal_setup)
##############################################################################


class RaedQuickSignal():
        def __init__(self):
                self.dialog = None

        def gotSession(self, session):
                self.session = session
                self.qsignal = None
                if os_path.exists("/tmp/.qsignal"):
                        os_remove("/tmp/.qsignal")
                keymap = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/keymap.xml")
                global globalActionMap
                readKeymap(keymap)
                if 'displayHelp' in globalActionMap.actions:
                        del globalActionMap.actions['displayHelp']
                elif 'showSherlock' in globalActionMap.actions:
                        del globalActionMap.actions['showSherlock']
                globalActionMap.actions['showRaedQuickSignal'] = self.ShowHide
##############################################################################

        def ShowHide(self):
                if os_path.exists("/tmp/.qsignal") == False:
                        if config.plugins.RaedQuickSignal.enabled.value:
                                self.session.open(RaedQuickSignalScreen)


##############################################################################
pSignal = RaedQuickSignal()
##############################################################################


class RaedQuickSignal_setup(ConfigListScreen, Screen):
        def __init__(self, session):
                self.session = session
                Screen.__init__(self, session)
                self.skin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal")
                if isHD():
                        self.skin = SKIN_setup
                else:
                        self.skin = SKIN_setup_FHD
                self.setTitle("RaedQuickSignal setup V %s" % VER)
                self.RaedQuickSignal_fake_entry = NoSave(ConfigNothing())
                self.list = []
                ConfigListScreen.__init__(self, self.list)
                self["key_red"] = StaticText(_("Close"))
                self["key_green"] = StaticText(_("Save"))
                #self["key_yellow"] = StaticText(_(" "))
                #self["key_blue"] = StaticText(_(" "))
                self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "green": self.save,
                        #"yellow": self.restart,
                        #"blue": self.keyOk,
                        "ok": self.keyOk
                }, -2)
                self.createConfigList()

        def createConfigList(self):
                self.list = []
                self.currenabled_value = config.plugins.RaedQuickSignal.enabled.value
                self.currkeyname_value = config.plugins.RaedQuickSignal.keyname.value
                self.list.append(getConfigListEntry(_("Enable Plugin"), config.plugins.RaedQuickSignal.enabled))
                self.list.append(getConfigListEntry(_("Enable/Disable DB Value"), config.plugins.RaedQuickSignal.enabledb))
                self.list.append(getConfigListEntry(_("Select key to show RaedQuickSignal"), config.plugins.RaedQuickSignal.keyname))
                self.list.append(getConfigListEntry(_("Select Path Of Picons Folder"), config.plugins.RaedQuickSignal.piconpath))
                self.list.append(getConfigListEntry(_("Select Style of Plugin"), config.plugins.RaedQuickSignal.style))
                self.list.append(getConfigListEntry(_("Refresh interval in minutes:"), config.plugins.RaedQuickSignal.refreshInterval))
                self.list.append(getConfigListEntry(_("Temperature unit:"), config.plugins.TSweather.degreetype))
                self.list.append(getConfigListEntry(_("Location #press OK to change:"), config.plugins.TSweather.city))
                self["config"].list = self.list
                self["config"].l.setList(self.list)

        def cancel(self):
                for i in self["config"].list:
                        i[1].cancel()
                self.close(False)

        def restart(self, answer=None):
                if answer:
                   self.session.open(TryQuitMainloop, 3)
                   return
                self.close(True)

        def keyOk(self):
            countriesFile = resolveFilename(SCOPE_PLUGINS, 'Extensions/RaedQuickSignal/countries')
            countries = open(countriesFile).readlines()
            clist = []
            for country in countries:
                countryCode, countryName = country.split(",")
                clist.append((countryName, countryCode))
            from Screens.ChoiceBox import ChoiceBox
            self.session.openWithCallback(self.choicesback, ChoiceBox, _('select your country'), clist)

        def choicesback(self, select):
                if select:
                    self.country = select[1]
                    config.plugins.TSweather.weather_location.value = self.country.lower() + "-" + self.country.upper()
                    config.plugins.TSweather.weather_location.save()
                    self.session.openWithCallback(self.citiesback, WeatherLocationChoiceList, self.country)

        def citiesback(self, select):
                if select:
                  weather_city = select
                  weather_city.capitalize()
                  config.plugins.TSweather.city.setValue(weather_city)
                  self.createConfigList()

        def save(self):
                if self["config"].isChanged():
                        for x in self['config'].list:
                            x[1].save()
                        configfile.save()
                        # we can not use resolveFilename(SCOPE_PLUGINS) here the keymap.xml will be not writable
                        if not os_path.exists('/usr/lib64'):
                            keyfile = open("/usr/lib/enigma2/python/Plugins/Extensions/RaedQuickSignal/keymap.xml", "w")
                        else:
                            keyfile = open("/usr/lib64/enigma2/python/Plugins/Extensions/RaedQuickSignal/keymap.xml", "w")
                        keyfile.write('<keymap>\n\t<map context="GlobalActions">\n\t\t<key id="%s" mapto="showRaedQuickSignal" flags="m" />\n\t</map>\n</keymap>' % config.plugins.RaedQuickSignal.keyname.value)
                        keyfile.close()
                        if not self.currenabled_value == config.plugins.RaedQuickSignal.enabled.value or not self.currkeyname_value == config.plugins.RaedQuickSignal.keyname.value:
                           self.session.openWithCallback(self.restart, MessageBox, _("Settings changed,restart enigma2 now?"))
                        else:
                                self.close(True)
                else:
                        self.close(False)
##############################################################################


def sessionstart(reason, session=None, **kwargs):
        if reason == 0:
                pSignal.gotSession(session)
##############################################################################


def main(session, **kwargs):
        session.open(RaedQuickSignal_setup)
##############################################################################


def Plugins(**kwargs):
        result = [
                PluginDescriptor(
                        where=[PluginDescriptor.WHERE_SESSIONSTART],
                        fnc=sessionstart
                ),
                PluginDescriptor(
                        name=_("RaedQuickSignal Setup"),
                        description=_("RAED's RaedQuickSignal setup"),
                        where=PluginDescriptor.WHERE_PLUGINMENU,
                        icon='RaedQuickSignal.png',
                        fnc=main
                ),
        ]
        return result
