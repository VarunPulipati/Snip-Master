import threading
import tkinter as tk
from tkinter import messagebox, ttk, Menu
from PIL import Image, ImageTk
import pyperclip
import keyboard
import time
import sys

clipboard_history = []  # To store clipboard history
clipboard_slots = {}  # To store slots with labels (e.g., 'a', 'b')
valid_identifiers = [chr(i) for i in range(97, 123)]  # 'a' to 'z'

# Automatically assign to default numbered slots for unspecified copies
def assign_default_slot(content):
    for i in range(1, 10):
        if str(i) not in clipboard_slots:
            clipboard_slots[str(i)] = content
            clipboard_history.append(f"Default Slot {i}: {content}")
            return
    messagebox.showwarning("Clipboard", "No available default slots")

def show_context_menu(event, options):
    """Display a context menu with provided options."""
    menu = Menu(root, tearoff=0)
    for label, command in options:
        menu.add_command(label=label, command=command)
    menu.post(event.x_root, event.y_root)

def delete_slot(identifier):
    if identifier in clipboard_slots:
        del clipboard_slots[identifier]
        messagebox.showinfo("Delete", f"Slot {identifier} deleted.")
        if hasattr(root, 'new_window') and root.new_window.winfo_exists():
            refresh_clipboard_window(root.new_window)
    else:
        messagebox.showwarning("Delete", f"Slot {identifier} does not exist.")

def edit_slot(identifier):
    """Edit the slot name."""
    if identifier in clipboard_slots:
        new_name = messagebox.askstring("Edit Slot", f"Enter new name for Slot {identifier}:")
        if new_name and new_name not in clipboard_slots:
            clipboard_slots[new_name] = clipboard_slots.pop(identifier)
            messagebox.showinfo("Edit Slot", f"Slot {identifier} renamed to {new_name}.")
        elif new_name in clipboard_slots:
            messagebox.showwarning("Edit Slot", f"Slot name {new_name} already exists.")
    else:
        messagebox.showwarning("Edit Slot", f"Slot {identifier} does not exist.")

def on_icon_click(event):
    """Callback function when the floating icon is clicked."""
    root.withdraw()  # Hide the icon window
    open_new_window()

