#!/usr/bin/env python
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

        self.var_dmz = tk.StringVar(self)
        self.var_loc = tk.StringVar(self)
        self.var_vc = tk.StringVar(self)

        self.var_dmz.trace('w', self.update_DMZ)
        self.var_loc.trace('w', self.update_VC)
        
        self.om_dmz = tk.OptionMenu(self, self.var_dmz, *self.dict.keys())
        self.om_loc = tk.OptionMenu(self, self.var_loc, '')
        self.om_vc = tk.OptionMenu(self, self.var_vc, '')
        self.om_dmz.configure(width=30)
        self.om_loc.configure(width=30)
        self.om_vc.configure(width=30)
        #self.vcLabel = tk.Label(self, command=self.update_VC)
        b1 = tk.Button(self, text="Submit", width=20, command=self.print_sel)

        self.var_dmz.set('Non-DMZ')
        self.var_loc.set('APDC')

        self.om_dmz.grid()
        self.om_loc.grid()
        self.om_vc.grid()
        b1.grid()
        self.grid()
        
    def update_DMZ(self, *args):
        DVCs = self.dict[self.var_dmz.get()]
        self.var_loc.set(DVCs[0])

        menu = self.om_loc['menu']
        menu.delete(0, 'end')

        for DVC in DVCs:
            menu.add_command(label=DVC, command=lambda dvcenter=DVC: self.var_loc.set(dvcenter))
            
    def update_VC(self, *args):
        VCs = self.vcloc[self.var_loc.get()]
        self.var_vc.set(VCs)
        
        
        menu = self.om_vc['menu']
        menu.delete(0, 'end')
                
        menu.add_command(label=VCs, command=lambda vcenter=VCs: self.var_vc.set(vcenter))

    def print_sel(self):
        m1 = tkMessageBox.showinfo("Hello", var_dmz.get())
        print self.var_dmz.get()
        print self.var_loc.get()
        print self.var_vc.get()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()