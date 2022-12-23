import tkinter as tk

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
        # Create a frame to hold the button and counter
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Create a label to display the total bets
        self.counter_label = tk.Label(self.frame, text="Total bets: 0 | Total cost: 0 GP\nSets: 0 | Profit: 0 GP")
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


        # Add a label and text entry widget for the payout value with a default value of 36
        tk.Label(self.settings_window, text="Payout:").pack()
        self.payout_entry = tk.Entry(self.settings_window)
        self.payout_entry.insert(0, "36")
        self.payout_entry.pack()


        # Add a label and text entry widget for the bet modifier value
        tk.Label(self.settings_window, text="Bet Modifier:").pack()
        self.bet_modifier_entry = tk.Entry(self.settings_window)
        self.bet_modifier_entry.insert(0, "2")
        self.bet_modifier_entry.pack()

        # Add a label and text entry widget for the starting bet value
        tk.Label(self.settings_window, text="Starting bet:").pack()
        self.starting_bet_entry = tk.Entry(self.settings_window)
        self.starting_bet_entry.insert(0, "50000")
        self.starting_bet_entry.pack()

        # Add a label and text entry widget for the set limit value
        tk.Label(self.settings_window, text="Set limit:").pack()
        self.set_limit_entry = tk.Entry(self.settings_window)
        self.set_limit_entry.insert(0, "16")
        self.set_limit_entry.pack()

        # Add a label to the settings window
        # Add a label to the settings window
        tk.Label(self.settings_window, text=f"Set limit 1 - {round(self.max_set_limit)}\n1 is agressive raising after every bet.\ndefault 16 to take it slow and steady.\nmake sure you can afford to lose well over 100 bets in a row.").pack()



        # Add a button to close the window and update the relevant variables
        tk.Button(self.settings_window, text="Save", command=self.close_settings_window).pack()

    def close_settings_window(self):
        # Get the values from the text entry widgets
        self.starting_bet = int(self.starting_bet_entry.get())
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
        self.update_counter_label()
        self.increment_button.config(text=f"Bet: {format(self.bet, ',')} GP")


    def update_counter_label(self):
        self.counter_label.config(text=f"Total bets: {format(self.counter, ',')} | Total cost: {format(self.total_cost, ',')} GP\nSets of {self.set_limit}: {format(self.sets, ',')} | Profit: {format(self.profit, ',')} GP")


    def increment_counter(self):
        self.counter += 1
        self.total_cost += self.bet
        self.profit = self.bet * self.payout - self.total_cost

        if self.counter % self.set_limit == 0:
            self.sets += 1
            self.bet *= self.bet_modifier
        
        self.update_counter_label()
        self.increment_button.config(text=f"Bet: {format(self.bet, ',')} GP")

    

def main():
    root = tk.Tk()
    root.attributes("-topmost", True)
    app = OverlayWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
