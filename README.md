HK Scientific Calculator
A professional, modular scientific calculator built in Python and Tkinter — packaged as a standalone executable with custom theming and extensive functionality.

🎯 Table of Contents
Features

Screenshots

Installation & Usage

Keyboard Shortcuts

Advanced Usage

Building from Source

Troubleshooting

Project Structure

Contributing

License

⭐ Features
🧮 Scientific & Mathematical: sin, cos, tan, log, ln, √, xⁿ, π, e, !, and more

🔄 Dual Function Modes: Switch primary/secondary functions with the 2nd button

💾 Memory Operations: M+, M-, MR, MC, with on-screen indicator

📜 History Panel: View and reuse past calculations

🧠 Smart Input: Auto-parentheses and syntax validation

🎨 Themes: Light/Dark mode toggle (q)

🖥️ Responsive UI: Dynamic layout & font resizing

⌨️ Keyboard First: Full hotkey support for operators, functions, theme, and history

📐 Rad/Deg Toggle: Angle unit switching (R)

📦 Standalone Executable: No Python install required

🖼️ Screenshots
Dark Mode Default	Dark Mode + History	Light Mode + History

💾 Installation & Usage
🪟 Windows (Executable)
Download HK_Calculator.exe from Releases

Double-click to run — no installation required

🐍 Run from Source
bash
Copy code
git clone https://github.com/yourusername/HK_Calculator.git
cd HK_Calculator
pip install -r requirements.txt  # If applicable
python src/main.py
⌨️ Keyboard Shortcuts
Key	Action
0–9, .	Input digits/decimal
+ - * /	Basic operations
Enter / =	Compute result
Backspace	Delete character
Esc	Clear all (AC)
2nd	Toggle 2ⁿᵈ functions
r	Radians / Degrees
q	Toggle theme
h	Toggle history panel

Function Shortcuts:

Key	Primary	2ⁿᵈ Function
s	sin(	sinh(
c	cos(	cosh(
t	tan(	tanh(
g	log(	logy(
l	ln(	(
x	x²	x³
!	factorial	1/x

🚀 Advanced Usage
🖱️ Click History to Reuse

📋 Right-Click Result to Copy

🎨 Customize Themes in yi_config.py

💡 Enable Persistent History by modifying logic.py

🛠️ Building from Source
bash
Copy code
pyinstaller --noconfirm --onefile --windowed ^
  --name=HK_Calculator ^
  --icon=docs/HK.ico ^
  --add-data "docs/HK_png.png;docs" ^
  src/main.py
🗃️ Output: dist/HK_Calculator.exe

🧹 Cleanup: Delete build/, dist/, *.spec if desired

⚠️ Troubleshooting
Issue	Solution
iconphoto() error	Ensure it's called right after Tk() creation
Missing images	Use resource_path() for packaging compatibility
Missing modules	Reinstall dependencies: pip install -r requirements.txt (if any)
Broken EXE	Confirm all paths are relative; rebuild with correct --add-data paths

📁 Project Structure
css
Copy code
HK_Calculator/
├── docs/
│   ├── HK.ico
│   ├── HK_png.png
│   └── screenshots/
├── src/
│   ├── main.py
│   ├── logic.py
│   ├── utils.py
│   └── yi_config.py
├── HK_Calculator.exe
└── README.md

👤 Author
Ali Heidari Khezri
Electrical Engineering student @ K.N. Toosi University of Technology
💡 Passionate about programming, automation, and creating useful tools

🤝 Contributing
Pull requests welcome!

Fork this repo

Create a new feature branch

Commit your changes

Open a pull request

📝 License
This project is licensed under the MIT License.
See LICENSE file for details.