def open_new_window():
    """Function to open a small window with pop-out animation and added features."""
    if hasattr(root, 'new_window') and root.new_window.winfo_exists():
        root.new_window.lift()  # Bring the existing window to the front
        return

    new_window = tk.Toplevel(root)
    root.new_window = new_window
    new_window.title("Welcome")
    x_position = root.winfo_x() - 250
    y_position = root.winfo_y()
    new_window.geometry(f"1x1+{x_position}+{y_position}")  # Start small at the icon position
    new_window.attributes("-topmost", True)  # Keep the new window on top

    # Style the new window
    new_window.configure(bg="#0f0f3f")

    # Add a rounded frame for a more aesthetic look
    frame = tk.Frame(new_window, bg="#1a1aff", padx=10, pady=10, relief="raised", bd=2)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add content to the new window
    label = tk.Label(frame, text="Hi, there! Welcome!", font=("Arial", 14, "bold"), fg="white", bg="#1a1aff")
    label.pack(pady=10)

    # Show clipboard slots
    slots_label = tk.Label(frame, text="Clipboard Slots:", fg="white", bg="#1a1aff", font=("Arial", 12))
    slots_label.pack(pady=5)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    slots_frame = tk.Frame(frame, bg="#1a1aff")
    slots_frame.pack(fill="both", expand=True, pady=5)

    for slot, content in clipboard_slots.items():
        slot_frame = ttk.Frame(slots_frame)
        slot_frame.pack(fill="x", pady=2)

        # Slot name label, functional for pasting
        slot_label = tk.Label(slot_frame, text=f"Slot {slot}:", fg="blue", cursor="hand2", anchor="w")
        slot_label.bind("<Button-1>", lambda e, i=slot: handle_paste(i))
        slot_label.bind("<Button-3>", lambda e, i=slot: show_context_menu(e, [
            ("Delete", lambda: delete_slot(i)),
            ("Assign", lambda: assign_slot(i)),
            ("Edit", lambda: edit_slot(i))
        ]))
        slot_label.grid(row=0, column=0, padx=5, pady=5)

        # Content display, functional for pasting
        content_label = tk.Label(slot_frame, text=content, fg="white", bg="#1a1aff", cursor="hand2", anchor="w")
        content_label.bind("<Button-1>", lambda e, i=slot: handle_paste(i))
        content_label.bind("<Button-3>", lambda e, i=slot: show_context_menu(e, [
            ("Delete", lambda: delete_slot(i)),
            ("Rewrite", lambda: rewrite_content(i)),
            ("Rephrase", lambda: rephrase_content(i))
        ]))
        content_label.grid(row=0, column=1, padx=5, pady=5)

    # Add a clear clipboard button
    clear_clipboard_button = tk.Button(
        frame,
        text="Clear Clipboard",
        command=clear_clipboard,
        bg="#ff4d4d",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        activebackground="#ff6666"
    )
    clear_clipboard_button.pack(pady=5)

    # Add a search dropdown
    search_frame = tk.Frame(frame, bg="#1a1aff")
    search_frame.pack(pady=5)

    search_label = tk.Label(search_frame, text="Search:", fg="white", bg="#1a1aff", font=("Arial", 12))
    search_label.pack(side=tk.LEFT, padx=5)

    search_var = tk.StringVar()
    search_dropdown = ttk.Combobox(search_frame, textvariable=search_var, font=("Arial", 12), state="readonly")
    search_dropdown['values'] = list(clipboard_slots.keys())  # Populate with slot keys
    search_dropdown.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(
        search_frame,
        text="Go",
        command=lambda: search_function(search_var.get()),
        bg="#33cc33",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        activebackground="#66ff66"
    )
    search_button.pack(side=tk.LEFT, padx=5)

    # Display most recent clipboard slots
    history_label = tk.Label(frame, text="Clipboard History:", fg="white", bg="#1a1aff", font=("Arial", 12))
    history_label.pack(pady=5)
    history_frame = tk.Frame(frame, bg="#1a1aff")
    history_frame.pack()

    for i, item in enumerate(clipboard_history[-4:]):
        item_label = tk.Label(history_frame, text=f"{i + 1}: {item}", fg="white", bg="#1a1aff", font=("Arial", 10))
        item_label.pack(anchor="w")

    close_button = tk.Button(frame, text="Close", command=lambda: close_new_window(new_window), bg="#ff4d4d", fg="white", font=("Arial", 12, "bold"))
    close_button.pack(pady=10)

    # Handle window close using window controls
    new_window.protocol("WM_DELETE_WINDOW", lambda: close_new_window(new_window))

    # Animate the window to pop out
    animate_window(new_window, 400, 500)

def animate_window(window, target_width, target_height):
    """Animate the window to smoothly pop out to the target size."""
    current_width = window.winfo_width()
    current_height = window.winfo_height()

    if current_width < target_width or current_height < target_height:
        new_width = min(current_width + 20, target_width)
        new_height = min(current_height + 20, target_height)
        window.geometry(f"{new_width}x{new_height}")
        window.after(10, lambda: animate_window(window, target_width, target_height))

def clear_clipboard():
    """Clear the system clipboard and show a message."""
    root.clipboard_clear()
    messagebox.showinfo("Clipboard", "Clipboard cleared!")
    clipboard_history.append("Cleared Clipboard")
    clipboard_slots.clear()

def handle_copy(identifier):
    print(f"Copy command triggered with identifier {identifier}")
    global clipboard_slots

    # Use threading to avoid blocking main execution
    def copy_content():
        time.sleep(0.1)  # Ensure clipboard updates first
        content = pyperclip.paste()  # Fetch the latest clipboard content

        if content.strip():  # Ensure valid content
            if identifier:
                clipboard_slots[identifier] = content
                #clipboard_history.append(f"Slot {identifier}: {content}")
            else:
                assign_default_slot(content)
            
            # Refresh the clipboard window if open
            if hasattr(root, 'new_window') and root.new_window.winfo_exists():
                refresh_clipboard_window(root.new_window)
        else:
            print("No valid content copied.")
    
    threading.Thread(target=copy_content).start()

def handle_cut(identifier):
    print(f"Cut command triggered with identifier {identifier}")
    global clipboard_slots
    keyboard.press_and_release('ctrl+x')  # Perform a system cut
    time.sleep(0.2)
    content = pyperclip.paste()
    pyperclip.copy('')  # Clear clipboard
    if content.strip():
        if identifier:
            clipboard_slots[identifier] = content
            #clipboard_history.append(f"Slot {identifier}: {content} (cut)")
        else:
            threading.Thread(target=assign_default_slot, args=(content,)).start()
        if hasattr(root, 'new_window') and root.new_window.winfo_exists():
            refresh_clipboard_window(root.new_window)

