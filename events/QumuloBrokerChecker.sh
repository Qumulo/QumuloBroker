#!/bin/bash


# Define the log file and the word to search for
LOG_FILE="/var/log/syslog"
SEARCH_WORD="ERROR"
SLEEP_INTERVAL=1


# Path to lock file
LOCK_FILE="/tmp/check_log.lock"


# Function to remove lock file on exit
cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT


# Ensure only one instance of the script is running
if [ -e "$LOCK_FILE" ]; then
    echo "Script is already running."
    exit 1
else
    touch "$LOCK_FILE"
fi


# Loop to run the check every second
while true; do
    # Get the current date and time
    CURRENT_DATE=$(date +"%Y-%m-%d %H:%M:%S")


    # Get the last 50 lines of the log file and count the occurrences of the search word
    LINE_COUNT=$(tail -n 50 "$LOG_FILE" | grep -c "$SEARCH_WORD")


    # Check if the occurrences are more than 49
    if [ "$LINE_COUNT" -gt 49 ]; then
        # Restart the docker containers and rsyslog service
    	cd /opt/qumulo/QumuloBroker/api
    	docker compose down
    	docker compose up -d
        sleep 5
        systemctl restart rsyslog
        echo "[$CURRENT_DATE] rsyslog service restarted because $SEARCH_WORD appeared in $LINE_COUNT out of the last 50 lines of the log."
    else
        echo "[$CURRENT_DATE] $SEARCH_WORD appeared in $LINE_COUNT out of the last 50 lines of the log. No action taken."
    fi


    # Sleep for the specified interval
    sleep $SLEEP_INTERVAL
done


# Remove lock file (cleanup function will be called on script exit)
cleanup
