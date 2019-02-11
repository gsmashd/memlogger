import os
import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTPUTDIR = "/var/log/memlogger/"

def log_mem(now):
    with open("/proc/meminfo","r") as meminf:
        for line in meminf:
            if line.startswith("MemTotal"):
                mem_tot = float(line.split(" ")[-2])/(1024*1024)
            if line.startswith("MemAvailable"):
                mem_avail = float(line.split(" ")[-2])/(1024*1024)

    mem_used = mem_tot - mem_avail
    date = now.strftime("%Y-%m-%d")
    os.makedirs(os.path.join(OUTPUTDIR,"data"),exist_ok=True)

    if os.path.exists(os.path.join(OUTPUTDIR,"data","{}.data".format(date))):
        logfile = open(os.path.join(OUTPUTDIR,"data","{}.data".format(date)),'a')
    else:
        logfile = open(os.path.join(OUTPUTDIR,"data","{}.data".format(date)),'w')
        logfile.write("date,mem_tot,mem_used,mem_avail\n")

    logfile.write("{},{},{},{}\n".format(now,mem_tot,mem_used,mem_avail))
    logfile.close()

def plot_mem(now):
    date = now.strftime("%Y-%m-%d")
    os.makedirs(os.path.join(OUTPUTDIR,"plot"),exist_ok=True)

    data = pd.read_csv(os.path.join(OUTPUTDIR,"data","{}.data".format(date)))
    data['date'] = pd.to_datetime(data['date'])
    plt.figure(1)
    line_used, = plt.plot(data['date'],data['mem_used'],label="Memory used")
    line_tot, = plt.plot(data['date'],data['mem_tot'],label="Total memory")
    plt.ylim(0,data['mem_tot'].iloc[-1]+5)
    plt.title("Memory used {}".format(date))
    plt.xlabel("Time")
    plt.ylabel("GB")
    plt.savefig(os.path.join(OUTPUTDIR,"plot","{}_mem_used.png".format(date)))

    plt.figure(2)
    line_avail, = plt.plot(data['date'],data['mem_avail'],label="Available memory")
    line_tot, = plt.plot(data['date'],data['mem_tot'],label="Total memory")
    plt.ylim(0,data['mem_tot'].iloc[-1]+5)
    plt.title("Memory available {}".format(date))
    plt.xlabel("Time")
    plt.ylabel("GB")
    plt.savefig(os.path.join(OUTPUTDIR,"plot","{}_mem_avail.png".format(date)))

def cleanup(now):
    yesterday = now - datetime.timedelta(days=1)
    date = yesterday.strftime("%Y-%m-%d")
    if os.path.exists(os.path.join(OUTPUTDIR,"data","{}.data".format(date))):
        os.remove(os.path.join(OUTPUTDIR,"data","{}.data".format(date)))
    last_month = now - datetime.timedelta(days=40)
    date = last_month.strftime("%Y-%m-%d")
    if os.path.exists(os.path.join(OUTPUTDIR,"plot","{}_mem_avail.png".format(date))):
        os.remove(os.path.join(OUTPUTDIR,"plot","{}_mem_avail.png".format(date)))
    if os.path.exists(os.path.join(OUTPUTDIR,"plot","{}_mem_used.png".format(date))):
        os.remove(os.path.join(OUTPUTDIR,"plot","{}_mem_used.png".format(date)))



NOW = datetime.datetime.now()
log_mem(NOW)
plot_mem(NOW)
cleanup(NOW)



