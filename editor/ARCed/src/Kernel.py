'''
Created on Dec 2, 2010

the extend-able backend to the main program

Classes in this module
-------------------------------------------
Component - holds a registered extension
Function - holds a registered extension (methods and functions)
Event - container for organizing events and calling attached functions
Type - container for organizing extensions that do the same thing
Package - container for organizing and registering groups of extensions
Manager - the main processor of the Kernel
'''
import os
import sys
import time
import traceback
import inspect

import ConfigParser
import re

import wx

#====================================================================================
# * ARC Constants
#====================================================================================

VERSION = "0.0.1"

#====================================================================================
# Global Object Storage
#====================================================================================

class GlobalObjects(object):
    '''
    a storage for global objects where a key is mapped to a list where the first value is a name that represents what created the key and the 
    second value is an object
    '''

    _objects = {"PROJECT":["CORE", None],
               "ProjectOpen":["CORE", False],
               "FileHistory":["CORE", None],
               "CurrentProjectDir":["CORE", ""],
               "Program_Dir":["CORE", os.path.dirname(os.path.abspath(__file__))],
               "Title":["CORE", ""],
               "Mode":["CORE", ""],
               "config":["CORE", None],
               "ARCconfig":["CORE", None],
               "programconfig":["CORE", None],
               "LoadedComponentDefaultsTemplate":["CORE", None],
               "ProjectModes":["CORE", {}],
               "ProjectCreators":["CORE", {}],
               "PanelManager": ["CORE", None],
               }
    
    @staticmethod
    def has_key(key):
        if GlobalObjects._objects.has_key(key):
            return True
        return False

    @staticmethod
    def request_new_key(key, name="PLUGIN", value=None):
        '''
        find out if a key exits if it does it return a tuple of (False, name) where name is an id for what 
        made the key. if it is made by a CORE component the name is "CORE"
        if the key didn't already exist it makes it and store the provided name and value then returns a tuple (True, name)
        '''
        if GlobalObjects._objects.has_key(key):
            return (False, GlobalObjects._objects[key][0])
        else:
            GlobalObjects._objects[key] = [name, value]
            return (True, name)

    @staticmethod
    def get_name(key):
        '''
        gets a name stored with a key key if a key exists other wise returns None
        '''
        if GlobalObjects._objects.has_key(key):
            return GlobalObjects._objects[key][0]
        else:
            return None
        
    @staticmethod
    def get_value(key):
        '''
        gets a value stored with a key if a key exists
        '''
        if GlobalObjects._objects.has_key(key):
            return GlobalObjects._objects[key][1]
        
    @staticmethod
    def set_value(key, value):
        '''
        sets a vlaue stored with a key if a key exists
        '''
        if GlobalObjects._objects.has_key(key):
            GlobalObjects._objects[key][1] = value

    @staticmethod
    def remove_key(key):
        '''
        removes a key if it exists
        '''
        if GlobalObjects._objects.has_key(key):
            del GlobalObjects._objects[key]


#====================================================================================
# Kernel classes
#====================================================================================

class Manager(object):
    '''The main Kernel processor'''

    types = {}
    events = {}
    packages = {}

    @staticmethod
    def register_types(*args):
        '''add passed types to the 'types' dict mapped to their name'''
        for type_obj in args:
            if not Manager.types.has_key(str(type_obj.name)):
                Manager.types[str(type_obj.name)] = type_obj

    @staticmethod
    def register_events(*args):
        '''add passed events to the 'events' dict mapped their their name'''
        for event in args:
            if not Manager.events.has_key(str(event.name)):
                Manager.events[str(event.name)] = event

    @staticmethod
    def raise_event(name, *args, **kwargs):
        '''call the event mapped to 'name' and pass extra arguments'''
        Manager.events[str(name)].call(*args, **kwargs)

    @staticmethod
    def get_type(name, super_name=None):
        '''gets a type object'''
        try:
            if super_name != None:
                return Manager.types[str(super_name)].get_type(str(name))
            else:
                return Manager.types[str(name)]
        except KeyError, AttributeError:
            return Type("None")

    @staticmethod
    def get_event(name):
        try:
            return Manager.events[str(name)]
        except KeyError, AttributeError:
            return Event("None")

    @staticmethod
    def get_component(type_name, supertype=None, name=None, author=None,
                      version=None, package=None):
        '''
        get a component, if no optional parameters are provided (other than 
        supertype) returns the default component, other wises gets the
        component identified by the name, author, version, and package. 
        package  
        returns a Kernel.Component object
        
        @param name: string type name
        @param supertype: string super type name. use if the type is under a 
        super type
        @param name: string name of the component
        @param author: string author
        @param version: string or int or float version of the package
        @param package: can be a Package object or a string name of the package
        '''
        default = (name == None and author == None and version == None and
                       package == None)
        if default:
            return (Manager.get_type(type_name, supertype).get_default_component())
        else:
            return (Manager.get_type(type_name, supertype).get_component(name, author, version))
        
    @staticmethod
    def add_package(package):
        '''
        @param package: a Kernel.Package object 
        @return: returns a 2-Tupel of the package's name and author used as a key to enable the package like so ("name", "author")
        '''
        Manager.packages[(package.name, package.author)] = package
        return (package.name, package.author)
        
    @staticmethod
    def enable_packages(*args):
        '''
        @param args: any number of 2-Tupels containing the  package's name and author as strings like so ("name", "author")
        '''
        for package in args:
            Manager.packages[package].register()
        
    @staticmethod
    def set_default_components_from_config(package):
        pass

