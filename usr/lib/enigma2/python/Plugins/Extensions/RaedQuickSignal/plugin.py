#RAEDQuickSignal (c) RAED 07-02-2014
#Thank's mfaraj to help with some codes

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
import datetime
import os
import re

Ver = "5.2"
now = datetime.datetime.now()
datetime_now = (now.strftime("%Y-%m-%d  %H:%M"))
lang = language.getLanguage()

def trace_error():
    import sys
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/RaedQuickSignal.log', 'a'))
    except:
        pass

def logdata(label_name = '', data = None):
    try:
        data=str(data)
        fp = open('/tmp/RaedQuickSignal.log', 'a')
        fp.write( str(label_name) + ': ' + data+"\n")
        fp.close()
    except:
        trace_error()    
        pass

def dellog(label_name = '', data = None):
    try:
        import os
        if os.path.exists('/tmp/RaedQuickSignal.log'):
                os.remove('/tmp/RaedQuickSignal.log')
    except:
        pass
##############################################################################
if getDesktop(0).size().width() == 1280:
        Space = "             "
        SKIN_setup = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Setup.xml")
        SKIN_WeatherLocation = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/WeatherLocation.xml")
        SKIN_AGC_Picon = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/AGC_Picon.xml")
        SKIN_AGC_Event_Des = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/AGC_Event_Des.xml")
        SKIN_AGC_Weather = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/AGC_Weather.xml")
        SKIN_Event_Progress_Picon = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Event_Progress_Picon.xml")
        SKIN_Event_Progress_Event_Des = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Event_Progress_Event_Des.xml")
        SKIN_Event_Progress_Weather = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Event_Progress_Weather.xml")
	SKIN_AGC_Picon_media = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/AGC_Picon_media.xml")
        SKIN_Event_Progress_Picon_media = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Event_Progress_Picon_media.xml")
else:
        Space = "                                          "
        SKIN_setup = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Setup_FHD.xml")
        SKIN_WeatherLocation = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/WeatherLocation.xml")
        SKIN_AGC_Picon = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/AGC_Picon_FHD.xml")
        SKIN_AGC_Event_Des = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/AGC_Event_Des_FHD.xml")
        SKIN_AGC_Weather = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/AGC_Weather_FHD.xml")
        SKIN_Event_Progress_Picon = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Event_Progress_Picon_FHD.xml")
        SKIN_Event_Progress_Event_Des = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Event_Progress_Event_Des_FHD.xml")
        SKIN_Event_Progress_Weather = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Event_Progress_Weather_FHD.xml")
	SKIN_AGC_Picon_media = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/AGC_Picon_media_FHD.xml")
        SKIN_Event_Progress_Picon_media = resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/screens/Event_Progress_Picon_media_FHD.xml")
##############################################################################
config.plugins.RaedQuickSignal = ConfigSubsection()
config.plugins.RaedQuickSignal.enabled = ConfigYesNo(default=True)
config.plugins.RaedQuickSignal.keyname = ConfigSelection(default = "KEY_TEXT", choices = [
                ("KEY_TEXT", "TEXT"),
                ("KEY_TV", "TV"),
                ("KEY_RADIO", "RADIO"),
                ("KEY_OK", "OK"),
                ("KEY_EXIT", "EXIT"),
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
                ])
config.plugins.RaedQuickSignal.style = ConfigSelection(default = "AGC1", choices = [
                ("AGC1", "AGC Progress + Picon"),
                ("AGC2", "AGC Progress + Event Description"),
                ("AGC3", "AGC Progress + Weather"),
                ("Event1", "Event Progress + Picon"),
                ("Event2", "Event Progress + Event Description"),
                ("Event3", "Event Progress + Weather"),
                ])
config.plugins.RaedQuickSignal.piconpath = ConfigSelection(default = "PLUGIN", choices = [
                ("PLUGIN", "Set Picon Path from Plugin"),
                ("MEDIA", "Set Picon Path from /media"),
                ])
