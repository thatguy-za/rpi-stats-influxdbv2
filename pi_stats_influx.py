  GNU nano 5.4                                                                             pi_stats_influx.py *                                                                                     
import influxdb_client
import datetime
import psutil

from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "influx"
org = "private"
token = "<your influx API token>"
# Store the URL of your InfluxDB instance
url="http://127.0.0.1:8086"

measurement_name = "rackpi"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

# take a timestamp for this measurement
time = datetime.datetime.utcnow()

# collect some stats from psutil
disk = psutil.disk_usage('/')
mem = psutil.virtual_memory()
load = psutil.getloadavg()
temp = psutil.sensors_temperatures()["cpu_thermal"]

# format the data as a single measurement for influx
body = [
    {
        "measurement": measurement_name,
        "time": time,
        "fields": {
            "load_1": load[0],
            "load_5": load[1],
            "load_15": load[2],
            "disk_percent": disk.percent,
            "disk_free": disk.free,
            "disk_used": disk.used,
            "mem_percent": mem.percent,
            "mem_free": mem.free,
            "mem_used": mem.used,
            "cpu_core0_temp": temp[0].current
        }
    }
]

write_api.write(bucket=bucket, org=org, record=body)
