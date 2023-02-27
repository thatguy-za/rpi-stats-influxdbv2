# A lightweight way to monitor raspberry pi (or other computer) statistics in InfluxDB

Inspired by [this guide](https://simonhearne.com/2020/pi-metrics-influx/), I wrote this script to send system stats to Influxdb 2.0+.

# Installation guide
1. Install InfluxDB (I did this in docker) and setup an API token 
2. Run ``` sudo apt install -y python3-pip ``` to install python
3. Run ``` sudo pip install psutil influxdb-client ``` to install the psutil library that we use to pull stats and the influxdb client
4. Download this script to your pi's home directory
5. Update the script with your influxdb credentials
6. Run ``` crontab -e ``` and add this scripr to run every minute by adding ` * * * * * /home/pi/rpi-stats-influx.py ` to the end of the file
7. Upload the dashboard_template.json file to influxdb so you have a basic dashboard to view metrics

# Preview
![alt text](https://i.imgur.com/V0Qfcrn.jpeg)
