#!/usr/bin/env python
import sys
if sys.version_info[0] >= 3:
    import tkinter as tk
else:
    import Tkinter as tk
    import tkMessageBox
    import atexit
    import requests
    import re
    from tools import cli
    from pyVmomi import vim
    from pyVim.connect import SmartConnect, Disconnect
   

class App(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.dict_dmz = {'Non-DMZ': ['APDC', 'EMEA Powergate', 'EMEA Romford', 'Gonfreville', 'Houston', 'Houston Lab',
                        'San Ramon', 'San Ramon Lab', 'Singapore'],
                        'DMZ': ['DMZ APDC', 'DMZ EMEA Powergate', 'DMZ Houston', 'DMZ San Antonio', 'DMZ Singapore']}
        self.dict_loc = {'Singapore': 'vc-sgdc1.chevron.com', 'APDC' : 'vc-ghp-f07058.chevron.com', 'EMEA Powergate' : 'vc-lonpwg.chevron.com',
                        'Houston Lab': 'vclab-boc.chevron.com'}
        self.dict_env = {'Production', 'Non-Production'}
        self.dict_inv = {'Singapore': 'SGDC1 AHS Cluster/Applications/Linux', 'APDC': 'Virtual Machines/Linux',
                        'Houston Lab': 'Unix'}
        self.dict_host = {'Production-APDC': 'F07058-Prod-GHP-Linux', 'Non-Production-APDC': 'F07058-NonProd-GHP-Linux',
                        'Non-Production-Houston Lab': 'Cluster 1'}
        
        #Initializa Variables to save parameters
        self.var_dmz = tk.StringVar(self)
        self.var_loc = tk.StringVar(self)
        self.var_vc = tk.StringVar(self)
        self.var_env = tk.StringVar(self)
        self.var_inv = tk.StringVar(self)
        self.var_host = tk.StringVar(self)
        self.var_dstore = tk.StringVar(self)

        #These trace changes to dropdowns
        self.var_dmz.trace('w', self.update_DMZ)
        self.var_loc.trace('w', self.update_VC)
        self.var_loc.trace('w', self.update_INV)
        self.var_env.trace('w', self.update_HOST)
        #self.var_host.trace('w', self.update_DSTORE)
            
        #These instantiate the dropdowns and contents
        self.om_dmz = tk.OptionMenu(self, self.var_dmz, *self.dict_dmz.keys())
        self.om_loc = tk.OptionMenu(self, self.var_loc, '')
        self.om_vc = tk.OptionMenu(self, self.var_vc, '')
        self.om_env = tk.OptionMenu(self, self.var_env, *self.dict_env)
        self.om_inv = tk.OptionMenu(self, self.var_inv, '')
        self.om_host = tk.OptionMenu(self, self.var_host, '')
        self.om_dstore = tk.OptionMenu(self, self.var_dstore, '')
        
        #These set initial values to vars
        self.var_dmz.set('Non-DMZ')
        self.var_loc.set('APDC')
        
        #These just set the width of dropdowns
        self.om_dmz.configure(width=50)
        self.om_loc.configure(width=50)
        self.om_vc.configure(width=50)
        self.om_env.configure(width=50)
        self.om_inv.configure(width=50)
        self.om_host.configure(width=50)
        self.om_dstore.configure(width=100)
        
        #self.vcLabel = tk.Label(self, command=self.update_VC)
        b1 = tk.Button(self, text="Submit", width=20, command=self.print_sel)
        b2 = tk.Button(self, text="Get DataStores", width=20, command=self.get_ds)
        
        #These instantiate labels       
        self.user_label = tk.Label(self, text="Enter !bang account: CT\\", justify="right", padx=10)
        self.pass_label = tk.Label(self, text="Enter password: ", padx=10)
        self.om_dmz_label = tk.Label(self, text="Select if non-DMZ or DMZ: ", padx=10, justify="left")
        self.om_loc_label = tk.Label(self, text="Select Location: ", padx=10, justify="left")
        self.om_vc_label = tk.Label(self, text="vCenter to deploy the VM on: ", padx=10, justify="left")
        self.om_env_label = tk.Label(self, text="Select server environment: ", padx=10, justify="left")
        self.om_inv_label = tk.Label(self, text="Inventory location to deploy VM on: ", padx=10, justify="right")
        self.om_host_label = tk.Label(self, text="Inventory location to deploy VM on: ", padx=10, justify="right")
        self.om_dstore_label = tk.Label(self, text="Datastore to deploy VM on: ", padx=10, justify="right")

        #These instantiate and Entry textboxes
        self.user_entry = tk.Entry(self)
        self.pass_entry = tk.Entry(self, show="*")
        self.user_entry.grid(row=1, column=1)
        self.pass_entry.grid(row=2, column=1)
        
        #GRID those labels
        self.user_label.grid(row=1, column=0)
        self.pass_label.grid(row=2, column=0)
        self.om_dmz_label.grid(row=4, column=0)
        self.om_loc_label.grid(row=5, column=0)
        self.om_vc_label.grid(row=6, column=0)
        self.om_inv_label.grid(row=7, column=0)
        self.om_env_label.grid(row=8, column=0)        
        self.om_host_label.grid(row=9, column=0)    
        self.om_dstore_label.grid(row=10, column=0)    
        
        #GRID those dropdowns
        self.om_dmz.grid(row=4, column=1)
        self.om_loc.grid(row=5, column=1)
        self.om_vc.grid(row=6, column=1)
        self.om_inv.grid(row=7, column=1)
        self.om_env.grid(row=8, column=1)
        self.om_host.grid(row=9, column=1)
        self.om_dstore.grid(row=10, column=1)
        b1.grid(row=11, column=1, pady=10)
        b2.grid(row=10, column=2, pady=10)
        self.grid(pady=100, padx=100)
        
    
    def update_DMZ(self, *args):
        DVCs = self.dict_dmz[self.var_dmz.get()]
        self.var_loc.set(DVCs[0])

        menu = self.om_loc['menu']
        menu.delete(0, 'end')

        for DVC in DVCs:
            menu.add_command(label=DVC, command=lambda dvcenter=DVC: self.var_loc.set(dvcenter))
            
    def update_VC(self, *args):
        VCs = self.dict_loc[self.var_loc.get()]
        self.var_vc.set(VCs)       
        
        menu = self.om_vc['menu']
        menu.delete(0, 'end')
                
        menu.add_command(label=VCs, command=lambda vcenter=VCs: self.var_vc.set(vcenter))

    def update_INV(self, *args):
        VCINVs = self.dict_inv[self.var_loc.get()]
        self.var_inv.set(VCINVs)
                
        menu = self.om_inv['menu']
        menu.delete(0, 'end')

        menu.add_command(label=VCINVs, command=lambda vcenterinv=VCINVs: self.var_inv.set(vcenterinv))        
    
    def update_HOST(self, *args):
        INVLOC = (self.var_env.get()) + "-" + (self.var_loc.get())
        VCHOST = self.dict_host[INVLOC]
        self.var_host.set(VCHOST)
                
        menu = self.om_host['menu']
        menu.delete(0, 'end')

        menu.add_command(label=VCHOST, command=lambda vcenterinv=VCHOST: self.var_host.set(vcenterinv))

    # def update_DSTORE(self, *args):
        # INVLOC = (self.var_env.get()) + "-" + (self.var_loc.get())
        # VCHOST = self.dict_host[INVLOC]
        # print self.var_vc.get()
        # self.var_host.set(VCHOST)
                
        # menu = self.om_host['menu']
        # menu.delete(0, 'end')

        # menu.add_command(label=VCHOST, command=lambda vcenterinv=VCHOST: self.var_host.set(vcenterinv))          
    
    def print_sel(self):
        m1 = tkMessageBox.askyesno("You've selected these options:", "You've selected " + self.var_dmz.get() + " " + self.var_loc.get() )
        if m1 == True:
            print self.var_dmz.get()
            print self.var_loc.get()
            print self.var_vc.get()
            print self.user_entry.get()
        else:
            print "NOOOOOO"
    
    def sizeof_fmt(self, num):
        """
        Returns the human readable version of a file size

        :param num:
        :return:
        """
        for item in ['bytes', 'KB', 'MB', 'GB']:
            if num < 1024.0:
                return "%3.1f%s" % (num, item)
            num /= 1024.0
        return "%3.1f%s" % (num, 'TB')
    
    def get_obj(self, content, vim_type, Name=None):
        self.obj = None
        #Lists ALL datastores
        
        self.container = self.content.viewManager.CreateContainerView(
            self.content.rootFolder, vim_type, True)
        #print self.container.view
        return self.container.view

    def print_datastore_info(self, ds_obj):
        self.lnx = re.compile('HOU', flags=re.IGNORECASE)
        self.summary = ds_obj.summary
        self.ds_capacity = self.summary.capacity
        self.ds_freespace = self.summary.freeSpace
        self.ds_provisioned = self.ds_capacity - self.ds_freespace
        if self.lnx.search(self.summary.name):
            
            return "Name : {}, Capacity: {}, Provisioned: {}, Free Space: {}".format(self.summary.name, self.sizeof_fmt(self.ds_capacity), self.sizeof_fmt(self.ds_provisioned), self.sizeof_fmt(self.ds_freespace))
        
        
    def get_ds(self, *args):
        #args = get_args()
   
        # connect to vc
        si = SmartConnect(
            host=self.var_vc.get(),
            user="CT\\" + self.user_entry.get(),
            pwd=self.pass_entry.get(),
            #user="ct\!dvzl",
            #pwd="OqkCPm6*)Pp1bH3rQL",
            port=443)
        # disconnect vc
        atexit.register(Disconnect, si)

        self.content = si.RetrieveContent()
        # Get list of ds mo
        
        menu = self.om_dstore['menu']
        menu.delete(0, 'end')
        
        self.ds_obj_list = self.get_obj(self.content, [vim.Datastore])
        
        for ds in self.ds_obj_list:
            ds_ret = self.print_datastore_info(ds)
            if ds_ret != None: 
                menu.add_command(label=ds_ret, command=lambda dstore=ds_ret: self.var_dstore.set(dstore))
            
            
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()