#!/usr/bin/python

import npyscreen
from views import home

class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', home.myEmployeeForm, name='')

if __name__ == '__main__':
    NMServer = MyApplication()
    NMServer.run()