import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import pyttsx3
import time
import platform

# ==========================================
#        CALIBRATION (UPDATE THESE)
# ==========================================
THUMB_TRIG  = 200  
INDEX_TRIG  = 220  
MIDDLE_TRIG = 220  

class ProfessionalGloveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture to Speech System")
        self.root.geometry("900x650")
        
        # --- Mac UI Polish ---
        self.bg_color = "#F5F5F7"  # Apple-style light gray
        self.header_color = "#007AFF" # Apple System Blue
        self.root.configure(bg=self.bg_color)
        
        # Configure Styles for Mac (Aqua)
        self.style = ttk.Style()
        try:
            self.style.theme_use('aqua')  # Force Mac Native Theme
        except:
            pass # Fallback if not on Mac
            
        self.style.configure("TCombobox", padding=5)
        
        # --- System Variables ---
        self.serial_port = tk.StringVar() 
        self.is_connected = False
        self.arduino = None
        self.last_gesture = "None"
        self.current_data = [0]*8
        self.scan_thread = None
        
        # --- UI Build ---
        self.create_header()
        self.create_controls()
        self.create_dashboard()
        self.create_footer()
        
        # Auto-start logic
        self.root.after(500, self.auto_connect_sequence)
        self.root.after(50, self.update_ui_loop)

    def create_header(self):
        # Mac Header: Clean, System Blue
        header = tk.Frame(self.root, bg=self.header_color, height=80)
        header.pack(fill=tk.X)
        
        # Use Helvetica Neue for Mac
        tk.Label(header, text="GESTURE SPEECH INTERFACE", fg="white", bg=self.header_color, 
                 font=("Helvetica Neue", 22, "bold")).pack(pady=20)

    def create_controls(self):
        ctrl_frame = tk.Frame(self.root, bg="#E5E5EA", pady=15, padx=10) # Darker gray strip
        ctrl_frame.pack(fill=tk.X)
        
        tk.Label(ctrl_frame, text="Port:", bg="#E5E5EA", fg="#333", font=("Helvetica Neue", 13)).pack(side=tk.LEFT, padx=(20, 5))
        
        # Native Dropdown
        self.port_dropdown = ttk.Combobox(ctrl_frame, textvariable=self.serial_port, width=30, state="readonly")
        self.port_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Refresh Button (Native Look)
        self.btn_refresh = ttk.Button(ctrl_frame, text="⟳ Scan", command=self.auto_connect_sequence, width=8)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        # Connect Button 
        # Note: On Mac, ttk.Button doesn't support background colors easily. 
        # We use tk.Button with 'highlightbackground' to fix the ugly border issue on Mac.
        self.btn_connect = tk.Button(ctrl_frame, text="Connect", command=self.toggle_connection, 
                                     bg="#34C759", fg="white", font=("Helvetica Neue", 13, "bold"), 
                                     highlightbackground="#E5E5EA", width=12, bd=0)
        self.btn_connect.pack(side=tk.LEFT, padx=20)
        
        self.lbl_status = tk.Label(ctrl_frame, text="Status: Scanning...", fg="#007AFF", bg="#E5E5EA", font=("Helvetica Neue", 13))
        self.lbl_status.pack(side=tk.LEFT, padx=20)

    def auto_connect_sequence(self):
        """Scans for Arduino and connects automatically."""
        self.lbl_status.config(text="Scanning...", fg="#007AFF")
        self.root.update()
        
        ports = serial.tools.list_ports.comports()
        candidates = []
        
        # FILTER LOGIC FOR MAC
        # Mac ports often contain "cu.usbmodem", "tty.usbserial", "cu.wchusb" (for clones)
        whitelist = ["Arduino", "Nano", "usbmodem", "usbserial", "wchusb", "serial"]
        
        for port in ports:
            desc = port.description
            device = port.device
            # Check if keyword matches description OR device path
            if any(keyword in desc for keyword in whitelist) or any(keyword in device for keyword in whitelist):
                candidates.append(f"{port.device}")
        
        if candidates:
            self.port_dropdown['values'] = candidates
            self.port_dropdown.current(0) 
            self.lbl_status.config(text="Device Found", fg="#34C759") # Apple Green
            
            if not self.is_connected:
                self.toggle_connection()
        else:
            self.port_dropdown['values'] = []
            self.serial_port.set("")
            self.lbl_status.config(text="No Device", fg="#FF3B30") # Apple Red
            
            if self.is_connected:
                self.toggle_connection()

    def create_dashboard(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Finger Data
        # Using ttk.LabelFrame for native Mac outline look
        finger_frame = ttk.LabelFrame(main_frame, text=" Flex Sensors ", padding=20)
        finger_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

        self.finger_bars = []
        self.finger_labels = []
        names = ["Thumb", "Index", "Middle"]
        
        for i, name in enumerate(names):
            f_container = tk.Frame(finger_frame, bg=self.bg_color)
            f_container.pack(fill=tk.X, pady=12)
            
            tk.Label(f_container, text=name, width=8, anchor="w", bg=self.bg_color, 
                     font=("Helvetica Neue", 12, "bold"), fg="#555").pack(side=tk.LEFT)
            
            # Canvas for bar graph
            canvas = tk.Canvas(f_container, width=180, height=15, bg="#E5E5EA", highlightthickness=0)
            canvas.pack(side=tk.LEFT, padx=10)
            # Rounded cap effect not easy in pure TK, sticking to rect
            rect = canvas.create_rectangle(0, 0, 0, 20, fill="#007AFF")
            self.finger_bars.append((canvas, rect))
            
            lbl = tk.Label(f_container, text="0", width=5, bg="white", fg="#333", 
                           font=("Menlo", 12), highlightthickness=1, highlightbackground="#ccc")
            lbl.pack(side=tk.LEFT)
            self.finger_labels.append(lbl)

        # 2. Orientation Data
        ori_frame = ttk.LabelFrame(main_frame, text=" IMU Data ", padding=20)
        ori_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

        # Using Menlo font for fixed-width numbers on Mac
        self.lbl_ori_x = tk.Label(ori_frame, text="X (Compass): 0", bg=self.bg_color, font=("Menlo", 14), pady=5)
        self.lbl_ori_x.pack(anchor="w")
        self.lbl_ori_y = tk.Label(ori_frame, text="Y (Roll):    0", bg=self.bg_color, font=("Menlo", 14), pady=5)
        self.lbl_ori_y.pack(anchor="w")
        self.lbl_ori_z = tk.Label(ori_frame, text="Z (Pitch):   0", bg=self.bg_color, font=("Menlo", 14), pady=5)
        self.lbl_ori_z.pack(anchor="w")

    def create_footer(self):
        # Dark Footer for Contrast
        footer = tk.Frame(self.root, bg="#1C1C1E", height=120)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="DETECTED OUTPUT", fg="#8E8E93", bg="#1C1C1E", font=("Helvetica Neue", 10, "bold")).pack(pady=(15, 5))
        
        self.lbl_gesture = tk.Label(footer, text="WAITING...", fg="#32D74B", bg="#1C1C1E", font=("Helvetica Neue", 40, "bold"))
        self.lbl_gesture.pack(pady=5)

    def toggle_connection(self):
        if not self.is_connected:
            try:
                selection = self.serial_port.get()
                if not selection:
                    return
                # On Mac/Linux, we usually take the whole path, not split by " - "
                port = selection.split(" - ")[0]
                
                self.arduino = serial.Serial(port, 9600, timeout=1)
                time.sleep(2) 
                self.is_connected = True
                
                # Update Button Style for Active State
                self.btn_connect.config(text="Disconnect", bg="#FF3B30") # Apple Red
                self.lbl_status.config(text="System Online", fg="#34C759")
                self.lbl_gesture.config(text="READY")
                self.port_dropdown.config(state="disabled")
                self.btn_refresh.config(state="disabled")
                
                self.thread = threading.Thread(target=self.serial_read_loop)
                self.thread.daemon = True
                self.thread.start()
            except Exception as e:
                print(e)
                self.lbl_status.config(text="Connection Failed", fg="#FF3B30")
        else:
            self.is_connected = False
            if self.arduino: 
                try:
                    self.arduino.close()
                except:
                    pass
            self.btn_connect.config(text="Connect", bg="#34C759") # Apple Green
            self.lbl_status.config(text="Disconnected", fg="#FF3B30")
            self.lbl_gesture.config(text="OFFLINE", fg="#8E8E93")
            self.port_dropdown.config(state="readonly")
            self.btn_refresh.config(state="normal")

    def serial_read_loop(self):
        while self.is_connected:
            try:
                if self.arduino.in_waiting > 0:
                    line = self.arduino.readline().decode('utf-8', errors='ignore').strip()
                    values = line.split(',')
                    if len(values) == 8:
                        data = [int(x) for x in values[:5]] + [float(x) for x in values[5:]]
                        self.process_logic(data)
            except Exception:
                pass

    def process_logic(self, data):
        self.current_data = data
        t, i, m = data[0], data[1], data[2]
        ox, oy, oz = data[5], data[6], data[7]
        
        t_open = t > THUMB_TRIG
        i_open = i > INDEX_TRIG
        m_open = m > MIDDLE_TRIG
        
        detected = "None"

        # --- LOGIC ---
        if oz > 50 and i_open and m_open: 
            detected = "Stop"
        elif abs(oy) > 40: 
            if not t_open and not i_open and not m_open: detected = "I need Help"
        elif detected == "None" and abs(oy) <= 40:
            if t_open and not i_open and not m_open:     detected = "Good Job"
            elif not t_open and i_open and not m_open:   detected = "Look at that"
            elif not t_open and i_open and m_open and abs(oy) > 40: detected = "Victory"
            elif not t_open and not i_open and m_open:   detected = "Perfect"
            elif t_open and i_open and m_open:           detected = "None"

        if detected != "None" and detected != self.last_gesture:
            self.last_gesture = detected
            self.lbl_gesture.config(text=detected.upper())
            self.speak(detected)
        elif detected == "None":
            self.last_gesture = "None"
            self.lbl_gesture.config(text="READY")

    def update_ui_loop(self):
        if self.is_connected:
            d = self.current_data
            thresholds = [THUMB_TRIG, INDEX_TRIG, MIDDLE_TRIG]
            for idx in range(3):
                val = d[idx]
                self.finger_labels[idx].config(text=str(val))
                
                # Scaled width logic
                w = max(0, min(180, (val - 100))) 
                canvas, rect = self.finger_bars[idx]
                canvas.coords(rect, 0, 0, w, 20)
                
                # Apple Colors: Green for Active, Blue for Inactive
                col = "#34C759" if val > thresholds[idx] else "#007AFF"
                canvas.itemconfig(rect, fill=col)

            self.lbl_ori_x.config(text=f"X (Compass): {d[5]:.0f}")
            self.lbl_ori_y.config(text=f"Y (Roll):    {d[6]:.0f}")
            self.lbl_ori_z.config(text=f"Z (Pitch):   {d[7]:.0f}")

        self.root.after(50, self.update_ui_loop)

    def speak(self, text):
        threading.Thread(target=self._speak_worker, args=(text,), daemon=True).start()

    def _speak_worker(self, text):
        try:
            # Re-initializing engine per thread is safer on some Mac setups to avoid loop blocks
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalGloveApp(root)
    root.mainloop()