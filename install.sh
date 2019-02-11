#!/bin/bash

chmod 744 memlogger.py
sudo apt install -y python3-pandas
SCRIPTDIR=$PWD
pushd /usr/bin/
sudo ln -s $SCRIPTDIR/memlogger.py memlogger.py
popd
TMP_CRONTAB=/tmp/tmp_cron
sudo crontab -l >> $TMP_CRONTAB
echo "* * * * * python3 /usr/bin/memlogger.py" >> $TMP_CRONTAB
sudo crontab $TMP_CRONTAB
sudo rm $TMP_CRONTAB
