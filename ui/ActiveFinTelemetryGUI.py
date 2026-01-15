import tkinter as tk
from tkinter import ttk
import serial
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

# --- SYSTEM CONFIG ---
COM_PORT = 'COM14'
BAUD_RATE = 115200


class AeroProDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("GROUND SEGMENT - TVC MISSION CONTROL")
        self.root.state('zoomed')
        self.root.configure(bg='#020202')

        # Data variables
        self.pitch, self.roll = 0.0, 0.0
        self.is_connected = False

        # Professional Color Palette
        self.bg_dark = "#020202"
        self.bg_panel = "#0A0A0F"
        self.border_color = "#1E1E26"
        self.accent = "#00F2FF"  # Cyan
        self.pitch_color = "#FF2E63"  # Soft Red/Pink
        self.roll_color = "#08FFC8"  # Seafoam Green
        self.volt_color = "#EAD350"  # Aviation Yellow

        # --- TOP NAVIGATION BAR ---
        self.header = tk.Frame(root, bg=self.bg_panel, height=40, bd=0, highlightbackground=self.border_color,
                               highlightthickness=1)
        self.header.pack(fill=tk.X, side=tk.TOP)

        tk.Label(self.header, text="◆ FLIGHT TELEMETRY SYSTEM v8.1", fg=self.accent, bg=self.bg_panel,
                 font=("Consolas", 12, "bold")).pack(side=tk.LEFT, padx=20)

        self.lbl_status = tk.Label(self.header, text="LINK: OFFLINE", fg="#444444", bg=self.bg_panel,
                                   font=("Consolas", 10, "bold"))
        self.lbl_status.pack(side=tk.RIGHT, padx=20)

        # --- MAIN VIEWPORT ---
        self.main_container = tk.Frame(root, bg=self.bg_dark)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # LEFT SIDEBAR: LARGE NUMERICS
        self.sidebar = tk.Frame(self.main_container, bg=self.bg_dark, width=320)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.create_pro_numerical_panel(self.sidebar, "ATTITUDE: PITCH", "lbl_pitch_val", self.pitch_color)
        self.create_pro_numerical_panel(self.sidebar, "ATTITUDE: ROLL", "lbl_roll_val", self.roll_color)

        # SYSTEM LOG BOX (Professional addition)
        log_frame = tk.Frame(self.sidebar, bg=self.bg_panel, bd=1, highlightbackground=self.border_color,
                             highlightthickness=1)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        tk.Label(log_frame, text="COMMUNICATION LOG", fg="#666666", bg=self.bg_panel, font=("Arial", 8, "bold")).pack(
            pady=5)
        self.log_text = tk.Text(log_frame, bg=self.bg_dark, fg="#00FF00", font=("Consolas", 8), bd=0, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # CENTER/RIGHT: GAUGES
        self.content_area = tk.Frame(self.main_container, bg=self.bg_dark)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = plt.figure(figsize=(10, 8), facecolor=self.bg_dark)
        self.fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
        self.ax_p_gauge = self.fig.add_subplot(121)
        self.ax_r_gauge = self.fig.add_subplot(122)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.content_area)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # BOTTOM: POWER DIAGNOSTICS
        self.bottom_bar = tk.Frame(root, bg=self.bg_panel, height=180, highlightbackground=self.border_color,
                                   highlightthickness=1)
        self.bottom_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        self.p_slots = []
        p_labels = ["BUS VOLTAGE: PWM", "LOAD CURRENT: PWM", "BUS VOLTAGE: MPU", "LOAD CURRENT: MPU"]
        for i in range(4):
            slot = self.create_power_meter(self.bottom_bar, p_labels[i])
            self.p_slots.append(slot)

        threading.Thread(target=self.bt_receive_loop, daemon=True).start()
        self.update_ui()

    def create_pro_numerical_panel(self, parent, title, attr, color):
        frame = tk.Frame(parent, bg=self.bg_panel, highlightbackground=self.border_color, highlightthickness=1)
        frame.pack(fill=tk.X, pady=5)
        tk.Label(frame, text=title, fg="#888888", bg=self.bg_panel, font=("Consolas", 10, "bold")).pack(anchor="w",
                                                                                                        padx=10, pady=5)
        lbl = tk.Label(frame, text="+00.00°", fg=color, bg=self.bg_panel, font=("Consolas", 42, "bold"))
        lbl.pack(pady=10)
        setattr(self, attr, lbl)

    def create_power_meter(self, parent, title):
        frame = tk.Frame(parent, bg=self.bg_panel)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        tk.Label(frame, text=title, fg="#888888", bg=self.bg_panel, font=("Consolas", 9)).pack(pady=5)

        val_lbl = tk.Label(frame, text="0.00", fg=self.volt_color, bg=self.bg_panel, font=("Consolas", 22, "bold"))
        val_lbl.pack()

        # Minimalist Progress Bar
        s = ttk.Style()
        s.theme_use('default')
        s.configure("TProgressbar", thickness=4, troughcolor="#111", background=self.volt_color, borderwidth=0)
        pb = ttk.Progressbar(frame, length=150, mode='determinate', style="TProgressbar")
        pb.pack(pady=10)
        pb['value'] = 40  # Dummy fill
        return val_lbl

    def draw_gauge(self, ax, val, label, color):
        ax.clear()
        ax.set_facecolor(self.bg_dark)

        # Draw HUD style circle
        angles = np.linspace(-np.pi, np.pi, 100)
        ax.plot(np.cos(angles), np.sin(angles), color=self.border_color, lw=1)

        # Tick marks every 15 degrees
        for deg in range(-180, 180, 15):
            rad = np.radians(deg + 90)
            lw = 2 if deg % 45 == 0 else 1
            alpha = 0.8 if deg % 45 == 0 else 0.3
            ax.plot([np.cos(rad) * 0.9, np.cos(rad)], [np.sin(rad) * 0.9, np.sin(rad)], color='white', lw=lw,
                    alpha=alpha)

        # Indicator Needle
        n_rad = np.radians(val + 90)
        ax.plot([0, np.cos(n_rad)], [0, np.sin(n_rad)], color=color, lw=4, alpha=0.9)
        ax.scatter(0, 0, color='white', s=20)

        ax.set_title(label, color='white', fontname="Consolas", fontsize=11, weight='bold')
        ax.set_xlim(-1.2, 1.2);
        ax.set_ylim(-1.2, 1.2);
        ax.axis('off')

    def bt_receive_loop(self):
        while True:
            try:
                # Open port with a specific timeout to prevent hanging
                with serial.Serial(COM_PORT, BAUD_RATE, timeout=0.05) as ser:
                    self.is_connected = True
                    # CRITICAL: Clear any old junk data sitting in the Bluetooth buffer
                    ser.reset_input_buffer()

                    while True:
                        if ser.in_waiting > 0:
                            # Read ALL waiting data but only keep the very last line
                            raw_data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                            lines = raw_data.strip().split('\n')

                            if lines:
                                last_line = lines[-1].strip()
                                if ',' in last_line:
                                    try:
                                        parts = last_line.split(',')
                                        self.pitch = float(parts[0])
                                        self.roll = float(parts[1])
                                    except (ValueError, IndexError):
                                        continue  # Skip broken lines

                        # Slow down the loop slightly to let the CPU breathe
                        time.sleep(0.01)
            except Exception as e:
                self.is_connected = False
                print(f"Connection Lost: {e}")
                time.sleep(2.0)  # Wait before auto-reconnecting

    def update_ui(self):
        # Update connection text with color
        status_text = "● LINK: STABLE" if self.is_connected else "○ LINK: SEARCHING"
        status_color = self.roll_color if self.is_connected else "#FF0000"
        self.lbl_status.config(text=status_text, fg=status_color)

        self.lbl_pitch_val.config(text=f"{self.pitch:+.2f}°")
        self.lbl_roll_val.config(text=f"{self.roll:+.2f}°")

        self.draw_gauge(self.ax_p_gauge, self.pitch, "PITCH OFFSET", self.pitch_color)
        self.draw_gauge(self.ax_r_gauge, self.roll, "ROLL OFFSET", self.roll_color)

        # Update simulated power data
        self.p_slots[0].config(text="5.04 V")
        self.p_slots[1].config(text=f"{abs(self.pitch * 2.5):.1f} mA")
        self.p_slots[2].config(text="3.31 V")
        self.p_slots[3].config(text="14.2 mA")

        self.canvas.draw()
        self.root.after(40, self.update_ui)


if __name__ == "__main__":
    root = tk.Tk()
    app = AeroProDashboard(root)
    root.mainloop()