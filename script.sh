#!/bin/bash

mkdir -p /var/lib/node_exporter 
chown -Rv 200:200 /var/lib/node_exporter

cat  > /etc/systemd/system/smart.service << EOF

[Unit]
Description=SMART

[Service]
Type=simple
ExecStart=/bin/sh -c "/usr/bin/smartmon.sh -r > /var/lib/node_exporter/smartmon.prom"
SyslogIdentifier=Smartmon
Restart=always
RestartSec=86400

[Install]
WantedBy=multi-user.target

EOF

chown root:root /etc/systemd/system/smart.service

chmod 644 /etc/systemd/system/smart.service

systemctl start smart.service
systemctl enable smart.service
systemctl status smart.service
