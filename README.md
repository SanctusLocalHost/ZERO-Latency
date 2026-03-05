# ZERO:LATENCY - LInux CApsLOck DElay FIx

A CLI (Command Line Interface) tool focused on permanently fixing the CapsLock key delay bug on Linux distributions running Wayland or X11. `"CAps LOck BUg EFfect"`. 

---

### 📸 Screenshots

#### 1. Main Menu
<img width="876" height="660" alt="Main Menu" src="https://github.com/user-attachments/assets/d0d8131e-aed1-46b6-8a27-32b150a6319b" />

---

#### 2. Fixing the Bug
<img width="876" height="660" alt="Fixing" src="https://github.com/user-attachments/assets/1e3a7c8d-7802-498d-a07a-de78629a8def" />

---

#### 3. Success
<img width="876" height="660" alt="Success" src="https://github.com/user-attachments/assets/b25b8560-5d9c-441e-924f-9c0242f597e9" />


---

### ⚙️ How It Works

1. **Safe Verification:** Reads the protected system file `/usr/share/X11/xkb/symbols/capslock`.
2. **Automatic Backup:** Saves the original configuration before making any modifications.
3. **Patch Injection:** Uses regular expressions (Regex) to locate the `ctrl_modifier` block and injects the correct routine (`type="ALPHABETIC"`, `repeat=No`, etc.) that eliminates the latency.

---

### 🛠️ How To Use

**1. Download and run (Double Click):**
- Download the `ZeroLatency.py` file from this repository.
- Right-click the file > **Properties** > **Permissions** tab > Check the option **"Allow executing file as program"**.
- **Double-click** the file (if the system asks, choose *"Run in Terminal"*).

> *(Alternatively, via terminal, just open the folder where you downloaded it and run: `python3 ZeroLatency.py`)*

**2. After applying the script's fix:**
To ensure the Operating System perfectly adopts the Patch:
- Open your system utility tool (e.g., **Gnome Tweaks**).
- Go to **Keyboard & Mouse** > **Additional Layout Options** > **Caps Lock behavior**.
- Enable the option: **"Make Caps Lock an additional Ctrl"**.
