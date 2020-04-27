#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
#Coders by Nikolasi
#EDit BY RAED To QuickSignal 2018
from Components.Pixmap import Pixmap 
from Renderer import Renderer
from enigma import getDesktop, iServiceInformation 
from string import upper 
from enigma import ePixmap 
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN, resolveFilename, SCOPE_PLUGINS, SCOPE_LIBDIR
from Components.config import config
from Components.Element import cached
import os
from Components.Converter.Poll import Poll

class RaedQuickSignalPicEmuF(Renderer, Poll):
        __module__ = __name__
        searchPaths = ('/usr/share/enigma2/%s/', '/media/sde1/%s/', '/media/cf/%s/', '/media/sdd1/%s/', '/media/usb/%s/', '/media/ba/%s/', '/mnt/ba/%s/', '/media/sda/%s/', '/etc/%s/')
	searchPaths.append(resolveFilename(SCOPE_PLUGINS, 'Extensions/%s/'))
        
        def __init__(self):
                Poll.__init__(self)
                Renderer.__init__(self)
                if getDesktop(0).size().width() == 1920:
                      self.path = 'emu2'
                else:
                      self.path = 'emu'
                self.nameCache = {}
                self.pngname = ''
                self.picon_default = "picon_default.png"
                
        def applySkin(self, desktop, parent):
                attribs = []
                for (attrib, value,) in self.skinAttributes:
                        if (attrib == 'path'):
                                self.path = value
                        elif (attrib == 'picon_default'):
                                self.picon_default = value
                        else:
                                attribs.append((attrib, value))
                                
                self.skinAttributes = attribs
                return Renderer.applySkin(self, desktop, parent)
                
        GUI_WIDGET = ePixmap

        @cached
        def getText(self):
                service = self.source.service
                info = service and service.info()
                if not service:
                        return None
                camd = ""
                serlist = None
                camdlist = None
                nameemu = []
                nameser = []
                if not info:
                        return ""
                # Alternative SoftCam Manager 
                if fileExists(resolveFilename(SCOPE_PLUGINS, "Extensions/AlternativeSoftCamManager/plugin.pyo")): 
                        if config.plugins.AltSoftcam.actcam.value != "none": 
                                return config.plugins.AltSoftcam.actcam.value 
                        else: 
                                return None
                #  GlassSysUtil 
                elif fileExists("/tmp/ucm_cam.info"):
                        return open("/tmp/ucm_cam.info").read()
                # egami
                elif os.path.isfile("/tmp/egami.inf"):
                        for line in open("/tmp/egami.inf"):
                                if 'Current emulator:' in line:
                                        return line.split(':')[-1].lstrip().strip('\n')
                # Pli
                elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
                        try:
                                for line in open("/etc/init.d/softcam"):
                                        if "echo" in line:
                                                nameemu.append(line)
                                camdlist = "%s" % nameemu[1].split('"')[1]
                        except:
                                pass
                        try:
                                for line in open("/etc/init.d/cardserver"):
                                        if "echo" in line:
                                                nameser.append(line)
                                serlist = "%s" % nameser[1].split('"')[1]
                        except:
                                pass
                        if serlist is not None and camdlist is not None:
                                return ("%s %s" % (serlist, camdlist))
                        elif camdlist is not None:
                                return "%s" % camdlist
                        elif serlist is not None:
                                return "%s" % serlist
                        return ""
                # TS-Panel & Ts images
                elif fileExists("/etc/startcam.sh"):
                        try:
                                for line in open("/etc/startcam.sh"):
                                        if "script" in line:
                                                return "%s" % line.split("/")[-1].split()[0][:-3]
                        except:
                                camdlist = None
                # domica 8
                elif fileExists("/etc/init.d/cam"):
                        if config.plugins.emuman.cam.value: 
                                return config.plugins.emuman.cam.value
                #PKT
                elif fileExists(resolveFilename(SCOPE_PLUGINS, "Extensions/PKT/plugin.pyo")):
                        if config.plugins.emuman.cam.value: 
                                return config.plugins.emuman.cam.value
                #HDMU
                elif fileExists("/etc/.emustart") and fileExists("/etc/image-version"):
                        try:
                                for line in open("/etc/.emustart"):
                                        return line.split()[0].split('/')[-1]
                        except:
                                return None
                # Domica        
                elif fileExists("/etc/active_emu.list"):
                        try:
                                camdlist = open("/etc/active_emu.list", "r")
                        except:
                                return None
                # Egami 
                elif fileExists("/tmp/egami.inf","r"):
                        for line in open("/tmp/egami.inf"):
                                item = line.split(":",1)
                                if item[0] == "Current emulator":
                                        return item[1].strip()
                
                # OoZooN
                elif fileExists("/tmp/cam.info"):
                        try:
                                camdlist = open("/tmp/cam.info", "r")
                        except:
                                return None
                # Merlin 2 & 3
                elif fileExists("/etc/clist.list"):
                        try:
                                camdlist = open("/etc/clist.list", "r")
                        except:
                                return None
                # ItalySat
                elif fileExists("/etc/CurrentItalyCamName"):
                        try:
                                camdlist = open("/etc/CurrentItalyCamName", "r")
                        except:
                                return None
                # BlackHole OE1.6
                elif fileExists("/etc/CurrentDelCamName"):
                        try:
                                camdlist = open("/etc/CurrentDelCamName", "r")
                        except:
                                return None
                # DE-OpenBlackHole      
                elif fileExists("/etc/BhFpConf"):
                        try:
                                camdlist = open("/etc/BhCamConf", "r")
                        except:
                                return None
                #Newnigma2 OE2.0
                elif fileExists(resolveFilename(SCOPE_LIBDIR, "enigma2/python/Plugins/newnigma2/eCamdCtrl/eCamdctrl.pyo")):
                        try:
                          from Plugins.newnigma2.eCamdCtrl.eCamdctrl import runningcamd
                          if config.plugins.camdname.skin.value: 
                                return runningcamd.getCamdCurrent()
                        except: 
                                return None
                #Newnigma2 OE2.5
                elif fileExists(resolveFilename(SCOPE_LIBDIR, "enigma2/python/Plugins/newnigma2/camdctrl/camdctrl.pyo")):
                        if config.plugins.camdname.skin.value:
                            return config.usage.emu_name.value
                        return None
                # GP3
                elif fileExists(resolveFilename(SCOPE_LIBDIR, "enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so")):
                        try:
                                from Plugins.Bp.geminimain.plugin import GETCAMDLIST
                                from Plugins.Bp.geminimain.lib import libgeminimain
                                camdl = libgeminimain.getPyList(GETCAMDLIST)
                                cam = None
                                for x in camdl:
                                        if x[1] == 1:
                                                cam = x[2] 
                                return cam
                        except:
                                return None
                # GP4
                elif fileExists(resolveFilename(SCOPE_LIBDIR, "enigma2/python/Plugins/GP4/geminicamswitch/gscamtools.so")):
                                from Plugins.GP4.geminicamswitch.gscamtools import readjsons
                                if config.gcammanager.currentbinary.value: 
                                        return config.gcammanager.currentbinary.value
                                return None
                # Dream Elite 
                elif fileExists(resolveFilename(SCOPE_LIBDIR, "enigma2/python/DE/DEPanel.so")):
                        try:
                                from DE.DELibrary import Tool
                                t = Tool()
                                emuname = t.readEmuName(t.readEmuActive()).strip()
                                emuactive = emuname != "None" and emuname or t.readEmuName(t.readCrdsrvActive()).strip()
                                return emuactive
                        except:
                                return None
                # AAF & ATV & VTI & droid & esi & plus & PURE2
                elif fileExists("/etc/image-version") and not fileExists("/etc/.emustart"):
                        emu = ""
                        server = ""
                        for line in open("/etc/image-version"):
                                l = line.lower()
                                ## Should write name be small letters
                                if "=aff" in l or "=openatv" in l or "=opendroid" in l or "=openesi" in l or "=openplus" in l or "=pure2" in l: 
                                        if config.softcam.actCam.value: 
                                                emu = config.softcam.actCam.value
                                        if config.softcam.actCam2.value: 
                                                server = config.softcam.actCam2.value
                                                if config.softcam.actCam2.value == "no CAM 2 active":
                                                        server = ""
                                elif "=vuplus" in line:
                                        if fileExists("/tmp/.emu.info"):
                                                for line in open("/tmp/.emu.info"):
                                                        emu = line.strip('\n')
                                # BlackHole     
                                elif "version=" in line and fileExists("/etc/CurrentBhCamName"):
                                        emu = open("/etc/CurrentBhCamName").read()
                        return "%s %s" % (emu, server)
                else:
                        return None
                        
                if serlist is not None:
                        try:
                                cardserver = ""
                                for current in serlist.readlines():
                                        cardserver = current
                                serlist.close()
                        except:
                                pass
                else:
                        cardserver = " "

                if camdlist is not None:
                        try:
                                emu = ""
                                for current in camdlist.readlines():
                                        emu = current
                                camdlist.close()
                        except:
                                pass
                else:
                        emu = " "
                        
                return "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])
                
        text = property(getText)

        def changed(self, what):
                self.poll_interval = 50
	        self.poll_enabled = True
                if self.instance:
                        pngname = ''
                        if (what[0] != self.CHANGED_CLEAR):
                                sname = ""
                                service = self.source.service
                                if service:
                                        info = (service and service.info())

                                        if info:
                                            caids = info.getInfoObject(iServiceInformation.sCAIDs)
                                            if fileExists("/tmp/ecm.info"):
                                              try:
                                                 value = self.getText()
                                                 value = value.lower()#change value to small letters
                                                 if value is None:
                                                        print("no emu installed")
                                                        sname=''
                                                 else:
                                                        ## Should write name be small letters
                                                        if ("ncam" in value):
                                                                sname = "ncam"
                                                        elif ("oscam" in value):
                                                                sname = "oscam"
                                                        elif ("mgcamd" in value):
                                                                sname = "Mgcamd"
                                                        elif ("wicard" in value or "wicardd" in value):
                                                                sname = "Wicardd"
                                                        elif ("gbox" in value):
                                                                sname = "Gbox"
                                                        elif ("camd3" in value):
                                                                sname = "Camd3"
                                                        elif fileExists("/tmp/ecm.info"):
                                                             try:
                                                                f = open("/tmp/ecm.info", "r")
                                                                content = f.read()
                                                                f.close()
                                                             except:
                                                                content = ""
                                                             contentInfo = content.split("\n")
                                                             for line in contentInfo:
                                                                     if ("address" in line):
                                                                             sname = "CCcam"
                                              except:
                                                print("")

                                            if caids:
                                                   if (len(caids) > 0):
                                                       for caid in caids:
                                                         caid = self.int2hex(caid)
                                                         if (len(caid) == 3):
                                                             caid = ("0%s" % caid)
                                                         caid = caid[:2]
                                                         caid = caid.upper()
                                                         if (caid != "") and (sname == ""):
                                                                 sname = "Unknown"

                                pngname = self.nameCache.get(sname, '')
                                if (pngname == ''):
                                        pngname = self.findPicon(sname)
                                        if (pngname != ''):
                                                self.nameCache[sname] = pngname

                        if (pngname == ''):
                                pngname = self.nameCache.get('Fta', '')
                                if (pngname == ''):
                                        pngname = self.findPicon('Fta')
                                        if (pngname == ''):
                                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                            if fileExists(tmp):
                                                    pngname = tmp
                                            self.nameCache['default'] = pngname

                        if (self.pngname != pngname):
                                self.pngname = pngname

                                self.instance.setPixmapFromFile(self.pngname)

        def int2hex(self, int):
            return ("%x" % int)
               
        def findPicon(self, serviceName):
 
                for path in self.searchPaths:
                        pngname = (((path % self.path) + serviceName) + '.png')
                        if fileExists(pngname):
                                return pngname
                return ''
