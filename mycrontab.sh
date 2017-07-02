# Crontab placed in /etc/cron.hourly
# Cron will run every min of the day, running the twitter_bot.py script 
# logging to log file mycron.log

* * * * * cd <directory of twitter_bot.py> && python twitter_bot.py >> ~/Desktop/mycron.log 2>&1
