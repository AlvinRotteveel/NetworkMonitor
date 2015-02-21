#!/usr/bin/python
import npyscreen
import termcolor


class HomeScreen(npyscreen.Form):
    def change_window(self):
        self.parentApp.NEXT_ACTIVE_FORM = None

    def create(self):
        self.logo = self.add(npyscreen.FixedText, name='name', value='Test')
        self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3,
                                     name='Department', values=['Department 1', 'Department 2', 'Department 3'])
        self.myDate = self.add(npyscreen.TitleDateCombo, name='Date Employed')

class Client(npyscreen.NPSAppManaged):
   def onStart(self):
        self.addForm('MAIN', HomeScreen)
        # Add more forms here....