def handle_paste(identifier):
    print(f"Paste command triggered with identifier {identifier}")
    text = clipboard_slots.get(identifier, '')
    if text:
        pyperclip.copy(text)
        keyboard.write(text)  # Simulate keyboard paste

def rewrite_content(identifier):
    """Rewrite the content in the slot."""
    new_content = messagebox.askstring("Rewrite", "Enter new content:")
    if new_content:
        clipboard_slots[identifier] = new_content
        messagebox.showinfo("Rewrite", f"Slot {identifier} updated.")

def rephrase_content(identifier):
    """Rephrase the content in the slot."""
    content = clipboard_slots.get(identifier, "")
    if content:
        rephrased = f"(Rephrased) {content}"  # Placeholder rephrased content
        clipboard_slots[identifier] = rephrased
        messagebox.showinfo("Rephrase", f"Slot {identifier} rephrased.")

def assign_slot(identifier):
    """Assign content to the slot."""
    new_content = messagebox.askstring("Assign", "Enter new content to assign:")
    if new_content:
        clipboard_slots[identifier] = new_content
        messagebox.showinfo("Assign", f"Slot {identifier} assigned.")

def setup_shortcuts():
    for identifier in valid_identifiers:
        keyboard.add_hotkey(f'ctrl+c+{identifier}', lambda i=identifier: handle_copy(i))
        keyboard.add_hotkey(f'ctrl+alt+v+{identifier}', lambda i=identifier: handle_paste(i))
        keyboard.add_hotkey(f'ctrl+x+{identifier}', lambda i=identifier: handle_cut(i))
    keyboard.add_hotkey('ctrl+c', lambda: handle_copy(None))
    keyboard.add_hotkey('ctrl+x', lambda: handle_cut(None))

def search_function(query):
    """Perform a search and highlight the result in clipboard slots."""
    if query in clipboard_slots:
        messagebox.showinfo("Search Result", f"Slot {query}: {clipboard_slots[query]}")
    else:
        messagebox.showwarning("Search", "No such slot found!")

def close_new_window(new_window):
    """Function to close the small window and show the icon again."""
    new_window.destroy()  # Close the small window
    root.deiconify()  # Show the floating icon again

def on_drag_start(event):
    """Capture the initial position when the drag starts."""
    event.widget._drag_data = {"x": event.x, "y": event.y}

def on_drag_motion(event):
    """Handle the movement while dragging."""
    x = root.winfo_x() + event.x - event.widget._drag_data["x"]
    y = root.winfo_y() + event.y - event.widget._drag_data["y"]
    root.geometry(f"+{x}+{y}")

def on_hover(event):
    """Show the close button when hovered."""
    close_button.place(relx=0.7, rely=0.0)  # Position top-right of the icon

def on_leave(event):
    """Hide the close button when the mouse leaves."""
    close_button.place_forget()  # Hide the button

def close_icon():
    """Function to close the floating icon."""
    root.destroy()  # Destroy the root window and exit the application
    sys.exit(0)

