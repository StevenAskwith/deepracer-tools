def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    closest_waypoints = params['closest_waypoints']
    track_width = params['track_width']
    steering_angle = params['steering_angle']
    steps = params['steps']
    waypoints = params['waypoints']
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
    
    import math 
    coord0 = waypoints[closest_waypoints[0]]
    coord1 = waypoints[closest_waypoints[1]]
    myradians = math.atan2(coord1[1]-coord0[1], coord1[0]-coord0[0]) 
    mydegrees = math.degrees(myradians)
    print("Waypoint0:{},X:{},Y:{},heading:{},trackwidth:{},steeringangle:{},steps:{}".format(closest_waypoints[0],coord0[0],coord0[1],mydegrees,track_width,steering_angle,steps))
    
    return float(reward)