class Component(object):
    '''A data class that holds a registered extension'''

    def __init__(self, obj, type_name, super_name=None, name="", author="", version=0,
                 package=None):
        '''
        initializes a Kernel.Component object
        
        @param obj: the extension object
        @param type_name: a string identifing a Type name, used to group the object for retrieval
        @param super_name: a string identifing the SuperType this component is grouped under
        @param name: a string that uniquely identifies the extension, used for retrieving the extension on request
        @param author: a string containing the name of the author of this component
        @param version: a number that is this component version
        @param package: a Package object that is used for grouping of extensions
        '''
        self.object = obj
        self.type = type_name
        self.super = super_name
        self.name = name
        self.author = author
        self.version = version
        self.package = package
        self.dependencies = []

    def add_dependencies(self, *args):
        '''called with a[n] Kernel.Dependency object['s] to be added'''
        self.dependencies.extend(args)

class Dependency(object):
    '''
    A data class that holds data on a dependency of a component or package
    '''
    def __init__(self, type_name=None, name="", author="", version=0):
        self.type = type_name
        self.name = name
        self.author = author
        self.version = version

class Event(object):
    '''A data class used as a container for organizing events as their 
    registered methods and methods'''

    def __init__(self, name=""):
        '''initializes a Kernel.Event object
        
        name - a string that uniquely identifies the event, used for retrieval
        '''
        self.name = name
        self.registered = []

    def register(self, function=None, master=None):
        '''registers a function or method to the event
        
        function - the Function or Method object
        master - for methods the objects that is passed as the self parameter
        '''
        if function != None and callable(function):
            self.registered.append([function, master])
        else: raise TypeError, "'function' must be a call-able object"

    def unregister(self, function=None, master=None):
        '''removes a function from the list of function to be called'''
        if function != None and callable(function):
            self.registered.remove([function, master])

    def call(self, *args, **kwargs):
        '''calls all the registered function passing all the arguments and 
        keyword arguments passed with the 
        call'''
        for function in self.registered:
            if function[1] != None:
                function[0](function[1], *args, **kwargs)
            else:
                function[0](*args, **kwargs)

class SuperType(object):
    '''a data class that is used for grouping types into larger groups, super 
    types can not be used to group super types'''
    def __init__(self, name):
        '''initializes a Kernel.SuperType object
        
        name - a string that uniquely identifies the super type'''
        self.name = name
        self.types = {}

    def add_types(self, *types):
        '''adds a type to the self.types dict mapped to name'''
        for type_obj in types:
            type_obj.super = self.name
            self.types[str(type_obj.name)] = type_obj

    def get_type(self, type_name):
        try:
            return self.types[type_name]
        except KeyError:
            return Type("None")

