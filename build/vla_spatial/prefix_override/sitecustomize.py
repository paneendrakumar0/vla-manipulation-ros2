import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/paneendra/vla_manipulation_ros2/install/vla_spatial'
