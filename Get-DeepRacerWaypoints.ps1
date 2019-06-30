#Requires -Version 6
#Requires -Modules AWSPowerShell.NetCore

# Generate list of waypoints for a Deepracer circuit and export them as a csv

[cmdletbinding()]
Param
(
    [Parameter(
        Mandatory=$true
    )]
    [String]$ProfileName,
    [Parameter(
        Mandatory=$true,
        HelpMessage='sim-77tg1gf24mjp/2019-05-13T14-48-58.300Z_5c9c56c2-4330-4c0e-b961-c95f1fe495d4/SimulationApplicationLogs'
    )]
    [String]$logstreamname
    
)
Initialize-AWSDefaultConfiguration -ProfileName $ProfileName -Region us-east-1

#-Limit <Int32>
#-NextToken <String>
$epochstart = Get-Date -Date "01/01/1970"
$starttime = "1/Jan/2018 00:00:00"
$endtime = "1/Jan/2039 00:00:00"
$starttimeepoch = (New-TimeSpan -Start $epochstart -End $starttime).TotalMilliseconds
$endtimeepoch = (New-TimeSpan -Start $epochstart -End $endtime).TotalMilliseconds
$loggroupname = '/aws/robomaker/SimulationJobs'

$cwlogseventsfiltered = Get-CWLFilteredLogEvent -FilterPattern 'Waypoint0' -LogStreamName $logstreamname -LogGroupName $loggroupname -StartTime $starttimeepoch -EndTime $endtimeepoch -Limit 500 
$dataobjects = @()
foreach($event in $cwlogseventsfiltered.Events)
{
    if ($event.message -match 'Waypoint0: (?<Waypoint>[0-9]+), X: (?<x>[.0-9]+), Y: (?<y>[.0-9]+)')
    {
        $data = [ordered]@{
            Waypoint = $Matches['Waypoint'].ToString() -as [int];
            x = $Matches['x'];
            y = $Matches['y'];
        }
        $dataObject = New-Object -TypeName psobject -Property $data
        $dataobjects += $dataObject
    }
}
$dataobjects | Sort-Object -Property 'Waypoint' -Unique | Export-Csv ./waypoints.csv -Force