def refresh_clipboard_window(new_window):
    """Refresh the clipboard window to reflect the latest slots."""
    for widget in new_window.winfo_children():
        widget.destroy()  # Clear all existing widgets

    # Style the window
    new_window.configure(bg="#0f0f3f")
    frame = tk.Frame(new_window, bg="#1a1aff", padx=10, pady=10, relief="raised", bd=2)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    label = tk.Label(frame, text="Hi, there! Welcome!", font=("Arial", 14, "bold"), fg="white", bg="#1a1aff")
    label.pack(pady=10)

    slots_label = tk.Label(frame, text="Clipboard Slots:", fg="white", bg="#1a1aff", font=("Arial", 12))
    slots_label.pack(pady=5)

    slots_frame = tk.Frame(frame, bg="#1a1aff")
    slots_frame.pack(pady=5)

    for slot, content in clipboard_slots.items():
        slot_frame = ttk.Frame(slots_frame)
        slot_frame.pack(fill="x", pady=2)

        # Slot name label
        slot_label = tk.Label(slot_frame, text=f"Slot {slot}:", fg="blue", cursor="hand2", anchor="w")
        slot_label.bind("<Button-1>", lambda e, i=slot: handle_paste(i))
        slot_label.bind("<Button-3>", lambda e, i=slot: show_context_menu(e, [
            ("Delete", lambda: delete_slot(i)),
            ("Assign", lambda: assign_slot(i)),
            ("Edit", lambda: edit_slot(i))
        ]))
        slot_label.grid(row=0, column=0, padx=5, pady=5)

        # Content display
        content_label = tk.Label(slot_frame, text=content, fg="white", bg="#1a1aff", cursor="hand2", anchor="w")
        content_label.bind("<Button-1>", lambda e, i=slot: handle_paste(i))
        content_label.bind("<Button-3>", lambda e, i=slot: show_context_menu(e, [
            ("Delete", lambda: delete_slot(i)),
            ("Rewrite", lambda: rewrite_content(i)),
            ("Rephrase", lambda: rephrase_content(i))
        ]))
        content_label.grid(row=0, column=1, padx=5, pady=5)

    clear_clipboard_button = tk.Button(
        frame,
        text="Clear Clipboard",
        command=clear_clipboard,
        bg="#ff4d4d",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        activebackground="#ff6666"
    )
    clear_clipboard_button.pack(pady=5)

    search_frame = tk.Frame(frame, bg="#1a1aff")
    search_frame.pack(pady=5)

    search_label = tk.Label(search_frame, text="Search:", fg="white", bg="#1a1aff", font=("Arial", 12))
    search_label.pack(side=tk.LEFT, padx=5)

    search_var = tk.StringVar()
    search_dropdown = ttk.Combobox(search_frame, textvariable=search_var, font=("Arial", 12), state="readonly")
    search_dropdown['values'] = list(clipboard_slots.keys())  # Populate with slot keys
    search_dropdown.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(
        search_frame,
        text="Go",
        command=lambda: search_function(search_var.get()),
        bg="#33cc33",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        activebackground="#66ff66"
    )
    search_button.pack(side=tk.LEFT, padx=5)

    history_label = tk.Label(frame, text="Clipboard History:", fg="white", bg="#1a1aff", font=("Arial", 12))
    history_label.pack(pady=5)

    history_frame = tk.Frame(frame, bg="#1a1aff")
    history_frame.pack()

    for i, item in enumerate(clipboard_history[-4:]):
        item_label = tk.Label(history_frame, text=f"{i + 1}: {item}", fg="white", bg="#1a1aff", font=("Arial", 10))
        item_label.pack(anchor="w")

    close_button = tk.Button(frame, text="Close", command=lambda: close_new_window(new_window), bg="#ff4d4d", fg="white", font=("Arial", 12, "bold"))
    close_button.pack(pady=10)

def setup_floating_icon():
    global root, close_button
    root = tk.Tk()
    root.title("Floating Icon")
    root.overrideredirect(True)  # Remove window decorations
    root.attributes("-topmost", True)  # Keep it on top of other windows

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Configure grid layout to make the icon resize dynamically
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Ensure the icon label resizes dynamically
    # Default position: top-right corner    
    window_width = 60
    window_height = 60
    x_offset = screen_width - window_width  # Adjust to place it on the right
    y_offset = 100  # Adjust to place it near the top

    # Set the position of the window
    root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

    # Allow resizing
    root.resizable(True, True)

    # Configure grid layout to make the icon resize dynamically
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Load the icon image
    icon_image = Image.open("cert.jpeg")  # Replace with your image path
    icon_image = icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Resize image to fit window
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Create a label to display the icon
    icon_label = tk.Label(root, image=icon_photo, bg="white")
    icon_label.grid(sticky="nsew")  # Ensure the label resizes with the window

    # Bind the click event to the label (triggered when mouse is released)
    icon_label.bind("<ButtonRelease-1>", on_icon_click)

    # Bind dragging events to make the icon movable
    icon_label.bind("<Button-1>", on_drag_start)  # Start dragging on left-click
    icon_label.bind("<B1-Motion>", on_drag_motion)  # Perform drag motion

    # Bind hover events to show/hide the close button
    icon_label.bind("<Enter>", on_hover)  # When mouse enters the icon
    icon_label.bind("<Leave>", on_leave)  # When mouse leaves the icon

    # Create a close button for the hover effect
    close_button = tk.Button(root, text="X", command=close_icon, bg="red", fg="white", bd=0, padx=5, pady=2)
    close_button.place_forget()  # Initially hide the button

    setup_shortcuts()  # Setup global shortcuts

    root.mainloop()

if __name__ == "__main__":
    setup_floating_icon()
