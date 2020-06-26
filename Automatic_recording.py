"""
Script to run 4 cameras (external synchronization) of Microsoft Azure Kinect DK

k4arecorder [options] output.mkv

 Options:
  -h, --help              Prints this help
  --list                  List the currently connected K4A devices
  --device                Specify the device index to use (default: 0)
  -l, --record-length     Limit the recording to N seconds (default: infinite)
  -c, --color-mode        Set the color sensor mode (default: 1080p), Available options:
                            3072p, 2160p, 1536p, 1440p, 1080p, 720p, 720p_NV12, 720p_YUY2, OFF
  -d, --depth-mode        Set the depth sensor mode (default: NFOV_UNBINNED), Available options:
                            NFOV_2X2BINNED, NFOV_UNBINNED, WFOV_2X2BINNED, WFOV_UNBINNED, PASSIVE_IR, OFF
  --depth-delay           Set the time offset between color and depth frames in microseconds (default: 0)
                            A negative value means depth frames will arrive before color frames.
                            The delay must be less than 1 frame period.
  -r, --rate              Set the camera frame rate in Frames per Second
                            Default is the maximum rate supported by the camera modes.
                            Available options: 30, 15, 5
  --imu                   Set the IMU recording mode (ON, OFF, default: ON)
  --external-sync         Set the external sync mode (Master, Subordinate, Standalone default: Standalone)
  --sync-delay            Set the external sync delay off the master camera in microseconds (default: 0)
                            This setting is only valid if the camera is in Subordinate mode.
  -e, --exposure-control  Set manual exposure value (-11 to 1) for the RGB camera (default: auto exposure)
  
"""
import argparse
import datetime
import os
import subprocess
import time
  
parser = argparse.ArgumentParser(description="Enter the specified time to start recodring")
parser.add_argument("--h", "--hour", type=int, metavar="{0..23}", action="store", 
                    default=False, help="Enter an hour to start recoding")

parser.add_argument("--m", "--minute", type=int, metavar="{0..60}", action="store", 
                    default=False, help="Enter a minute to start recoding")

parser.add_argument("--s", "--second", type=int, metavar="{0..60}", action="store", 
                    default=0, help="Enter a second to start recoding")

parser.add_argument("--ms", "--microsecond", type=int, metavar="{0..10^6}", action="store", 
                    default=0, help="Enter a microsecond to start recoding")


args = parser.parse_args()

now = datetime.datetime.now()
start_time = datetime.datetime.now().replace(hour=args.h, minute=args.m, second=args.s, microsecond=args.ms)

def KinectWait(Time=now, Starting_Time=start_time):
    """
    Enter the specific time to start recording
    Input should be an array:
    input = [hour, minute, second]

    Returns
    -------
    Waiting till the specified time to start recording

    """
    #now = datetime.datetime.now()
    #start_time = datetime.datetime.now().replace(hour=14, minute=42, second=0, microsecond=0)
    difference = start_time - now
    print("----------------------------------------------------------------------------")
    print(f"Going to sleep for {difference}")
    print("----------------------------------------------------------------------------")
    time.sleep(difference.seconds)
    #print(difference, 'done')
    print("----------------------------------------------------------------------------")
    print("Waking up")
    print("----------------------------------------------------------------------------")
    
def KinectTimer(records = 0):
    
    KinectWait(now, start_time)
    
    # for time range between 9 am to 7 pm the number of records is set to 22
    while records < 2:
        print("----------------------------------------------------------------------------")
        print("In operation is lasting 30 minutes")
        print("----------------------------------------------------------------------------")
        # --device need to be configured according to USB ports
        path_save_file = "C:/Users/user_name/Desktop/Folder/"
        command_Sub_1 = f"k4arecorder.exe --imu OFF -r 15 --device 0 --external-sync Subordinate -l 1800 {path_save_file}output_sub_1_{records}.mkv"
        command_Sub_2 = f"k4arecorder.exe --imu OFF -r 15 --device 2 --external-sync Subordinate -l 1800 {path_save_file}output_sub_2_{records}.mkv"
        command_Sub_3 = f"k4arecorder.exe --imu OFF -r 15 --device 3 --external-sync Subordinate -l 1800 {path_save_file}output_sub_3_{records}.mkv"  
        command_Master = f"k4arecorder.exe --imu OFF -r 15 --device 1 --external-sync Master -l 1800 {path_save_file}output_master{records}.mkv"

        subprocess.Popen(os.path.join('C:/Program Files/Azure Kinect SDK v1.4.0/tools/', command_Sub_1))
        subprocess.Popen(os.path.join('C:/Program Files/Azure Kinect SDK v1.4.0/tools/', command_Sub_2))
        subprocess.Popen(os.path.join('C:/Program Files/Azure Kinect SDK v1.4.0/tools/', command_Sub_3))
        subprocess.Popen(os.path.join('C:/Program Files/Azure Kinect SDK v1.4.0/tools/', command_Master))
        
        # Timer is set to the same amount of time as recoding (time.sleep(1800) )
        time.sleep(1800)
        print(f"The current record number is {records}")
        print("----------------------------------------------------------------------------")
        print("Finishing operation and going to sleep for 60 seconds")
        print("----------------------------------------------------------------------------")
        # Time is set to save the recorder part
        time.sleep(60)
        print("Starting new operation")
        records += 1
        
if __name__ == "__main__":
    KinectTimer()
    
print("----------------------------------------------------------------------------")
print("Finished operation")   
print("----------------------------------------------------------------------------")
