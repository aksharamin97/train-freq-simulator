#THIS PROGRAM IS WRITTEN BY A COLLECTION OF WRITERS.

#Akshar - Incorporated Wheel Size function with sliders/buttons into program. 



import tkinter as tk
from tkinter import messagebox
import time
import pigpio
from threading import Timer
import gc


class Window(tk.Frame):
    def __init__(self,master):
        self.master=master
        self.master.geometry('{}x{}'.format(800,480))
        self.master.maxsize(width=800,height=480)

        self.frame1=tk.Frame(self.master,width=600,height=120,relief=tk.RIDGE,bd=3)
        self.frame2=tk.Frame(self.master,width=600,height=360,bg='white',relief=tk.RIDGE,bd=3)
        self.frame3=tk.Frame(self.master,width=100,height=480,relief=tk.RIDGE,bd=3)
        self.frame4=tk.Frame(self.master,width=100,height=480,relief=tk.RIDGE,bd=3)
        self.frame7=tk.Frame(self.master,width=600,height=480,bg='white',relief=tk.RIDGE,bd=3)  #7 to ensure no conflict
        
        self.canvas_height=360
        self.canvas_width=600
        self.start_x=80
        self.check_count=0

        ####DELAY####
        self.delayTime = 30;
        self.delayTimeMax=60;   #default
        self.delayMaxBool = False;
        self.delayMinBool = False;
        self.delayTimeStr = tk.StringVar();
        self.delayTimeStr.set(str(self.delayTime) + " sec")
        self.killDelay = False;

        self.canvas1=tk.Canvas(self.frame2,width=600,height=360,bg='white')
        self.scroll1=tk.Scrollbar(self.frame2,orient=tk.HORIZONTAL,width=20)
        self.canvas1.config(xscrollcommand=self.scroll1.set)
        self.scroll1.config(command=self.canvas1.xview)
        
        self.frame4.grid(row=0,column=0,rowspan=24,columnspan=5,sticky=tk.N+tk.S+tk.W+tk.E)
        self.frame2.grid(row=0,column=6,rowspan=17,columnspan=28)
        self.frame2.grid_rowconfigure(0,weight=1)
        self.frame2.grid_columnconfigure(0,weight=1)
        self.canvas1.grid(row=0,column=0)
        self.frame3.grid(row=0,column=35,rowspan=24,columnspan=5,sticky=tk.N+tk.S+tk.W+tk.E)        
        self.scroll1.grid(row=1,column=0,sticky=tk.W+tk.E)
        self.frame1.grid(row=18,column=6,rowspan=6,columnspan=28,sticky=tk.W+tk.E)

        ##############Initial Manual/Auto Screen################
        self.canvas7=tk.Canvas(self.frame7,width=600,height=480,bg='white')
        self.initButtons = {}
        self.initBtnNames = ["autoBtn", "manBtn"];
        self.initButtons["autoBtn"] = tk.Button(self.frame7,text="Auto",command=self.autoMode,padx=5,pady=2,height=8,width=12,disabledforeground="gray",state=tk.ACTIVE)
        self.initButtons["manBtn"] = tk.Button(self.frame7,text="Manual",command=self.manMode,padx=5,pady=2,height=8,width=12,disabledforeground="gray",state=tk.ACTIVE)
        self.initButtons["autoBtn"].grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.initButtons["manBtn"].grid(row=0, column=0, columnspan=2, sticky=tk.E)

        self.frame7.grid(row=0,column=6,rowspan=17,columnspan=28)
        self.frame7.grid_rowconfigure(0,weight=1)
        self.frame7.grid_columnconfigure(0,weight=1)
        self.canvas7.grid(row=0,column=0, rowspan=17, columnspan=28)
        self.canvas7.create_text(300, 480/2, text = "VRE Automatic Announcement Test BOX \n\nTo begin testing, please select the method of simulation.", justify=tk.CENTER)   #Spaces for onscreen spacing

        self.just_ran=False
        self.cancel_cancel=False

        
        self.gear_teeth=128
        self.wheel_travel=31/12*3.14159
        self.pulse_counter=0
        self.time_mod=1

        self.pi = pigpio.pi()
        self.pi.set_mode(19, pigpio.OUTPUT)
        self.pi.set_mode(17,pigpio.OUTPUT)
        self.pi.set_mode(12,pigpio.OUTPUT)        
        self.pi.set_mode(23,pigpio.OUTPUT)
        self.pi.set_mode(21,pigpio.OUTPUT)
                
    def restart(self):
        #same as _init_, just accessible
        try:
            if self.runMode=="auto":
                self.killDelay=True;
                self.cancel_simulation();
            else:
                self.manual_stop()
        except:
            print("Manual Stop Unsuccessful")
            
        self.frame7.destroy();
        self.frame1.destroy();
        self.frame3.destroy();
        self.frame4.destroy();
        self.frame7.destroy();
        self.dist_real=0
        self.speed=0
        self.time_iter=0
        self.frame1=tk.Frame(self.master,width=600,height=120,relief=tk.RIDGE,bd=3)
        self.frame2=tk.Frame(self.master,width=600,height=360,bg='white',relief=tk.RIDGE,bd=3)
        self.frame3=tk.Frame(self.master,width=100,height=480,relief=tk.RIDGE,bd=3)
        self.frame4=tk.Frame(self.master,width=100,height=480,relief=tk.RIDGE,bd=3)
        self.frame7=tk.Frame(self.master,width=600,height=480,bg='white',relief=tk.RIDGE,bd=3)  #7 to ensure no conflict
        
        self.canvas_height=360
        self.canvas_width=600
        self.start_x=80
        self.check_count=0

        self.canvas1=tk.Canvas(self.frame2,width=600,height=360,bg='white')
        self.scroll1=tk.Scrollbar(self.frame2,orient=tk.HORIZONTAL,width=20)
        self.canvas1.config(xscrollcommand=self.scroll1.set)
        self.scroll1.config(command=self.canvas1.xview)
        
        self.frame4.grid(row=0,column=0,rowspan=24,columnspan=5,sticky=tk.N+tk.S+tk.W+tk.E)
        self.frame2.grid(row=0,column=6,rowspan=17,columnspan=28)
        self.frame2.grid_rowconfigure(0,weight=1)
        self.frame2.grid_columnconfigure(0,weight=1)
        self.canvas1.grid(row=0,column=0)
        self.frame3.grid(row=0,column=35,rowspan=24,columnspan=5,sticky=tk.N+tk.S+tk.W+tk.E)        
        self.scroll1.grid(row=1,column=0,sticky=tk.W+tk.E)
        self.frame1.grid(row=18,column=6,rowspan=6,columnspan=28,sticky=tk.W+tk.E)

        ##############Initial Manual/Auto Screen################
        self.canvas7=tk.Canvas(self.frame7,width=600,height=480,bg='white')
        self.initButtons = {}
        self.initBtnNames = ["autoBtn", "manBtn"];
        self.initButtons["autoBtn"] = tk.Button(self.frame7,text="Auto",command=self.autoMode,padx=5,pady=2,height=8,width=12,disabledforeground="gray",state=tk.ACTIVE)
        self.initButtons["manBtn"] = tk.Button(self.frame7,text="Manual",command=self.manMode,padx=5,pady=2,height=8,width=12,disabledforeground="gray",state=tk.ACTIVE)
        self.initButtons["autoBtn"].grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.initButtons["manBtn"].grid(row=0, column=0, columnspan=2, sticky=tk.E)

        self.frame7.grid(row=0,column=6,rowspan=17,columnspan=28)
        self.frame7.grid_rowconfigure(0,weight=1)
        self.frame7.grid_columnconfigure(0,weight=1)
        self.canvas7.grid(row=0,column=0, rowspan=17, columnspan=28)
        self.canvas7.create_text(300, 480/2, text = "VRE Automatic Announcement Test Panel\n\nTo begin testing, please select the method of simulation.", justify=tk.CENTER)   #Spaces for onscreen spacing

        self.just_ran=False
        self.cancel_cancel=False

        self.gear_teeth=128
        self.wheel_travel=31/12*3.14159

        self.pulse_counter=0
        self.time_mod=1

        self.pi = pigpio.pi()
        self.pi.set_mode(19, pigpio.OUTPUT)
        self.pi.set_mode(17,pigpio.OUTPUT)
        self.pi.set_mode(12,pigpio.OUTPUT)        
        self.pi.set_mode(23,pigpio.OUTPUT)
        self.pi.set_mode(21,pigpio.OUTPUT)

    
    def manMode(self):
        self.runMode = "manual"
        #This will set up the GUI for Manual use. Utilizing as many existing functions as physically possible.
        self.manBtns = {};
        self.canvas7.delete(tk.ALL)
        for btn in range(0, len(self.initButtons)):
            self.initButtons[self.initBtnNames[btn]].destroy();     #Clears the buttons from the main screen

        self.train_speed=tk.StringVar()
        self.label2=tk.Label(self.frame7,textvariable=self.train_speed,bg="yellow")
        self.label2.grid(row=2, sticky=tk.W)
        self.dist_travel=tk.StringVar()
        self.label3=tk.Label(self.frame7,textvariable=self.dist_travel,bg="red")
        self.label3.grid(row=3, sticky=tk.W)
        self.dist_travel.set("0 ft")
        self.train_speed.set("0 mph")

        self.dist_real=0
        self.speed=0
        self.time_iter=0

        self.door_sequence=False;

        self.min_reached=True
        self.max_reached=False
        self.is_finished=False
        self.skip_next_bool=False

        self.time_delay=[0,2015,998,685,495,395,326,279,243,215,192,173,158]
        #self.time_delay=[0,2018,1001,668,498,398,329,282,246,218,195,176,161]
        #self.time_delay=[0,2020,1003,670,500,400,331,284,248,220,197,178,163]
        #self.time_delay=[0,1017,678,508,406,339,290,254,226,203,184,169,156,145,135]
        #self.time_delay=[0,2034,1017,678,508,406,339,290,254,226,203,184,169,156,145,135]
        
        self.button_speed_up=tk.Button(self.frame7,text="Increase \nSpeed",padx=2,pady=2,height=7,width=10,command=self.manual_speed_up,disabledforeground="gray",state=tk.ACTIVE)        
        self.button_speed_down=tk.Button(self.frame7,text="Decrease \nSpeed",padx=2,pady=2,height=7,width=10,command=self.manual_speed_down,disabledforeground="gray",state=tk.DISABLED)
        self.button_speed_up.grid(row=0,column=0,columnspan=1,sticky=tk.W)
        self.button_speed_down.grid(row=1,column=0,columnspan=1,sticky=tk.W)
        self.button_stop=tk.Button(self.frame7,text="STOP",padx=2,pady=2, height=7,width=10,command=self.manual_stop,bg="red",disabledforeground="gray",state=tk.DISABLED)
        self.button_stop.grid(row=4,column=0,columnspan=1,sticky=tk.W)
        
        self.wheel_travel=31/12*3.14159
        #self.wheel_travel=30/12*3.14159

        self.doorOpenBtn = tk.Button(self.frame7, text="Door\nOpen", padx=2, pady=2, height=7, width=10, command=self.door_open, disabledforeground="gray", state=tk.ACTIVE)
        self.doorOpenBtn.grid(row=0, column=1, columnspan=1)
        self.doorCloseBtn = tk.Button(self.frame7, text="Door\nClose", padx=2, pady=2, height=7, width=10, command=self.door_close, disabledforeground="gray", state=tk.DISABLED)
        self.doorCloseBtn.grid(row=1, column=1, columnspan=1)
        self.please_call=self.pi.callback(19,pigpio.RISING_EDGE ,self.call_out) #Lets the program update distance and speed consistently

        self.resetBtn = tk.Button(self.frame7, text="Main\nMenu", padx=2, pady=2, height=7, width=9, command=self.restart, disabledforeground="gray", state=tk.ACTIVE)
        self.resetBtn.grid(row=4, column=1, columnspan=1)

        
    def autoMode(self):
        self.runMode = "auto"
        begin_text="VRE Automatic Announcement Test Panel \n \nTo begin testing, prepare the AACP for the route to be simulated. \nWhen ready, select the appropiate route below to begin simulation."
        self.canvas1.create_text(300,self.canvas_height*(1/3),text=begin_text)

        self.frame7.destroy()   #Runs the program as usual

        self.killDelay = False;

        self.num_button=5
        
        self.button_names=[None]*self.num_button

        for o in range(0,self.num_button):
            self.button_names[o]="button"+str(o+1)

        self.buttons={}
        
        self.buttons[self.button_names[0]]=tk.Button(self.frame1,text="Manassas\n to DC",command=self.manassas_dc,padx=5,pady=2,height=8,width=11,disabledforeground="gray",state=tk.ACTIVE)
        self.buttons[self.button_names[1]]=tk.Button(self.frame1,text="Spotsylvania \n to DC",command=self.fredericksburg_dc,padx=5,pady=2,height=8,width=11,disabledforeground="gray",state=tk.ACTIVE)
        self.buttons[self.button_names[2]]=tk.Button(self.frame1,text="DC to\n Spotsylvania",command=self.dc_fredericksburg,padx=5,pady=2,height=8,width=11,disabledforeground="gray",state=tk.ACTIVE)
        self.buttons[self.button_names[3]]=tk.Button(self.frame1,text="DC to \nManassas",command = self.dc_manassas,padx=5,pady=2,height=8,width=11,disabledforeground="gray",state=tk.ACTIVE)
        self.buttons[self.button_names[4]]=tk.Button(self.frame1,text="Cancel \nSimulation",command = self.check_cancel,padx=5,pady=2,height=8,width=11,disabledforeground="gray",state=tk.DISABLED)
        self.buttons["reset"]=tk.Button(self.frame1, text="Main\nMenu", command=self.restart, padx=5, pady=2, height=8, width=9, disabledforeground="gray", state=tk.ACTIVE)

        self.delayBtns={}   #Allow the user to set the length of the delay
        self.delayBtns["timeUp"]=tk.Button(self.frame4, text="Dwell\nTime\nUp", command=self.delayUp, padx=2, pady=2, height=7, width=10, disabledforeground="gray", state=tk.ACTIVE)
        self.delayBtns["timeDown"]=tk.Button(self.frame4, text="Dwell\nTime\nDown", command=self.delayDown, padx=2, pady=2, height=7, width=10, disabledforeground="gray", state=tk.ACTIVE)
        self.delayLabel=tk.Label(self.frame4,textvariable=self.delayTimeStr,bg="green")
                                 
        
        self.buttons[self.button_names[0]].grid(row=0,column=0,columnspan=2,sticky=tk.N)
        self.buttons[self.button_names[1]].grid(row=0,column=2,columnspan=2,sticky=tk.N)
        self.buttons[self.button_names[2]].grid(row=0,column=4,columnspan=2,sticky=tk.N)
        self.buttons[self.button_names[3]].grid(row=0,column=6,columnspan=2,sticky=tk.N)
        self.buttons[self.button_names[4]].grid(row=0,column=8,columnspan=2,sticky=tk.N)
        self.buttons["reset"].grid(row=0, column=10, columnspan=2, sticky=tk.N)

        self.delayBtns["timeUp"].grid(row=1, sticky=tk.W);
        self.delayBtns["timeDown"].grid(row=3, sticky=tk.W);
        self.delayLabel.grid(row=2, sticky=tk.W);
        

        self.routes_final=[]

        self.routes_final.append("Manassas to DC")
        self.routes_final.append("Spotsylvania to DC")
        self.routes_final.append("DC to Spotsylvania")
        self.routes_final.append("DC to Manassas")

        self.train_list={}
        for u in range(0,4):
            if u == 0:
                self.train_list["route"+str(u)]=[None]*10
                self.train_list["dist"+str(u)]=[None]*10
                self.train_list["exit"+str(u)]=[None]*10
                self.train_list["entry"+str(u)]=[None]*10
                
                self.train_list["route"+str(u)][0]="Broad Run"
                self.train_list["route"+str(u)][1]="Manassas"
                self.train_list["route"+str(u)][2]="Manassas Park"
                self.train_list["route"+str(u)][3]="Burke Center"
                self.train_list["route"+str(u)][4]="Rolling Road"
                self.train_list["route"+str(u)][5]="Backlick Road"
                self.train_list["route"+str(u)][6]="Alexandria"
                self.train_list["route"+str(u)][7]="Crystal City"
                self.train_list["route"+str(u)][8]="L'Enfant"
                self.train_list["route"+str(u)][9]="Union Station"
                
                self.train_list["dist"+str(u)][0]=0
                self.train_list["dist"+str(u)][1]=17350
                self.train_list["dist"+str(u)][2]=28370
                self.train_list["dist"+str(u)][3]=75910                
                self.train_list["dist"+str(u)][4]=87640                
                self.train_list["dist"+str(u)][5]=109650               
                self.train_list["dist"+str(u)][6]=145640               
                self.train_list["dist"+str(u)][7]=166880               
                self.train_list["dist"+str(u)][8]=180010               
                self.train_list["dist"+str(u)][9]=189390
                
                self.train_list["exit"+str(u)][0]=5280
                self.train_list["exit"+str(u)][1]=20850
                self.train_list["exit"+str(u)][2]=33650
                self.train_list["exit"+str(u)][3]=79410
                self.train_list["exit"+str(u)][4]=92920
                self.train_list["exit"+str(u)][5]=114930
                self.train_list["exit"+str(u)][6]=150920
                self.train_list["exit"+str(u)][7]=170880
                self.train_list["exit"+str(u)][8]=183010
                self.train_list["exit"+str(u)][9]=189390
                
                self.train_list["entry"+str(u)][0]=12070
                self.train_list["entry"+str(u)][1]=24870
                self.train_list["entry"+str(u)][2]=70630
                self.train_list["entry"+str(u)][3]=84140
                self.train_list["entry"+str(u)][4]=104370
                self.train_list["entry"+str(u)][5]=140360
                self.train_list["entry"+str(u)][6]=161600
                self.train_list["entry"+str(u)][7]=176010
                self.train_list["entry"+str(u)][8]=186390
                self.train_list["entry"+str(u)][9]=189390
            if u == 1:
                self.train_list["route"+str(u)]=[None]*13
                self.train_list["dist"+str(u)]=[None]*13
                self.train_list["exit"+str(u)]=[None]*13
                self.train_list["entry"+str(u)]=[None]*13
                
                self.train_list["route"+str(u)][0]="Spotsylvania"
                self.train_list["route"+str(u)][1]="Fredericksburg"
                self.train_list["route"+str(u)][2]="Leeland Road"
                self.train_list["route"+str(u)][3]="Brooke"
                self.train_list["route"+str(u)][4]="Quantico"
                self.train_list["route"+str(u)][5]="Rippon"
                self.train_list["route"+str(u)][6]="Woodbridge"
                self.train_list["route"+str(u)][7]="Lorton"
                self.train_list["route"+str(u)][8]="Franconia\nSpringfield"
                self.train_list["route"+str(u)][9]="Alexandria"
                self.train_list["route"+str(u)][10]="Crystal City"
                self.train_list["route"+str(u)][11]="L'Enfant"
                self.train_list["route"+str(u)][12]="Union Station"
                
                self.train_list["dist"+str(u)][0]=0                
                self.train_list["dist"+str(u)][1]=31680            
                self.train_list["dist"+str(u)][2]=52970            
                self.train_list["dist"+str(u)][3]=76860          
                self.train_list["dist"+str(u)][4]=133710            
                self.train_list["dist"+str(u)][5]=170220            
                self.train_list["dist"+str(u)][6]=187360            
                self.train_list["dist"+str(u)][7]=210780            
                self.train_list["dist"+str(u)][8]=234590            
                self.train_list["dist"+str(u)][9]=273410            
                self.train_list["dist"+str(u)][10]=294470 # KLM: changed from 293470 to distance given by VRE 
                self.train_list["dist"+str(u)][11]=307540           
                self.train_list["dist"+str(u)][12]=316920
                
                self.train_list["exit"+str(u)][0]=5280
                self.train_list["exit"+str(u)][1]=36960
                self.train_list["exit"+str(u)][2]=58250
                self.train_list["exit"+str(u)][3]=87420
                self.train_list["exit"+str(u)][4]=138990
                self.train_list["exit"+str(u)][5]=175500
                self.train_list["exit"+str(u)][6]=192640
                self.train_list["exit"+str(u)][7]=216060
                self.train_list["exit"+str(u)][8]=239870
                self.train_list["exit"+str(u)][9]=278690
                self.train_list["exit"+str(u)][10]=298370
                self.train_list["exit"+str(u)][11]=310540
                self.train_list["exit"+str(u)][12]=316920
                
                self.train_list["entry"+str(u)][0]=26400
                self.train_list["entry"+str(u)][1]=47690
                self.train_list["entry"+str(u)][2]=71580
                self.train_list["entry"+str(u)][3]=123150
                self.train_list["entry"+str(u)][4]=164940
                self.train_list["entry"+str(u)][5]=182080
                self.train_list["entry"+str(u)][6]=205500
                self.train_list["entry"+str(u)][7]=229310
                self.train_list["entry"+str(u)][8]=268130
                self.train_list["entry"+str(u)][9]=289090
                self.train_list["entry"+str(u)][10]=303540
                self.train_list["entry"+str(u)][11]=313920
                self.train_list["entry"+str(u)][12]=316920
            if u == 2:
                self.train_list["route"+str(u)]=[None]*13
                self.train_list["dist"+str(u)]=[None]*13
                self.train_list["exit"+str(u)]=[None]*13
                self.train_list["entry"+str(u)]=[None]*13
                
                self.train_list["route"+str(u)][0]="Union Station"
                self.train_list["route"+str(u)][1]="L'Enfant"
                self.train_list["route"+str(u)][2]="Crystal City"
                self.train_list["route"+str(u)][3]="Alexandria"
                self.train_list["route"+str(u)][4]="Franconia\nSpringfield"
                self.train_list["route"+str(u)][5]="Lorton"
                self.train_list["route"+str(u)][6]="Woodbridge"
                self.train_list["route"+str(u)][7]="Rippon"
                self.train_list["route"+str(u)][8]="Quantico"
                self.train_list["route"+str(u)][9]="Brooke"
                self.train_list["route"+str(u)][10]="Leeland Road"
                self.train_list["route"+str(u)][11]="Fredericksburg"              
                self.train_list["route"+str(u)][12]="Spotsylvania"
                
                self.train_list["dist"+str(u)][0]=0                
                self.train_list["dist"+str(u)][1]=9380            
                self.train_list["dist"+str(u)][2]=22550            
                self.train_list["dist"+str(u)][3]=43510            
                self.train_list["dist"+str(u)][4]=82330            
                self.train_list["dist"+str(u)][5]=106140            
                self.train_list["dist"+str(u)][6]=129560            
                self.train_list["dist"+str(u)][7]=146700            
                self.train_list["dist"+str(u)][8]=183210            
                self.train_list["dist"+str(u)][9]=240060            
                self.train_list["dist"+str(u)][10]=263950           
                self.train_list["dist"+str(u)][11]=285240           
                self.train_list["dist"+str(u)][12]=316920
                
                self.train_list["exit"+str(u)][0]=3000
                self.train_list["exit"+str(u)][1]=13380
                self.train_list["exit"+str(u)][2]=27830
                self.train_list["exit"+str(u)][3]=48790
                self.train_list["exit"+str(u)][4]=87610
                self.train_list["exit"+str(u)][5]=111420
                self.train_list["exit"+str(u)][6]=134840
                self.train_list["exit"+str(u)][7]=151980
                self.train_list["exit"+str(u)][8]=193770
                self.train_list["exit"+str(u)][9]=245340
                self.train_list["exit"+str(u)][10]=269230
                self.train_list["exit"+str(u)][11]=290520
                self.train_list["exit"+str(u)][12]=316920
                
                self.train_list["entry"+str(u)][0]=6380
                self.train_list["entry"+str(u)][1]=18550
                self.train_list["entry"+str(u)][2]=38230
                self.train_list["entry"+str(u)][3]=77050
                self.train_list["entry"+str(u)][4]=100860
                self.train_list["entry"+str(u)][5]=124280
                self.train_list["entry"+str(u)][6]=141420
                self.train_list["entry"+str(u)][7]=177930
                self.train_list["entry"+str(u)][8]=229500
                self.train_list["entry"+str(u)][9]=258670
                self.train_list["entry"+str(u)][10]=279960
                self.train_list["entry"+str(u)][11]=311640
                self.train_list["entry"+str(u)][12]=316920
            if u == 3: 
                self.train_list["route"+str(u)]=[None]*10
                self.train_list["dist"+str(u)]=[None]*10
                self.train_list["exit"+str(u)]=[None]*10
                self.train_list["entry"+str(u)]=[None]*10

                self.train_list["route"+str(u)][9]="Broad Run"
                self.train_list["route"+str(u)][8]="Manassas"
                self.train_list["route"+str(u)][7]="Manassas Park"
                self.train_list["route"+str(u)][6]="Burke Center"
                self.train_list["route"+str(u)][5]="Rolling Road"
                self.train_list["route"+str(u)][4]="Backlick Road"
                self.train_list["route"+str(u)][3]="Alexandria"
                self.train_list["route"+str(u)][2]="Crystal City"
                self.train_list["route"+str(u)][1]="L'Enfant"
                self.train_list["route"+str(u)][0]="Union Station"
                
                self.train_list["dist"+str(u)][0]=0
                self.train_list["dist"+str(u)][1]=9380
                self.train_list["dist"+str(u)][2]=22520 # KLM: changed from 22510 to distance given by VRE
                self.train_list["dist"+str(u)][3]=43750                
                self.train_list["dist"+str(u)][4]=79740              
                self.train_list["dist"+str(u)][5]=101760 # KLM: changed from 101750 to distance given by VRE  
                self.train_list["dist"+str(u)][6]=113490 # KLM: changed from 133480 to distance given by VRE  
                self.train_list["dist"+str(u)][7]=161020               
                self.train_list["dist"+str(u)][8]=172050 # KLM: changed from 172040 to distance given by VRE
                self.train_list["dist"+str(u)][9]=189390
                
                self.train_list["exit"+str(u)][0]=3000
                self.train_list["exit"+str(u)][1]=13380
                self.train_list["exit"+str(u)][2]=27800 # KLM: changed from 27790 to distance given by VRE
                self.train_list["exit"+str(u)][3]=49030
                self.train_list["exit"+str(u)][4]=85020
                self.train_list["exit"+str(u)][5]=105260 # KLM: changed from 105250 to distance given by VRE
                self.train_list["exit"+str(u)][6]=118770 # KLM: changed from 118760 to distance given by VRE
                self.train_list["exit"+str(u)][7]=164520
                self.train_list["exit"+str(u)][8]=177330 # KLM: changed from 177320 to distance given by VRE
                self.train_list["exit"+str(u)][9]=189390
                
                self.train_list["entry"+str(u)][0]=6380
                self.train_list["entry"+str(u)][1]=18520 # KLM: changed from 18510 to distance given by VRE
                self.train_list["entry"+str(u)][2]=38470
                self.train_list["entry"+str(u)][3]=74460
                self.train_list["entry"+str(u)][4]=96480 # KLM: changed from 96470 to distance given by VRE
                self.train_list["entry"+str(u)][5]=109990 # KLM: changed from 109980 to distance given by VRE
                self.train_list["entry"+str(u)][6]=155740
                self.train_list["entry"+str(u)][7]=168550 # KLM: changed from 168540 to distance given by VRE
                self.train_list["entry"+str(u)][8]=184110
                self.train_list["entry"+str(u)][9]=189390

    def delayUp(self):
        #Sets the delay time in intervals of 5 sec. 45 sec cap
        if self.delayMinBool:
            self.delayBtns["timeDown"]['state']='active'
            self.delayMinBool=False;
        if (self.delayTime+5)>=self.delayTimeMax:
            self.delayTime=self.delayTimeMax
            self.delayBtns["timeUp"]['state']='disabled';
            self.delayMaxBool=True;
        else:
            self.delayTime+=5;
        self.delayTimeStr.set(str(self.delayTime) + " sec")
            
    def delayDown(self):
        #Sets the delay time in intervals of 5 sec. 0 sec minimum
        if self.delayMaxBool:
            self.delayBtns["timeUp"]['state'] = 'active'
            self.delayMaxBool=False;
        if (self.delayTime-5)<=0:
            self.delayTime=0;
            self.delayBtns["timeDown"]['state']='disabled';
            self.delayMinBool=True;
        else:
            self.delayTime-=5;
        self.delayTimeStr.set(str(self.delayTime) + " sec")
    
    def door_sequence(self):
        #OBSOLETE
        #only intended for the manual button callback
        self.manual_stop()  #Automatically stops the train
        self.door_sequence=True
        self.doorBtn['state'] = 'disabled'
        self.canvas7.create_rectangle(self.canvas_width/2-50,self.canvas_height/2-(self.canvas_height/4)-20,self.canvas_width/2+50,self.canvas_height/2-(self.canvas_height/4)+20,fill="yellow",width=2,tag="doors1")
        self.canvas7.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text="Doors Opening")
        self.pi.write(17,1)
        self.pi.write(23,1)
        self.frame7.update()
        time.sleep(5)
        self.canvas7.delete("doors")
        self.frame7.update()
        counter = self.delayTime;
        for t in range(0, counter):
            if not self.killDelay:
                self.canvas7.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text=str(counter-t)+ " sec remain")
                time.sleep(1);
                self.canvas7.delete("doors")
            else:
                break
        self.canvas7.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text="Doors Closing")
        self.frame7.update()
        time.sleep(5)
        
        self.canvas7.delete("doors")
        self.canvas7.delete("doors1")
        self.frame7.update()
        self.pi.write(17,0)            
        self.pi.write(23,0)
        self.door_sequence=False
        self.doorBtn['state'] = 'active'

    def door_open(self):
        self.manual_stop()         #Uncomment to prevent user from opening doors on a moving train
        self.door_sequence=True
        self.doorOpenBtn['state']='disabled'
        self.canvas7.create_rectangle(self.canvas_width/2-50,self.canvas_height/2-(self.canvas_height/4)-20,self.canvas_width/2+50,self.canvas_height/2-(self.canvas_height/4)+20,fill="yellow",width=2,tag="doors1")
        self.canvas7.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text="Doors Open")
        self.pi.write(17,1)
        self.pi.write(23,1)
        self.doorCloseBtn['state']='active'
        self.frame7.update()
        
    def door_close(self):
        self.doorCloseBtn['state']='disabled'
        self.canvas7.delete("doors")
        self.canvas7.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text="Doors Closing")
        self.frame7.update()

        self.pi.write(17,0)
        self.pi.write(23,0)
        self.canvas7.delete("doors")
        self.canvas7.delete("doors1")
        self.door_sequence=False
        self.doorOpenBtn['state']='active'
        self.frame7.update()
    
    def load_train(self,train_num):
        if self.just_ran==True:
            self.canvas1.delete(tk.ALL)
            self.screen_text.set("")
        else:
           self.canvas1.delete(tk.ALL) 
        self.time_mod=1

        if train_num==3:
            self.wheel_travel=31/12*3.14159
        else:
            self.wheel_travel=30/12*3.14159
        
        self.len=len(self.train_list["dist"+str(train_num)])
        self.station_pix=[None]*self.len
        self.last_stop=(self.train_list["dist"+str(train_num)][self.len-1])/5280
        self.pix_per_mile=66
        self.canvas1.create_line(0,self.canvas_height/2+2,self.start_x+self.last_stop*self.pix_per_mile+self.start_x,self.canvas_height/2+2,tag="station_info")
        self.canvas1.create_line(0,self.canvas_height/2-2,self.start_x+self.last_stop*self.pix_per_mile+self.start_x,self.canvas_height/2-2,tag="station_info")
        self.canvas1.configure(scrollregion=self.canvas1.bbox('all'))
        self.iterate=0
        for w in range(0,self.train_list["dist"+str(train_num)][self.len-1]+1):
            if w == self.train_list["dist"+str(train_num)][self.iterate]:                
                self.x0=self.start_x+self.train_list["dist"+str(train_num)][self.iterate]/5280*self.pix_per_mile-5
                self.x1=self.start_x+self.train_list["dist"+str(train_num)][self.iterate]/5280*self.pix_per_mile+5
                self.y0=self.canvas_height/2+5
                self.y1=self.canvas_height/2-5
                self.canvas1.create_oval(self.x0,self.y0,self.x1,self.y1,fill="yellow",tag="station_info")
                self.xdot=self.x0+5
                self.station_pix[self.iterate]=self.xdot
                self.ydot=self.canvas_height/2+20
                self.canvas1.create_text(self.xdot,self.ydot,tag="station_info",text=self.train_list["route"+str(train_num)][self.iterate])                
                self.iterate+=1
            if w==self.train_list["dist"+str(train_num)][self.len-1]:
                self.xdot+=800
                self.canvas1.create_text(self.xdot,self.ydot,tag="station_info",text="END")
                

        self.screen_text=tk.StringVar()
        self.label1=tk.Label(self.frame3,textvariable=self.screen_text,bg="white")
        self.label1.grid(row=1,column=0,columnspan=4,rowspan=2,sticky=tk.W+tk.E)
        self.train_speed=tk.StringVar()
        self.label2=tk.Label(self.frame3,textvariable=self.train_speed,bg="yellow")
        self.label2.grid(row=3,column=0,columnspan=4,rowspan=2,sticky=tk.W+tk.E)
        self.dist_travel=tk.StringVar()
        self.label3=tk.Label(self.frame3,textvariable=self.dist_travel,bg="red")
        self.label3.grid(row=5,column=0,rowspan=2,columnspan=4,sticky=tk.W+tk.E)
        self.aacp=tk.StringVar()
        self.door=tk.StringVar()
        self.aacp.set("AACP Announcements")
        self.master.after(7000,self.clear_aacp)
        self.dist_travel.set("0 ft")
        self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2+(self.canvas_height/4),tag="aacp",text=self.aacp.get())

        self.button_speed_up=tk.Button(self.frame3,text="Increase \nSpeed",padx=2,pady=2,height=7,width=10,command=self.manual_speed_up,disabledforeground="gray",state=tk.ACTIVE)        
        self.button_speed_down=tk.Button(self.frame3,text="Decrease \nSpeed",padx=2,pady=2,height=7,width=10,command=self.manual_speed_down,disabledforeground="gray",state=tk.DISABLED)
        self.button_speed_up.grid(row=0,column=0,columnspan=4,sticky=tk.W+tk.E)
        self.button_speed_down.grid(row=7,column=0,columnspan=4,sticky=tk.W+tk.E)
        self.button_stop=tk.Button(self.frame3,text="STOP",padx=2,pady=2, height=7,width=10,command=self.manual_stop,bg="red",disabledforeground="gray",state=tk.DISABLED)
        self.button_stop.grid(row=8,column=0,columnspan=4,sticky=tk.W+tk.E)

        self.button_stop_next=tk.Button(self.frame4,text="Skip Next \nStation",padx=2,pady=2, height=7,width=10,command=self.skip_next,bg="yellow",disabledforeground="gray",state=tk.DISABLED)
        self.button_stop_next.grid(row=0,columnspan=4,sticky=tk.W+tk.E)
        
        self.button_speed_up['state']='disabled'
        self.button_speed_down['state']='disabled'
        self.button_stop['state']='disabled'
        
        self.screen_text.set("Ready\nTo Simulate")
        
        self.train_speed.set("0 mph")
        
        self.car_Matrix=[[0 for x in range(4)] for y in range(4)]

        for i in range(0,4):
            for w in range(0,4):
                if w == 0:
                    self.car_Matrix[i][w]=self.start_x-15*(i+1)
                if w == 1:
                    self.car_Matrix[i][w]=self.canvas_height/2+5
                if w == 2:
                    self.car_Matrix[i][w]=self.start_x-15*i
                if w == 3:
                    self.car_Matrix[i][w]=self.canvas_height/2-5
            self.canvas1.create_rectangle(self.car_Matrix[i][0],self.car_Matrix[i][1],self.car_Matrix[i][2],self.car_Matrix[i][3],fill="red",width=3,tag="train")

        self.please_call=self.pi.callback(19,pigpio.RISING_EDGE ,self.call_out)
        
        self.frame2.update()
        
        self.door_sequence=True
        self.canvas1.create_rectangle(self.canvas_width/2-50,self.canvas_height/2-(self.canvas_height/4)-20,self.canvas_width/2+50,self.canvas_height/2-(self.canvas_height/4)+20,fill="yellow",width=2,tag="doors1")
        self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text="Doors Opening")
        self.pi.write(17,1)
        self.pi.write(23,1)
        self.frame2.update()
        time.sleep(5)
        self.canvas1.delete("doors")
        self.frame2.update()
        counter=self.delayTime
        for t in range(0, counter):
            if not self.killDelay:
                self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text=str(counter-t)+ " sec remain")
                self.frame2.update()
                time.sleep(1);
                self.canvas1.delete("doors")
            else:
                break
            
        self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text="Doors Closing")
        self.frame2.update()
        time.sleep(5)
        
        self.canvas1.delete("doors")
        self.canvas1.delete("doors1")
        self.frame2.update()
        self.pi.write(17,0)            
        self.pi.write(23,0)
        self.door_sequence=False

        self.dist_real=0
        self.last_dist_real=0
        self.dist_pix=0
        self.dist_move=0
        self.calibrate1=0
        self.station_at=0
        self.speed=0
        self.aacp1=-1
        self.aacp2=-1
        
        self.time_delay=[0,2015,998,685,495,395,326,279,243,215,192,173,158]
        #self.time_delay=[0,2018,1001,668,498,398,329,282,246,218,195,176,161]
        #self.time_delay=[0,2020,1003,670,500,400,331,284,248,220,197,178,163]
        #self.time_delay=[0,2034,1017,678,508,406,339,290,254,226,203,184,169,156,145,135]
        #self.time_delay=[0,2034,1017,678,508,406,339,290,254,226,203]
        
        self.time_iter=0
        self.min_reached=True
        self.max_reached=False
        self.is_finished=False
        self.skip_next_bool=False
        
        self.car_simulation(train_num)
        
        
        strang=""
        use_space=False
        a=0
        string1="Going to\n" +str(self.train_list["route"+str(train_num)][self.station_at+1])
        for word in string1:
            if use_space==False:
                if word == " ":
                     strang+="\n"
                     use_space=False
                     a=0
                else:
                     strang+=word
            else:
                strang+=word
                a+=1
                if a > 10:
                     use_space=True

        self.button_speed_up['state']='active'
        self.button_stop_next['state']='active'
                     
        self.screen_text.set(strang)
        self.frame2.update()
        self.choose_train=train_num
        self.car_simulation(self.choose_train)

    def skip_next(self):
        if self.skip_next_bool==False:
            self.skip_next_bool=True
            self.button_stop_next['text']='Stop at \nNext Station'
            self.button_stop_next['bg']='#7fff00'
            self.button_stop_next['activebackground']='#7fff00'
            self.screen_text.set("Going to\n" +str(self.train_list["route"+str(self.choose_train)][self.station_at+2]))
        else:
            self.skip_next_bool=False
            self.button_stop_next['text']='Skip \nNext Station'
            self.button_stop_next['bg']='yellow'
            self.button_stop_next['activebackground']='yellow'
            self.screen_text.set("Going to\n" +str(self.train_list["route"+str(self.choose_train)][self.station_at+1]))
        self.frame4.update()

    def finish_up(self):        
        self.just_ran=True

        
        self.pi.wave_tx_stop()
        self.pi.write(19,0)
        self.pi.write(17,0)
        self.pi.write(12,0)
        self.pi.write(21,0)
        self.pi.write(23,0)
        self.pi.wave_clear()
        self.pi.stop()
        
        self.choose_train=0
        self.time_iter=0
        self.dist_real=0
        self.last_dist_real=0
        self.dist_pix=0
        self.dist_move=0
        self.calibrate1=0
        self.station_at=0
        self.speed=0
        self.aacp1=-1
        self.aacp2=-1
        
        
        self.canvas1.configure(scrollregion=self.canvas1.bbox('all'))
       
        for i in range(0,self.num_button-1):
            self.buttons[self.button_names[i]]['state']='active'
            self.buttons[self.button_names[i]]['bg']='gray'
            self.buttons[self.button_names[i]]['fg']='black'
            

        self.buttons[self.button_names[self.num_button-1]]['state']='disabled'
        self.button_speed_up['state']='disabled'
        self.button_speed_down['state']='disabled'
        self.button_stop['state']='disabled'
        self.button_stop_next['state']='disabled'

        self.pi = pigpio.pi()
        self.pi.set_mode(19, pigpio.OUTPUT)
        self.pi.set_mode(17,pigpio.OUTPUT)        
        self.pi.set_mode(12,pigpio.OUTPUT)        
        self.pi.set_mode(23,pigpio.OUTPUT)        
        self.pi.set_mode(21,pigpio.OUTPUT)
        


    def manual_speed_up(self):
        if self.door_sequence!=True:
            self.pi.write(21,1)
            self.pi.write(12,1)
            self.time_iter+=1
            self.speed+=10*5280/3600
            self.train_speed.set(str(round(self.speed*3600/5280)) + " mph")
            self.send_wave()
            if self.min_reached==True:            
                self.button_speed_down['state']='active'
                self.button_stop['state']='active'
                self.min_reached=False
            if self.time_iter==len(self.time_delay)-1:
                self.button_speed_up['state']='disabled'
                self.max_reached=True

    def manual_speed_down(self):
        self.time_iter+=-1
        self.speed+=-10*5280/3600
        if self.speed<=0:
            self.speed = 0;
            self.button_speed_down['state']='disabled'
            self.min_reached=True
            self.time_iter=0;
        if self.time_iter==0:
            self.pi.write(21,0)
            self.pi.wave_tx_stop()
            self.pi.write(19,0)
            self.pi.write(12,0)
            self.button_speed_down['state']='disabled'
            self.button_stop['state']='disabled'
            self.min_reached=True
        else:
            self.send_wave()
        if self.max_reached==True:
            self.button_speed_up['state']='active'
            self.max_reached=False
        self.train_speed.set(str(round(self.speed*3600/5280)) + " mph")

    def manual_stop(self):
        self.pi.write(21,0)
        self.pi.wave_tx_stop()
        self.pi.write(19,0)
        self.pi.write(12,0)

        try:
            self.button_speed_down['state']='disabled'
            self.button_stop['state']='disabled'
        except:
            print("Buttons DNE")
          
        self.min_reached=True
        if self.max_reached==True:
            self.button_speed_up['state']='active'
            self.max_reached=False
            
        self.time_iter=0

        self.speed=0
        self.train_speed.set(str(round(self.speed*3600/5280)) + " mph")
            

    def send_wave(self):
        square=[]
        square.append(pigpio.pulse(1<<19,0,self.time_delay[self.time_iter]))
        square.append(pigpio.pulse(0,1<<19,self.time_delay[self.time_iter]))
        self.pi.wave_add_generic(square)
        wid = self.pi.wave_create()
        self.pi.wave_send_repeat(wid)

    def call_out(self,gpio,level,tick):
        self.pulse_counter+=1
        if self.pulse_counter==self.gear_teeth:
            self.check_count+=self.pulse_counter
            self.pulse_counter=0
            self.dist_real+=self.wheel_travel
            if self.runMode=="auto":
                self.car_simulation(self.choose_train)
            else:
                self.dist_travel.set(str(round(self.dist_real))+" ft")
        
        
            

    def car_simulation(self,train_num):   
        self.hardStop = False;
        if self.dist_real > self.train_list["dist"+str(train_num)][self.station_at+1]:
            if self.skip_next_bool==False:
                self.dist_travel.set(str(round(self.dist_real)) +" ft")
                self.door_sequence=True
                self.pi.wave_tx_stop()
                self.pi.write(19,0)
                self.pi.write(21,0)
                self.pi.write(12,0)
                self.pi.wave_clear()
                self.train_speed.set("0 mph")
                
                self.button_speed_down['state']='disabled'
                self.button_speed_up['state']='disabled'
                self.button_stop['state']='disabled'
                self.button_stop_next['state']='disabled'
                
                self.dist_to_next=self.train_list["dist"+str(train_num)][self.station_at+1]-self.dist_real
                if self.dist_to_next > 0:
                    #print("under shot stop, dist to next is " + str(self.dist_to_next))
                    self.station_at+=1
                if self.dist_to_next < 0:
                    #print("over shot stop, dist to next is " + str(self.dist_to_next))
                    self.station_at+=1
                if self.dist_to_next==0:
                    #print("good stop, dist to next is " + str(self.dist_to_next))
                    self.station_at+=1
                #GPIO.output(17, True)
                self.screen_text.set("Stopping at\n " +str(self.train_list["route"+str(train_num)][self.station_at]))
                self.frame2.update()
                
                self.canvas1.delete("doors")
                self.door.set("Doors Opening")
                self.canvas1.create_rectangle(self.canvas_width/2-50,self.canvas_height/2-(self.canvas_height/4)-20,self.canvas_width/2+50,self.canvas_height/2-(self.canvas_height/4)+20,fill="yellow",width=2,tag="doors1")
                self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text=self.door.get())
                self.pi.write(17,1)
                self.pi.write(23,1)
                self.frame2.update()
                time.sleep(5)
                self.canvas1.delete("doors")
                counter = self.delayTime;
                for t in range(0, counter):
                    if not self.killDelay:
                        self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text=str(counter-t)+ " sec remain")
                        time.sleep(1);
                        self.canvas1.delete("doors")
                    else:
                        self.hardStop = True;
                        break
                self.door.set("Doors Closing")
                self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="doors",text=self.door.get())
                interdelay=0 if self.hardStop else 5
                time.sleep(interdelay)
                self.canvas1.delete("doors")
                self.canvas1.delete("doors1")
                self.pi.write(17,0)            
                self.pi.write(23,0)

                if self.killDelay:      #Preventing leaking into manual program
                    self.hardStop=True;
                
                if self.min_reached==True:
                    self.button_speed_up['state']='active'
                else:
                    if self.max_reached==True:
                        self.button_speed_down['state']='active'
                        self.button_stop['state']='active'
                    else:
                        self.button_speed_up['state']='active'
                        self.button_speed_down['state']='active'
                        self.button_stop['state']='active'

                self.pi.write(21,1)
                self.pi.write(12,1)

                if self.killDelay:
                    self.hardStop=True;

                if self.hardStop!=True:
                    self.send_wave()
                    self.train_speed.set(str(round(self.speed*3600/5280)) + " mph")
                self.door_sequence=False
                
            else:
                self.skip_next_bool=False
                self.station_at+=1
            
            if self.station_at==self.len-1:

                char=len(self.routes_final[train_num])
                self.canvas1.create_rectangle(self.canvas_width/2-50*int(char/5),self.canvas_height/2-(self.canvas_height/4)+10*int(char/5),self.canvas_width/2+50*int(char/5),self.canvas_height/2-(self.canvas_height/4)-10*int(char/5),fill="#7fff00",width=2,tag="doors1")
                self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2-(self.canvas_height/4),tag="fin",text="Finished Route:\n" + str(self.routes_final[train_num]))
                self.screen_text.set("")
                self.train_speed.set(str("0 mph"))
                self.is_finished=True
                self.finish_up()
            else:
                if self.station_at+1==self.len-1:
                    self.button_stop_next['state']='disabled'
                    self.button_stop_next['text']='Skip \nNext Station'
                    self.button_stop_next['bg']='gray'
                    self.skip_next_bool=False
                else:
                    self.button_stop_next['state']='active'
                    self.button_stop_next['text']='Skip \nNext Station'
                    self.button_stop_next['bg']='yellow'
                    self.button_stop_next['activebackground']='yellow'
                    self.skip_next_bool=False
                self.screen_text.set("Going to\n" +str(self.train_list["route"+str(train_num)][self.station_at+1]))
                self.is_finished=False                
                
                
                
        
        self.dist_travel.set(str(round(self.dist_real)) +" ft")

        if self.is_finished==False:
            if self.dist_real>=self.train_list["exit"+str(train_num)][self.station_at]:
                if self.station_at+1==self.len-1:
                    self.add_word="Last"
                else:
                    self.add_word="Next"
                if self.aacp1<self.station_at:
                    char2=len("AACP: "+str(self.add_word)+" Stop " + self.train_list["route"+str(train_num)][self.station_at+1])
                    self.aacp1=self.station_at
                    self.clear_aacp()
                    self.aacp.set("AACP: "+str(self.add_word)+" Stop " + self.train_list["route"+str(train_num)][self.station_at+1])
                    
                    self.canvas1.create_rectangle(self.canvas_width/2-50*int(char2/8),self.canvas_height/2+(self.canvas_height/4)-10*int(char2/8),self.canvas_width/2+50*int(char2/8),self.canvas_height/2+(self.canvas_height/4)+10*int(char2/8),tag="aacp",fill="yellow",width=2)
                    self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2+(self.canvas_height/4),tag="aacp",text=self.aacp.get())
                    self.master.after(10000,self.clear_aacp)
                    
            if self.dist_real>self.train_list["entry"+str(train_num)][self.station_at]:
                if self.aacp2<self.station_at:
                    self.aacp2=self.station_at

                    
                    self.clear_aacp()
                    self.aacp.set("AACP: Arriving at " + self.train_list["route"+str(train_num)][self.station_at+1])
                    char3=len("AACP: Arriving at " + self.train_list["route"+str(train_num)][self.station_at+1])
                    self.canvas1.create_rectangle(self.canvas_width/2-50*int(char3/8),self.canvas_height/2+(self.canvas_height/4)-10*int(char3/8),self.canvas_width/2+50*int(char3/8),self.canvas_height/2+(self.canvas_height/4)+10*int(char3/8),tag="aacp",fill="yellow",width=2)
                    self.canvas1.create_text(self.canvas_width/2,self.canvas_height/2+(self.canvas_height/4),tag="aacp",text=self.aacp.get())
                    self.master.after(10000,self.clear_aacp)
            
            self.dist_move=int(((self.dist_real-self.last_dist_real)*self.pix_per_mile/5280))
            self.calibrate1+=((self.dist_real-self.last_dist_real)*self.pix_per_mile/5280)-int(((self.dist_real-self.last_dist_real)*self.pix_per_mile/5280))
            self.dist_pix+=self.dist_move
            self.canvas1.move("station_info",-1*self.dist_move,0)
            
            if self.calibrate1>1:
                self.canvas1.move("station_info",-1*int(self.calibrate1),0)
                self.calibrate1+=-1*int(self.calibrate1)
                self.dist_pix+=int(self.calibrate1)
            self.last_dist_real=self.dist_real
            self.canvas1.configure(scrollregion=self.canvas1.bbox('all'))

    def check_cancel(self):
        message1=messagebox.askquestion("Cancel Simulation","Are you sure you want to cancel the Simulation?")

        if message1=='yes':            
            if self.door_sequence==True:
                message2=messagebox.showinfo("Doors Closing","Allow Doors to Close")
            else:
                self.cancel_simulation()

    def cancel_simulation(self):
        
        
        self.pi.stop()
        
        self.is_finished=False
        self.just_ran=False
        self.min_reached=True
        self.max_reached=False
        self.skip_next_bool=False

        self.button_stop_next['text']='Skip \nNext Station'
        self.button_stop_next['bg']='yellow'
        
        
        self.time_iter=0
        self.dist_real=0
        self.last_dist_real=0
        self.dist_pix=0
        self.dist_move=0
        self.calibrate1=0
        self.station_at=0
        self.speed=0
        self.aacp1=-1
        self.aacp2=-1
        
        self.canvas1.delete(tk.ALL)
        self.screen_text.set("")
        
        for i in range(0,self.num_button-1):
            self.buttons[self.button_names[i]]['state']='active'
            self.buttons[self.button_names[i]]['bg']='gray'
            self.buttons[self.button_names[i]]['fg']='black'

        self.buttons[self.button_names[self.num_button-1]]['state']='disabled'
        self.button_speed_up['state']='disabled'
        self.button_speed_down['state']='disabled'
        self.button_stop['state']='disabled'
        self.button_stop_next['state']='disabled'

        self.pi = pigpio.pi()
        self.pi.set_mode(19, pigpio.OUTPUT)
        self.pi.set_mode(17,pigpio.OUTPUT)
        self.pi.set_mode(23,pigpio.OUTPUT)
        self.pi.set_mode(21,pigpio.OUTPUT)
        self.pi.set_mode(12,pigpio.OUTPUT)
        self.pi.wave_tx_stop()
        self.pi.write(19,0)
        self.pi.write(17,0)
        self.pi.write(12,0)
        self.pi.write(23,0)
        self.pi.write(21,0)
        self.pi.wave_clear()
        self.train_speed.set("0 mph")
        self.dist_travel.set("0 ft")
        
        
    def manassas_dc(self):

        self.buttons[self.button_names[0]]['bg']='#7fff00'

        for i in range(0,self.num_button-1):
            self.buttons[self.button_names[i]]['state']='disabled'
            
        self.buttons[self.button_names[self.num_button-1]]['state']='active'

        self.load_train(0)
                             
                

    def fredericksburg_dc(self):

        self.buttons[self.button_names[1]]['bg']='#7fff00'

        for i in range(0,self.num_button-1):
            self.buttons[self.button_names[i]]['state']='disabled'

        self.buttons[self.button_names[self.num_button-1]]['state']='active'

        self.load_train(1)   



    def dc_fredericksburg(self):

        self.buttons[self.button_names[2]]['bg']='#7fff00'

        for i in range(0,self.num_button-1):
            self.buttons[self.button_names[i]]['state']='disabled'

        self.buttons[self.button_names[self.num_button-1]]['state']='active'
            
        self.load_train(2)



    def dc_manassas(self):

        self.buttons[self.button_names[3]]['bg']='#7fff00'
        

        for i in range(0,self.num_button-1):
            self.buttons[self.button_names[i]]['state']='disabled'

        self.buttons[self.button_names[self.num_button-1]]['state']='active'
            
        self.load_train(3)



    def clear_aacp(self):
        self.canvas1.delete("aacp")



def close(event):
    pi = pigpio.pi()
    
    pi.set_mode(19, pigpio.OUTPUT)
    pi.set_mode(17, pigpio.OUTPUT)    
    pi.set_mode(12, pigpio.OUTPUT)
    pi.set_mode(21, pigpio.OUTPUT)
    pi.set_mode(23, pigpio.OUTPUT)
    
    pi.wave_tx_stop()
    
    pi.write(19,0)
    pi.write(17,0)
    pi.write(21,0)
    pi.write(23,0)
    pi.write(12,0)
    
    root.destroy()

root=tk.Tk()
root.title("VRE Sample")
w=800
h=480
root.geometry("%dx%d+0+0" % (w,h))
root.attributes('-fullscreen',True)
root.focus_set()
root.bind("<Escape>",close)
action=Window(root)
tk.mainloop()
        
