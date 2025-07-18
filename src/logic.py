import math as m
import re
from .utils import (
    handle_error,
    find_matching_closing,
    find_last_operand,
    clean_number,
    update_memory_label,
    bind_hover_effect,
    bind_hover_effect_2nd
    )

def preprocess_expression(expr):
    expr = re.sub(r'(\d+(?:\.\d+)?)([+\-])(\d+(?:\.\d+)?)%', lambda m: f"({m.group(1)}{m.group(2)}{m.group(1)}*{m.group(3)}/100)", expr)

    expr = re.sub(r'(\%)(\d)', r'\1*\2', expr)
    expr = expr.replace("%", "/100").replace("MOD", "%").replace("^", "**").replace("×", "*").replace("÷", "/").replace("EXP", "*10**")

    #adding * if needed:
    expr = re.sub(r'(\d+(?:\.\d+)?)e([+-]?\d+)', r'(\1*10**\2)', expr)

    expr = re.sub(r'(\d)([a-zA-Z\(\π])',r'\1*\2', expr)
    expr = re.sub(r'(\))(\d|[a-zA-Z]|\()',r'\1*\2', expr)
    
    prev = None
    while prev != expr:
        prev = expr
        expr = re.sub(r'(e)(e|π)', r'\1*\2', expr)
        expr = re.sub(r'(π)(e|π)', r'\1*\2', expr)

    expr = re.sub(r'(π|e)(\d)', r'\1*\2', expr)
    expr = re.sub(r'(π|e)(a|s|l|c|t|\()', r'\1*\2', expr)

    functions = ['sin', 'cos', 'tan', 'log', 'ln']
    for func in functions:
        expr = re.sub(rf'{func}(\d+(\.\d+)?)', rf'{func}(\1)', expr)
    
    #auto-close unmatched parentheses
    open_parens = expr.count('(')
    close_parens = expr.count(')')
    if open_parens > close_parens:
        expr += ')'* (open_parens - close_parens)
    
    expr = expr.replace("rand", "rand()").replace("π", "pi")
    return expr

def button_click(value, entry, expression_label, state):
    if state["just_calculated"] == "success" and value.isdigit():
        entry.delete(0, "end")
        expression_label.config(text="")
    elif state["just_calculated"] == "error":
        entry.delete(0, "end")
        expression_label.config(text="")
    state["just_calculated"] = None
    current = entry.get()
    if value.isdigit():
        match = re.search(r'(?:^|[\+\-\÷\×\(\)\^])0$', current)
        if match:
            entry.delete(len(current) - 1, "end")
    elif current and current[-1] == '.':
        return
    entry.insert("end", value)
    expression_label.config(text=entry.get())

