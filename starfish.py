import sublime, sublime_plugin
import json
import httplib
import os

class starfishCommand(sublime_plugin.TextCommand):
	showData = []

	def run(self, edit):
		self.showData = []
		filename = self.view.file_name()
		if filename is None:
			return
		jsindex = filename.index("/js/")
		filenamelen = len(filename)
		jspath = filename[jsindex:filenamelen]
		starfashapi = "/api1/geturlapp?file=" + jspath

		conn = httplib.HTTPConnection("starfish.alif2e.com")
		conn.request("GET", starfashapi)
		r1 = conn.getresponse()
		data1 = r1.read()
		conn.close()

		jsonData = json.loads(data1)
		jsonDataValue = jsonData["value"];
		jsonDataValueList = jsonDataValue[jspath];
		for item in jsonDataValueList:
			self.showData.append(item["url"])

		window = sublime.active_window()
		window.show_quick_panel(self.showData,self.panelcallback)

	def panelcallback(self, picked):
		if picked == -1:
			return
		item = self.showData[picked]
		os.system("open " + item)