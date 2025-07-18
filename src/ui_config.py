from tkinter import Entry, Label, Button, Frame, Scrollbar, Canvas, ttk, VERTICAL, RIGHT, LEFT, Y
from .logic import (
    button_click,
    insert_operator,
    clear,
    delete,
    negative,
    ABS,
    insert_factorial,
    toggle_2nd_mode,
    Mp, Ms, Mc, Mr,
    ans,
    Round,
    dot,
    x_1,
    percent,
    closing,
    floor,
    ceil,
    toggle_theme,
    rad_deg,
    up,
    clear_history,
    calculate
)
from .utils import (
    bind_hover_effect,
    bind_hover_effect_2nd,
    bind_scroll_behavior
)

#Themes

themes = {
    "dark": {
        "root"         :{"bg": "#232323"},
        "main_frame"   :{"bg": "#232323"},
        "history_frame":{"bg": "#202020"}, 
        "history"         :{
            "even_bg"      : "#262626",
            "odd_bg"       : "#202020",
            "hover"        : "#333333",
            "expression_fg": "gray",
            "answer_fg"    : "white"
        },
        "clear_btn"       :{
            "bg": "#404040",
            "fg": "white",
            "activebackground": "#303030",
            "activeforeground": "gray"
        },
        "top_frame"    :{"bg": "#232323"},
        "top_bar"      :{"bg": "#232323"},
        "bottom_bar"   :{"bg": "#232323"},
        "button_frame" :{"bg": "#232323"},
        "memory_label"    :{
            "bg": "#232323",
            "fg": "gray",
        },
        "expression_label":{
            "bg": "#232323",
            "fg": "gray"
        },
        "entry"           :{
            "bg": "#202020",
            "fg": "white"
        },
        "theme_btn"       :{
            "text"            : "🌙",
            "bg"              : "#232323",
            "fg"              : "white",
            "activebackground": "#232323",
            "activeforeground": "gray"
        },
        "rad_btn"         :{
            "bg"              : "gray12",
            "fg"              : "white",
            "activebackground": "gray7",
            "activeforeground": "gray"
        },
        "2nd_btn"         :{
            "bg"              : "gray12",
            "fg"              : "white",
            "activebackground": "gray7",
            "activeforeground": "gray",
            "2nd_bg"          : "gray30",
            "2nd_activebackground": "gray7"
        },
        "buttons_color"   :{# (row, colum): (bg, fg, activebackground, activeforeground)
            (0, 1): ("gray12", "white", "gray7", "gray"),
            (0, 2): ("gray12", "white", "gray7", "gray"),
            (0, 3): ("gray12", "white", "gray7", "gray"),
            (0, 4): ("gray12", "white", "gray7", "gray"),
            (1, 0): ("gray12", "white", "gray7", "gray"),
            (1, 1): ("gray12", "white", "gray7", "gray"),
            (1, 2): ("gray12", "white", "gray7", "gray"),
            (1, 3): ("gray12", "white", "gray7", "gray"),
            (1, 4): ("gray12", "white", "gray7", "gray"),
            (2, 0): ("gray12", "white", "gray7", "gray"),
            (2, 1): ("gray12", "white", "gray7", "gray"),
            (2, 2): ("gray12", "white", "gray7", "gray"),
            (2, 3): ("gray12", "white", "gray7", "gray"),
            (2, 4): ("gray12", "white", "gray7", "gray"),
            (3, 0): ("gray12", "white", "gray7", "gray"),
            (3, 1): ("gray12", "white", "gray7", "gray"),
            (3, 2): ("gray12", "white", "gray7", "gray"),
            (3, 3): ("gray12", "white", "gray7", "gray"),
            (3, 4): ("gray12", "white", "gray7", "gray"),
            (4, 0): ("gray20", "white", "gray7", "gray"), # # # #
            (4, 1): ("gray20", "white", "gray7", "gray"),
            (4, 2): ("gray20", "white", "gray7", "gray"),
            (4, 3): ("gray30", "white", "gray7", "gray"),
            (4, 4): ("gray30", "white", "gray7", "gray"),
            (5, 0): ("gray20", "white", "gray7", "gray"),
            (5, 1): ("gray20", "white", "gray7", "gray"),
            (5, 2): ("gray20", "white", "gray7", "gray"),
            (5, 3): ("gray30", "white", "gray7", "gray"),
            (5, 4): ("gray30", "white", "gray7", "gray"),
            (6, 0): ("gray20", "white", "gray7", "gray"),
            (6, 1): ("gray20", "white", "gray7", "gray"),
            (6, 2): ("gray20", "white", "gray7", "gray"),
            (6, 3): ("gray30", "white", "gray7", "gray"),
            (6, 4): ("gray30", "white", "gray7", "gray"),
            (7, 0): ("gray20", "white", "gray7", "gray"),
            (7, 1): ("gray20", "white", "gray7", "gray"),
            (7, 2): ("gray20", "white", "gray7", "gray"),
            (7, 3): ("gray30", "white", "gray7", "gray"),
            (7, 4): ("gray30", "#FF9500", "gray7", "#D57C00")
        }   
    },
    "light": {
        "root"         :{"bg": "#F2F2F2"},
        "main_frame"   :{"bg": "#F2F2F2"},
        "history_frame":{"bg": "#DDDDEF"},
        "history"         :{
            "even_bg"      : "#EDEDED",
            "odd_bg"       : "#DDDDDD",
            "hover"        : "#CCCCCC",
            "expression_fg": "#555555",
            "answer_fg"    : "#000000"
        },
        "clear_btn"       :{
            "bg": "#E0E0E0",
            "fg": "#000000",
            "activebackground": "#CCCCCC",
            "activeforeground": "#000000"
        },
        "top_frame"    :{"bg": "#F2F2F2"},
        "top_bar"      :{"bg": "#F2F2F2"},
        "bottom_bar"   :{"bg": "#F2F2F2"}, 
        "button_frame" :{"bg": "#F2F2F2"},
        "memory_label"    :{
            "bg": "#F2F2F2",
            "fg": "#303030"
        },
        "expression_label":{
            "bg": "#F2F2F2",
            "fg": "#303030"
        },
        "entry"           :{
            "bg": "#FFFFFF",
            "fg": "#000000",
            "insertbackground": "#050505"
        },
        "theme_btn"       :{
            "text"            : "⭐",
            "bg"              : "#F2F2F2",
            "fg"              : "#232323",
            "activebackground": "#F2F2F2",
            "activeforeground": "#202020"
        },
        "rad_btn"         :{
            "bg"              : "#D6E4F0",
            "fg"              : "#050505",
            "activebackground": "#C6D4E0",
            "activeforeground": "#000000"
        },
        "2nd_btn"         :{
            "bg"              : "#D6E4F0",
            "fg"              : "#050505",
            "activebackground": "#C6D4E0",
            "activeforeground": "#000000",
            "2nd_bg"          : "#E4DAF5",
            "2nd_activebackground": "#D0C4EB"
        },
        "buttons_color"   :{# (row, colum): (bg, fg, activebackground, activeforeground)
            (0, 1): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (0, 2): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (0, 3): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (0, 4): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (1, 0): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (1, 1): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (1, 2): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (1, 3): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (1, 4): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (2, 0): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (2, 1): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (2, 2): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (2, 3): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (2, 4): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (3, 0): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (3, 1): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (3, 2): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (3, 3): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (3, 4): ("#D6E4F0", "#050505", "#C6D4E0", "#000000"),
            (4, 0): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"), # # # #
            (4, 1): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (4, 2): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (4, 3): ("#E4DAF5", "#050505", "#D0C4EB", "#000000"),
            (4, 4): ("#E4DAF5", "#050505", "#D0C4EB", "#000000"),
            (5, 0): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (5, 1): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (5, 2): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (5, 3): ("#E4DAF5", "#050505", "#D0C4EB", "#000000"),
            (5, 4): ("#E4DAF5", "#050505", "#D0C4EB", "#000000"),
            (6, 0): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (6, 1): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (6, 2): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (6, 3): ("#E4DAF5", "#050505", "#D0C4EB", "#000000"),
            (6, 4): ("#E4DAF5", "#050505", "#D0C4EB", "#000000"),
            (7, 0): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (7, 1): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (7, 2): ("#F5F5F5", "#050505", "#E0E0E0", "#000000"),
            (7, 3): ("#E4DAF5", "#050505", "#D0C4EB", "#000000"),
            (7, 4): ("#E4DAF5", "#FF9500", "#D0C4EB", "#F08000")
        }   
    }
}

