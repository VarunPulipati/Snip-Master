from os import name
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk
import json
import re
import datetime
import pyperclip
import keyboard
import pystray
from PIL import Image,ImageTk
from pystray import MenuItem as item


valid_identifiers = [str(i) for i in range(10)] + [chr(i) for i in range(97, 123)]

def create_image():
    # Create an image for the icon
    image = Image.open("cert.jpeg")
    return image

def on_clicked(icon, item):
    # Action on click (e.g., restore the window or quit)
    icon.stop()

def setup_system_tray():
    icon_image = create_image()
    menu = pystray.Menu(pystray.MenuItem('Quit', on_clicked))
    icon = pystray.Icon("test_icon", icon_image, "Your App", menu)
    icon.run()

def update_dropdown(*args):
    global clipboard_slots
    filtered_slots = [slot for slot, content in clipboard_slots.items() if content] 
    dropdown['values'] = filtered_slots  # Update dropdown values
    dropdown.set('')
def update_dropdown_values():
    global clipboard_slots
    # Update dropdown values but don't clear the selection
    filtered_slots = [slot for slot, content in clipboard_slots.items() if content]
    dropdown['values'] = filtered_slots

# Binding to update the entry of the dropdown when an item is selected
def on_combobox_select(event):
    # When an item is selected, set search_var to that item and paste its content
    selected_slot = dropdown.get()
    search_var.set(selected_slot)
    paste_from_dropdown()

def load_config(filename='shortcuts_config.json'):
    # Provide a default configuration structure
    default_config = {"copy_shortcuts": {}, "paste_shortcuts": {}, "cut_shortcuts": {}}
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
        # Ensure all keys are present in the loaded config
        for key in default_config:
            config.setdefault(key, default_config[key])
        return config
    except FileNotFoundError:
        # Return default config if file does not exist
        return default_config

def save_config(config, filename='shortcuts_config.json'):
    with open(filename, 'w') as file:
        json.dump(config, file, indent=4)

def log_action(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{current_time}] {message}"
    log_text.config(state='normal')
    log_text.insert(tk.END, formatted_message + '\n')
    log_text.config(state='disabled')
    log_text.yview(tk.END)

def update_shortcut(slot=None):
    global config
    if slot is None:
        slot = simpledialog.askstring("Input", "Enter the identifier for the new slot:")
    if slot in config['copy_shortcuts'] or slot in config['paste_shortcuts']:
        messagebox.showerror("Invalid Slot", "This slot identifier already exists.")
        return
    shortcut_type = simpledialog.askstring("Input", f"Enter new shortcut for slot {slot} (copy/paste):")
    if shortcut_type and validate_shortcut(shortcut_type):
        if 'copy' in shortcut_type:
            config['copy_shortcuts'][slot] = shortcut_type
        elif 'paste' in shortcut_type:
            config['paste_shortcuts'][slot] = shortcut_type
        save_config(config)
        messagebox.showinfo("Shortcut Updated", f"The new shortcut for slot {slot} has been saved.")
        log_action(f"Updated shortcut for slot {slot}: {shortcut_type}")
        display_shortcuts()
        update_dropdown()
    else:
        messagebox.showerror("Invalid Shortcut", "Shortcut format is invalid. Please use format like 'ctrl+shift+c+1'.")

def validate_shortcut(shortcut):
    pattern = re.compile(r"^(ctrl\+shift\+)([a-z]|\d)$")
    return bool(pattern.match(shortcut.lower()))

def display_shortcuts():
    for widget in frame.winfo_children():
        widget.destroy()
    row = 0
    for slot, shortcut in config['copy_shortcuts'].items():
        tk.Label(frame, text=f"Copy Slot {slot}: {shortcut}").grid(row=row, column=0, sticky="w")
        tk.Button(frame, text="Edit", command=lambda slot=slot: update_shortcut(slot)).grid(row=row, column=1)
        row += 1
    for slot, shortcut in config['paste_shortcuts'].items():
        tk.Label(frame, text=f"Paste Slot {slot}: {shortcut}").grid(row=row, column=0, sticky="w")
        tk.Button(frame, text="Edit", command=lambda slot=slot: update_shortcut(slot)).grid(row=row, column=1)
        row += 1
    tk.Button(frame, text="Add New Slot", command=lambda: update_shortcut()).grid(row=row, column=0, columnspan=2)