config.plugins.RaedQuickSignal.refreshInterval = ConfigNumber(default=30) #in minutes
##############################################################################
try:
        config.plugins.TSweather = ConfigSubsection()       
        config.plugins.TSweather.city = ConfigText(default="manama", visible_width = 250, fixed_size = False)       
        config.plugins.TSweather.windtype = ConfigSelection(default="ms", choices = [
                ("ms", _("m/s")),
                ("fts", _("ft/s")),
                ("kmh", _("km/h")),
                ("mph", _("mp/h")),
                ("knots", _("knots"))])
        config.plugins.TSweather.degreetype = ConfigSelection(default="C", choices = [
                ("C", _("Celsius")),
                ("F", _("Fahrenheit"))])
        config.plugins.TSweather.weather_location= ConfigText(default="bh-BH", visible_width = 250, fixed_size = False)       
except:
        trace_error()
        pass

def readurl(url):
    import urllib2
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data
    except urllib2.URLError as e:
        if hasattr(e, 'code'):
            print 'We failed with error code - %s.' % e.code
        elif hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: %s' % e.reason

def getcities(weather_location):
        url='http://www.geonames.org/advanced-search.html?q=&country=%s&featureClass=P&continentCode=' % weather_location.upper()
        #url='http://www.geonames.org/search.html?q=&country=%s' % weather_location
        data=readurl(url)
        if data is None:
                return []
        try:
                regx='''<a href=".*?"><img src=".*?" border="0" alt=".*?"></a></td><td><a href=".*?">(.*?)</a>'''
                match=re.findall(regx,data, re.M|re.I)
                cities=[]
                for item in match:
                    cityName=item.replace(',',"").strip()
                    try:
                            cityName=cityName.encode("utf-8","ignore")
                    except:
                            pass
                    if cityName in cities:
                        continue
                    cities.append(cityName)
                cities.sort()
                return cities                   
        except:
                return []

