# Copyright 2021. All right reserved.
# Author: Roopesha Sheshappa, Rai


SSID="295A-PSK-SSID"
PSK="aruba123"

echo -e "Connecting to SSID $SSID"
sudo nmcli dev wifi connect \"$SSID\" password \"$PSK\"
outputs=$(sudo nmcli --terse -f active,ssid dev wifi | egrep '^yes')
if [ -z "$outputs" ]; then
    echo -e "Unable to connect to SSID $SSID"
else
    ssid=$(echo ${outputs} | awk -F":" '{print $2}')
    echo "Connected to ssid \"$ssid\", expected \"$SSID\""
fi
