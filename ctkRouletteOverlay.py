import customtkinter as tk
#from tkinter import ttk
"""
Copyright (C) 2023 eXtremeVisionGaming # EMAIL: west@extremevisiongaming.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

class OverlayWindow:
    def __init__(self, root):
        self.root = root
        self.geometry = "500x300+70+630"
        self.counter = 0
        self.payout = 36
        self.bet_modifier = 2
        self.sets = 0
        self.max_set_limit = self.payout * 0.5
        self.min_set_limit = 1
        self.set_limit = int(self.max_set_limit * 0.9)
        self.starting_bet = 50000
        self.bet = self.starting_bet
        self.total_cost = 0
        self.profit = 0
        self.probability = 1 - ((self.payout/(self.payout + 1)) ** (self.counter))
        self.odds = 100 * self.probability
        # Create a frame to hold the button and counter
        self.frame = tk.CTkFrame(self.root)
        self.frame.pack()

        # Create a label to display the total bets
        self.counter_label = tk.CTkLabel(self.frame, text="Total bets: 0    |    Total cost: 0 GP\nSets: 0 | Profit: 0 GP | Odds: {:.2f}%".format(self.odds))
        self.counter_label.pack()

        # Create a button and displays the value of the bet variable
        self.increment_button = tk.CTkButton(self.frame, text=f"Bet: {format(self.bet, ',')} GP", command=self.increment_counter, width=90, height=60)
        self.increment_button.pack()

        # Create a frame to hold the reset and settings buttons
        self.button_frame = tk.CTkFrame(self.frame)
        self.button_frame.pack(side='left')

        # Add a reset button
        self.reset_button = tk.CTkButton(self.button_frame, text="Reset", command=self.reset_counter, width=40, height=30)
        self.reset_button.pack(side='left')

        # Add a button to open the settings window
        self.settings_button = tk.CTkButton(self.button_frame, text="Settings", command=self.open_settings_window, width=40, height=30)
        self.settings_button.pack(side='left')

        # Add a button to Donate
        self.donate_button = tk.CTkButton(self.button_frame, text="Donate", command=self.open_donate_window, width=40, height=30)
        self.donate_button.pack(side='left')

        # Add a button to open a table of odds, total cost, and profit
        self.table_button = tk.CTkButton(self.button_frame, text="Table", command=self.open_table_window, width=40, height=30)
        self.table_button.pack(side='left')

        # Add a button to change the active currency
        self.active_currency = tk.StringVar()  # variable to store the active currency
        self.active_currency.set("GP")  # set the initial value of the variable

        self.active_currency = tk.CTkOptionMenu(self.button_frame, values=["GP", "$", "crypto"], command=self.update_increment_button, width=40, height=30)
        self.active_currency.pack(side='left')
        #self.active_currency.trace("w", self.update_increment_button)


    

    def update_increment_button(self, *args):
        self.reset_counter()
        if self.active_currency.get() == "GP":
            self.total_cost = 0
            self.starting_bet = int(50000)
            self.switch_currency()
        elif self.active_currency.get() == "$":
            self.total_cost = tk.DoubleVar()
            self.starting_bet = tk.DoubleVar()
            self.starting_bet.set(0.01)
            self.switch_currency()
        elif self.active_currency.get() == "crypto":
            self.total_cost = tk.DoubleVar()
            self.starting_bet = tk.DoubleVar()
            self.starting_bet.set(0.00000500)
            self.switch_currency()
            
        
        
       

    def open_table_window(self):
        # Create a new top-level window
        self.table_window = tk.CTkToplevel(self.root)
        self.table_window.geometry("500x700+850+100")
        self.table_window.title("Table")
        # display a table of odds, total cost, and profit for 200 bets
        tk.CTkLabel(self.table_window, text="            Bets      |           Total Cost         |                   Profit        |                  Odds         ", justify='left', anchor="w").grid(row=0, column=0, sticky="w")
        
        self.table_window.grid_rowconfigure(1, weight=1)
        self.table_window.grid_columnconfigure(0, weight=1)
        # set pretable values
        self.pretable_total_cost = self.total_cost
        self.pretable_profit = self.profit
        self.pretable_bet = self.bet
        self.pretable_odds = self.odds
        self.pretable_sets = self.sets

        # create scrollable frame
        self.scrollable_frame = tk.CTkScrollableFrame(self.table_window)
        self.scrollable_frame.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        
        table_text = []
        for i in range(200):
            self.increment_counter()
            if self.active_currency.get() == "GP":
                bet_text = f"  {self.counter:03} {format(self.total_cost, ',.0f'):>30} {format(self.profit, ',.0f'):>30} {format(self.odds, '.2f'):>24}%"
            elif self.active_currency.get() == "$":
                bet_text = f"  {self.counter:03} {format(self.total_cost, ',.2f'):>30} {format(self.profit, ',.2f'):>30} {format(self.odds, '.2f'):>24}%"
            elif self.active_currency.get() == "crypto":
                bet_text = f"  {self.counter:03} {format(self.total_cost, ',.8f'):>30} {format(self.profit, ',.8f'):>30} {format(self.odds, '.2f'):>24}%"
            
            tk.CTkLabel(self.scrollable_frame, text=bet_text).grid(row=i, column=0, padx=10, pady=5, sticky="w")

        scrollbar = tk.CTkScrollbar(self.table_window)
      
        # subtract 200 from counter and update the label on close
        self.table_window.protocol("WM_DELETE_WINDOW", self.close_table_window)

    

    def close_table_window(self):
        self.counter -= 200
        self.total_cost = self.pretable_total_cost
        self.profit = self.pretable_profit
        self.bet = self.pretable_bet
        self.odds = self.pretable_odds
        self.sets = self.pretable_sets
        self.update_counter_label()
        self.table_window.destroy()    
       

    def open_donate_window(self):
        # Create a new top-level window
        self.donate_window = tk.CTkToplevel(self.root)
        self.donate_window.geometry("550x170+400+200")
        self.donate_window.title("Donate")

        tk.CTkLabel(self.donate_window, text="Your success with this tool is a testament to its value.\nIf you'd like to support the developer and help continue to improve and create great products,\nplease consider donating through one of these options.").pack()
        tk.CTkLabel(self.donate_window, text="Paypal:").pack()
        tk.CTkLabel(self.donate_window, text="https://paypal.me/XvGwest").pack()
        tk.CTkLabel(self.donate_window, text="ETH:").pack()
        tk.CTkLabel(self.donate_window, text="0x712ac061FCDAC3b7861D367D3bF995d814775F66").pack()


    def open_settings_window(self):
        # Create a new top-level window
        self.settings_window = tk.CTkToplevel(self.root)
        self.settings_window.geometry("300x300+450+200")
        self.settings_window.title("Settings")
        
        # set presettings values
        self.presettings_payout = self.payout
        self.presettings_bet_modifier = self.bet_modifier
        self.presettings_starting_bet = self.starting_bet


        
        # Add a label and text entry widget for the payout value with a default value of 36
        tk.CTkLabel(self.settings_window, text="Payout:").pack()
        self.payout_entry = tk.CTkEntry(self.settings_window)
        self.payout_entry.insert(0, str(round(self.payout)))
        self.payout_entry.bind("<FocusOut>", self.update_set_limit)
        self.payout_entry.pack()


        # Add a label and text entry widget for the bet modifier value
        tk.CTkLabel(self.settings_window, text="Bet Multiplier:").pack()
        self.bet_modifier_entry = tk.CTkEntry(self.settings_window)
        self.bet_modifier_entry.insert(0, "2")
        self.bet_modifier_entry.pack()

        # Add a label and text entry widget for the starting bet value
        tk.CTkLabel(self.settings_window, text="Starting bet:").pack()
        self.starting_bet_entry = tk.CTkEntry(self.settings_window)
        if self.active_currency.get() == "GP":
            self.starting_bet_entry.insert(0, "50000")
        elif self.active_currency.get() == "$":
            self.starting_bet_entry.insert(0, "0.01")
        elif self.active_currency.get() == "crypto":
            self.starting_bet_entry.insert(0, "0.00000500")
        self.starting_bet_entry.pack()

        # Add a label and text entry widget for the set limit value
        tk.CTkLabel(self.settings_window, text="Set limit:").pack()
        self.set_limit_entry = tk.CTkEntry(self.settings_window)
        self.set_limit_entry.insert(0, str(round(self.set_limit)))
        self.set_limit_entry.pack()

        # Add a label to the settings window
        self.recommended_label = tk.CTkLabel(self.settings_window, text=f"Set limit 1 - {round(self.max_set_limit)}\n1 is agressive raising after every bet.\nrecommended to stay between 1-{round(self.max_set_limit)}")
        self.recommended_label.pack()



        # Add a button to close the window and update the relevant variables
        tk.CTkButton(self.settings_window, text="Save", command=self.close_settings_window).pack()

    def update_set_limit(self, *args):
        
        self.payout = float(self.payout_entry.get())
        self.max_set_limit = self.payout * 0.5
        self.set_limit = int(self.max_set_limit * 0.9)
        self.set_limit_entry.delete(0,tk.END)
        self.set_limit_entry.insert(0, int(self.set_limit))
        self.recommended_label.configure(text=f"Set limit 1 - {int(self.max_set_limit)}\n1 is agressive raising after every bet.\nrecommended to stay between 1-{int(self.max_set_limit)}")
       
        
    def switch_currency(self):
        if self.active_currency.get() == "GP":
            self.starting_bet = int(50000)
        elif self.active_currency.get() == "$":
            self.starting_bet = float(0.01)
        elif self.active_currency.get() == "crypto":
            self.starting_bet = float(0.00000500)
    
        
        self.set_limit = int(self.set_limit)
        self.bet_modifier = float(self.bet_modifier)
    
        self.reset_counter()

    def close_settings_window(self):
        # Get the values from the text entry widgets
        if self.active_currency.get() == "GP":
            self.starting_bet = int(self.starting_bet_entry.get())
        elif self.active_currency.get() == "$":
            self.starting_bet = float(self.starting_bet_entry.get())
        elif self.active_currency.get() == "crypto":
            self.starting_bet = float(self.starting_bet_entry.get())
    
        self.payout = float(self.payout_entry.get())
        self.set_limit = int(self.set_limit_entry.get())
        self.bet_modifier = float(self.bet_modifier_entry.get())

        if self.payout == self.presettings_payout and self.bet_modifier == self.presettings_bet_modifier and self.starting_bet == self.presettings_starting_bet:
            self.settings_window.destroy()
            return
        else:

            self.update_set_limit()
            self.reset_counter()

            # Close the settings window
            self.settings_window.destroy()



    def reset_counter(self):
        self.counter = 0
        self.sets = 0
        self.bet = self.starting_bet
        self.total_cost = 0
        self.profit = 0
        self.probability = 1 - ((self.payout/(self.payout + 1)) ** (self.counter))
        self.odds = 100 * self.probability
        self.update_counter_label()

        

        


    def update_counter_label(self):
        if self.active_currency.get() == "GP":
            self.counter_label.configure(text=f"Total bets: {format(self.counter, ',.0f')}     |     Total cost: {format(int(self.total_cost), ',.0f')} GP\nSets of {self.set_limit}: {format(self.sets, ',.0f')} | Profit: {format(int(self.profit), ',.0f')} GP | Odds: {format(self.odds, '.2f')}%")
            self.increment_button.configure(text=f"Bet: {format(self.bet, ',')} GP")
        elif self.active_currency.get() == "$":
            self.counter_label.configure(text=f"Total bets: {format(self.counter, ',')}     |     Total cost: ${format(self.total_cost, ',.2f')}\nSets of {self.set_limit}: {format(self.sets, ',')} | Profit: ${format(self.profit, ',.2f')} | Odds: {format(self.odds, '.2f')}%")
            self.increment_button.configure(text=f"Bet: ${format(self.bet, ',.2f')}")
        elif self.active_currency.get() == "crypto":
            self.counter_label.configure(text=f"Total bets: {format(self.counter, ',')}     |     Total cost: Ξ{format(self.total_cost, ',.8f')}\nSets of {self.set_limit}: {format(self.sets, ',')} | Profit: Ξ{format(self.profit, ',.8f')} | Odds: {format(self.odds, '.2f')}%")
            self.increment_button.configure(text=f"Bet: Ξ{format(self.bet, ',.8f')}")


    def increment_counter(self):
        self.counter += 1
        if isinstance(self.bet, int):
            self.total_cost = int(self.total_cost + self.bet)
            self.profit = int(self.bet * self.payout - self.total_cost)
        else:
            self.total_cost = float(self.total_cost + self.bet)
            self.profit = float(self.bet * self.payout - self.total_cost)

        self.probability = 1 - ((self.payout/(self.payout + 1)) ** (self.counter))
        self.odds = 100 * self.probability
        
        if self.counter % self.set_limit == 0:
            self.sets += 1
            self.bet *= self.bet_modifier
        
        self.update_counter_label()
    
    
    

def main():
    root = tk.CTk()
    root.attributes("-topmost", True)
    root.title("Roulette Overlay")
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    # set customtkinter theme
    tk.set_appearance_mode("dark")
    tk.set_default_color_theme("dark-blue")
    


    if screen_height > 1080 and screen_width > 1920:
        icon_path = "./icons/icon128X128.ico"
    elif screen_height > 720 and screen_width > 1280:
        icon_path = "./icons/icon64X64.ico"
    else:
        icon_path = "./icons/icon32X32.ico"

    root.iconbitmap(icon_path)
    app = OverlayWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