def isInteger(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

class WeatherLocationChoiceList(Screen):
	def __init__(self, session, country):
                with open(SKIN_WeatherLocation, 'r') as f:
                     self.skin = f.read()
                     f.close()
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
                try:
                        self.timer.callback.append(self.createChoiceList)
                except:
                        self.timer_conn = self.timer.timeout.connect(self.createChoiceList)
                self.timer.start(5, False)

	def createChoiceList(self):
                self.timer.stop()
		list = []
		list=getcities(self.country)
		self["choicelist"].l.setList(list)

	def control_xml(self, result, retval, extra_args):
		if retval is not 0:
			self.write_none()

	def write_none(self):
		with open('/tmp/weathermsn.xml', 'w') as noneweather:
			noneweather.write('None')
		noneweather.close()

	def get_xmlfile(self,weather_city,weather_location):
                degreetype = config.plugins.TSweather.degreetype.value
                weather_city=weather_city.replace(" ","+")
                url='http://weather.service.msn.com/data.aspx?weadegreetype=%s&culture=%s&weasearchstr=%s&src=outlook' % (degreetype, weather_location, weather_city)
                file_name='/tmp/weathermsn.xml'
                import urllib
                # Download the file from `url` and save it locally under `file_name`:
                try:
                       urllib.urlretrieve(url, file_name)
                       return True
                except:
                       return False

        def add_city(self):
                 self.session.openWithCallback(self.cityCallback, InputBox, title=_("Please enter a name of the city"), text="cityname", maxSize=False, visible_width =250)

        def cityCallback(self,city=None):
                if city:
                        if os.path.exists('/tmp/weathermsn.xml'):
                          os.remove('/tmp/weathermsn.xml')
                        returnValue = city
                        countryCode=self.country.lower()+"-"+self.country.upper()
                        if self.get_xmlfile(returnValue,countryCode)==False:
                          self.session.open(MessageBox, _("Sorry, your city is not available."),MessageBox.TYPE_ERROR)
                          return 
                        if not fileExists('/tmp/weathermsn.xml'):
                                self.write_none()
                                self.session.open(MessageBox, _("Sorry, your city is not available."),MessageBox.TYPE_ERROR)
                                return None
                        if returnValue is not None:
                                self.close(returnValue)
                        else:
                                self.keyCancel()

	def keyOk(self):
                if os.path.exists('/tmp/weathermsn.xml'):
                  os.remove('/tmp/weathermsn.xml')
		returnValue = self["choicelist"].l.getCurrentSelection()
		countryCode=self.country.lower()+"-"+self.country.upper()
		if self.get_xmlfile(returnValue,countryCode)==False:
                  self.session.open(MessageBox, _("Sorry, your city is not available."),MessageBox.TYPE_ERROR)
                  return 
		if not fileExists('/tmp/weathermsn.xml'):
			self.write_none()
			self.session.open(MessageBox, _("Sorry, your city is not available."),MessageBox.TYPE_ERROR)
			return None
		if returnValue is not None:
			self.close(returnValue)
		else:
			self.keyCancel()

	def keyCancel(self):
		self.close(None)

class RaedQuickSignalScreen(Screen):
        def __init__(self, session):
                Screen.__init__(self, session)
                dellog()
                if config.plugins.RaedQuickSignal.style.value == "AGC1":
                        if config.plugins.RaedQuickSignal.piconpath.value == "PLUGIN":
                             with open(SKIN_AGC_Picon, 'r') as f:
                                  self.skin = f.read()
                                  f.close()
                        elif config.plugins.RaedQuickSignal.piconpath.value == "MEDIA":
                             with open(SKIN_AGC_Picon_media, 'r') as f:
                                  self.skin = f.read()
                                  f.close()
                elif config.plugins.RaedQuickSignal.style.value == "AGC2":
                        with open(SKIN_AGC_Event_Des, 'r') as f:
                             self.skin = f.read()
                             f.close()
                elif config.plugins.RaedQuickSignal.style.value == "AGC3":
                        with open(SKIN_AGC_Weather, 'r') as f:
                             self.skin = f.read()
                             f.close()
                elif config.plugins.RaedQuickSignal.style.value == "Event1":
                        if config.plugins.RaedQuickSignal.piconpath.value == "PLUGIN":
                             with open(SKIN_Event_Progress_Picon, 'r') as f:
                                  self.skin = f.read()
                                  f.close()
                        elif config.plugins.RaedQuickSignal.piconpath.value == "MEDIA":
                             with open(SKIN_Event_Progress_Picon_media, 'r') as f:
                                  self.skin = f.read()
                                  f.close()
                elif config.plugins.RaedQuickSignal.style.value == "Event2":
                        with open(SKIN_Event_Progress_Event_Des, 'r') as f:
                             self.skin = f.read()
                             f.close()
                elif config.plugins.RaedQuickSignal.style.value == "Event3":
                        with open(SKIN_Event_Progress_Weather, 'r') as f:
                             self.skin = f.read()
                             f.close()
                self.session=session
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
                         "menu":self.showsetup,
                         "up": self.keyUp,
                         "down": self.keyDown,
                         "left": self.keyLeft,
                         "right": self.keyRight,
                    })
                shown=True
                self.onLayoutFinish.append(self.layoutFinished)

        def layoutFinished(self):
                self.instance.show()
                self.setTitle("QuickSignal by RAED V" + str(Ver + Space + datetime_now))
                cfile=open("/tmp/.qsignal","w")
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
                if os.path.exists("/tmp/.qsignal"):
                        os.remove("/tmp/.qsignal")
                config.servicelist.startupservice.value = self.startupservice
                config.servicelist.startupservice.save()
                self.close()

        def setupback(self,answer=False):
                if answer:
                        self.exit()
                        
        def showsetup(self):
                self.session.openWithCallback(self.setupback,RaedQuickSignal_setup)
##############################################################################
class RaedQuickSignal():
        def __init__(self):
                self.dialog = None

        def gotSession(self, session):
                self.session = session
                self.qsignal=None
                if os.path.exists("/tmp/.qsignal"):
                       os.remove("/tmp/.qsignal")
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
                if os.path.exists("/tmp/.qsignal")==False:
                        if config.plugins.RaedQuickSignal.enabled.value:
                                self.session.open(RaedQuickSignalScreen)
