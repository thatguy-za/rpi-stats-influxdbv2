import influxdb_client
import datetime
import psutil
import time

from influxdb_client.client.write_api import SYNCHRONOUS

# influxdb connection info
bucket = "influx"
org = "private"
token = "<your api token>"
url="http://127.0.0.1:8086"

# client name
measurement_name = "raspberrypi"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

# take a timestamp for this measurement
timeNow = datetime.datetime.utcnow()

# collect stats from psutil
disk = psutil.disk_usage('/')
mem = psutil.virtual_memory()
load = psutil.getloadavg()
temp = psutil.sensors_temperatures()["cpu_thermal"]
cpu_usage_all_cores = psutil.cpu_percent(interval=1)

# Collect network stats
net_stat = psutil.net_io_counters(pernic=True, nowrap=True)["eth0"]
net_in_1 = net_stat.bytes_recv
net_out_1 = net_stat.bytes_sent
time.sleep(1)
net_stat = psutil.net_io_counters(pernic=True, nowrap=True)["eth0"]
net_in_2 = net_stat.bytes_recv
net_out_2 = net_stat.bytes_sent

net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)

# format the data as a single measurement for influx
body = [
    {
        "measurement": measurement_name,
        "time": timeNow,
        "fields": {
            "load_1": load[0],
            "load_5": load[1],
            "load_15": load[2],
            "cpu_usage": cpu_usage_all_cores,
            "disk_percent": disk.percent,
            "disk_free": disk.free,
            "disk_used": disk.used,
            "mem_percent": mem.percent,
            "mem_free": mem.free,
            "mem_used": mem.used,
            "cpu_temp": temp[0].current,
            "eth0_in": net_in,
            "eth0_out": net_out
        }
    }
]

write_api.write(bucket=bucket, org=org, record=body)
