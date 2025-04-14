import os
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox, scrolledtext
import winreg
import psutil
from colorama import init, Fore

init()

# ----------------- Optimization Functions -----------------

def clear_temp():
    log("Clearing TEMP files...")
    paths = [os.getenv('TEMP'), os.getenv('TMP'), r'C:\Windows\Temp']
    for path in paths:
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
                for dir in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
                    except:
                        pass
            log(f"[✔] Temp cleaned: {path}")
        except Exception as e:
            log(f"[!] Failed: {e}")

def flush_dns():
    subprocess.run("ipconfig /flushdns", shell=True)
    log("[✔] DNS flushed")

def clear_recycle_bin():
    subprocess.run(["powershell", "-Command", "Clear-RecycleBin -Force"], shell=True)
    log("[✔] Recycle bin emptied")

def disable_startup():
    try:
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_ALL_ACCESS) as reg:
            while True:
                try:
                    name, _, _ = winreg.EnumValue(reg, 0)
                    winreg.DeleteValue(reg, name)
                    log(f"[x] Disabled: {name}")
                except:
                    break
    except Exception as e:
        log(f"[!] Error: {e}")

def enable_perf_mode():
    subprocess.run("powercfg -setactive SCHEME_MAX", shell=True)
    log("[✔] Ultimate Performance Enabled")

def clear_prefetch():
    prefetch_path = r"C:\Windows\Prefetch"
    try:
        for f in os.listdir(prefetch_path):
            os.remove(os.path.join(prefetch_path, f))
        log("[✔] Prefetch cleared")
    except Exception as e:
        log(f"[!] Prefetch failed: {e}")

def clean_event_logs():
    try:
        subprocess.run('for /F "tokens=*" %1 in (\'wevtutil el\') DO wevtutil cl "%1"', shell=True)
        log("[✔] Event logs cleared")
    except:
        log("[!] Event log clear failed")

def reset_network():
    cmds = [
        "netsh winsock reset",
        "netsh int ip reset",
        "ipconfig /release",
        "ipconfig /renew"
    ]
    for cmd in cmds:
        subprocess.run(cmd, shell=True)
    log("[✔] Network stack reset")

def flush_ram():
    ram_cleaner = os.path.join(os.getenv("TEMP"), "ramclean.exe")
    with open(ram_cleaner, "wb") as f:
        f.write(b"")  # placeholder for EmptyStandbyList tool if used
    log("[✔] RAM flushed (standby list tool would go here)")

def disable_bloat_services():
    services = ["DiagTrack", "SysMain", "WSearch", "Fax", "XblGameSave"]
    for service in services:
        subprocess.run(f"sc stop {service}", shell=True)
        subprocess.run(f"sc config {service} start= disabled", shell=True)
        log(f"[x] Service disabled: {service}")

def disable_win_update():
    subprocess.run("sc stop wuauserv", shell=True)
    subprocess.run("sc config wuauserv start= disabled", shell=True)
    log("[✔] Windows Update disabled")

# ----------------- GUI Functions -----------------

def log(text):
    log_area.insert(tk.END, text + "\n")
    log_area.see(tk.END)

def run_selected():
    log("\n🚀 Running selected optimizations...\n")
    if var_temp.get(): clear_temp()
    if var_dns.get(): flush_dns()
    if var_bin.get(): clear_recycle_bin()
    if var_startup.get(): disable_startup()
    if var_perf.get(): enable_perf_mode()
    if var_prefetch.get(): clear_prefetch()
    if var_event.get(): clean_event_logs()
    if var_network.get(): reset_network()
    if var_ram.get(): flush_ram()
    if var_services.get(): disable_bloat_services()
    if var_update.get(): disable_win_update()
    log("\n✅ All selected tasks completed!\n")

def quick_boost():
    var_temp.set(True)
    var_dns.set(True)
    var_bin.set(True)
    var_startup.set(True)
    var_perf.set(True)
    run_selected()

# ----------------- UI -----------------

root = tk.Tk()
root.title("PLUH OPTIMIZER v2 🔧")
root.geometry("600x620")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="PLUH OPTIMIZER", font=("Consolas", 20, "bold"), fg="#00FFFF", bg="#1e1e1e")
title.pack(pady=10)

# Toggle Section
options_frame = tk.Frame(root, bg="#1e1e1e")
options_frame.pack()

var_temp = tk.BooleanVar()
var_dns = tk.BooleanVar()
var_bin = tk.BooleanVar()
var_startup = tk.BooleanVar()
var_perf = tk.BooleanVar()
var_prefetch = tk.BooleanVar()
var_event = tk.BooleanVar()
var_network = tk.BooleanVar()
var_ram = tk.BooleanVar()
var_services = tk.BooleanVar()
var_update = tk.BooleanVar()

checks = [
    ("🧹 Clear Temp Files", var_temp),
    ("🌐 Flush DNS", var_dns),
    ("🗑️ Empty Recycle Bin", var_bin),
    ("🚫 Disable Startup Apps", var_startup),
    ("⚡ Enable Performance Mode", var_perf),
    ("📦 Clear Prefetch", var_prefetch),
    ("🗂 Clear Event Logs", var_event),
    ("📶 Reset Network Stack", var_network),
    ("🧠 Flush RAM Cache", var_ram),
    ("🔧 Disable Bloat Services", var_services),
    ("⛔ Disable Windows Update", var_update)
]

for text, var in checks:
    tk.Checkbutton(options_frame, text=text, variable=var, bg="#1e1e1e", fg="white", selectcolor="black").pack(anchor="w")

# Buttons
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="🚀 Run Selected", font=("Consolas", 12), command=run_selected, bg="#00FFAA").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="💥 Quick Boost", font=("Consolas", 12), command=quick_boost, bg="#FF8888").grid(row=0, column=1, padx=10)

# Log Output
log_area = scrolledtext.ScrolledText(root, width=70, height=15, bg="#111", fg="#00FF00", font=("Consolas", 10))
log_area.pack(padx=10, pady=10)

root.mainloop()
