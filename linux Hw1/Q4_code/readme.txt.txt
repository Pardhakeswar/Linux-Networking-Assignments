
pre requirements: execute chmod a+x <filename.sh> for all the 3 bash files
1. Copy and paste HW1 file in the Home/desktop directory to use the given cronjob commands directly
(59 * * * * $HOME/HW1/caller.sh   for script)
(59 * * * * $HOME/HW1/remove_log.sh for clearing logs)



2. Use command bash caller.sh to run the monitor script. 

(Caller will check process status and then calls q4.sh (which is the main bash file) 
This is done to handle exit conditions while using cron job and prevent 
duplicate instance of the script from running.)  

3. remove_log.sh is the script to clear the log files 

4. logs are recorded in alert.csv and log .csv

5. a section in the code contains comment for enabling graph 
 