import glob
import tkinter as tk
from tkinter import filedialog, messagebox, font
import os
import re
import subprocess

# Syntax highlighting patterns
KEYWORDS = r"\b(?:class|def|for|while|if|elif|else|try|except|finally|return|raise|pass|break|continue|import|from|as|global|nonlocal|with|assert|lambda|print|def)\b"
STRINGS = r'"[^"]*"|\'[^\']*\''
COMMENTS = r"#.*"
last_saved_state = ""
# Define the tag styles
def init_styles(text_widget):
    text_widget.tag_configure("CLASS", foreground="#569cd6")
    text_widget.tag_configure("DEF", foreground="#d69c56")
    text_widget.tag_configure("FOR", foreground="#608b4e")
    text_widget.tag_configure("IF", foreground="#b5cea8")
    text_widget.tag_configure("ELSE", foreground="#f92672")
    text_widget.tag_configure("TRY", foreground="#ffa07a")
    text_widget.tag_configure("EXCEPT", foreground="#ffd700")
    text_widget.tag_configure("FINALLY", foreground="#ffffff")
    text_widget.tag_configure("RETURN", foreground="#c70039")
    text_widget.tag_configure("RAISE", foreground="#8856a7")
    text_widget.tag_configure("PASS", foreground="#ef2929")
    text_widget.tag_configure("BREAK", foreground="#cc7832")
    text_widget.tag_configure("CONTINUE", foreground="#6a8759")
    text_widget.tag_configure("IMPORT", foreground="#6c71c4")
    text_widget.tag_configure("FROM", foreground="#2aa198")
    text_widget.tag_configure("AS", foreground="#d33682")
    text_widget.tag_configure("GLOBAL", foreground="#458588")
    text_widget.tag_configure("NONLOCAL", foreground="#bdae93")
    text_widget.tag_configure("WITH", foreground="#f4bf75")
    text_widget.tag_configure("ASSERT", foreground="#ff8c00")
    text_widget.tag_configure("LAMBDA", foreground="#ff4500")
    text_widget.tag_configure("PRINT", foreground="#7800FF")
    text_widget.tag_configure("STRING", foreground="#ce9178")
    text_widget.tag_configure("COMMENT", foreground="#608b4e")

# Apply syntax highlighting
def apply_syntax_highlighting(text_widget):
    clear_tags(text_widget)
    content = text_widget.get("1.0", tk.END)
    apply_style(text_widget, r"\bclass\b", "CLASS", content)
    apply_style(text_widget, r"\bdef\b", "DEF", content)
    apply_style(text_widget, r"\bfor\b", "FOR", content)
    apply_style(text_widget, r"\bif\b", "IF", content)
    apply_style(text_widget, r"\belif\b", "ELSE", content)
    apply_style(text_widget, r"\belse\b", "ELSE", content)
    apply_style(text_widget, r"\btries?\b", "TRY", content)
    apply_style(text_widget, r"\bexcept\b", "EXCEPT", content)
    apply_style(text_widget, r"\bfinally\b", "FINALLY", content)
    apply_style(text_widget, r"\breturn\b", "RETURN", content)
    apply_style(text_widget, r"\braises?\b", "RAISE", content)
    apply_style(text_widget, r"\bpass\b", "PASS", content)
    apply_style(text_widget, r"\bbreak\b", "BREAK", content)
    apply_style(text_widget, r"\bcontinue\b", "CONTINUE", content)
    apply_style(text_widget, r"\bimport\b", "IMPORT", content)
    apply_style(text_widget, r"\bfrom\b", "FROM", content)
    apply_style(text_widget, r"\bas\b", "AS", content)
    apply_style(text_widget, r"\bglobal\b", "GLOBAL", content)
    apply_style(text_widget, r"\bnonlocal\b", "NONLOCAL", content)
    apply_style(text_widget, r"\bwith\b", "WITH", content)
    apply_style(text_widget, r"\bassert\b", "ASSERT", content)
    apply_style(text_widget, r"\blambda\b", "LAMBDA", content)
    apply_style(text_widget, r"\bprint\b", "PRINT", content)
    apply_style(text_widget, STRINGS, "STRING", content)
    apply_style(text_widget, COMMENTS, "COMMENT", content)

