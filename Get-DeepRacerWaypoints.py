import boto3
import datetime
import re
import matplotlib.path as mpath
import argparse

# args
parser = argparse.ArgumentParser(description='Generate list of waypoints for a Deepracer circuit as a String Path')
parser.add_argument('--profile', required=True, help='aws credentials profile')
parser.add_argument('--logstreamname', required=True, help='e.g. sim-nd2x8c3ph1d3/2019-06-06T14-39-31.940Z_3f5ddea9-6555-44d0-b1c7-ceb4b054f884/SimulationApplicationLogs')

args = parser.parse_args()

# constants
starttimeepoch = int(datetime.datetime(2018, 1, 30, 18, 0, 0).timestamp()) * 1000
endtimeepoch =   int(datetime.datetime(2030, 1, 30, 18, 0, 0).timestamp()) * 1000
loggroupname = '/aws/robomaker/SimulationJobs'
logstreamname = args.logstreamname
profile=args.profile
region='us-east-1'

session = boto3.Session(profile_name=profile,region_name=region)
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
logs_client = session.client('logs')

def get_string_path_data(loggroupname,logstreamname,filterPattern):
    nextToken = ''
    count = 0
    events = []
    while nextToken is not None:
        if nextToken == '':
            response = logs_client.filter_log_events(
                logGroupName=loggroupname,
                logStreamNames=[logstreamname],
                startTime=starttimeepoch,
                endTime=endtimeepoch,
                filterPattern=filterPattern,
                limit=5000
            )
        else:
            response = logs_client.filter_log_events(
                logGroupName=loggroupname,
                logStreamNames=[logstreamname],
                startTime=starttimeepoch,
                endTime=endtimeepoch,
                filterPattern=filterPattern,
                nextToken=nextToken,
                limit=5000
            )
        events += response['events']
        count += len(response['events'])
        print (count)
        
        ## while 
        if 'nextToken' not in response.keys():
            print ('End')
            break
        else:
            nextToken=response['nextToken']
            #break # unhash out for testing
        #print (nextToken)

    #regex = re.compile()
    print (len(events))
    coords = []
    print('Parsing Data...')
    for event in events:
        commasplit = event['message'].split(',')
        waypoint=int(commasplit[0].split(':')[1].strip())
        x=float(commasplit[1].split(':')[1].strip())
        y=float(commasplit[2].split(':')[1].strip())
        coord = {'waypoint': waypoint, 'x': x, 'y': y}
        coords.append(coord)
        #print("X: {}, Y: {}".format(x,y))

    #print(len(coords))
    uniquewaypoints = list({v['waypoint']:v for v in coords}.values()) # get unique items in list of dicts
    print("Unique Waypoints:{}".format(len(uniquewaypoints)))
    uniquewaypoints = sorted(uniquewaypoints, key = lambda i: i['waypoint']) 

    string_path_data = []
    firstwaypoint=True
    for waypoint in uniquewaypoints:
        if firstwaypoint:
            string_path_data.append((mpath.Path.MOVETO, (waypoint['x'],waypoint['y'])))
        else:
            string_path_data.append((mpath.Path.CURVE4, (waypoint['x'],waypoint['y'])))
        #print(waypoint)
        firstwaypoint=False
    return string_path_data

collected_string_path_data = get_string_path_data(loggroupname,logstreamname,'Waypoint0')
print(collected_string_path_data)