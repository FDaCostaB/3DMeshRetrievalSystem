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
from Settings import readSettings, settings, settingsName

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
        layout.add_widget(Image(source = iPath, allow_stretch=True,height=200))
        layout.add_widget(Label(text=distance,height=10))
        self.widget_list.add_widget(layout)

    def addWidgets(self,results):
        parDir = os.path.join(os.path.realpath('output'), 'screenshot')
        for dir in os.scandir(parDir):
            print(dir.name)
            if dir.name == "query.jpg":
                self.image_input.source = os.path.realpath(dir)
            else:
                n = dir.name.split(".")[0]
                self.addImage(os.path.realpath(dir),results[n])

    def load(self, path, filename):
        queryPath = os.path.join(path, filename[0])
        k = int(self.slider.value)
        with futures.ThreadPoolExecutor(max_workers=5) as executor:
            future = executor.submit(db.query,queryPath,k)
            queryResEucl, queryResEMD = future.result()
            future = executor.submit(db.saveQueryRes,queryPath, queryResEucl)
            imageDist = future.result()
        self.dismiss_popup()
        print(imageDist)
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
    cleanDir()
    Editor().run()