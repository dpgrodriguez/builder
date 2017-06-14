#!/usr/bin/python
import sys
if sys.version_info[0] >= 3:
    import tkinter as tk
else:
    import Tkinter as tk


class App(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.dict = {'Non-DMZ': ['APDC', 'EMEA Powergate', 'EMEA Romford', 'Gonfreville', 'Houston', 'San Ramon', 'San Ramon Lab', 'Singapore'],
                     'DMZ': ['DMZ APDC', 'DMZ EMEA Powergate', 'DMZ Houston', 'DMZ San Antonio', 'DMZ Singapore']}
        self.vcloc = {'Singapore': 'vc-sgdc1.chevron.com', 'APDC' : 'vc-ghp-f07058.chevron.com', 'EMEA Powergate' : 'vc-lonpwg.chevron.com'}
        
        self.variable_a = tk.StringVar(self)
        self.variable_b = tk.StringVar(self)
        self.variable_c = tk.StringVar(self)

        self.variable_a.trace('w', self.update_DMZ)
        self.variable_b.trace('w', self.update_VC)
        
        self.optionmenu_a = tk.OptionMenu(self, self.variable_a, *self.dict.keys())
        self.optionmenu_b = tk.OptionMenu(self, self.variable_b, '')
        self.optionmenu_c = tk.OptionMenu(self, self.variable_c, '')
        #self.vcLabel = tk.Label(self, command=self.update_VC)
       
        self.variable_a.set('Non-DMZ')
        self.variable_b.set('APDC')

        self.optionmenu_a.pack()
        self.optionmenu_b.pack()
        self.optionmenu_c.pack()
       
        #self.vcLabel.pack()
        self.pack()
        
    def update_DMZ(self, *args):
        DVCs = self.dict[self.variable_a.get()]
        self.variable_b.set(DVCs[0])

        menu = self.optionmenu_b['menu']
        menu.delete(0, 'end')

        for DVC in DVCs:
            menu.add_command(label=DVC, command=lambda dvcenter=DVC: self.variable_b.set(dvcenter))
            
    def update_VC(self, *args):
        VCs = self.vcloc[self.variable_b.get()]
        self.variable_c.set(VCs)
        
        
        menu = self.optionmenu_c['menu']
        menu.delete(0, 'end')
                
        menu.add_command(label=VCs, command=lambda vcenter=VCs: self.variable_c.set(vcenter))
                
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()