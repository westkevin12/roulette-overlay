import tkinter as tk
from tkinter import ttk
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
        self.counter = 0
        self.payout = 36
        self.bet_modifier = 2
        self.sets = 0
        self.max_set_limit = self.payout * 0.5
        self.min_set_limit = 1
        self.set_limit = 16
        self.starting_bet = 50000
        self.bet = self.starting_bet
        self.total_cost = 0
        self.profit = 0
        self.odds = 2.7
        # Create a frame to hold the button and counter
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Create a label to display the total bets
        self.counter_label = tk.Label(self.frame, text="Total bets: 0    |    Total cost: 0 GP\nSets: 0 | Profit: 0 GP | Odds: {:.2f}%".format(self.odds))
        self.counter_label.pack()

        # Create a button and displays the value of the bet variable
        self.increment_button = tk.Button(self.frame, text=f"Bet: {format(self.bet, ',')} GP", command=self.increment_counter, width=25, height=6)
        self.increment_button.pack()

        # Create a frame to hold the reset and settings buttons
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(side='left')

        # Add a reset button
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_counter)
        self.reset_button.pack(side='left')

        # Add a button to open the settings window
        self.settings_button = tk.Button(self.button_frame, text="Settings", command=self.open_settings_window)
        self.settings_button.pack(side='left')

        # Add a button to Donate
        self.donate_button = tk.Button(self.button_frame, text="Donate", command=self.open_donate_window)
        self.donate_button.pack(side='left')

        # Add a button to open a table of odds, total cost, and profit
        self.table_button = tk.Button(self.button_frame, text="Table", command=self.open_table_window)
        self.table_button.pack(side='left')

        # Add a button to change the active currency
        self.active_currency = tk.StringVar()  # variable to store the active currency
        self.active_currency.set("GP")  # set the initial value of the variable

        self.currency_dropdown = ttk.OptionMenu(self.button_frame, self.active_currency, "GP", "GP", "$", "crypto")
        self.currency_dropdown.pack(side='left')
        self.active_currency.trace("w", self.update_increment_button)


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
            self.starting_bet.set(0.00001)
            self.switch_currency()
            
        
        
       

    def open_table_window(self):
        # Create a new top-level window
        self.table_window = tk.Toplevel(self.root)
        self.table_window.geometry("400x600+400+150")

        # display a table of odds, total cost, and profit for 200 bets
        tk.Label(self.table_window, text="Bets   |         Total Cost       |                      Profit        |                         Odds         ", justify='left', anchor="w").pack()


        # set pretable values
        self.pretable_total_cost = self.total_cost
        self.pretable_profit = self.profit
        self.pretable_bet = self.bet
        self.pretable_odds = self.odds

        self.listbox = tk.Listbox(self.table_window)
        self.listbox.pack(expand=True, fill='both')
        for i in range(200):
            self.increment_counter()
            if self.active_currency.get() == "GP":
                self.listbox.insert(tk.END, f"  {self.counter:03} | {format(self.total_cost, ','):>30} | {format(self.profit, ','):>30} | {format(self.odds, '.2f'):>24}%")
            elif self.active_currency.get() == "$":
                self.listbox.insert(tk.END, f"  {self.counter:03} | {format(self.total_cost, ',.2f'):>30} | {format(self.profit, ',.2f'):>30} | {format(self.odds, '.2f'):>24}%")
            elif self.active_currency.get() == "crypto":
                self.listbox.insert(tk.END, f"  {self.counter:03} | {format(self.total_cost, ',.5f'):>30} | {format(self.profit, ',.5f'):>30} | {format(self.odds, '.2f'):>24}%")
            

        scrollbar = tk.Scrollbar(self.table_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # subtract 200 from counter and update the label on close
        self.table_window.protocol("WM_DELETE_WINDOW", self.close_table_window)

    def close_table_window(self):
        self.counter -= 200
        self.total_cost = self.pretable_total_cost
        self.profit = self.pretable_profit
        self.bet = self.pretable_bet
        self.odds = self.pretable_odds
        self.update_counter_label()
        self.table_window.destroy()    
       

    def open_donate_window(self):
        # Create a new top-level window
        self.donate_window = tk.Toplevel(self.root)
        self.donate_window.geometry("400x140+400+200")

        tk.Label(self.donate_window, text="Your success with this tool is a testament to its value.\nIf you'd like to support the developer and help continue to improve and create great products,\nplease consider donating through one of these options.").pack()
        tk.Label(self.donate_window, text="Paypal:").pack()
        tk.Label(self.donate_window, text="https://paypal.me/XvGwest").pack()
        tk.Label(self.donate_window, text="ETH:").pack()
        tk.Label(self.donate_window, text="0x712ac061FCDAC3b7861D367D3bF995d814775F66").pack()


    def open_settings_window(self):
        # Create a new top-level window
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.geometry("300x250+400+200")


        # Add a label and text entry widget for the payout value with a default value of 36
        tk.Label(self.settings_window, text="Payout:").pack()
        self.payout_entry = tk.Entry(self.settings_window)
        self.payout_entry.insert(0, "36")
        self.payout_entry.pack()


        # Add a label and text entry widget for the bet modifier value
        tk.Label(self.settings_window, text="Bet Multiplier:").pack()
        self.bet_modifier_entry = tk.Entry(self.settings_window)
        self.bet_modifier_entry.insert(0, "2")
        self.bet_modifier_entry.pack()

        # Add a label and text entry widget for the starting bet value
        tk.Label(self.settings_window, text="Starting bet:").pack()
        self.starting_bet_entry = tk.Entry(self.settings_window)
        if self.active_currency.get() == "GP":
            self.starting_bet_entry.insert(0, "50000")
        elif self.active_currency.get() == "$":
            self.starting_bet_entry.insert(0, "0.01")
        elif self.active_currency.get() == "crypto":
            self.starting_bet_entry.insert(0, "0.0000100000000000")
        self.starting_bet_entry.pack()

        # Add a label and text entry widget for the set limit value
        tk.Label(self.settings_window, text="Set limit:").pack()
        self.set_limit_entry = tk.Entry(self.settings_window)
        self.set_limit_entry.insert(0, "16")
        self.set_limit_entry.pack()

        # Add a label to the settings window
        tk.Label(self.settings_window, text=f"Set limit 1 - {round(self.max_set_limit)}\n1 is agressive raising after every bet.\nrecommended to stay between 1-{round(self.max_set_limit)}").pack()



        # Add a button to close the window and update the relevant variables
        tk.Button(self.settings_window, text="Save", command=self.close_settings_window).pack()

    def switch_currency(self):
        if self.active_currency.get() == "GP":
            self.starting_bet = int(50000)
        elif self.active_currency.get() == "$":
            self.starting_bet = float(0.01)
        elif self.active_currency.get() == "crypto":
            self.starting_bet = float(0.0000100000000000)
    
        self.payout = int(36)
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
    
        self.payout = int(self.payout_entry.get())
        self.set_limit = int(self.set_limit_entry.get())
        self.bet_modifier = float(self.bet_modifier_entry.get())
        
        # Update the max set limit
        self.max_set_limit = self.payout * 0.5
    
        self.reset_counter()

        # Close the settings window
        self.settings_window.destroy()



    def reset_counter(self):
        self.counter = 0
        self.sets = 0
        self.bet = self.starting_bet
        self.total_cost = 0
        self.profit = 0
        self.odds = 2.7
        self.update_counter_label()

        

        


    def update_counter_label(self):
        if self.active_currency.get() == "GP":
            self.counter_label.config(text=f"Total bets: {format(self.counter, ',')}     |     Total cost: {format(self.total_cost, ',')} GP\nSets of {self.set_limit}: {format(self.sets, ',')} | Profit: {format(self.profit, ',')} GP | Odds: {format(self.odds, '.2f')}%")
            self.increment_button.config(text=f"Bet: {format(self.bet, ',')} GP")
        elif self.active_currency.get() == "$":
            self.counter_label.config(text=f"Total bets: {format(self.counter, ',')}     |     Total cost: ${format(self.total_cost, ',.2f')}\nSets of {self.set_limit}: {format(self.sets, ',')} | Profit: ${format(self.profit, ',.2f')} | Odds: {format(self.odds, '.2f')}%")
            self.increment_button.config(text=f"Bet: ${format(self.bet, ',.2f')}")
        elif self.active_currency.get() == "crypto":
            self.counter_label.config(text=f"Total bets: {format(self.counter, ',')}     |     Total cost: Ξ{format(self.total_cost, ',.16f')}\nSets of {self.set_limit}: {format(self.sets, ',')} | Profit: Ξ{format(self.profit, ',.16f')} | Odds: {format(self.odds, '.2f')}%")
            self.increment_button.config(text=f"Bet: Ξ{format(self.bet, ',.16f')}")


    def increment_counter(self):
        self.counter += 1
        if isinstance(self.bet, int):
            self.total_cost = int(self.total_cost + self.bet)
            self.profit = int(self.bet * self.payout - self.total_cost)
        else:
            self.total_cost = float(self.total_cost + self.bet)
            self.profit = float(self.bet * self.payout - self.total_cost)

        self.probability = 1 - ((36/37) ** (self.counter))
        self.odds = 100 * self.probability
        
        if self.counter % self.set_limit == 0:
            self.sets += 1
            self.bet *= self.bet_modifier
        
        self.update_counter_label()
    
    
    

def main():
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.title("Roulette Overlay")
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()

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
