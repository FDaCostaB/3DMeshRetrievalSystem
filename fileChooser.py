from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
import DBData as db
from functools import partial
from concurrent import futures
from Settings import readSettings, setDistance
import time

import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    layouts = []

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def addImage(self, iPath, distance):
        layout = GridLayout(cols=1)
        newImg = Image(source = iPath, allow_stretch=True,height=200)
        newImg.reload()
        layout.add_widget(newImg)
        layout.add_widget(Label(text=distance,height=20))
        self.widget_list.add_widget(layout)

    def addWidgets(self,results):
        parDir = os.path.join(os.path.realpath('output'), 'screenshot')
        self.widget_list.clear_widgets()
        for dir in os.scandir(parDir):
            if dir.name == "query.jpg":
                self.image_input.source = os.path.realpath(dir)
                self.image_input.reload()
            else:
                n = dir.name.split(".")[0]
                self.addImage(os.path.realpath(dir),results[n])

    def load(self, path, filename):
        queryPath = os.path.join(path, filename[0])
        k = int(self.slider.value)
        distFunc = ""
        if self.euclidean.active:
            distFunc = "euclidean"
        if self.emd.active:
            distFunc = "emd"
        if self.ann.active:
            distFunc = "ann"
        with futures.ProcessPoolExecutor(max_workers=5) as executor:
            cleanDir()
            future = executor.submit(db.query, queryPath, distFunc , tree, rowLabel,k)
            queryRes = future.result()
            future = executor.submit(db.saveQueryRes,queryPath, queryRes)
            imageDist = future.result()
        time.sleep(2)
        self.dismiss_popup()
        self.addWidgets(imageDist)


    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()


class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

def cleanDir():
        parDir = os.path.join(os.path.realpath('output'), 'screenshot')
        for dir in os.scandir(parDir):
            os.remove(dir)
if __name__ == '__main__':
    readSettings()
    tree, rowLabel = db.buildTree()
    cleanDir()
    Editor().run()