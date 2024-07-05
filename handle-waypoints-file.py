class MavlinkMissionItem:
    def __init__(self, seq:int, frame:int, command:int, current:int, autocontinue:int, param1:float, param2:float, param3:float, param4:float, latitude:int, longitude:int, altitude:float) -> None:
        self.seq = seq  # Waypoint ID (sequence number). Starts at zero
        self.current = current # false:0,true:1
        self.frame = frame # The coordinate system of the waypoint.
        self.autocontinue = autocontinue
        self.command = command 
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.x = int(latitude * 10**7) # latitude in degrees 10^7
        self.y = int(longitude * 10**7) # longitude in degrees 10^7
        self.z = altitude # altitude in meters
    def __str__(self) -> str:
        return (
            f"{self.seq}\t{self.current}\t{self.frame}\t{self.command}\t"
            f"{self.param1}\t{self.param2}\t{self.param3}\t{self.param4}\t"
            f"{float(self.x / 10**7)}\t{float(self.y / 10**7)}\t{self.z}\t{self.autocontinue}\r\n"
        )
wp_list = []

def parse_waypoint(chunks: list[str])->MavlinkMissionItem:
    if(len(chunks) != 12):
        raise Exception("Invalid file format!")
    seq = int(chunks[0]) 
    current = int(chunks[1]) 
    frame = int(chunks[2]) 
    command = int(chunks[3])
    param1 = float(chunks[4])
    param2 = float(chunks[5])
    param3 = float(chunks[6])
    param4 = float(chunks[7])
    latitude = float(chunks[8])
    longitude = float(chunks[9])
    altitude = float(chunks[10])
    autocontinue = int(chunks[11])
    return MavlinkMissionItem(seq, frame, command, current, autocontinue, param1, param2, param3, param4, latitude, longitude, altitude)

def read_waypoint_list(file_path = ''):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if(lines[0].strip() != "QGC WPL 110"):
            raise Exception("Invalid file format!")
        # seq   current frame   command param1      param2      param3      param4      latitude        longitude       altitude    autocontinue
        # 1     0       3       16	    0.00000000	0.00000000	0.00000000	0.00000000	-35.36295040	149.16518700	100.000000	1
        # 2     0       3       16	    0.00000000	0.00000000	0.00000000	0.00000000	-35.36292090	149.16552630	100.000000	1
        for i in range(1, len(lines)):
            chunks = lines[i].split('\t')
            item = parse_waypoint(chunks)
            wp_list.append(item)
        print(f'Waypoints read and parsed from {file_path} successfully.')

def write_waypoint_list(file_path = ''):
    with open(file_path, 'w') as outFile:
        outFile.write('QGC WPL 110\r\n')
        for wp in wp_list:
            # writing file with CRLF line endings
            outFile.write(str(wp)) 
        print(f'Waypoints saved to {file_path} successfully.')

read_waypoint_list('./mp-test.waypoints')
write_waypoint_list('./mp-output.waypoints')
for wp in wp_list:
    print(wp)