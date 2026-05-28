import cpuinfo
import psutil
import wmi
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

getCPU = cpuinfo.get_cpu_info()
 
cpuName = getCPU["brand_raw"]
cpuPercentFirst = psutil.cpu_percent()
speed = psutil.cpu_freq().current / 1000

L1Cache = getCPU.get("l1_data_cache_size", "Unknown")
L2Cache = getCPU.get("l2_cache_size", "Unknown")
L3Cache = getCPU.get("l3_cache_size", "Unknown")
 
# Converting cache to MB
if (L1Cache != "Unknown"):
    L1Cache = L1Cache / 1048576
if (L2Cache != "Unknown"):
    L2Cache = L2Cache / 1048576
if (L3Cache != "Unknown"):
    L3Cache = L3Cache / 1048576
 
# Main window settings
root = tk.Tk()
root.title("Performance Monitor")
root.geometry("1920x1080")
root.configure(bg="#0d0f14")
 
# Loading images
logo_icon = ImageTk.PhotoImage(
    Image.open("icons/logo.png").resize((30, 30))
)

percent_icon = ImageTk.PhotoImage(
    Image.open("icons/percent.png").resize((100, 100))
)

speed_icon = ImageTk.PhotoImage(
    Image.open("icons/speed.png").resize((100, 100))
)

# Sidebar
sidebar = tk.Frame(root, bg = "#0f1117", width=220)
sidebar.pack(side="left", fill="y")

# Logo section
logoSection = tk.Frame(sidebar, bg="#0f1117")
logoSection.pack(fill="x", pady=20)

logo = tk.Label(logoSection, image=logo_icon, bg = "#0f1117")
logo.pack(side="left", padx=10)
logo.image = logo_icon

title = tk.Label(
    logoSection,
    text="Performance Monitor",
    font=("Segoe UI", 14, "bold"),
    bg="#0f1117",
    fg="white"
)

title.pack(side="left")

# Main frame
main = tk.Frame(root, bg="#0d0f14")
main.pack(side="left", fill="both", expand=True)

# CPU name section
cpuNameSection = tk.Frame(main, bg = "#0d0f14")
cpuNameSection.pack(fill="x", pady=30)

cpuTitle = tk.Label(
    cpuNameSection,
    text="CPU",
    font=("Segoe UI", 28, "bold"),
    bg="#0d0f14",
    fg="white"
)

cpuNameText = tk.Label(
    cpuNameSection,
    text=cpuName,
    font=("Segoe UI", 28, "bold"),
    bg="#0d0f14",
    fg="white"
)

cpuTitle.pack(side="left", padx=30)
cpuNameText.pack(side="right", padx=30)

# Graph section
cpuGraphSection = tk.Frame(main, bg = "#0d0f14", height=400)
cpuGraphSection.pack(fill="x", padx=30, pady=30)

# CPU load graph
cpu_data = [0] * 60

cpuFig = Figure(figsize=(10,4), dpi=100)

ax = cpuFig.add_subplot(111)
cpuFig.patch.set_facecolor("#141720")
cpuFig.patch.set_edgecolor("#4b86e8")
#cpuFig.patch.set_linewidth(5)

ax.set_ylim(0,100)
ax.set_xlim(0,59)
ax.set_facecolor("#141720")
ax.spines["bottom"].set_color("#4b86e8")
ax.spines["left"].set_color("#4b86e8")
ax.spines["top"].set_color("#4b86e8")
ax.spines["right"].set_color("#4b86e8")
ax.tick_params(colors="#4b86e8")
ax.set_title("CPU Usage", color="#4b86e8")


line, = ax.plot(cpu_data, color="#4b86e8", linewidth=3)

cpuGraph = FigureCanvasTkAgg(cpuFig, master=cpuGraphSection)
cpuGraph.get_tk_widget().pack(side="left")

cpuInfo = tk.Frame(cpuGraphSection, bg = "#141720", height=400, width=400)
cpuInfo.pack(side="right", fill="x", pady=30)
cpuInfo.pack_propagate(False)

cpuUtilization = tk.Frame(cpuInfo, bg="#141720", height=200, width=400)
cpuUtilization.pack(side="top", fill="x")
cpuUtilization.pack_propagate(False)

percentImage = tk.Label(cpuUtilization, image=percent_icon, bg = "#141720")
percentImage.pack(side="left", padx=(30,0))
percentImage.image = percent_icon

percentText = tk.Label(
    cpuUtilization,
    text=cpuPercentFirst,
    font=("Segoe UI", 60, "bold"),
    bg="#141720",
    fg="#4b86e8"
)

percentText.pack(side="right", padx=30)


cpuSpeedFrame = tk.Frame(cpuInfo, bg="#141720", height=200, width=400)
cpuSpeedFrame.pack(side="bottom", fill="x")
cpuSpeedFrame.pack_propagate(False)

speedImage = tk.Label(cpuSpeedFrame, image=speed_icon, bg = "#141720")
speedImage.pack(side="left", padx=(30, 0))
speedImage.image = speed_icon

speedText = tk.Label(
    cpuSpeedFrame,
    text= f"{speed:.2f} GHz",
    font=("Segoe UI", 40, "bold"),
    bg="#141720",
    fg="#4b86e8"
)

speedText.pack(side="right", padx=(0, 30))

def update():

    cpuPercent = psutil.cpu_percent()

    cpu_data.pop(0)
    cpu_data.append(cpuPercent)

    line.set_ydata(cpu_data)
    line.set_xdata(range(len(cpu_data)))

    cpuGraph.draw()

    percentText.config(text=cpuPercent)

    root.after(1000, update)

update()

root.mainloop()