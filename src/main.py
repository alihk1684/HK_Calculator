import os
import sys
from tkinter import Tk, PhotoImage
import math as m
from random import random
from src.ui_config import setup_ui
from src.logic import (
    on_key_press,
    Mc,
    Mr,
    button_click,
    insert_operator,
    closing,
    percent,
    insert_factorial,
    ABS,
    ans,
    floor,
    ceil,
    Mp,
    Ms,
    up,
    toggle_history_view
)

state = {
    "just_calculated": None,
    "memory": 0,
    "Ans": None,
    "is_radian": True,
    "is_2nd": False,
    "theme": "dark"
}

safe_env ={
    'abs': abs,
    'sqrt': m.sqrt,
    'log': m.log10,
    'ln': m.log,
    'logy': m.log,
    'sin': m.sin,
    'cos': m.cos,
    'tan': m.tan,
    'pi': m.pi,
    'e': m.e,
    'EXP': m.exp,
    'asin': m.asin,
    'acos': m.acos,
    'atan': m.atan,
    'sinh': m.sinh,
    'cosh': m.cosh,
    'tanh': m.tanh,
    'floor': m.floor,
    'ceil': m.ceil,
    'factorial': m.factorial,
    'rand': random,
    'round': round,
    '__builtins__': None
}

def update_scrollbar_style(ui, theme):
    canvas = ui["canvas"]
    scrollbar = ui["scrollbar"]
    history_content = ui["history_content"]
    
    # Force immediate style update
    style_name = "Dark.Vertical.TScrollbar" if theme == "dark" else "Light.Vertical.TScrollbar"
    scrollbar.configure(style=style_name)
    
    # Update the widget immediately
    scrollbar.update_idletasks()
    
    # Calculate if scrolling is needed
    canvas.update_idletasks()
    
    # Get content height - handle empty state
    if ui["history_items"]:
        content_height = history_content.winfo_reqheight()
    else:
        content_height = 0
    
    frame_height = canvas.winfo_height()
    
    needs_scroll = content_height > frame_height
    
    if needs_scroll:
        scrollbar.state(["!disabled"])
        # Enable mouse wheel binding
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
    else:
        scrollbar.state(["disabled"])
        # Disable mouse wheel binding
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
        # Reset scroll position to top
        canvas.yview_moveto(0)
    
    # Force scrollbar to update its appearance
    scrollbar.update_idletasks()
        
def handle_resize(event, root, ui):
    width = root.winfo_width()
    height = root.winfo_height()

    min_height = 550
    max_height = 700
    height_clamped = max(min_height, min(height, max_height))
    factor = (height_clamped - min_height) / (max_height - min_height)
    entry_top_pady = 5 + factor * (15 - 5)
    entry_bottom_pady = 5 + factor * (25 - 5)
 
    if width >= 780:
        ui["history_frame"].pack(side="right", fill="y")
        ui["history_frame"].config(width=390)
        ui["history_frame"].pack_propagate(False)

        main_width = width - 390
        ui["main_frame"].pack(side="left", fill="both", expand=True)
        ui["main_frame"].config(width=main_width)
    else:
        ui["history_frame"].pack_forget()
        ui["main_frame"].pack(fill="both", expand=True)
        ui["main_frame"].config(width=width)

    if height <= 550:
        font_expr = ("Arial", 14)
        font_mem = ("Arial", 12)
        font_entry = ("Arial", 16)
    elif height < 700:
        font_expr = ("Arial", 17)
        font_mem = ("Arial", 15)
        font_entry = ("Arial", 19)
    else:
        font_expr = ("Arial", 20)
        font_mem = ("Arial", 18)
        font_entry = ("Arial", 22)

    ui["expression_label"].config(font=font_expr)
    ui["memory_label"].config(font=font_mem)
    ui["entry"].config(font=font_entry)
    ui["entry"].pack_configure(pady=(int(entry_top_pady), int(entry_bottom_pady)))

    ui["update_scrollbar_style"](ui, state["theme"])
    ui["canvas"].update_idletasks()
    ui["history_content"].update_idletasks()

def resource_path(relative_path):
    # For PyInstaller to find files inside the bundle
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def main():
    root = Tk()
    icon = PhotoImage(file=resource_path("docs/HK_png.png"))
    root.iconphoto(True, icon)
    root.minsize(390, 550)
    ui = setup_ui(root, safe_env, state)
    root.bind("<Configure>", lambda e: handle_resize(e, root, ui))

    ui["update_scrollbar_style"] = update_scrollbar_style
    root.after(50, lambda: update_scrollbar_style(ui, state["theme"]))

    entry = ui["entry"]
    expression_label = ui["expression_label"]
    memory_label = ui["memory_label"]
    key_to_command = {
        'primary':{
            '\\': lambda: Mc(memory_label, state),
            'm': lambda: Mr(entry, expression_label, state),
            'g': lambda: button_click('log(', entry, expression_label, state),
            'l': lambda: button_click('ln(', entry, expression_label, state),
            's': lambda: button_click('sin(', entry, expression_label, state),
            'c': lambda: button_click('cos(', entry, expression_label, state),
            't': lambda: button_click('tan(', entry, expression_label, state),
            'x': lambda: insert_operator('^2', entry, expression_label, state),
            '^': lambda: insert_operator('^', entry, expression_label, state),
            '(': lambda: button_click('(', entry, expression_label, state),
            ')': lambda: closing(entry, expression_label, state),
            '%': lambda: percent(entry, expression_label, state),
            'e': lambda: button_click('e', entry, expression_label, state),
            'p': lambda: button_click('π', entry, expression_label, state),
            '!': lambda: insert_factorial(entry, expression_label, safe_env, state),
            '|': lambda: ABS(entry, expression_label, state),
            '[': lambda: Mp(entry, memory_label, safe_env, state),
            ']': lambda: Ms(entry, memory_label, safe_env, state),
            'E': lambda: insert_operator('EXP', entry, expression_label, state),
            'w': lambda: insert_operator('^(1÷2)', entry, expression_label, state)
        },
        'second':{
            'r': lambda: button_click('rand', entry, expression_label, state),
            ',': lambda: insert_operator(',', entry, expression_label, state),
            'a': lambda: ans(entry, expression_label, state),
            'A': lambda: ans(entry, expression_label, state),
            'f': lambda: floor(entry, expression_label, state),
            'u': lambda: ceil(entry, expression_label, state),
            'S': lambda: button_click('asin(', entry, expression_label, state),
            'C': lambda: button_click('acos(', entry, expression_label, state),
            'T': lambda: button_click('atan(', entry, expression_label, state),
            'G': lambda: button_click('logy(', entry, expression_label, state),
            'X': lambda: insert_operator('^3', entry, expression_label, state),
            'W': lambda: insert_operator('^(1÷3)', entry, expression_label, state),
            'N': lambda: insert_operator('^(1÷', entry, expression_label, state),
            'v': lambda: button_click('sinh(', entry, expression_label, state),
            'b': lambda: button_click('cosh(', entry, expression_label, state),
            'n': lambda: button_click('tanh(', entry, expression_label, state)
        },
        "up": lambda: up(entry, expression_label),
    }
    root.bind("h", lambda e: toggle_history_view(root))
    root.bind_all("<KeyPress>", lambda event: on_key_press(event, root, ui["button_map"], key_to_command, state))
    root.mainloop()

if __name__ == "__main__":
    main()