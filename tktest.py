import tkinter as tk
import cpuinfo
import psutil
from PIL import Image, ImageTk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

getCPU = cpuinfo.get_cpu_info()

cpuName = getCPU["brand_raw"]

l1_data = getCPU.get("l1_data_cache_size", "Unknown")
l2_cache = getCPU.get("l2_cache_size", "Unknown")
l3_cache = getCPU.get("l3_cache_size", "Unknown")

root = tk.Tk()
root.title("Performance Monitor")
root.geometry("1200x800")
root.configure(bg="#f4f2f3")

color1 = "#1e90ff"
color2 = "#8ffaeb"

sidebar = tk.Canvas(
    root,
    width=250,
    highlightthickness=0,
    bg="#f4f2f3"
)

sidebar.pack(side="left", fill="y")


def draw_gradient(canvas, color1, color2, width, height, radius=40):

    r1, g1, b1 = root.winfo_rgb(color1)
    r2, g2, b2 = root.winfo_rgb(color2)

    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):

        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))

        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"

        if i < radius:
            offset = radius - int((radius**2 - (radius - i)**2) ** 0.5)

        elif i > height - radius:
            dy = i - (height - radius)
            offset = radius - int((radius**2 - dy**2) ** 0.5)

        else:
            offset = 0

        canvas.create_line(
            offset,
            i,
            width - offset,
            i,
            fill=color
        )


draw_gradient(sidebar, color1, color2, 250, 800, radius=40)

process_icon = ImageTk.PhotoImage(
    Image.open("icons/processes.png").resize((30, 30))
)

cpu_icon = ImageTk.PhotoImage(
    Image.open("icons/CPU.png").resize((30, 30))
)

gpu_icon = ImageTk.PhotoImage(
    Image.open("icons/GPU.png").resize((30, 30))
)

memory_icon = ImageTk.PhotoImage(
    Image.open("icons/memory.png").resize((30, 30))
)

disk_icon = ImageTk.PhotoImage(
    Image.open("icons/disk.png").resize((30, 30))
)

internet_icon = ImageTk.PhotoImage(
    Image.open("icons/internet.png").resize((30, 30))
)

items = [
    (process_icon, "Processes"),
    (cpu_icon, "CPU"),
    (gpu_icon, "GPU"),
    (memory_icon, "Memory"),
    (disk_icon, "Disk"),
    (internet_icon, "Internet")
]

def on_click(name):
    print(f"{name} clicked")

start_y = 250
spacing = 65

for i, (icon, text) in enumerate(items):

    y = start_y + i * spacing

    icon_id = sidebar.create_image(
        40,
        y,
        image=icon,
        anchor="w"
    )

    text_id = sidebar.create_text(
        85,
        y,
        text=text,
        fill="white",
        font=("Segoe UI", 15),
        anchor="w"
    )

    # Click
    sidebar.tag_bind(
        icon_id,
        "<Button-1>",
        lambda e, t=text: on_click(t)
    )

    sidebar.tag_bind(
        text_id,
        "<Button-1>",
        lambda e, t=text: on_click(t)
    )

    # Hover
    sidebar.tag_bind(
        text_id,
        "<Enter>",
        lambda e, item=text_id:
        sidebar.itemconfig(item, fill="#d6f4ff")
    )

    sidebar.tag_bind(
        text_id,
        "<Leave>",
        lambda e, item=text_id:
        sidebar.itemconfig(item, fill="white")
    )

cpu_card = tk.Frame(
    root,
    bg="white",
    width=550,
    height=500,
    highlightbackground="#d9d9d9",
    highlightthickness=1
)

cpu_card.place(x=320, y=60)

cpu_card.pack_propagate(False)

cpu_name_label = tk.Label(
    cpu_card,
    text=cpuName,
    font=("Segoe UI", 16, "bold"),
    bg="white",
    wraplength=500,
    justify="left"
)

cpu_name_label.pack(anchor="nw", padx=20, pady=(15, 10))

cpu_load_label = tk.Label(
    cpu_card,
    text="Load: 0%",
    font=("Segoe UI", 14),
    bg="white"
)

cpu_load_label.pack(anchor="nw", padx=20)

cpu_temp_label = tk.Label(
    cpu_card,
    text="Temperature: N/A",
    font=("Segoe UI", 14),
    bg="white"
)

cpu_temp_label.pack(anchor="nw", padx=20, pady=(5, 0))

cpu_speed_label = tk.Label(
    cpu_card,
    text="Speed: 0 GHz",
    font=("Segoe UI", 14),
    bg="white"
)

cpu_speed_label.pack(anchor="nw", padx=20, pady=(5, 0))

threads_label = tk.Label(
    cpu_card,
    text="Threads: 0",
    font=("Segoe UI", 14),
    bg="white"
)

threads_label.pack(anchor="nw", padx=20, pady=(5, 0))

handles_label = tk.Label(
    cpu_card,
    text="Handles: 0",
    font=("Segoe UI", 14),
    bg="white"
)

handles_label.pack(anchor="nw", padx=20, pady=(5, 0))

l1_label = tk.Label(
    cpu_card,
    text=f"L1 Cache: {l1_data}",
    font=("Segoe UI", 14),
    bg="white"
)

l1_label.pack(anchor="nw", padx=20, pady=(5, 0))

l2_label = tk.Label(
    cpu_card,
    text=f"L2 Cache: {l2_cache}",
    font=("Segoe UI", 14),
    bg="white"
)

l2_label.pack(anchor="nw", padx=20, pady=(5, 0))

l3_label = tk.Label(
    cpu_card,
    text=f"L3 Cache: {l3_cache}",
    font=("Segoe UI", 14),
    bg="white"
)

l3_label.pack(anchor="nw", padx=20, pady=(5, 10))

cpu_data = []

fig = Figure(figsize=(5, 2.2), dpi=100)

ax = fig.add_subplot(111)

ax.set_title("CPU Usage")
ax.set_ylim(0, 100)
ax.set_ylabel("%")

line, = ax.plot(cpu_data)

graph = FigureCanvasTkAgg(fig, master=cpu_card)

graph.get_tk_widget().pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)

def update_stats():

    cpu_percent = psutil.cpu_percent()

    cpu_load_label.config(
        text=f"Load: {cpu_percent}%"
    )

    # Temperature
    try:
        temps = psutil.sensors_temperatures()

        if temps:
            first = list(temps.values())[0]

            if first:
                temp = first[0].current

                cpu_temp_label.config(
                    text=f"Temperature: {temp}°C"
                )

    except:
        cpu_temp_label.config(
            text="Temperature: N/A"
        )

    # Speed
    speed = psutil.cpu_freq().current / 1000

    cpu_speed_label.config(
        text=f"Speed: {speed:.2f} GHz"
    )

    # Threads
    threads = psutil.cpu_count(logical=True)

    threads_label.config(
        text=f"Threads: {threads}"
    )

    # Handles
    handles = psutil.Process().num_handles()

    handles_label.config(
        text=f"Handles: {handles}"
    )

    # Graph
    cpu_data.append(cpu_percent)

    if len(cpu_data) > 20:
        cpu_data.pop(0)

    line.set_ydata(cpu_data)
    line.set_xdata(range(len(cpu_data)))

    ax.set_xlim(0, max(20, len(cpu_data)))

    graph.draw()

    root.after(1000, update_stats)

# Start updates
update_stats()

root.mainloop()