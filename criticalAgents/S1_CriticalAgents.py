import datetime, io, requests
import pandas as pd

#API call variables
url = 'https://YOURS1CONSOLEURL.net//web/api/v2.1/export/agents'
header = {"Authorization": "ApiToken YOURAPITOKEN"}
#Export dir/filename variables
exportDir = r"THEFILEPATHTOSTORETHEFILE"
date = datetime.datetime.now().strftime("%Y_%m_%d")
reportName = r'\S1_CriticalAgents_' + date
filePath = exportDir + reportName + '.xlsx'
#Blank dataframes to sort lines into for each excel sheet we want
dfThreats = pd.DataFrame()
dfFailed = pd.DataFrame()
dfPending = pd.DataFrame()
dfSvr = pd.DataFrame()
dfWs = pd.DataFrame()
#Datetime filters for the offline servers and workstations. Anything older than X days will show in the report.
svrDateFilter = datetime.datetime.now() - datetime.timedelta(days=1)
wsDateFilter = datetime.datetime.now() - datetime.timedelta(days=30)

#Query the S1 console and convert the data into the format that we need to sort and filter it
agents = requests.get(url, headers=header).content
data = pd.read_csv(io.StringIO(agents.decode('utf-8')))
data['Last Active'] = pd.to_datetime(data['Last Active'], format='%b %d, %Y %I:%M:%S %p')

#Select the columns we want, sort, and reset the index for our loops
df = (data[[
        'Endpoint Name',
        'Site',
        'Device Type',
        'Operational State',
        'Health Status',
        'Reboot Required due to Threat',
        'Pending Uninstall',
        'User Action Required',
        'Subscribed On',
        'OS',
        'OS Version',
        'Last Active'
    ]].sort_values(
        by=['Site']
    ).reset_index(drop=True
    )
)

for ind in df.index:
    #Get the current line's data
    line = pd.DataFrame(df.iloc[[ind]])
    if line['Health Status'][ind]!='Healthy' or line['Reboot Required due to Threat'][ind]!='No':
        #Select just the columns we want for each sheet
        lineThreats = line[['Endpoint Name','Site','Health Status','Reboot Required due to Threat']]
        #Write the data to the individual dataframes
        dfThreats = pd.concat([dfThreats, lineThreats], ignore_index=True)
    if line['Operational State'][ind]!='Not disabled':
        lineFailed = line[['Endpoint Name','Site','Operational State']]
        dfFailed = pd.concat([dfFailed, lineFailed], ignore_index=True)
    if line['User Action Required'][ind]!='No' or line['Pending Uninstall'][ind]!='No':
        linePending = line[['Endpoint Name','Site','User Action Required', 'Pending Uninstall', 'Subscribed On', 'OS']]
        dfPending = pd.concat([dfPending, linePending], ignore_index=True)
        
    #Write just the servers to the servers dataframe. Some servers show up as 'unknown' in the console
    if line['Device Type'][ind] == 'server' or line['Device Type'][ind] == 'unknown':
        if df['Last Active'][ind] <= svrDateFilter:
            lineSvr = line[['Endpoint Name','Site','Last Active','OS Version']]
            dfSvr = pd.concat([dfSvr, lineSvr], ignore_index=True)
    #Write everything else to the workstations dataframe
    else:
        if line['Last Active'][ind] <= wsDateFilter:    
            lineWs = line[['Endpoint Name','Site','Last Active','OS Version']]
            dfWs = pd.concat([dfWs, lineWs], ignore_index=True)

with pd.ExcelWriter(filePath) as writer:
    dfThreats.to_excel(writer, sheet_name='Threats', index=None)
    dfFailed.to_excel(writer, sheet_name='Failed State', index=None)
    dfPending.to_excel(writer, sheet_name='Pending Actions', index=None)
    dfSvr.sort_values(by=['Last Active']).to_excel(writer, sheet_name='Offline Servers', index=None)
    dfWs.sort_values(by=['Last Active']).to_excel(writer, sheet_name='Offline Workstations', index=None)
