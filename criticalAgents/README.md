# Critical Agents Report
This report will include a list of agents identified as critical.

## Required changes
  1. Update the url variable to include your S1 console URL.
  2. Update the header variable to include your API Token.
  3. Update the exportDir varibale to include the filepath you wish to write the file to.

## Excel Tab information
The first three tabs are sorted by site name while the offline endpoints tabs are sorted by last active date. This can be changed to a different column by updating the df.sort_values parameter for each dataframe.

###### Threats Tab
Agents with an infected status or agents in need of a reboot to finish mitigating a threat.

###### Failed State Tab
Agents with an operational state other than active.

###### Pending Actions
Agents with any pending actions that require user interaction. 
  This can include agents that just need a reboot after the initial installation to have full functionality, which is why the "Subscribed On" column is there.
  This includes macOS devices that are still in need of app permissions changes after the initial installation, which is why the OS column is there. 
    - See the "Installing the macOS Agent" or "Installing macOS - Kextless Agent" KB for instructions on how to grant S1 the required permissions.

###### Offline Servers
By default my script lists servers offline for 24+ hours in order by last active date.
  - Change the svrDateFilter variable to the number of days or hours you wish to filter by.

###### Offline Workstations
By default my script lists workstations offline for 30+ days in order by last active date.
  - Change the wsDateFilter variable to the number of days or hours you wish to filter by.
