import os
import time
import psutil
import GPUtil
import platform
import wmi
import cpuinfo

getCPU = cpuinfo.get_cpu_info()

myPC = wmi.WMI()
getGPU = myPC.Win32_VideoController()[0]

while True:
    print("CPU: ", getCPU["brand_raw"])
    cpuPercent = psutil.cpu_percent()
    print(f"CPU usage: {cpuPercent:.1f} % ")

    print("GPU: ", getGPU.Caption)
    gpus = GPUtil.getGPUs()
    gpuUsage = gpus[0].load * 100 if gpus else 0
    print(f"Gpu usage: {gpuUsage:.1f} %")

    ramTotal = round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 2)
    ramUsed = round(psutil.virtual_memory().used / 1024 / 1024 / 1024, 2)
    ramPercent = ramUsed / ramTotal * 100
    print(f"RAM Total: {ramTotal} | RAM used: {ramUsed}")
    print(f"RAM usage: {ramPercent} %")

    print("System's Network Name: ", platform.node())
    print("Architecture: ", platform.architecture())
    print("System's Network Name: ", platform.platform())

    time.sleep(1)
    os.system("cls")
