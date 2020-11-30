import multiprocessing
if __name__ == '__main__':
    multiprocessing.freeze_support()
    
import threading

from ProcessTest import Proc

from Globals import globalVars
from kivy.config import Config 
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '650')


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        globalVars.init()
        self.cols = 3
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        but = Button(text="OK")
        but.bind(on_press=self.buttonThr)
        self.add_widget(but)
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=""))

    def buttonThr(self, instance):
        thr = threading.Thread(target=self.buttonProcess)
        thr.start()

    def buttonProcess(self):
        dataIn = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        proces = Proc(dataIn, results)
        proces.daemon = True
        print("main - startujeme process")
        proces.start()

        for i in range(3):
            dataIn.put(1)
            result = results.get() 
            print("main result " + str(result))

        dataIn.put(0)

    def graphProcess(slef):
        dataIn = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        gen = GenProcess(dataIn, results)
        gen.daemon = True
        gen.start()

        dataIn.put([100, 0.1, 0.1, 20, 10, 'ahoj.txt', 'ahoj.txt'])
        result = results.get()

        for i in range(10):
            dataIn.put(1)
            result = results.get()           
            print(str(result[0]))
            print(str(result[1]))
            print(str(result[2]))

        dataIn.put(0)


class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    myapp = MyApp()
    myapp.run()
    