from datetime import datetime
import Tkinter as tk
import tkMessageBox
import korea

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Korean Job Checker")
        self.geometry("300x200")

        self.company = self.input("Company Name: ")
        self.check = self.button("Run Check", self.runCheck)

    def input(self, text, hide = False):
        tk.Label(self.master, text = text).pack()
        entry = tk.Entry(self.master, show = "*" if hide else None)
        entry.pack()
        return entry

    def button(self, text, onclick = None):    
        button = tk.Button(self.master, text = text)
        button.pack()
        if onclick:
            button.bind("<Button-1>", onclick)

    def checkMessage(self,msg):
        tkMessageBox.showinfo("Check", msg)

    def runCheck(self, event):
        msg = "Results:\n"
        msg += "\nBlacklist search came back " + ("positive" if korea.isBlacklisted(self.company.get()) else "negative")
        msg += "\nGreenlist search came back " + ("positive" if korea.isGreenlisted(self.company.get()) else "negative")
        msg += "\nClosest blacklist school: " + korea.closestBlacklistSchool(self.company.get())
        msg += "\nClosest greenlist school: " + korea.closestGreenlistSchool(self.company.get())
        self.checkMessage(msg)

def runGUI():
    GUI().mainloop()