##############################################################################
pSignal = RaedQuickSignal()
##############################################################################
class RaedQuickSignal_setup(ConfigListScreen, Screen):
        def __init__(self, session):
                self.session = session
                Screen.__init__(self, session)
                with open(SKIN_setup, 'r') as f:
                     self.skin = f.read()
                     f.close()
                self.setTitle(_("RAED's RaedQuickSignal setup V" + Ver))
                self.RaedQuickSignal_fake_entry = NoSave(ConfigNothing())
                self.list = []
                ConfigListScreen.__init__(self, self.list)
                self["key_red"] = StaticText(_("Close"))
                self["key_green"] = StaticText(_("Save"))
                self["key_yellow"] = StaticText(_(" "))
                self["key_blue"] = StaticText(_(" "))
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

        def run(self):
                  self.session.open(RaedQuickSignalScreen)
                
        def createConfigList(self):
                self.list = []
                self.currenabled_value=config.plugins.RaedQuickSignal.enabled.value
                self.currkeyname_value=config.plugins.RaedQuickSignal.keyname.value
                self.list.append(getConfigListEntry(_("Enable Plugin"), config.plugins.RaedQuickSignal.enabled))
                self.list.append(getConfigListEntry(_("Select key to show RaedQuickSignal"), config.plugins.RaedQuickSignal.keyname))
		self.list.append(getConfigListEntry(_("Select Path Of Picons Prov/Sat"), config.plugins.RaedQuickSignal.piconpath))
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
                
        def restart(self,answer=None):
                if answer:
                   self.session.open(TryQuitMainloop, 3)
                   return
                self.close(True)

        def keyOk(self):
            countriesFile = resolveFilename(SCOPE_PLUGINS, 'Extensions/RaedQuickSignal/countries')
            countries=open(countriesFile).readlines()
            clist=[]
            for country in countries:
                countryCode,countryName=country.split(",")
                clist.append((countryName,countryCode))
            from Screens.ChoiceBox import ChoiceBox
            self.session.openWithCallback(self.choicesback, ChoiceBox, _('select your country'), clist)

        def choicesback(self, select):
                if select:
                    self.country=select[1]
                    config.plugins.TSweather.weather_location.value=self.country.lower()+"-"+self.country.upper()
                    config.plugins.TSweather.weather_location.save()
                    self.session.openWithCallback(self.citiesback, WeatherLocationChoiceList, self.country)
                    
        def citiesback(self,select):
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
                        keyfile = open(resolveFilename(SCOPE_PLUGINS, "Extensions/RaedQuickSignal/keymap.xml", "w"))
                        keyfile.write('<keymap>\n\t<map context="GlobalActions">\n\t\t<key id="%s" mapto="showRaedQuickSignal" flags="m" />\n\t</map>\n</keymap>' % config.plugins.RaedQuickSignal.keyname.value)
                        keyfile.close()
                        if not self.currenabled_value==config.plugins.RaedQuickSignal.enabled.value or not self.currkeyname_value==config.plugins.RaedQuickSignal.keyname.value :
                       
                           self.session.openWithCallback(self.restart, MessageBox, _("Settings changed,restart enigma2 now?"))
                        else:
                                self.close(True)
                else:
                        self.close(False)
##############################################################################
def sessionstart(reason,session=None, **kwargs):
        if reason == 0:
                pSignal.gotSession(session)
##############################################################################
def main(session, **kwargs):
        session.open(RaedQuickSignal_setup)
##############################################################################
def Plugins(**kwargs):
        result = [
                PluginDescriptor(
                        where = [PluginDescriptor.WHERE_SESSIONSTART],
                        fnc = sessionstart
                ),
                PluginDescriptor(
                        name=_("RaedQuickSignal Setup"),
                        description = _("RAED's RaedQuickSignal setup"),
                        where = PluginDescriptor.WHERE_PLUGINMENU,
                        icon = 'RaedQuickSignal.png',
                        fnc = main
                ),
        ]
        return result