class Type(object):
    '''a data class that is used for the grouping of extensions that do the 
    same thing'''
    def __init__(self, name):
        '''initializes a Kernel.Type object
        
        name - a string that uniquely identifies the type'''
        self.name = name
        self.super = None
        self.default = None
        self.components = {}

    def add_component(self, component, package=None):
        '''
        adds the component to the type's dict mapped  to a string name 
        constructed from the component's name, suthor, version number, and 
        package name.
        
        @param component: a Component object
        @param package: optional; either a Package object or the string 
        version of the packages name 
        '''
        key = self.get_key(component.name, component.author, component.version, package)
        self.components[key] = component

    def get_key(self, name, author, version, package):
        '''
        creates a key
        
        @param name: string name
        @param author: string author
        @param version: version number converted to string with str()
        @param package: either a string or a Package object
        '''
        pack = ""
        if isinstance(package, Package):
            pack = str(package.name)
        elif package != None:
            pack = str(package)
        return (str(pack), str(name), str(author), str(version))

    def set_default_component(self, name, author, version, package=None):
        '''sets the default component
        
        @param name: string name
        @param author: string author
        @param version: version number converted to string with str()
        @param package: either a string or a Package object
        '''
        key = self.get_key(name, author, version, package)
        try:
            self.default = self.components[key]
        except KeyError:
            self.default = None
            return False
        return True

    def get_default_component(self):
        '''
        gets the default component or the first component added if it has 
        not been set
        '''
        if self.default != None:
            return self.default
        else:
            try:
                return self.components.values()[0]
            except IndexError:
                return Component(None, "None")

    def get_component(self, name, author, version, package=None):
        '''
        get a component given it's name author version and a package name
        
        @param name: string name
        @param author: string author
        @param version: version number converted to string with str()
        @param package: either a string or a Package object
        '''
        key = self.get_key(name, author, version, package)
        return self.components[key]

class Package(object):
    '''A data class intended to hold information regarding a package and all 
    it's components, intended to be subclassed and used to register more than
    one component at once by registering the package'''

    __manager = Manager

    def __init__(self, name, author):
        '''
        initializes a Kernel.Plugin object
        
        @param name: a string that uniquely identifies the package
        '''
        self.name = name
        self.author = author
        self.components = []
        self.types = []
        self.events = []
        self.event_hooks = []
        self.dependencies = []

    def register(self):
        '''
        register both the types and the components contained in the 
        package to the Kernel
        '''
        self.__manager.register_types(*self.types)
        self.__manager.register_events(*self.events)
        for component in self.components:
            Package.__manager.get_type(component.type, component.super).add_component(component, self)
        for event_hook in self.event_hooks:
            event = self.__manager.get_event(event_hook[0])
            if event != None:
                event.register(event_hook[1], event_hook[2])

    def add_types(self, *types):
        '''
        adds a Kernal.Type or Kernal.SuperType object to the types list the 
        type is not registered to the Kernel
        '''
        for type_obj in types:
            if isinstance(type_obj, (Type, SuperType)):
                self.types.append(type_obj)
                
    def add_events(self, *events):
        '''
        adds a Kernel.Event object to the event list
        the event is not registered to the Kernel
        '''
        for event_obj in events:
            if isinstance(event_obj, Event):
                self.events.append(event_obj)

    def add_component(self, component):
        '''
        adds a Kernal.Component object to the components list
        
        adds a Kernal.Component object to the components list after checking 
        to be sure it is indeed a component. the component is NOT registered 
        to the Kernel
        '''
        if isinstance(component, Component):
            self.components.append(component)
            
    def add_event_hook(self, name, function, master=None):
        '''
        set up a function to be registered to an event when the package is registered
        '''
        self.event_hooks.append((name, function, master))

    def add_dependencies(self, *args):
        '''
        called with one or more Kernel.Dependency object's to be added
        '''
        self.dependencies.extend(args)

#====================================================================================
# Configuration classes (loader and data structure)
#====================================================================================

class ConfigTemplate(object):

    def __init__(self):

        self.types = {}

    def add_type(self, type_obj):
        '''
        adds the ConfigType object to the types dict mapped the the type's name
        
        @param type: ConfigType object
        '''
        self.types[type_obj.name] = type_obj

    def remove_type(self, name):
        '''
        removes the type mapped to name
        
        @param name: string name
        '''
        del self.types[name]

    def has_type(self, name):
        '''
        returns if name has been mapped to a type or not
        '''
        return self.types.has_key(name)

    def get_type(self, name):
        '''
        return the type mapped to name
        '''
        return self.types[name]

class ConfigType(object):

    def __init__(self, name=""):

        self.name = name
        self.super = False
        self.default = None

class ConfigSuperType(object):

    def __init__(self, name=""):

        self.name = name
        self.super = True
        self.types = {}

    def add_type(self, type_obj):
        '''
        adds the ConfigType object to the types dict mapped the the type's name
        
        @param type: ConfigType object
        '''
        self.types[type_obj.name] = type_obj

    def remove_type(self, name):
        '''
        removes the type mapped to name
        
        @param name: string name
        '''
        del self.types[name]

    def has_type(self, name):
        '''
        returns if name has been mapped to a type or not
        '''
        return self.types.has_key(name)

    def get_type(self, name):
        '''
        return the type mapped to name
        '''
        return self.types[name]

