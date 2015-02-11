#!/usr/bin/python

import curses
import npyscreen

import npyscreen


class myEmployeeForm(npyscreen.Form):
    def create(self):
        self.myName = self.add(npyscreen.TitleText, name='Name')