def setup_ui(root, safe_env, state, theme="dark"):
    button_map ={}
    buttons = {}
    toggle_buttons = {}
    ui = {
        "2nd_btn"            : None,
        "memory_label"       : None,
        "history_items"      : [],
        "main_frame"         : None,
        "history_frame"      : None,
        "clear_btn"          : None,
        "top_frame"          : None,
        "top_bar"            : None,
        "bottom_bar"         : None,
        "expression_label"   : None,
        "entry"              : None,
        "button_frame"       : None,
        "style"              : None,
        "scrollbar"          : None,
        "adjust_scrollregion": None
    }

    root.configure(bg="#232323")
    root.title("Python Calculator HK")
    root.geometry("390x550")
    
    main_frame = Frame(root, bg="#232323")
    main_frame.pack(side="top", fill="both", expand=True)

    # History Frame
    history_frame = Frame(root, bg="#202020")
    
    scroll_area = Frame(history_frame, bg ="#202020")
    scroll_area.pack(side="top", fill="both", expand=True)
    
    canvas = Canvas(scroll_area, bg="#202020", highlightthickness=0)
    
    style = ttk.Style()
    style.theme_use("default")
    
    # Enhanced scrollbar styles with active states
    style.map(
        "Dark.Vertical.TScrollbar",
        background=[("active", "#777"), ("disabled", "#444")],
        troughcolor=[("active", "#333"), ("disabled", "#2E2E2E")]
    )
    
    style.map(
        "Light.Vertical.TScrollbar",
        background=[("active", "#999"), ("disabled", "#777")],
        troughcolor=[("active", "#ddd"), ("disabled", "#ccc")]
    )
    
    style.configure("Dark.Vertical.TScrollbar",
        troughcolor="#2E2E2E",
        background="#555",
        bordercolor="#111",
        arrowcolor="#ddd",
        relief="flat",
        width=10
    )
    
    style.configure("Light.Vertical.TScrollbar",
        troughcolor="#ccc",
        background="#888",
        bordercolor="#ddd",
        arrowcolor="#222",
        relief="flat",
        width=10
    )

    style_name = "Dark.Vertical.TScrollbar" if theme == "dark" else "Light.Vertical.TScrollbar"
    scrollbar = ttk.Scrollbar(scroll_area, orient=VERTICAL, command=canvas.yview, style=style_name)
    
    history_content = Frame(canvas, bg="#202020")

    def adjust_scrollregion(event=None):
        canvas.update_idletasks()
        
        # Handle empty history case
        if not ui["history_items"]:
            canvas.configure(scrollregion=(0, 0, 0, 0))
        else:
            bbox = canvas.bbox("all") or (0, 0, 0, 0)
            canvas.configure(scrollregion=bbox)
        
        # Always update scrollbar after adjusting region
        if "update_scrollbar_style" in ui:
            ui["update_scrollbar_style"](ui, state["theme"])


    history_content.bind("<Configure>", adjust_scrollregion)    
    canvas_window_id = canvas.create_window((0, 0), window=history_content, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window_id, width=e.width))
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=LEFT, fill="both", expand=True)
    scrollbar.pack(side=RIGHT, fill="y")
    
    bind_scroll_behavior(canvas)

    root.after(100, adjust_scrollregion)

    #   Clear button
    clear_btn = Button(
        history_frame,
        text="Clear",
        font=("Arial", 12),
        bg="#404040",
        fg="white",
        activebackground="#303030",
        activeforeground="gray",
        command =lambda: clear_history(ui, state)
    )
    clear_btn.pack(side="bottom", fill="x")

    main_frame.grid_rowconfigure(0, weight=1) # Top frame
    main_frame.grid_rowconfigure(1, weight=5) # Button frame
    main_frame.grid_columnconfigure(0, weight=1)

    top_frame = Frame(main_frame, bg="#232323")
    top_frame.grid(row=0, column=0, sticky="nsew")

    top_bar = Frame(top_frame, bg="#232323")
    top_bar.pack(fill="x", pady=(5, 10), padx=10)

    bottom_bar = Frame(top_frame, bg="#232323")
    bottom_bar.pack(side="bottom", fill="x", pady=(0, 10), padx=10)
    
    expression_label = Label(bottom_bar, text="", font=("Arial", 14), fg="gray", bg="#232323", anchor="e")
    expression_label.pack(padx=10, fill="x")

    entry = Entry(bottom_bar, bg="#202020", fg="white", font=("Arial", 16), borderwidth=2, relief="ridge", justify="right")
    entry.pack(padx=10, pady=(5, 5), fill="x")

    button_frame = Frame(main_frame, bg="#232323")
    button_frame.grid(row=1, column=0, sticky="nsew", padx=7, pady=(0, 7))

    expression_label.bind("<Button-1>", lambda event: up(entry, expression_label))
    expression_label.config(cursor="hand2")

    #Buttons
    #1. top buttons

    rad_btn = Button(top_bar, text="Rad", font=("Arial", 14), bg="gray12", fg="white", activebackground="gray7", activeforeground="gray", command=lambda: rad_deg(rad_btn, safe_env, state))
    rad_btn.pack(side="right")
    button_map["r"] = rad_btn
    bind_hover_effect(rad_btn, "gray12", "gray20")

    theme_btn = Button(top_bar, text="🌙", font=("Arial", 14, "bold"), bg="#232323", fg="white", activebackground="#232323", activeforeground="gray", bd=0, highlightthickness=0, relief="flat", command=lambda: toggle_theme(root, themes, ui, rad_btn, theme_btn, buttons, state))
    theme_btn.pack(side="left")
    button_map["t"] = theme_btn

    memory_label = Label(top_bar, text="M: 0", font=("Arial", 12), fg="gray", bg="#232323")
    memory_label.pack(side="left", padx=(8, 0))

    ui["memory_label"] = memory_label


    #2. main buttons

    btns = [
        ['2nd','M+', 'M-', 'MC', 'MR'],
        ['log','ln','sin','cos','tan'],
        ['x²', '√', '^' , '(' , ')' ],
        ['%'  , 'e', 'π' , 'n!','|x|'],
        ['7'  , '8', '9' ,'DEL', 'AC'],
        ['4'  , '5', '6' , '×' , '÷' ],
        ['1'  , '2', '3' , '+' , '-' ],
        ['±'  , '0', '.' ,'EXP', '=' ]
    ]

    color_and_commad = {
    ('2nd'): ("gray12", lambda: toggle_2nd_mode(primary_mode, second_mode, toggle_buttons, second_btn, themes, state)),
    ('M+') : ("gray12", lambda: Mp(entry, memory_label, safe_env, state)),
    ('M-') : ("gray12", lambda: Ms(entry, memory_label, safe_env, state)),
    ('MC') : ("gray12", lambda: Mc(memory_label, state)),
    ('MR') : ("gray12", lambda: Mr(entry, expression_label, state)),
    ('log'): ("gray12", lambda: button_click('log(', entry, expression_label, state)),#logx_y
    ('ln') : ("gray12", lambda: button_click('ln(', entry, expression_label, state)),#e^x
    ('sin'): ("gray12", lambda: button_click('sin(', entry, expression_label, state)),#arcsin
    ('cos'): ("gray12", lambda: button_click('cos(', entry, expression_label, state)),#arccos
    ('tan'): ("gray12", lambda: button_click('tan(', entry, expression_label, state)),#arctan
    ('x²') : ("gray12", lambda: insert_operator('^2', entry, expression_label, state)),#x^3
    ('√')  : ("gray12", lambda: insert_operator('^(1÷2)', entry, expression_label, state)),#3√
    ('^')  : ("gray12", lambda: insert_operator('^', entry, expression_label, state)),#n√
    ('(')  : ("gray12", lambda: button_click('(', entry, expression_label, state)),
    (')')  : ("gray12", lambda: closing(entry, expression_label, state)),
    ('%')  : ("gray12", lambda: percent(entry, expression_label, state)),#MOD
    ('e')  : ("gray12", lambda: button_click('e', entry, expression_label, state)),#sinh
    ('π')  : ("gray12", lambda: button_click('π', entry, expression_label, state)),#cosh
    ('n!') : ("gray12", lambda: insert_factorial(entry, expression_label, safe_env, state)),#10^x
    ('|x|'): ("gray12", lambda: ABS(entry, expression_label, state)),#1/x
    ('7')  : ("gray20", lambda: button_click('7', entry, expression_label, state)),
    ('8')  : ("gray20", lambda: button_click('8', entry, expression_label, state)),
    ('9')  : ("gray20", lambda: button_click('9', entry, expression_label, state)),
    ('DEL'): ("gray30", lambda: delete(entry, expression_label, state)),
    ('AC') : ("gray30", lambda: clear(entry, expression_label)),
    ('4')  : ("gray20", lambda: button_click('4', entry, expression_label, state)),
    ('5')  : ("gray20", lambda: button_click('5', entry, expression_label, state)),
    ('6')  : ("gray20", lambda: button_click('6', entry, expression_label, state)),
    ('×')  : ("gray30", lambda: insert_operator('×', entry, expression_label, state)),
    ('÷')  : ("gray30", lambda: insert_operator('÷', entry, expression_label, state)),
    ('1')  : ("gray20", lambda: button_click('1', entry, expression_label, state)),
    ('2')  : ("gray20", lambda: button_click('2', entry, expression_label, state)),
    ('3')  : ("gray20", lambda: button_click('3', entry, expression_label, state)),
    ('+')  : ("gray30", lambda: insert_operator('+', entry, expression_label, state)),
    ('-')  : ("gray30", lambda: insert_operator('-', entry, expression_label, state)),
    ('±')  : ("gray20", lambda: negative(entry, expression_label, state)),
    ('0')  : ("gray20", lambda: button_click('0', entry, expression_label, state)),
    ('.')  : ("gray20", lambda: dot(entry, expression_label, state)),
    ('EXP'): ("gray30", lambda: insert_operator('EXP', entry, expression_label, state)),
    ('=')  : ("gray30", lambda: calculate(entry, expression_label, safe_env, state, ui, themes)),
    }

    primary_mode = {
        (0, 1): ('M+' , lambda: Mp(entry, memory_label, safe_env, state)),
        (0, 2): ('M-' , lambda: Ms(entry, memory_label, safe_env, state)),
        (0, 3): ('MC' , lambda: Mc(memory_label, state)),
        (0, 4): ('MR' , lambda: Mr(entry, expression_label, state)),
        (1, 0): ('log', lambda: button_click('log(', entry, expression_label, state)),
        (1, 1): ('ln' , lambda: button_click('ln(', entry, expression_label, state)),
        (1, 2): ('sin', lambda: button_click('sin(', entry, expression_label, state)),
        (1, 3): ('cos', lambda: button_click('cos(', entry, expression_label, state)),
        (1, 4): ('tan', lambda: button_click('tan(', entry, expression_label, state)),
        (2, 0): ('x²' , lambda: insert_operator('^2', entry, expression_label, state)),
        (2, 1): ('√'  , lambda: insert_operator('^(1÷2)', entry, expression_label, state)),
        (2, 2): ('^'  , lambda: insert_operator('^', entry, expression_label, state)),
        (2, 3): ('('  , lambda: button_click('(', entry, expression_label, state)),
        (2, 4): (')'  , lambda: closing(entry, expression_label, state)),
        (3, 0): ('%'  , lambda: percent(entry, expression_label, state)),
        (3, 1): ('e'  , lambda: button_click('e', entry, expression_label, state)),
        (3, 2): ('π'  , lambda: button_click('π', entry, expression_label, state)),
        (3, 3): ('n!' , lambda: insert_factorial(entry, expression_label, safe_env, state)),
        (3, 4): ('|x|', lambda: ABS(entry, expression_label, state))
    }
    second_mode = {
        (0, 1): ('rand'    , lambda: button_click('rand', entry, expression_label, state)),
        (0, 2): ('round'   , lambda: Round(entry, expression_label, state)),
        (0, 3): (','       , lambda: insert_operator(',', entry, expression_label, state)),
        (0, 4): ('ANS'     , lambda: ans(entry, expression_label, state)),
        (1, 0): ('log(x,y)', lambda: button_click('logy(', entry, expression_label, state)),
        (1, 1): ('e^x'     , lambda: button_click('e^(', entry, expression_label, state)),#
        (1, 2): ('arcsin'  , lambda: button_click('asin(', entry, expression_label, state)),
        (1, 3): ('arccos'  , lambda: button_click('acos(', entry, expression_label, state)),
        (1, 4): ('arctan'  , lambda: button_click('atan(', entry, expression_label, state)),
        (2, 0): ('x³'      , lambda: insert_operator('^3', entry, expression_label, state)),
        (2, 1): ('³√'      , lambda: insert_operator('^(1÷3)', entry, expression_label, state)),
        (2, 2): ('ⁿ√'      , lambda: insert_operator('^(1÷', entry, expression_label, state)),
        (2, 3): ('⌊x⌋'      , lambda: floor(entry, expression_label, state)),
        (2, 4): ('⌈x⌉'      , lambda: ceil(entry, expression_label, state)),
        (3, 0): ('MOD'     , lambda: insert_operator('MOD', entry, expression_label, state)),
        (3, 1): ('sinh'    , lambda: button_click('sinh(', entry, expression_label, state)),
        (3, 2): ('cosh'    , lambda: button_click('cosh(', entry, expression_label, state)),
        (3, 3): ('tanh'    , lambda: button_click('tanh(', entry, expression_label, state)),
        (3, 4): ('1/x'     , lambda: x_1(entry, expression_label, state))
    }

    for r, row in enumerate(btns):
        for c, text in enumerate(row):
            color , cmd = color_and_commad.get(text)
            button = Button(
                button_frame,
                text=text,
                font=("Arial", 14),
                width=1, height=1,
                bg=color,
                fg="#FF9500" if text == "=" else "white",
                activebackground="gray7",
                activeforeground="#D57C00" if text == "=" else "gray",
                command=cmd
            )
            button_map[text] = button
            buttons[(r, c)] = button
            if (r, c) in primary_mode:
                toggle_buttons[(r, c)] = button
            
            if text == '2nd':
                second_btn = button
                bind_hover_effect_2nd(
                    second_btn, themes["dark"]["2nd_btn"]["bg"],
                    themes["dark"]["2nd_btn"]["2nd_bg"],
                    "gray20",
                    state
                )
            else:
                hover_color = "gray20" if color == "gray12" else "gray12"
                bind_hover_effect(button, color, hover_color)

            button.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
    for i in range(8):
        button_frame.rowconfigure(i, weight=1)

    for i in range(5):
        button_frame.columnconfigure(i, weight=1)

    ui["2nd_btn"] = second_btn
    ui["button_map"] = button_map
    ui["main_frame"] = main_frame
    ui["history_frame"] = history_frame
    ui["canvas"] = canvas
    ui["history_content"] = history_content
    ui["clear_btn"] = clear_btn
    ui["top_frame"] = top_frame 
    ui["top_bar"] = top_bar
    ui["bottom_bar"] = bottom_bar 
    ui["expression_label"] = expression_label
    ui["entry"] = entry
    ui["button_frame"] = button_frame
    ui["style"] = style
    ui["scrollbar"] = scrollbar
    ui["adjust_scrollregion"] = adjust_scrollregion
    
    if theme == "light":
        toggle_theme(root, themes, ui, rad_btn, theme_btn, buttons, state)

    root.after(100, ui["adjust_scrollregion"])

    return ui