class ConfigDefault(object):

    def __init__(self, name="", author="", version=0, package=None):
        self.name = name
        self.author = author
        self.version = version
        self.package = package

    def set_default(self, name=None, author=None, version=None, package=None):
        '''
        sets the default, calling with no arguments clears the values, 
        calling with one or more arguments sets those values but leaves the others alone
        '''
        flag = nflag = aflag = vflag = pflag = False
        if name != None:
            flag = nflag = True
        if author != None:
            flag = aflag = True
        if version != None:
            flag = vflag = True
        if package != None:
            flag = pflag = True
        if flag:
            if nflag:
                self.name = name
            if aflag:
                self.author = author
            if vflag:
                self.version = version
            if pflag:
                self.package = package

class ConfigLoader(object):

    @staticmethod
    def load(template):
        '''
        sets the default components using a passed ConfigTamplate
        
        @param template: a ConfigTemplate object to load the defaults from
        '''
        for typename, type_obj in template.types.iteritems():
            if type_obj.super:
                for subtypename, subtype in type_obj.types.iteritems():
                    typeobj = Manager.get_type(subtypename, typename)
                    result = typeobj.set_default_component(subtype.default.name,
                                                           subtype.default.author,
                                                           subtype.default.version,
                                                           subtype.default.package)
            else:
                typeobj = Manager.get_type(typename)
                result = typeobj.set_default_component(type_obj.default.name,
                                                       type_obj.default.author,
                                                       type_obj.default.version,
                                                       type_obj.default.package)

    @staticmethod
    def build_from_file(filename, template=None):
        '''
        builds a ConfigTemplate from a configuration file and returns the 
        template
        
        can build from an existing template
        
        @param filename: the path to the configuration file
        @param template: 
        @return: ConfigTemplate
        '''

        if template == None:
            template = ConfigTemplate()
        config = ConfigParser.ConfigParser()
        config.read(filename)
        for section in config.sections():
            #see if the section is in the supertype::subtupe pattern
            match = re.search("(.+)::(.+)", str(section))
            if match:
                #yep supertype::subtype pattern
                supertype = match.group(1)
                type_name = match.group(2)
                if template.has_type(supertype):
                    supertypeobj = template.get_type(supertype)
                else:
                    supertypeobj = ConfigSuperType(supertype)
                    template.add_type(supertypeobj)
                if supertypeobj.has_type(type_name):
                    typeobj = supertypeobj.get_type(type_name)
                else:
                    typeobj = ConfigType(type_name)
                    supertypeobj.add_type(typeobj)
            else:
                #nope just a normal type name
                type_name = section
                if template.has_type(type_name):
                    typeobj = template.get_type(type_name)
                else:
                    typeobj = ConfigType(type_name)
                    template.add_type(typeobj)
            #now that everything is linked properly be can fill in the default
            #config for this type
            default = ConfigDefault()
            for item, value in config.items(section):
                if item == "name" or item == "Name" or item == "NAME":
                    if value == "None":
                        default.name = None
                    else:
                        default.name = value
                if item == "author" or item == "Author" or item == "AUTHOR":
                    if value == "None":
                        default.name = None
                    else:
                        default.author = value
                if item == "version" or item == "Version" or item == "VERSION":
                    if value == "None":
                        default.name = None
                    else:
                        default.version = float(value)
                if item == "package" or item == "Package" or item == "PACKAGE":
                    if value == "None":
                        default.name = None
                    else:
                        default.package = value
            typeobj.default = default
        #ok we've built the template lets return it
        return template

    @staticmethod
    def load_from_file(filename, template=None):
        '''
        builds a template from a configuration file, loads the defaults from it
        and returns the template.
        
        can build from an existing template
        
        @param filename: the path to the configuration file
        @return: ConfigTemplate
        '''

        template = ConfigLoader.build_from_file(filename, template)
        ConfigLoader.load(template)
        return template

    @staticmethod
    def save_to_file(template, filename):
        '''
        saves a template to a configuration file
        
        @param template: the ConfigTemplate object to save
        @param filename: the path to the configuration file
        '''
        config = ConfigParser.ConfigParser()
        for typename, type_obj in template.types:
            if type_obj.super:
                for subtypename, subtype in type_obj.types:
                    section = str(typename) + "::" + str(subtypename)
                    config.add_section(section)
                    config.set(section, "Name", str(subtype.default.name))
                    config.set(section, "Author", str(subtype.default.author))
                    config.set(section, "Version", str(subtype.default.version))
                    config.set(section, "Package", str(subtype.default.package))
            else:
                section = str(typename)
                config.add_section(section)
                config.set(section, "Name", str(type_obj.default.name))
                config.set(section, "Author", str(type_obj.default.author))
                config.set(section, "Version", str(type_obj.default.version))
                config.set(section, "Package", str(type_obj.default.package))
        f = open(filename, "wb")
        config.write(file)
        f.close()

