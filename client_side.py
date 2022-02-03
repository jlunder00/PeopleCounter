"""
NAME: Jason Lunder 
CLASS: CPSC 321
DATE: December 16, 2021
HOMEWORK: Project
DESCRIPTION: SQL Database For Gonzaga Toilet Reviews
"""
import mysql.connector
import config
import tkinter as tk
from dbaccessor import DBAccessor

class GUI():
    def __init__(self, accessor, analyzer, recorder):
        self.database_access = accessor
        self.analyzer = analyzer
        self.recorder = recorder
        self.windows = {}
        self.window_pages = {}
        self.labels = {}
        self.entries = {}
        self.buttons = {}

        
    def check_credentials(self, username, password):
        qy =  "SELECT * FROM User_Profile"
        self.database_access.query_db(qy)
        result = self.database_access.get_rs()

        for (cuser, cpass) in result:
            if username == cuser and password == cpass:
                return True

    def hide_all(self, window, page):
        for label in self.labels[window][page].values():
            self.hide(label)
        
        for entry in self.entries[window][page].values():
            self.hide(entry)

        for button in self.buttons[window][page].values():
            self.hide(button)

    def hide_page(self, window, page):
        self.hide(self.window_pages[window][page])

    def show_page(self, window, page, side):
        self.show(self.window_pages[window][page], side)

    def hide(self, widget):
        widget.pack_forget()
    
    def show(self, widget, side):
        widget.pack(side=side)
    
    def get_widget(self, type, window, page, name):
        if type == 'label':
            return self.labels[window][page][name]
        elif type == 'entry':
            return self.entries[window][page][name]
        elif type == 'button': 
            return self.buttons[window][page][name]
        else:
            return None

    def show_by_name(self, type, window, page, name, side):
        widget = self.get_widget(type, window, page, name)
        if widget is not None:
            self.show(widget, side)   
   
    def hide_by_name(self, type, window, page, name, side):
        widget = self.get_widget(type, window, page, name)
        if widget is not None:
            self.show(widget, side)   
    
    def set_up_page_dictionaries(self, window, frame_names, frame_sides):
        for i in range(len(frame_names)):
            frame_name = frame_names[i]
            frame_side = frame_sides[i]
            self.window_pages[window][frame_name] = tk.Frame(window)
            self.window_pages[window][frame_name].pack(side=frame_side)
            self.labels[window][frame_name] = {}
            self.entries[window][frame_name] = {}
            self.buttons[window][frame_name] = {}

    def front_page(self):
        window = tk.Tk()
        self.windows['Main_Window'] = window
        self.window_pages[window] = {}
        self.labels[window] = {}
        self.entries[window] = {}
        self.buttons[window] = {}
        self.login_page(window)
        window.mainloop()
    


    def login_page(self, window):
        frame_names = ['Login_top', 'Login_left', 'Login_bottom', 'Login_right']
        frame_sides = ['top', 'left', 'bottom', 'right']
        self.set_up_page_dictionaries(window, frame_names, frame_sides)
        self.set_up_login_page(window)

    def set_up_login_page(self, window):
        window.title("Next Gen Tech Bar People Counter Access")
        window.geometry("850x600")

        self.labels[window]['Login_top']['Main Label'] = tk.Label(self.window_pages[window]['Login_top'], text="People Counter Access", font=("Helvetica", 50))
        self.labels[window]['Login_top']['Main Label'].pack()

        self.labels[window]['Login_top']['Username Label'] = tk.Label(self.window_pages[window]['Login_top'], text="Username:", font=("Helvetica", 12))
        self.labels[window]['Login_top']['Username Label'].pack()
        
        self.entries[window]['Login_top']['Username Field'] = tk.Entry(self.window_pages[window]['Login_top'])
        self.entries[window]['Login_top']['Username Field'].pack() 

        self.labels[window]['Login_top']['Password Label'] = tk.Label(self.window_pages[window]['Login_top'], text="Password:", font=("Helvetica", 12))
        self.labels[window]['Login_top']['Password Label'].pack()

        self.entries[window]['Login_top']['Password Field'] = tk.Entry(self.window_pages[window]['Login_top'], show='*')
        self.entries[window]['Login_top']['Password Field'].pack()
        
        self.labels[window]['Login_top']['Wrong Password'] = tk.Label(self.window_pages[window]['Login_top'], text="Incorrect Password", font=("Helvetica", 12))

        #Function when button is clicked
        def enter_btn_clicked():
            username = self.entries[window]['Login_top']['Username Field'].get()
            password = self.entries[window]['Login_top']['Password Field'].get()
            verification = self.check_credentials(username, password)
            if verification == True:
                self.hide_page(window, 'Login_top')
                self.hide_page(window, 'Login_bottom')
                self.hide_page(window, 'Login_left')
                self.hide_page(window, 'Login_right')
                self.home_page(window)
            else:
                self.labels[window]['Login_top']['Wrong Password'].pack()

        def create_account_button_clicked():
            self.create_account_page()
        
        self.buttons[window]['Login_top']['Enter Button'] = tk.Button(self.window_pages[window]['Login_top'], text="Enter", command=enter_btn_clicked)
        self.buttons[window]['Login_top']['Enter Button'].pack()
        
        self.buttons[window]['Login_bottom']['Create Account Button'] = tk.Button(self.window_pages[window]['Login_bottom'], text="Create Account", command=create_account_button_clicked)
        self.buttons[window]['Login_bottom']['Create Account Button'].pack(side='right')
    
    def create_account_page(self):
        window = tk.Tk()
        window.title("Next Gen Tech Bar People Counter Account Creation")
        window.geometry("400x500")
        self.windows['Create_Account'] = window
        self.window_pages[window] = {}
        self.labels[window] = {}
        self.entries[window] = {}
        self.buttons[window] = {}
        frame_names = ['Create_Account']
        frame_sides = ['top']
        self.set_up_page_dictionaries(window, frame_names, frame_sides)
        self.set_up_create_account_page(window)

    def set_up_create_account_page(self, window):
        self.labels[window]['Create_Account']['Username Label'] = tk.Label(self.window_pages[window]['Create_Account'], text='Enter a username', font=("Helvetica", 12))
        self.labels[window]['Create_Account']['Username Label'].pack()

        self.entries[window]['Create_Account']['Username Field'] = tk.Entry(self.window_pages[window]['Create_Account'])
        self.entries[window]['Create_Account']['Username Field'].pack() 

        self.labels[window]['Create_Account']['Password Label'] = tk.Label(self.window_pages[window]['Create_Account'], text='Enter a passwprd', font=("Helvetica", 12))
        self.labels[window]['Create_Account']['Password Label'].pack()
        
        self.entries[window]['Create_Account']['Password Field'] = tk.Entry(self.window_pages[window]['Create_Account'], show='*')
        self.entries[window]['Create_Account']['Password Field'].pack()

        def create_button_clicked(): 
            new_username = self.entries[window]['Create_Account']['Username Field'].get()
            new_password = self.entries[window]['Create_Account']['Password Field'].get()
            query = '''SELECT username FROM User_Profile WHERE username = %s'''
            self.database_access.query_db(query, (new_username,))
            rs = self.database_access.get_rs()
            row = rs.fetchone()
            if(row != None):
                if 'Bad Input' not in self.labels[window]['Create_Account'].keys():
                    self.labels[window]['Create_Account']['Bad Input'] = tk.Label(window, text="An account with this username already exists", font=("Helvetica",12))
                    self.labels[window]['Create_Account']['Bad Input'].pack()
            else:
                input_query = '''INSERT INTO User_Profile Values (%s, %s)'''
                self.database_access.query_db(input_query, (new_username, new_password))
                self.delete_window(window)

        self.buttons[window]['Create_Account']['Create Button'] = tk.Button(self.window_pages[window]['Create_Account'], text="Enter", command=create_button_clicked)
        self.buttons[window]['Create_Account']['Create Button'].pack()


    def delete_window(self, window):
        self.labels.pop(window)
        self.entries.pop(window)
        self.buttons.pop(window)
        window.destroy()


    def results_window(self, name, title, txt):
        win_name='Results '+name
        window = tk.Tk()
        window.title(title)
        window.geometry("400x900")
        self.windows[win_name] = window
        self.window_pages[window] = {}
        self.labels[window] = {}
        self.entries[window] = {}
        self.buttons[window] = {}

        frame_names = ['Results_top']
        frame_sides = ['top']
        self.set_up_page_dictionaries(window, frame_names, frame_sides)
        self.set_up_results_page(window, txt)
        window.mainloop()

    def set_up_results_page(self, window, text):
        def back_button_clicked():
            self.delete_window(window)

        self.buttons[window]['Results_top']['back'] = tk.Button(self.window_pages[window]['Results_top'], text = 'Back', command=back_button_clicked)
        self.buttons[window]['Results_top']['back'].pack()

        self.labels[window]['Results_top']['results'] = tk.Label(self.window_pages[window]['Results_top'], text=text, font=("Helvetica", 12))
        self.labels[window]['Results_top']['results'].pack() 


            
        
                

    def home_page(self, window):
        frame_names = ['Home_top', 'Home_left', 'Home_bottom', 'Home_right']
        frame_sides = ['top', 'left', 'bottom', 'right']
        self.set_up_page_dictionaries(window, frame_names, frame_sides)
        self.set_up_home_page(window)
        
    def set_up_home_page(self, window): 
        self.labels[window]['Home_top']['Title'] = tk.Label(self.window_pages[window]['Home_top'], text="People Counter Access", font=("Helvetica", 50))
        self.labels[window]['Home_top']['Title'].pack()

        self.labels[window]['Home_left']['Analysis'] = tk.Label(self.window_pages[window]['Home_left'], text="Analytics", font=("Helvetica", 12))
        self.labels[window]['Home_left']['Analysis'].pack()

        def num_walk_ins_clicked():
            rs = self.analyzer.get_number_of_walk_ins()
            num = rs.fetchone()
            print(rs, num, num[0])
            name = 'Total Walk Ins'
            title = 'Total Number of Walk Ins'
            txt = 'Number of Walk Ins\n\n'+str(num[0])
            self.results_window(name, title, txt)
        
        self.buttons[window]['Home_left']['num_walk_ins'] = tk.Button(self.window_pages[window]['Home_left'], text = 'Get Number Of Walk Ins', command=num_walk_ins_clicked)
        self.buttons[window]['Home_left']['num_walk_ins'].pack()

        self.labels[window]['Home_left']['Walk_In_Between_Times'] = tk.Label(self.window_pages[window]['Home_left'], text="Input Time Range", font=("Helvetica", 12))
        self.labels[window]['Home_left']['Walk_In_Between_Times'].pack()
        
        self.labels[window]['Home_left']['Start Time Label'] = tk.Label(self.window_pages[window]['Home_left'], text='Enter a start time in hh:mm:ss', font=("Helvetica", 12))
        self.labels[window]['Home_left']['Start Time Label'].pack()

        self.entries[window]['Home_left']['Start Time Field'] = tk.Entry(self.window_pages[window]['Home_left'])
        self.entries[window]['Home_left']['Start Time Field'].pack() 

        self.labels[window]['Home_left']['End Time Label'] = tk.Label(self.window_pages[window]['Home_left'], text='Enter a end time in hh:mm:ss', font=("Helvetica", 12))
        self.labels[window]['Home_left']['End Time Label'].pack()
        
        self.entries[window]['Home_left']['End Time Field'] = tk.Entry(self.window_pages[window]['Home_left'])
        self.entries[window]['Home_left']['End Time Field'].pack()

        def num_walk_ins_in_time_period_clicked():
            start = self.entries[window]['Home_left']['Start Time Field'].get() 
            end = self.entries[window]['Home_left']['End Time Field'].get()
            
            rs = self.analyzer.get_number_of_walk_ins_between_times(start, end)
            num = rs.fetchone()
            name = 'Walk_Ins_In_Time'
            txt = 'Number of Walk Ins Between '+start+' and '+end+'\n\n'+str(num[0])
            title = 'Results - Walk ins in time period'
            self.results_window(name, title, txt)

        self.buttons[window]['Home_left']['num_walk_ins_in_time'] = tk.Button(self.window_pages[window]['Home_left'], text = 'Get Number Of Walk Ins In Time Period', command=num_walk_ins_in_time_period_clicked)
        self.buttons[window]['Home_left']['num_walk_ins_in_time'].pack()
        

        self.labels[window]['Home_left']['Walk_In_By_Service'] = tk.Label(self.window_pages[window]['Home_left'], text="Get Walk ins by service", font=("Helvetica", 12))
        self.labels[window]['Home_left']['Walk_In_By_Service'].pack()
        
        self.labels[window]['Home_left']['Walk_In_By_Service'] = tk.Label(self.window_pages[window]['Home_left'], text="Enter a Service (optional)", font=("Helvetica", 12))
        self.labels[window]['Home_left']['Walk_In_By_Service'].pack()

        self.entries[window]['Home_left']['Walk_In_By_Service'] = tk.Entry(self.window_pages[window]['Home_left'])
        self.entries[window]['Home_left']['Walk_In_By_Service'].pack() 


        def num_walk_ins_by_service_clicked():
            service = self.entries[window]['Home_left']['Walk_In_By_Service'].get() 
            print(service)
            if service == '':
                service = None
            rs = self.analyzer.get_number_of_walk_ins_by_service(service)
            txt = 'Number of Walk Ins by service\n\n'
            for (service, count) in rs:
                txt += 'Service: '+service+ ' Count: '+count + '\n\n'
            name = 'Walk_Ins_In_Time'
            title = 'Results - Walk ins by service'
            self.results_window(name, title, txt)

        self.buttons[window]['Home_left']['Walk_In_By_Service'] = tk.Button(self.window_pages[window]['Home_left'], text = 'Get Number Of Walk Ins By Service', command=num_walk_ins_by_service_clicked)
        self.buttons[window]['Home_left']['Walk_In_By_Service'].pack()

        self.labels[window]['Home_left']['Average_Time_Inside_By_Service'] = tk.Label(self.window_pages[window]['Home_left'], text="Get average time inside by service", font=("Helvetica", 12))
        self.labels[window]['Home_left']['Average_Time_Inside_By_Service'].pack()
        
        self.labels[window]['Home_left']['Average_Time_Inside_By_Service_Field_Label'] = tk.Label(self.window_pages[window]['Home_left'], text="Enter a Service (optional)", font=("Helvetica", 12))
        self.labels[window]['Home_left']['Average_Time_Inside_By_Service_Field_Label'].pack()

        self.entries[window]['Home_left']['Average_Time_Inside_By_Service'] = tk.Entry(self.window_pages[window]['Home_left'])
        self.entries[window]['Home_left']['Average_Time_Inside_By_Service'].pack() 

        self.labels[window]['Home_left']['Average_Time_Inside_By_Service_Order'] = tk.Label(self.window_pages[window]['Home_left'], text="Enter ASC or DESC to sort", font=("Helvetica", 12))
        self.labels[window]['Home_left']['Average_Time_Inside_By_Service_Order'].pack()

        self.entries[window]['Home_left']['Average_Time_Inside_By_Service_Order'] = tk.Entry(self.window_pages[window]['Home_left'])
        self.entries[window]['Home_left']['Average_Time_Inside_By_Service_Order'].pack() 

        def average_time_inside_by_service_clicked():
            service = self.entries[window]['Home_left']['Average_Time_Inside_By_Service'].get()
            order = ''''''+self.entries[window]['Home_left']['Average_Time_Inside_By_Service_Order'].get()
            if service == '':
                service = None
            rs = self.analyzer.average_time_spent_inside_by_service(order, service)
            txt = 'Average Time Spent Inside by service\n\n'
            for (service, time) in rs:
                txt += 'Service: '+str(service)+ ' Average Time: '+str(time) + '\n\n'
            name = 'Average_Time_Inside_By_Service'
            title = 'Results - Walk ins average time inside by service'
            self.results_window(name, title, txt)

        self.buttons[window]['Home_left']['Average_Time_Inside_By_Service'] = tk.Button(self.window_pages[window]['Home_left'], text = 'Get Number Of Walk Ins By Service', command=average_time_inside_by_service_clicked)
        self.buttons[window]['Home_left']['Average_Time_Inside_By_Service'].pack()


        def filter_tickets_clicked():
            self.ticket_filter_window()

        self.buttons[window]['Home_left']['Filter_Tickets'] = tk.Button(self.window_pages[window]['Home_left'], text = 'Filter Tickets', command=filter_tickets_clicked)
        self.buttons[window]['Home_left']['Filter_Tickets'].pack()

        self.labels[window]['Home_right']['Add Data'] = tk.Label(self.window_pages[window]['Home_left'], text="Adding Data:", font=("Helvetica", 12))
        self.labels[window]['Home_right']['Add Data'].pack()

        def record_walk_in_clicked():
            self.record_walk_in_window()

        def add_walk_in_time_out_clicked():
            self.add_walk_in_time_out_window()

        self.buttons[window]['Home_right']['record_walk_in'] = tk.Button(self.window_pages[window]['Home_right'], text = 'Record a Walk In', command=record_walk_in_clicked)
        self.buttons[window]['Home_right']['record_walk_in'].pack()
        
        self.buttons[window]['Home_right']['add_walk_in_time_out'] = tk.Button(self.window_pages[window]['Home_right'], text = 'Record a Walk Ins exit time', command=add_walk_in_time_out_clicked)
        self.buttons[window]['Home_right']['add_walk_in_time_out'].pack()
    
    def record_walk_in_window(self):
        window = tk.Tk()
        window.title('record walk in')
        window.geometry('600x300')
        self.windows['Record Walk In'] = window
        self.window_pages[window] = {}
        self.labels[window] = {}
        self.entries[window] = {}
        self.buttons[window] = {}

        frame_names = ['WI_top']
        frame_sides = ['top']
        self.set_up_page_dictionaries(window, frame_names, frame_sides)
        self.set_up_WI_page(window)
    
    def set_up_WI_page(self, window):
        page = 'WI_top'
        def back_button_clicked():
            self.delete_window(window)

        self.buttons[window][page]['back'] = tk.Button(self.window_pages[window][page], text = 'Back', command=back_button_clicked)
        self.buttons[window][page]['back'].pack()

        self.labels[window][page]['height'] = tk.Label(self.window_pages[window][page], text="height:")
        self.labels[window][page]['height'].pack(side='top')
        self.entries[window][page]['height'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['height'].pack(side='top')
        height = self.entries[window][page]['height']

        self.labels[window][page]['enter_time'] = tk.Label(self.window_pages[window][page], text="enter_time:")
        self.labels[window][page]['enter_time'].pack(side='top')
        self.entries[window][page]['enter_time'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['enter_time'].pack(side='top')
        enter_time = self.entries[window][page]['enter_time']

        self.labels[window][page]['enter_date'] = tk.Label(self.window_pages[window][page], text="enter_date:")
        self.labels[window][page]['enter_date'].pack(side='top')
        self.entries[window][page]['enter_date'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['enter_date'].pack(side='top')
        enter_date = self.entries[window][page]['enter_date']
        
        def submit_button_clicked():
            h = height.get()
            et = enter_time.get()
            ed = enter_date.get()
            
            self.recorder.record_walk_in(h, et, ed)

        submit_btn = tk.Button(self.window_pages[window][page], text="submit",command=submit_button_clicked)
        submit_btn.pack()



    def add_walk_in_time_out_window(self):
        window = tk.Tk()
        window.title('add walk in time out')
        window.geometry('600x300')
        self.windows['Add Walk In time out'] = window
        self.window_pages[window] = {}
        self.labels[window] = {}
        self.entries[window] = {}
        self.buttons[window] = {}

        frame_names = ['WITO_top']
        frame_sides = ['top']
        self.set_up_page_dictionaries(window, frame_names, frame_sides)
        self.set_up_WITO_page(window)
    
    def set_up_WITO_page(self, window):
        page = 'WITO_top'
        def back_button_clicked():
            self.delete_window(window)

        self.buttons[window][page]['back'] = tk.Button(self.window_pages[window][page], text = 'Back', command=back_button_clicked)
        self.buttons[window][page]['back'].pack()

        self.labels[window][page]['height'] = tk.Label(self.window_pages[window][page], text="height:")
        self.labels[window][page]['height'].pack(side='top')
        self.entries[window][page]['height'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['height'].pack(side='top')
        height = self.entries[window][page]['height']

        self.labels[window][page]['enter_time'] = tk.Label(self.window_pages[window][page], text="enter_time:")
        self.labels[window][page]['enter_time'].pack(side='top')
        self.entries[window][page]['enter_time'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['enter_time'].pack(side='top')
        enter_time = self.entries[window][page]['enter_time']

        self.labels[window][page]['enter_date'] = tk.Label(self.window_pages[window][page], text="enter_date:")
        self.labels[window][page]['enter_date'].pack(side='top')
        self.entries[window][page]['enter_date'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['enter_date'].pack(side='top')
        enter_date = self.entries[window][page]['enter_date']
        
        self.labels[window][page]['exit_time'] = tk.Label(self.window_pages[window][page], text="exit_time:")
        self.labels[window][page]['exit_time'].pack(side='top')
        self.entries[window][page]['exit_time'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['exit_time'].pack(side='top')
        exit_time = self.entries[window][page]['exit_time']
        
        self.labels[window][page]['exit_date'] = tk.Label(self.window_pages[window][page], text="exit_date:")
        self.labels[window][page]['exit_date'].pack(side='top')
        self.entries[window][page]['exit_date'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['exit_date'].pack(side='top')
        exit_date = self.entries[window][page]['exit_date']
        
        def submit_button_clicked():
            h = height.get()
            et = enter_time.get()
            ed = enter_date.get()
            ext = exit_time.get()
            exd = exit_date.get()
            
            self.recorder.add_walk_in_time_out(h, et, ed, ext, exd)
        
        submit_btn = tk.Button(self.window_pages[window][page], text="submit",command=submit_button_clicked)
        submit_btn.pack()
        



    def ticket_filter_window(self):
        window = tk.Tk()
        window.title('Filter Tickets')
        window.geometry('600x300')
        self.windows['Ticket_Filter'] = window
        self.window_pages[window] = {}
        self.labels[window] = {}
        self.entries[window] = {}
        self.buttons[window] = {}

        frame_names = ['TF_top']
        frame_sides = ['top']
        self.set_up_page_dictionaries(window, frame_names, frame_sides)
        self.set_up_TF_page(window)

    def set_up_TF_page(self, window):
        page = 'TF_top'
        def back_button_clicked():
            self.delete_window(window)

        self.buttons[window][page]['back'] = tk.Button(self.window_pages[window][page], text = 'Back', command=back_button_clicked)
        self.buttons[window][page]['back'].pack()


        self.labels[window][page]['Item_Num'] = tk.Label(self.window_pages[window][page], text="Ticket Id Number:")
        self.labels[window][page]['Item_Num'].pack(side='top')
        self.entries[window][page]['Item_Num'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['Item_Num'].pack(side='top')
        id_num = self.entries[window][page]['Item_Num']


        status = tk.StringVar(self.window_pages[window][page])
        status.set("New")
        filter_status = tk.OptionMenu(self.window_pages[window][page], status, 'New', 'In Proccess', 'Open', 'On Hold', 'Resolved', 'Closed')

        filter_status.pack(side='top')
        
        self.labels[window][page]['service'] = tk.Label(self.window_pages[window][page], text="Service:")
        self.labels[window][page]['service'].pack(side='top')
        self.entries[window][page]['service'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['service'].pack(side='top')
        service = self.entries[window][page]['service']


        self.labels[window][page]['asc_desc'] = tk.Label(self.window_pages[window][page], text="Enter ASC or DESC:")
        self.labels[window][page]['asc_desc'].pack(side='top')
        self.entries[window][page]['asc_desc'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['asc_desc'].pack(side='top')
        asc_desc = self.entries[window][page]['asc_desc']


        self.labels[window][page]['subject'] = tk.Label(self.window_pages[window][page], text="Subject:")
        self.labels[window][page]['subject'].pack(side='top')
        self.entries[window][page]['subject'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['subject'].pack(side='top')
        subject = self.entries[window][page]['subject']

        self.labels[window][page]['Description'] = tk.Label(self.window_pages[window][page], text="Description:")
        self.labels[window][page]['Description'].pack(side='top')
        self.entries[window][page]['Description'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['Description'].pack(side='top')
        description = self.entries[window][page]['Description']


        self.labels[window][page]['Requestor'] = tk.Label(self.window_pages[window][page], text="Requestor:")
        self.labels[window][page]['Requestor'].pack(side='top')
        self.entries[window][page]['Requestor'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['Requestor'].pack(side='top')
        requestor = self.entries[window][page]['Requestor']
       
        self.labels[window][page]['Responsible'] = tk.Label(self.window_pages[window][page], text="Responsible:")
        self.labels[window][page]['Responsible'].pack(side='top')
        self.entries[window][page]['Responsible'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['Responsible'].pack(side='top')
        responsible = self.entries[window][page]['Responsible']

        self.labels[window][page]['height'] = tk.Label(self.window_pages[window][page], text="height:")
        self.labels[window][page]['height'].pack(side='top')
        self.entries[window][page]['height'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['height'].pack(side='top')
        height = self.entries[window][page]['height']
        
        self.labels[window][page]['enter_time'] = tk.Label(self.window_pages[window][page], text="enter_time:")
        self.labels[window][page]['enter_time'].pack(side='top')
        self.entries[window][page]['enter_time'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['enter_time'].pack(side='top')
        enter_time = self.entries[window][page]['enter_time']
        

        self.labels[window][page]['enter_date'] = tk.Label(self.window_pages[window][page], text="enter_date:")
        self.labels[window][page]['enter_date'].pack(side='top')
        self.entries[window][page]['enter_date'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['enter_date'].pack(side='top')
        enter_date = self.entries[window][page]['enter_date']

        self.labels[window][page]['exit_time'] = tk.Label(self.window_pages[window][page], text="exit_time:")
        self.labels[window][page]['exit_time'].pack(side='top')
        self.entries[window][page]['exit_time'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['exit_time'].pack(side='top')
        exit_time = self.entries[window][page]['exit_time']

        self.labels[window][page]['exit_date'] = tk.Label(self.window_pages[window][page], text="exit_date:")
        self.labels[window][page]['exit_date'].pack(side='top')
        self.entries[window][page]['exit_date'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['exit_date'].pack(side='top')
        exit_date = self.entries[window][page]['exit_date']
        
        self.labels[window][page]['last_modifier'] = tk.Label(self.window_pages[window][page], text="last_modifier:")
        self.labels[window][page]['last_modifier'].pack(side='top')
        self.entries[window][page]['last_modifier'] = tk.Entry(self.window_pages[window][page])
        self.entries[window][page]['last_modifier'].pack(side='top')
        last_modifier = self.entries[window][page]['last_modifier']


        def filter_btn_clicked():
            id_num_button = id_num.get()
            status_button = status.get()
            service_button = service.get()
            subject_button = subject.get()
            description_button = description.get()
            requestor_button = requestor.get()
            responsible_button = responsible.get()
            h_button = height.get()
            et_button = enter_time.get()
            ed_button = enter_date.get()
            ext_button = exit_time.get()
            exd_button = exit_date.get()
            last_mod_button = last_modifier.get()
            rs = self.analyzer.get_tickets_filtered(id_num_button, status_button, service_button, subject_button, description_button, requestor_button, responsible_button, h_button, et_button, ed_button, ext_button, exd_button, last_mod_button)
            txt = ""
            for (id, st, sr, sub, descr, req, resp, h, en_t, en_d, ex_t, ex_d, l_m) in rs:
                txt += 'id: '+id+' status: '+st+' service: '+sr+' subject: '+sub+' description: '+descr+' requestor: '+req+' responsible: '+resp+' height: '+h+' enter time: '+en_t+' enter date: '+en_d+' exit time: '+ex_t+' exit date: '+ex_d+' last modifier: '+l_m+'\n\n'

            self.results_window('Filtered Tickets', 'Filtered Tickets', txt)
                
        
        filter_btn = tk.Button(self.window_pages[window][page], text="Filter",command=filter_btn_clicked)
        filter_btn.pack(side='left')


        

