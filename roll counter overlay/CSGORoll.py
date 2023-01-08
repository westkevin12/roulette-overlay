import tkinter as tk
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
        self.payout = 14
        self.bet_modifier = 2
        self.sets = 0
        self.max_set_limit = self.payout * 0.5
        self.min_set_limit = 1
        self.set_limit = 6
        self.starting_bet = tk.DoubleVar()
        self.starting_bet.set(0.01)
        self.bet = self.starting_bet.get()
        self.total_cost = 0
        self.profit = 0
        # Create a frame to hold the button and counter
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Create a label to display the total bets
        self.counter_label = tk.Label(self.frame, text="Total bets: 0 | Total cost: $0.00\nSets: 0 | Profit: $0.00")
        self.counter_label.pack()

        # Create a button and displays the value of the bet variable
        self.increment_button = tk.Button(self.frame, text=f"Bet: ${self.bet:.2f}", command=self.increment_counter, width=25, height=6)
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
        self.donate_button.pack(side='right')

    def open_donate_window(self):
        # Create a new top-level window
        self.donate_window = tk.Toplevel(self.root)

        tk.Label(self.donate_window, text="Your success with this tool is a testament to its value.\nIf you'd like to support the developer and help continue to improve and create great products,\nplease consider donating through one of these options.").pack()
        tk.Label(self.donate_window, text="Paypal:").pack()
        tk.Label(self.donate_window, text="https://paypal.me/XvGwest").pack()
        tk.Label(self.donate_window, text="ETH:").pack()
        tk.Label(self.donate_window, text="0x712ac061FCDAC3b7861D367D3bF995d814775F66").pack()


    def open_settings_window(self):
        # Create a new top-level window
        self.settings_window = tk.Toplevel(self.root)


        # Add a label and text entry widget for the payout value
        tk.Label(self.settings_window, text="Payout Modifier:").pack()
        self.payout_entry = tk.Entry(self.settings_window)
        self.payout_entry.insert(0, self.payout)
        self.payout_entry.pack()

        # Add a label and text entry widget for the bet modifier value
        tk.Label(self.settings_window, text="Bet Modifier:").pack()
        self.bet_modifier_entry = tk.Entry(self.settings_window)
        self.bet_modifier_entry.insert(0, self.bet_modifier)
        self.bet_modifier_entry.pack()

        # Add a label and text entry widget for the starting bet value
        tk.Label(self.settings_window, text="Starting bet:").pack()
        self.starting_bet_entry = tk.Entry(self.settings_window)
        self.starting_bet_entry.insert(0, self.starting_bet.get())
        self.starting_bet_entry.pack()

        # Add a label and text entry widget for the set limit value
        tk.Label(self.settings_window, text="Set limit:").pack()
        self.set_limit_entry = tk.Entry(self.settings_window)
        self.set_limit_entry.insert(0, self.set_limit)
        self.set_limit_entry.pack()

        tk.Label(self.settings_window, text=f"Set limit 1 - {round(self.max_set_limit)}").pack()

        # Add a button to close the window and update the relevant variables
        tk.Button(self.settings_window, text="Save", command=self.close_settings_window).pack()

    def close_settings_window(self):
        # Get the values from the text entry widgets
        self.starting_bet.set(float(self.starting_bet_entry.get()))
        self.payout = float(self.payout_entry.get())
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
        self.bet = self.starting_bet.get()
        self.total_cost = 0
        self.profit = 0
        self.update_counter_label()
        self.increment_button.config(text=f"Bet: ${format(self.bet, ',.2f')}")

    def update_counter_label(self):
        self.counter_label.config(text=f"Total bets: {format(self.counter, ',')} | Total cost: ${format(self.total_cost, ',.2f')}\nSets of {self.set_limit}: {format(self.sets, ',')} | Profit: ${format(self.profit, ',.2f')}")
        #self.counter_label.config(text=f"Total bets: {format(self.counter, ',')} | Total cost: ${format(self.total_cost, ',')}\nSets of {self.set_limit}: {format(self.sets, ',')} | Profit: ${format(self.profit, ',')}")


    def increment_counter(self):
        self.counter += 1
        self.total_cost += self.bet
        self.profit = self.bet * self.payout - self.total_cost

        if self.counter % self.set_limit == 0:
            self.sets += 1
            self.bet *= self.bet_modifier
        
        self.update_counter_label()
        self.increment_button.config(text=f"Bet: ${format(self.bet, ',.2f')}")
        #self.increment_button.config(text=f"Bet: ${format(self.bet, ',')}")

    

def main():
    root = tk.Tk()
    root.attributes("-topmost", True)
    app = OverlayWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