#====================================================================================
# * Protect (a class to wrap wround functions like event handelers to ceatch errors)
#====================================================================================

class Protect(object):
     def __init__(self, fn):
         self.fn = fn

     def __call__(self, *args, **kwargs):
        try:
            self.fn(*args, **kwargs)
        except Exception, excp:
            if inspect.ismethod(self.fn):
                messege = "Exception in protected method  %s bound to class %s" % (self.fn.__name__, self.fn.im_self.__class__.__name__ )
            elif inspect.isfunction(self.fn):
                message = "Exception in protected function %s" % self.fn.__name__
            else:
                message = "Exception in protected call"
            Log(message="message", inform=True, error=True)

#====================================================================================
# * Kernel Functions
#====================================================================================
def GetDataFolder():
    if sys.platform.startswith('win32'):
        path = os.path.expandvars(os.path.join("%ALLUSERSPROFILE%", "ARCed"))
    elif sys.platform.startswith('lynix'):
        path = os.path.join("", "etc", "ARCed")
    elif sys.platform.startswith('darwin'):
        path = os.path.join("", "Library", "Preferences", "ARCed")
    else:
        path = os.path.join("", "ARCed")
    if not os.path.exists(path) or not os.path.isdir(path):
        os.makedirs(path)
    return path

def GetConfigFolder():
    path = GetDataFolder()
    path = os.path.join(path, "Config")
    if not os.path.exists(path) or not os.path.isdir(path):
        os.makedirs(path)
    return path

def GetLogFolder():
    path = GetDataFolder()
    path = os.path.join(path, "Logs")
    if not os.path.exists(path) or not os.path.isdir(path):
        os.makedirs(path)
    return path

def GetPluginFolder():
    path = GetDataFolder()
    path = os.path.join(path, "Plugins")
    if not os.path.exists(path) or not os.path.isdir(path):
        os.makedirs(path)
    return path

def Log(message=None, prefix="[Kernel]", inform=False, error=False):
    '''
    time stamps a message and writes it to a log file, it can also attach a trace back of the latest error. 
    always adds a new line at the end of the message
    '''
    if message == None:
        error = True
        message = ""
    logdir = GetLogFolder()
    f = open(os.path.join(logdir, "ARCed.log"), "ab")
    time_str = time.strftime("%a %d %b %Y %H:%M:%S [%Z] ")
    if error:
        message += " [Error] " + traceback.format_exc()
    f.write(time_str + prefix + " " + message + "\n")
    f.close
    if inform:
        Inform(prefix, message, error)

def Inform(title, message, error=False):
    if wx.GetApp() is not None:
        if error:
            style = wx.OK|wx.STAY_ON_TOP|wx.ICON_INFORMATION
        else:
            style = wx.OK|wx.STAY_ON_TOP|wx.ICON_ERROR
        dlg = wx.MessageDialog(None, message, caption=title, style=style)
        dlg.ShowModal()


#=======================================================================
# NOTE: the below is for testing purposes only
#=======================================================================

if __name__ == '__main__':

    test_type = Type("TEST")
    test_type2 = Type("TEST2")
    test_type3 = Type("TEST3")

    Manager.register_types(test_type)
    Manager.register_types(test_type2, test_type3)

    class TestPackage(Package):
        def __init__(self, manager):
            super(TestPackage, self).__init__("TESTP")
            self.add_component(Component(TestExtension, "TEST", "TESTE", "ME",
                                         1.0, self))
            self.register()


    class TestExtension(object):
        def __init__(self, name):
            self.name = name

        def say_name(self):
            print self.name

    package1 = TestPackage(Manager)

    component = Manager.get_component("TEST")
    print component.author
    print component.name
    print component.type
    print component.version
    initcomponent = component.object("bob")
    initcomponent.say_name()