# Apply style to regex pattern matches
def apply_style(text_widget, pattern, tag, content):
    for match in re.finditer(pattern, content):
        start = f"{match.start()}.0"
        end = f"{match.end()}.0"
        text_widget.tag_add(tag, start, end)

# Clear old tags
def clear_tags(text_widget):
    for tag in text_widget.tag_names():
        text_widget.tag_remove(tag, "1.0", tk.END)

# Function to create a new file
def new_file():
    text_widget.delete("1.0", tk.END)
    apply_syntax_highlighting(text_widget)

# Function to open a file
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, file.read())
            apply_syntax_highlighting(text_widget)

# Function to save a file
def save_file():
    global current_file
    try:
        if current_file:
            with open(current_file, "w") as file:
                file.write(text_widget.get("1.0", tk.END))
        else:
            save_file_as()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")
        
def auto_save():
    global last_saved_state
    current_content = text_widget.get("1.0", tk.END)
    if current_content != last_saved_state:
        save_file()
        last_saved_state = current_content
    # Schedule the next auto-save check
    window.after(1000, auto_save)  # Auto-save every  10 seconds

# Function to save a file as
def save_file_as():
    global current_file
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("All files", "*.*")])
    if file_path:
        current_file = file_path
        save_file()
        
def help():
    global help
    messagebox.showinfo("Help", "This program has 'auto-save' but it will not work until you manually save once! Developed by Thoq. (C) 2024 CEdit")


def get_info():
    global help
    if messagebox.askyesno("Get Info", "Would you like to run the 'Get Info' script now? This will retrieve info on the program."):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        batch_script_path = os.path.join(script_dir, 'Get_Info.bat')
        subprocess.run([batch_script_path], shell=True)
    
# Function to exit the editor
def exit_editor():
    if messagebox.askokcancel("CEdit exit bootstrap", "Do you want to close CEdit?"):
        window.destroy()

# Function to handle the window close event
def on_close():
    if messagebox.askyesno("CEdit exit bootstrap", "Do you want to close CEdit?"):
        window.destroy()

# Create the main window
window = tk.Tk()
window.title("CEdit")
window.geometry("960x720")

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the path to the project directory
project_dir = os.path.abspath(os.path.join(script_dir, '..'))

# Construct the path to the font file
font_path = os.path.join(project_dir, 'product_sans.ttf')

# Define a default font
default_font = ('Helvetica',   14)

# Check if the font file exists
if os.path.exists(font_path):
    # Create a custom font
    custom_font = font.nametofont('CustomFont')
    custom_font.actual(family='Product Sans', size=17)
else:
    # Use the default font if the custom font file is not found
    custom_font = default_font

# Create the text area with a custom background color, white text, larger font size, and Product Sans font
text_widget = tk.Text(window, bg="#242424", fg="white", font=custom_font)
text_widget.pack(fill=tk.BOTH, expand=True)

# Initialize styles
init_styles(text_widget)

# Apply syntax highlighting after opening or creating a new file
apply_syntax_highlighting(text_widget)

# Bind the key release event to update syntax highlighting
text_widget.bind("<KeyRelease>", lambda event: apply_syntax_highlighting(text_widget))

# Create the menu bar
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_file_as)
file_menu.add_command(label="Help", command=help)
file_menu.add_command(label="Get Info", command=get_info)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor)
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="", menu=file_menu)
window.config(menu=menu_bar)

# Variable to hold the current file path
current_file = None

# Bind the window close event to the on_close function
window.protocol("WM_DELETE_WINDOW", on_close)

# Start the main event loop
window.mainloop()
