import re

def find_matching_closing(current, index):
    depth = 0
    for i in range(index, len(current)):
        if current[i] == "(":
            depth += 1
        elif current[i] == ")":
            if depth == 0:
                return i
            depth -= 1
    return -1

def find_last_operand(expr):
    expr = expr.strip()
    if not expr:
        return ""
    i = len(expr) - 1
    count = 0
    while i >= 0:
        char = expr[i]
        if char == ')':
            count += 1
        elif char == '(':
            count -= 1
        elif count == 0 and re.match(r"[+\-*/×÷^%]", char):
            break
        elif count == 0 and expr[max(0, i-2):i+1] in ["MOD", "EXP"]:
            i -= 2
            break
        i -= 1
    return expr[i+1:].strip()

def clean_number(n):
    if isinstance(n, float):
        n = round(n, 12)
        if n.is_integer():
            return int(n)
    return n

def handle_error(entry, expression_label, state):
    if state["just_calculated"] == "error":
        entry.delete(0, "end")
        expression_label.config(text="")
    state["just_calculated"] = None

def bind_hover_effect(button, normal_color, hover_color):
    button.bind("<Enter>", lambda e: button.config(bg=hover_color))
    button.bind("<Leave>", lambda e: button.config(bg=normal_color))
    
def bind_hover_effect_2nd(button, bg, bg_2nd, hover, state):
    button.bind("<Enter>", lambda e: button.config(bg=hover))
    button.bind("<Leave>", lambda e: button.config(bg=bg_2nd if state["is_2nd"] else bg))
    
def update_memory_label(memory_lable, state):
    memory_lable.config(text=f'M: {state["memory"]}')

def bind_scroll_behavior(canvas):
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/macOS
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux up
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux down
