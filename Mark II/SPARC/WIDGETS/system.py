import platform
import psutil
import GPUtil

def info():
    """
    Gathers and prints system information including CPU, RAM, and GPU details.
    """
    
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")

    # CPU information
    print("="*40, "CPU Info", "="*40)
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

    # Memory Information
    print("="*40, "Memory Information", "="*40)
    svmem = psutil.virtual_memory()
    print(f"Total: {svmem.total / (1024.0 ** 3):.2f} GB")
    print(f"Available: {svmem.available / (1024.0 ** 3):.2f} GB")
    print(f"Used: {svmem.used / (1024.0 ** 3):.2f} GB")
    print(f"Percentage: {svmem.percent}%")

    # GPU information
    print("="*40, "GPU Info", "="*40)
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            print(f"GPU ID: {gpu.id}")
            print(f"  GPU Name: {gpu.name}")
            print(f"  GPU Load: {gpu.load*100:.2f}%")
            print(f"  GPU Memory Total: {gpu.memoryTotal:.2f}MB")
            print(f"  GPU Memory Used: {gpu.memoryUsed:.2f}MB")
            print(f"  GPU Memory Free: {gpu.memoryFree:.2f}MB")
            print(f"  GPU Temperature: {gpu.temperature:.2f} °C")
    except Exception as e:
        return(f"Error getting GPU information: {e}")
    
    return("system information has been returned")


if __name__ == "__main__":
    info()