def insert_operator(symbol, entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in "+-÷×(^.PD,":
        return
    entry.insert("end", symbol)
    expression_label.config(text=entry.get())

def clear(entry, expression_label):
    entry.delete(0, "end")
    expression_label.config(text="")

def delete(entry, expression_label, state):
    current = entry.get()
    if not current:
        return
    if current[-1].isalpha():
        for keyword in ['floor', 'ceil', 'abs', 'round', 'logy', 'log', 'rand', 'ln', 'asin', 'acos', 'atan', 'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'MOD', 'EXP', 'pi']:
            if current.endswith(keyword):
                entry.delete(len(current) - len(keyword), "end")
                expression_label.config(text=entry.get())
                state["just_calculated"] = None
                return
    entry.delete(len(current)-1, "end")
    expression_label.config(text=entry.get())
    state["just_calculated"] = None


def negative(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get().strip()
    if not current:
        entry.insert(0, '-')
        expression_label.config(text='-')
        return
    if current == '(-1)×(' or current == '(-1)×' or current == '-' or current == '-(':
        entry.delete(0, "end")
        expression_label.config(text="")
        return
    if re.fullmatch(r'-?\d+(\.\d+)?', current) or re.fullmatch(r'-?\d+\.', current):
        if current.startswith('-'):
            new = current[1:]
        else:
            new = '-' + current
        entry.delete(0, "end")
        entry.insert(0, new)
        expression_label.config(text=new)
        return
    if current.startswith('('):
        closing_index = find_matching_closing(current, 1)
        if closing_index == len(current) - 1:
            entry.delete(0, "end")
            entry.insert(0, '-' + current)
            expression_label.config(text='-' + current)
            return
    if current.startswith('-('):
        closing_index = find_matching_closing(current, 2)
        if closing_index == len(current) - 1:
            unwrapped = current[2:-1]
            entry.delete(0, "end")
            entry.insert(0, unwrapped)
            expression_label.config(text=unwrapped)
            return    
    if current.startswith("(-1)×("):
        closing_index = find_matching_closing(current, 6)
        if closing_index == len(current) - 1:
            unwrapped = current[6:-1]
            entry.delete(0, "end")
            entry.insert(0, unwrapped)
            expression_label.config(text=unwrapped)
            return
    wrapped = f"-({current})"
    entry.delete(0, "end")
    entry.insert(0, wrapped)
    expression_label.config(text=wrapped)


def ABS(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get().strip()
    if not current or current[-1] in "+-÷×(^PD,":
        entry.insert("end", 'abs(')
        expression_label.config(text=entry.get())
        return
    if current.startswith("abs("):
        closing_index = find_matching_closing(current, 4)
        if closing_index == len(current) - 1:
            return
    last = find_last_operand(current)
    if not last:
        entry.insert("end", 'abs(')
        expression_label.config(text=entry.get())
        return
    if last.startswith('(') and last.endswith(')'):
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + "abs" + last)
        expression_label.config(text=entry.get())
        return
    if last[-1] == '.':
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + "abs(" + last)
        expression_label.config(text=entry.get())
        return
    entry.delete(0, "end")
    entry.insert(0, current[:-len(last)] + "abs(" + last + ")")
    expression_label.config(text=entry.get())

def insert_factorial(entry, expression_label, safe_env, state):
    handle_error(entry, expression_label, state)
    current = entry.get().strip()
    if not current or current[-1] in "+-÷×(^DP%":
        entry.insert("end", "factorial(")
        expression_label.config(text=entry.get())
        return
    last = find_last_operand(current)
    try:
        val = eval(last, safe_env)
        if not (isinstance(val, int) and val >= 0):
            raise ValueError
        if last.startswith('(') and last.endswith(')'):
            new_expr = current[:-len(last)] + f"factorial{last}"
        else:    
            new_expr = current[:-len(last)] + f"factorial({last})"
    except:
        new_expr = current + "×factorial("
    entry.delete(0, "end")
    entry.insert(0, new_expr)
    expression_label.config(text=new_expr)

def toggle_2nd_mode(primary_mode, second_mode, toggle_buttons, second_btn, themes, state):
    state["is_2nd"] = not state["is_2nd"]
    mode = second_mode if state["is_2nd"] else primary_mode
    for pos, (text, cmd) in mode.items():
        btn = toggle_buttons.get(pos)
        if btn:
            btn.config(text=text, command=cmd)
    second_btn.config(
        bg=themes[state["theme"]]["2nd_btn"]["2nd_bg"] if state["is_2nd"] else themes[state["theme"]]["2nd_btn"]["bg"],
        activebackground=themes[state["theme"]]["2nd_btn"]["2nd_activebackground"] if state["is_2nd"] else themes[state["theme"]]["2nd_btn"]["activebackground"]
    ) 

def Mp(entry, memory_lable, safe_env, state):
    try:
        current = entry.get()
        if current.endswith('%') and re.match(r'^\d+(\.\d+)?%$', current):
            percent_value = float(current[:-1])
            base = state['memory']
            val = base * percent_value / 100
        else:
            current = preprocess_expression(current) 
            val = eval(current, safe_env)
        val = clean_number(val)
        state["memory"] += val
        state["memory"] = clean_number(state["memory"])
        update_memory_label(memory_lable, state)
    except:
        pass

def Ms(entry, memory_label, safe_env, state):
    try:
        current = entry.get()
        if current.endswith('%') and re.match(r'^\d+(\.\d+)?%$', current):
            percent_value = float(current[:-1])
            base = state['memory']
            val = base * percent_value / 100
        else:
            current = preprocess_expression(current)
            val = eval(current, safe_env)
        val = clean_number(val)
        state["memory"] -= val
        state["memory"] = clean_number(state["memory"])
        update_memory_label(memory_label, state)
    except:
        pass

def Mc(memory_label, state):
    state["memory"] = 0
    update_memory_label(memory_label, state)

def Mr(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in '+-÷×^%(DP':  # inserting just memory
        entry.insert("end", str(state["memory"]))
    else:
        entry.insert("end", '×' + str(state["memory"]))
    expression_label.config(text=entry.get())

def ans(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    if not state["Ans"]:
        return
    current = entry.get()
    if not current or current[-1] in "+-÷×(^%DP":
        entry.insert("end", str(state["Ans"]))
    else:
        entry.insert("end", '×' + str(state["Ans"]))
    expression_label.config(text=entry.get())


def Round(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in "+-÷×(^":
        entry.insert("end", "round(")
        expression_label.config(text=entry.get())
        return
    last = find_last_operand(current)
    if not last:
        entry.insert("end", "round(")
        expression_label.config(text=entry.get())
        return
    if last.startswith("round(") and last.endswith(")"):
        return
    new_expr = current[:-len(last)] + f'round({last}'
    entry.delete(0, "end")
    entry.insert(0, new_expr)
    expression_label.config(text=new_expr)

def dot(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in "+-÷×()^.PD,%":
        return
    tokens = re.split(r'[+\-÷×*/^(),]', current)
    last_token = tokens[-1] if tokens else ''
    if '.' in last_token:
        return
    entry.insert("end", '.')
    expression_label.config(text=entry.get())

def x_1(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in "+-÷×()^PD,":
        entry.insert("end", '1÷(')
        expression_label.config(text=entry.get())
        return
    last = find_last_operand(current)
    if not last:
        entry.insert("end", '1÷(')
        expression_label.config(text=entry.get())
        return
    if last.startswith("1÷(") and last.endswith(")"):
        inside = last[3:-1]
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + inside)
        expression_label.config(text=entry.get())
        return
    if last[0] == '(' and last[-1] == ')':
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + "1÷" + last)
        expression_label.config(text=entry.get())
        return
    if last[-1] == '.':
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + "1÷(" + last)
        expression_label.config(text=entry.get())
        return    
    entry.delete(0, "end")
    entry.insert(0, current[:-len(last)] + '1÷(' + last + ')')
    expression_label.config(text=entry.get())

def percent(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in "+-÷×()^PD,%":
        entry.insert("end", "1%")
    elif current[-1] == ".":
        return
    else:
        entry.insert("end", "%")
    expression_label.config(text=entry.get())

def closing(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get().strip()
    if not current or current[-1] in "+-÷×(^.PD,%":
        return
    open_count = current.count("(")
    close_count = current.count(")")
    if open_count > close_count:
        entry.insert("end", ")")
        expression_label.config(text=entry.get())

def floor(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in "+-÷×(^PD,":
        entry.insert("end", "floor(")
        expression_label.config(text=entry.get())
        return
    last = find_last_operand(current)
    if not last:
        entry.insert("end", "floor(")
        expression_label.config(text=entry.get())
        return
    if last.endswith('.'):
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + "floor(" + last)
        expression_label.config(text=entry.get())
        return
    if last.startswith("floor(") and last.endswith(")"):
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + last[6:-1])
        expression_label.config(text=entry.get())
        return
    entry.delete(0, "end")
    entry.insert(0, current[:-len(last)] + f"floor({last})")
    expression_label.config(text=entry.get())

def ceil(entry, expression_label, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in "+-÷×(^PD,":
        entry.insert("end", "ceil(")
        expression_label.config(text=entry.get())
        return
    last = find_last_operand(current)
    if not last:
        entry.insert("end", "ceil(")
        expression_label.config(text=entry.get())
        return
    if last.endswith('.'):
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + "ceil(" + last)
        expression_label.config(text=entry.get())
        return
    if last.startswith("ceil(") and last.endswith(")"):
        entry.delete(0, "end")
        entry.insert(0, current[:-len(last)] + last[6:-1])
        expression_label.config(text=entry.get())
        return
    entry.delete(0, "end")
    entry.insert(0, current[:-len(last)] + f"ceil({last})")
    expression_label.config(text=entry.get())

def toggle_theme(root, themes, ui, rad_btn, theme_btn, buttons, state):
    # Toggle theme name
    current = state.get("theme")
    new_theme = "dark" if current == "light" else "light"
    theme = themes[new_theme]
    state["theme"] = new_theme
    # Apply root and containers
    root.config(bg=theme["root"]["bg"])
    ui["main_frame"].config(bg=theme["main_frame"]["bg"])
    ui["top_frame"].config(bg=theme["top_frame"]["bg"])
    ui["bottom_bar"].config(bg=theme["bottom_bar"]["bg"])
    ui["top_bar"].config(bg=theme["top_bar"]["bg"])
    ui["button_frame"].config(bg=theme["button_frame"]["bg"])
    # History
    ui["history_frame"].config(bg=theme["history_frame"]["bg"])
    ui["canvas"].config(bg=theme["history_frame"]["bg"])
    ui["history_content"].config(bg=theme["history_frame"]["bg"])
    ui["clear_btn"].config(
        bg=theme["buttons_color"][(4, 0)][0],
        fg=theme["entry"]["fg"],
        activebackground=theme["buttons_color"][(4, 0)][2],
        activeforeground=theme["buttons_color"][(4, 0)][3]
    )
    for i, item in enumerate(ui["history_items"]):
        bg = theme["history"]["even_bg"] if i % 2 == 0 else theme["history"]["odd_bg"]
        item.config(bg=bg)
        children = item.winfo_children()
        children[0].config(bg=bg, fg=theme["expression_label"]["fg"])    # expression label
        children[1].config(bg=bg, fg=theme["entry"]["fg"])              # answer label
        bind_hover_effect(children[0], bg, theme["history"]["hover"])
        bind_hover_effect(children[1], bg, theme["history"]["hover"])
    # Force scrollbar update after theme change
    ui["update_scrollbar_style"](ui, state["theme"])
    # Force immediate UI refresh
    ui["canvas"].update_idletasks()

    # Lables and entry
    ui["memory_label"].config(**theme["memory_label"])
    ui["expression_label"].config(**theme["expression_label"])
    ui["entry"].config(**theme["entry"])
    # Theme button and rad button
    theme_btn.config(**theme["theme_btn"])
    rad_btn.config(**theme["rad_btn"])
    if new_theme == "dark":
        bind_hover_effect(rad_btn, "gray12", "gray20") 
    elif new_theme == "light":
        bind_hover_effect(rad_btn, theme["rad_btn"]["bg"], "#BFD3EB")
    # 2nd button
    ui["2nd_btn"].config(
        bg=theme["2nd_btn"]["bg"],
        fg=theme["2nd_btn"]["fg"],
        activebackground=theme["2nd_btn"]["activebackground"],
        activeforeground=theme["2nd_btn"]["activeforeground"]
    )
    if new_theme == "dark":
        bind_hover_effect_2nd(ui["2nd_btn"], theme["2nd_btn"]["bg"], theme["2nd_btn"]["2nd_bg"], "gray20", state)
    elif new_theme == "light":
        bind_hover_effect_2nd(ui["2nd_btn"], theme["2nd_btn"]["bg"], theme["2nd_btn"]["2nd_bg"], "#BFD3EB", state)
    # button grid
    for (row, col), btn in buttons.items():
        if (row, col) in theme["buttons_color"]:
            bg, fg, abg, afg = theme["buttons_color"][(row, col)]
            btn.config(bg=bg, fg=fg, activebackground=abg, activeforeground=afg)
            if new_theme == "dark":
                hover_color = "gray20" if bg == "gray12" else "gray12"
                bind_hover_effect(btn, bg, hover_color) 
            elif new_theme == "light":
                hover_color = "#BFD3EB" if bg == "#D6E4F0" else "#CFCFCF"
                bind_hover_effect(btn, bg, hover_color)

def rad_deg(rad_btn, safe_env, state):
    state["is_radian"] = not state["is_radian"]
    rad_btn.config(text="Rad" if state["is_radian"] else "Deg")
    def sin_func(x):
        return m.sin(x if state["is_radian"] else m.radians(x))
    def cos_func(x):
        return m.cos(x if state["is_radian"] else m.radians(x))
    def tan_func(x):
        return m.tan(x if state["is_radian"] else m.radians(x))
    def asin_func(x):
        val = m.asin(x)
        return val if state["is_radian"] else m.degrees(val)
    def acos_func(x):
        val = m.acos(x)
        return val if state["is_radian"] else m.degrees(val)
    def atan_func(x):
        val = m.atan(x)
        return val if state["is_radian"] else m.degrees(val)
    def sinh_func(x):
        return m.sinh(x if state["is_radian"] else m.radians(x))
    def cosh_func(x):
        return m.cosh(x if state["is_radian"] else m.radians(x))
    def tanh_func(x):
        return m.tanh(x if state["is_radian"] else m.radians(x))
    
    safe_env.update({
        'sin': sin_func,
        'cos': cos_func,
        'tan': tan_func,
        'asin': asin_func,
        'acos': acos_func,
        'atan': atan_func,
        'sinh': sinh_func,
        'cosh': cosh_func,
        'tanh': tanh_func
    })
    rad_btn.config(text="Rad" if state["is_radian"] else "Deg")

def up(entry, expression_label):
    expr = expression_label.cget("text")
    if expr:
        if expr[-1] == '=':
            entry.delete(0, "end")
            entry.insert(0, expr[:-1])

def calculate(entry, expression_label, safe_env, state, ui, themes):
    try:
        current = entry.get()
        if not current:
            return
        processed = preprocess_expression(current)
        result = eval(processed, safe_env)
        result = clean_number(result)
        expr = processed.replace('%', 'MOD').replace('/100', '%') \
                        .replace("*10**", 'EXP').replace('**', '^') \
                        .replace("*", "×").replace("/", "÷") \
                        .replace("pi", "π").replace("rand()", "rand")
        expression_label.config(text=expr + '=')
        entry.delete(0, "end")
        entry.insert(0, str(result))
        state["Ans"] = result
        state["just_calculated"] = "success"
        add_to_history(expr, str(result), ui, themes, state)
        
    except Exception as e:
        entry.delete(0, "end")
        entry.insert(0, "Error")
        state["just_calculated"] = "error"

def insert_history_expression(entry, expression_label, value):
    entry.delete(0, "end")
    entry.insert(0, value)
    expression_label.config(text=entry.get())

def insert_history_ans(entry, expression_label, value, state):
    handle_error(entry, expression_label, state)
    current = entry.get()
    if not current or current[-1] in "+-÷×(^%DP":
        entry.insert("end", str(value))
    else:
        entry.insert("end", '×' + str(value))
    expression_label.config(text=entry.get())

def add_to_history(expression, answer, ui, themes, state):
    from tkinter import Frame, Label
    MAX_HISTORY = ui.get("max_history", 20)
    items = ui["history_items"]
    if "history_index" not in ui:
        ui["history_index"] = 1

    if len(items) >= MAX_HISTORY:
        old = items.pop(0)
        old.destroy()
    if ui["history_index"] % 2 == 0:
        ui["history_index"] -= 1
    else:
        ui["history_index"] += 1
    idx = ui["history_index"]
    theme = themes[state["theme"]]
    bg = theme["history"]["even_bg"] if idx % 2 ==0 else theme["history"]["odd_bg"]
    font_expr = ui["expression_label"].cget("font")
    font_ans = ui["entry"].cget("font")
    wrapper = Frame(ui["history_content"], bg=bg)
    wrapper.pack(fill="x", pady=2, padx=5)
    expr_lbl = Label(wrapper, text=expression + '=', font=font_expr, bg=bg, fg=theme["history"]["expression_fg"], anchor="e", justify="right")
    expr_lbl.pack(fill="x")
    ans_lbl = Label(wrapper, text=answer, font=font_ans, bg=bg, fg=theme["history"]["answer_fg"], anchor="e", justify="right")
    ans_lbl.pack(fill="x")

    expr_lbl.bind("<Button-1>", lambda e, val = expression: insert_history_expression(ui["entry"], ui["expression_label"], val))
    ans_lbl.bind("<Button-1>", lambda e, val=answer: insert_history_ans(ui["entry"], ui["expression_label"], val, state))

    bind_hover_effect(expr_lbl, bg, theme["history"]["hover"])
    bind_hover_effect(ans_lbl, bg, theme["history"]["hover"])

    ui["history_items"].append(wrapper)
    
    # Force immediate UI update
    ui["canvas"].update_idletasks()
    ui["adjust_scrollregion"]()
    ui["update_scrollbar_style"](ui, state["theme"])
    
    # Scroll to bottom only if needed
    content_height = ui["history_content"].winfo_reqheight()
    frame_height = ui["canvas"].winfo_height()
    if content_height > frame_height:
        ui["canvas"].yview_moveto(1.0)

def clear_history(ui, state):
    for item in ui["history_items"]:
        item.destroy()
    ui["history_items"].clear()
    ui["history_index"] = 1  # Reset index
    
    # Reset scroll region and position
    canvas = ui["canvas"]
    canvas.configure(scrollregion=(0, 0, 0, 0))
    canvas.yview_moveto(0)
    
    # Explicitly update scrollbar state
    ui["update_scrollbar_style"](ui, state["theme"])
    
    # Force immediate UI update
    canvas.update_idletasks()
    ui["history_content"].update_idletasks()

def toggle_history_view(root):
    if root.winfo_width() < 780:
        root.geometry("780x550")
    else:
        root.geometry("390x550")

def show_help():
    import tkinter as tk
    from tkinter import Toplevel, Text, Scrollbar

    help_text = """\
🔑 Hotkeys:

----- Basic -----
Digits         → 0-9
Enter or =     → =
Backspace or d → DEL
Delete         → AC
z              → ±

----- Operators -----
+  -           → +  -
*  /           → ×  ÷
^  N           → ^  ⁿ√
%              → %
(  )           → (  )
.  ,           → .  ,

----- Functions -----
g              → log
G              → log(x,y)
l              → ln
s / c / t      → sin / cos / tan
S / C / T      → arcsin / arccos / arctan
v / b / n      → sinh / cosh / tanh
p              → π
e              → e
E              → EXP
x / X          → x² / x³
w / W          → √ / ³√
!              → n!
|              → |x| (ABS)

----- Memory -----
m              → MR (Recall)
\\              → MC (Clear)
[ / ]          → M+ / M-
a or A         → ANS

----- Advanced -----
r              → rand
f / u          → floor/ceil
` (backtick)   → Switch Mode
h              → Toggle history frame
R or F2        → Switch Rad-Deg
q or F9        → Switch Theme
H or F1        → Help
"""
    help_win = Toplevel()
    help_win.title("Help / Hotkeys")
    help_win.geometry("390x550")
    
    text_widget = Text(help_win, wrap="word", font=("Consolas", 11), bg="#1e1e1e", fg="white")
    text_widget.insert("1.0", help_text)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True)

    # Optional: make window modal
    help_win.transient()
    help_win.grab_set()


key_to_button_text = {
    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
    '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    'Return': '=', 'KP_Enter': '=', 'enter': '=', 'equal': '=',
    'BackSpace': 'DEL', 'd': 'DEL', 'Delete': 'AC',
    'F1': 'Help', 'H': 'Help', 'F9': 't', 'q': 't', 'F2': 'r', 'R': 'r',
    'z': '±',
    'm': 'MR', 'g': 'log', 'l': 'ln', 'E': 'EXP',
    'x': 'x²', 'e': 'e', 'p': 'π', 'n': 'n!', 'M+': 'M+', 'MC': 'MC', 'w': '√'
}

shift_map = {
    '*': '×', '/': '÷', '+': '+', '-': '-',
    '.': '.', '`': '2nd', '[': 'M+', ']': 'M-',
    '^': '^', '(': '(', ')': ')', '%': '%', '!': 'n!', '|': '|x|',
    '\\': 'MC', 's': 'sin', 'c': 'cos', 't': 'tan'
}

second_to_primary = {
    'r': 'M+',
    ',': 'MC',
    'a': 'm',
    'A': 'm',
    'f': '(',
    'u': ')',
    'S': 's',
    'C': 'c',
    'T': 't',
    'G': 'g',
    'X': 'x',
    'W': 'w',
    'N': '^',
    'v': 'e',
    'b': 'p',
    'n': '!'
}

def on_key_press(event, root, button_map, key_to_command, state):
    key = event.keysym
    char = event.char

    cmd1 = key_to_command['primary'].get(key) or key_to_command['primary'].get(char)
    cmd2 = key_to_command['second'].get(key) or key_to_command['second'].get(char)

    if state['is_2nd'] and cmd1:
        cmd1()
        return
    if not state['is_2nd'] and cmd2:
        cmd2()
        return
    if state['is_2nd'] and cmd2:
        cmd2()
        btn_key = key if key in key_to_command['second'] else char
        text = second_to_primary.get(btn_key)
        btn_text = key_to_button_text.get(text) or shift_map.get(text)
        if btn_text:
            btn = button_map.get(btn_text)
            if btn:
                btn.config(relief="sunken")
                root.after(100, lambda: btn.config(relief="raised"))
        return
    btn_text = key_to_button_text.get(key) or shift_map.get(char)
    if btn_text:
        if btn_text == 'Help':
            show_help()
            return
        btn = button_map.get(btn_text)
        if btn:
            btn.config(relief="sunken")
            root.after(100, lambda: btn.config(relief="raised"))
            btn.invoke()
    elif event.keysym == "Up":
        cmd = key_to_command["up"]
        cmd()