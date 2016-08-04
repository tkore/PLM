import sublime
import sublime_plugin
import threading
import os
import urllib

class plmInitCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.settings = sublime.load_settings('plm.sublime-settings')
        self.sortLibraries()
        self.openLibrariesPanel()
        self.index = 0

    def sortLibraries(self):
        self.libraries = self.settings.get('libraries')
        self.tempLibraries = []
        tempLibrary = []

        for library in self.libraries:
            tempLibrary = []
            tempLibrary.append(library["name"])
            tempLibrary.append('Version: ' + library["version"])
            tempLibrary.append('Source: ' + library["source"])
            self.tempLibraries.append(tempLibrary)

        return self

    def getCWD(self):
        return sublime.active_window().extract_variables()['file_path']

    def openLibrariesPanel(self):
        sublime.active_window().show_quick_panel(self.tempLibraries, self.selectLibrary)

        return self

    def selectLibrary(self, index):
        self.index = index
        if (self.index < 0):
            return

        self.checkDirectory().initiateThread()

    def checkDirectory(self):
        if not os.path.isdir(self.getCWD() + '/' + self.settings.get('includes_dirname')):
            os.makedirs(self.getCWD() + '/' + self.settings.get('includes_dirname'))

        return self

    def initiateThread(self):
        self.thread = plmThread(self.libraries, self.index, self.getCWD(), self.view)
        self.thread.start()

class plmThread(threading.Thread):

    def __init__(self, libraries, index, cwd, view):
        self.settings = sublime.load_settings('plm.sublime-settings')
        self.libraries = libraries
        self.index = index
        self.view = view
        self.cwd = cwd
        threading.Thread.__init__(self)

    def run(self):
        self.downloadLibrary()

    def downloadLibrary(self):
        tagLocation = self.settings.get('includes_dirname') + '/' + self.libraries[self.index]['source'].split('/').pop()
        urllib.request.URLopener().retrieve(self.libraries[self.index]['source'], self.cwd + '/' + tagLocation)
        self.view.run_command('plm_append_tags', {"tag": tagLocation})

        if not 'attachments' in self.libraries[self.index]:
            return self

        self.handleAttachments()


    def handleAttachments(self):
        tagLocation = ''

        for attachment in self.libraries[self.index]['attachments']:
            urllib.request.URLopener().retrieve(attachment, self.cwd + '/' + self.settings.get('includes_dirname') + '/' + attachment.split('/').pop())
            tagLocation = self.settings.get('includes_dirname') + '/' + attachment.split('/').pop()
            self.view.run_command('plm_append_tags', {"tag": tagLocation})


        return self

class plmAppendTagsCommand(sublime_plugin.TextCommand):

    def run(self, edit, tag):
        self.tagContainer = self.view.find("(<[/]head>)", 0)
        self.endOfContainer = int(str(self.tagContainer).split(',')[0].replace('(', ''))
        self.tag = tag
        self.edit = edit
        self.tagPattern = ''

        self.configureTag().addTag()

    def configureTag(self):
        if '.js' in self.tag:
            self.tagPattern = '<script type="text/javascript" src="' + self.tag + '"></script>'
        elif '.css' in self.tag:
            self.tagPattern = '<link rel="stylesheet" href="' + self.tag + '" />'

        return self

    def addTag(self):
        self.view.insert(self.edit, self.endOfContainer, self.tagPattern + '\n')
        self.reindent()

        return self

    def reindent(self):
        self.view.run_command('reindent', {'single_line': False})

        return self;
