#!/bin/bash
echo "Starting Alpha-Video"
python /app/main.py > /var/log/alpha-video.log&
echo "Starting Supervisord"
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
bash