clipboard_slots = {}

def clear_clipboard():
    global clipboard_slots
    clipboard_slots.clear()
    pyperclip.copy('')  # Clear the system clipboard
    log_action("Clipboard cleared.")
    
    # Update the dropdown values and clear the current selection
    dropdown['values'] = []
    dropdown.set('')
    
    # Also update the search entry to clear it
    search_var.set('')

    # Call display functions to reflect changes in the GUI
    display_copied_texts()
    update_dropdown()

def display_copied_texts():
    for widget in copied_texts_frame.winfo_children():
        widget.destroy()

    for row, (identifier, text) in enumerate(clipboard_slots.items(), start=1):
        # Frame for each slot
        slot_frame = ttk.Frame(copied_texts_frame)
        slot_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        slot_label = tk.Label(slot_frame, text=f"Slot {row}:", anchor='w', fg="blue", cursor="hand2")
        slot_label.bind("<Button-1>", lambda e, i=identifier: handle_paste(e, i))
        slot_label.grid(row=0, column=0, padx=5, pady=5)
        # Label for slot identifier
        tk.Label(slot_frame, text=f"Slot {identifier}:", anchor='w').grid(row=0, column=0, padx=5, pady=5)

        # Horizontal scrollbar for the text widget
        h_scroll = ttk.Scrollbar(slot_frame, orient='horizontal')
        h_scroll.grid(row=1, column=1, sticky='ew')

        # Text widget for the content
        content_text = tk.Text(slot_frame, wrap='none', xscrollcommand=h_scroll.set, width=50, height=3)
        content_text.grid(row=0, column=1, sticky='ew')
        content_text.insert('end', text)
        content_text['state'] = 'disabled'
        h_scroll['command'] = content_text.xview

        # Keep the slot label and text widget from expanding beyond their size
        slot_frame.grid_columnconfigure(1, weight=1)
        slot_frame.grid_columnconfigure(0, weight=0)

        # Edit button
        edit_button = ttk.Button(slot_frame, text="Edit", command=lambda i=identifier: edit_slot(i))
        edit_button.grid(row=0, column=2, padx=5, pady=5)

        # Delete button
        delete_button = ttk.Button(slot_frame, text="Delete", command=lambda i=identifier: delete_slot(i))
        delete_button.grid(row=0, column=3, padx=5, pady=5)

    # Update the frame geometry to redraw the layout
    copied_texts_frame.update_idletasks()


def handle_copy(identifier):
    print(f"Copy command triggered with identifier {identifier}")
    global clipboard_slots
    clipboard_slots[identifier] = pyperclip.paste()
    log_action(f"Copied to slot '{identifier}': {clipboard_slots[identifier]}")
    display_copied_texts()
    update_dropdown()  # Ensure this is called to reflect changes

def handle_cut(identifier):
    print(f"Cut command triggered with identifier {identifier}")
    global clipboard_slots
    clipboard_slots[identifier] = pyperclip.paste()
    log_action(f"Cut to slot '{identifier}': {clipboard_slots[identifier]}")
    # Clearing the clipboard to simulate a cut operation
    pyperclip.copy('')  
    display_copied_texts()
    update_dropdown()  # Ensure this is called to reflect changes


def handle_paste(identifier):
    print(f"Paste command triggered with identifier {identifier}")
    log_action(f"Attempt to paste from slot '{identifier}'")
    text = clipboard_slots.get(identifier, '')
    if text:
        pyperclip.copy(text)
        keyboard.write(text)  # Simulate the keyboard press to paste
        log_action(f"Text copied to clipboard for slot '{identifier}': {text}")

        log_action(f"Pasted from slot '{identifier}'.")
        time.sleep(0.5)  # Half a second delay
        try:
            keyboard.send('ctrl+v')
            log_action(f"Pasted from slot '{identifier}'.")
        except Exception as e:
            log_action(f"Failed to paste from slot '{identifier}': {str(e)}")
    else:
        log_action(f"Slot '{identifier}' is empty.")

def edit_slot(identifier):
    # This function will prompt the user to enter new text for the slot
    new_text = simpledialog.askstring("Edit Slot", f"Edit text for slot '{identifier}':", initialvalue=clipboard_slots[identifier])
    if new_text is not None:
        clipboard_slots[identifier] = new_text
        log_action(f"Slot '{identifier}' edited.")
        display_copied_texts()

def delete_slot(identifier):
    # This function will remove the slot from the clipboard
    if messagebox.askyesno("Delete Slot", f"Are you sure you want to delete slot '{identifier}'?"):
        clipboard_slots.pop(identifier, None)  # Remove the slot if it exists
        log_action(f"Slot '{identifier}' deleted.")
        display_copied_texts()
        update_dropdown()  # Update the dropdown to reflect the deletion

def paste_from_dropdown():
    slot = dropdown.get()
    if slot:
        handle_paste(slot)

def setup_shortcuts():
    for identifier in valid_identifiers:
        keyboard.add_hotkey(f'ctrl+c+{identifier}', lambda i=identifier: handle_copy(i), suppress=True)
        keyboard.add_hotkey(f'ctrl+alt+v+{identifier}', lambda i=identifier: handle_paste(i), suppress=True)
        keyboard.add_hotkey(f'ctrl+x+{identifier}', lambda i=identifier: handle_cut(i), suppress=True)

def setup_gui():
    global root, frame, copied_texts_frame, log_frame, log_text, search_bar_frame, search_var, dropdown
    root = tk.Tk()
    root.title("Clipboard Manager Configuration")
    root.attributes("-topmost", True)
    root.after(100, update_dropdown)
    # Set theme for ttk
    style = ttk.Style()
    style.theme_use('clam')  # or 'default', 'classic', 'alt', etc.

    # Style configurations
    style.configure('TFrame', background='white')
    style.configure('TButton', font=('Helvetica', 12), padding=5)
    style.configure('TLabel', background='white', font=('Helvetica', 12))
    style.configure('TEntry', font=('Helvetica', 12), padding=5)

    frame = ttk.Frame(root, padding="10")
    frame.pack(expand=True, fill='both', side='top', padx=10, pady=10)

    copied_texts_frame = tk.Frame(root)
    copied_texts_frame.pack(padx=10, pady=5)

    log_frame = tk.Frame(root)
    log_frame.pack(padx=10, pady=10)

    log_text = scrolledtext.ScrolledText(log_frame, state='disabled', height=10, wrap='word')
    log_text.pack(fill='both', expand=True)

    # Search bar and dropdown setup
    search_bar_frame = tk.Frame(root)
    search_bar_frame.pack(side=tk.TOP, anchor='ne', padx=10, pady=5)  # pack to the top right

    search_label = tk.Label(search_bar_frame, text="Search Slot:")
    search_label.pack(side=tk.LEFT, padx=(0, 10))

    search_var = tk.StringVar()
    dropdown = ttk.Combobox(search_bar_frame, textvariable=search_var, state="readonly")
    dropdown.pack(side=tk.LEFT, padx=(0, 10))
    dropdown.bind('<<ComboboxSelected>>', on_combobox_select)

    search_var.trace_add('write', lambda *args: update_dropdown_values())

    update_dropdown_values()
    # Clear clipboard button (if you want to add a button for clearing clipboard)
    clear_button = ttk.Button(search_bar_frame, text="Clear Clipboard", command=clear_clipboard)
    clear_button.pack(side=tk.RIGHT)
# Setup the rest of the GUI components
    setup_shortcuts()
    display_shortcuts()
    display_copied_texts()
    log_action("Application started.")

    root.mainloop()


if __name__ == "__main__":  # Correct this line
    config = load_config()
    # Initialize clipboard_slots with content from config
    clipboard_slots = {key: "" for key in config['copy_shortcuts'].keys()}
    clipboard_slots.update({key: "" for key in config['paste_shortcuts'].keys()})
    clipboard_slots.update({key: "" for key in config['cut_shortcuts'].keys()})

    for identifier in valid_identifiers:
        # Assuming your config file has a "cut_shortcuts" section
        if f'cut+{identifier}' not in config['cut_shortcuts']:
            config['cut_shortcuts'][f'cut+{identifier}'] = ''

    setup_gui()
    setup_system_tray()

