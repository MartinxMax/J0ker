import subprocess
import re
from loguru import logger
import sys
import argparse
import textwrap
import random
import string
import socket

VERSION = "V1.0"
TITLE = f'''
************************************************************************************
<免责声明>:本工具仅供学习实验使用,请勿用于非法用途,否则自行承担相应的法律责任
<Disclaimer>:This tool is onl y for learning and experiment. Do not use it
for illegal purposes, or you will bear corresponding legal responsibilities
************************************************************************************
'''
LOGO = f'''


          JJJJJJJJJJJ     000000000     kkkkkkkk
          J:::::::::J   00:::::::::00   k::::::k
          J:::::::::J 00:::::::::::::00 k::::::k
          JJ:::::::JJ0:::::::000:::::::0k::::::k
            J:::::J  0::::::0   0::::::0 k:::::k    kkkkkkk    eeeeeeeeeeee    rrrrr   rrrrrrrrr
            J:::::J  0:::::0     0:::::0 k:::::k   k:::::k   ee::::::::::::ee  r::::rrr:::::::::r
            J:::::J  0:::::0     0:::::0 k:::::k  k:::::k   e::::::eeeee:::::eer:::::::::::::::::r
            J:::::j  0:::::0 000 0:::::0 k:::::k k:::::k   e::::::e     e:::::err::::::rrrrr::::::r
            J:::::J  0:::::0 000 0:::::0 k::::::k:::::k    e:::::::eeeee::::::e r:::::r     r:::::r
JJJJJJJ     J:::::J  0:::::0     0:::::0 k:::::::::::k     e:::::::::::::::::e  r:::::r     rrrrrrr
J:::::J     J:::::J  0:::::0     0:::::0 k:::::::::::k     e::::::eeeeeeeeeee   r:::::r
J::::::J   J::::::J  0::::::0   0::::::0 k::::::k:::::k    e:::::::e            r:::::r
J:::::::JJJ:::::::J  0:::::::000:::::::0k::::::k k:::::k   e::::::::e           r:::::r
 JJ:::::::::::::JJ    00:::::::::::::00 k::::::k  k:::::k   e::::::::eeeeeeee   r:::::r
   JJ:::::::::JJ        00:::::::::00   k::::::k   k:::::k   ee:::::::::::::e   r:::::r
     JJJJJJJJJ            000000000     kkkkkkkk    kkkkkkk    eeeeeeeeeeeeee   rrrrrrr
                                                    Github==>https://github.com/MartinxMax
                                                    @Мартин. @ S-H4CK13 J0ker {VERSION}
'''



class server():


    def __init__(self,args):
        self.__init_logger()
        if args.GET :
            logger.log("SYSTEM","Camera list>> "+(' , '.join(self.__get_camera_name())))
        else:
            if args.SERVER:
                self.__server_rtsp(args.SERVER)
            else:
                if args.RPORT and args.RHOST:
                    if args.DESKTOP:
                        self.__monitor_desktop(args.RHOST,args.RPORT,self.__random_key())
                    elif args.CAMERA:
                        self.__monitor_camera(args.CAMERA,args.RHOST,args.RPORT,self.__random_key())
                    else:
                        logger.log("SYSTEM","Choose a parameter between the two to use (-desktop), (-camera <camera name>)!!")
                elif args.PLAY:
                    self.__rtsp_play(args.PLAY)
                else:
                    logger.log("SYSTEM","You must use - rhost, - rport to specify the streaming server, for example (- rhost 1.1.1.1- rport 8554)!!")


    def __local_ip(self):
        return socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)[0][4][0]


    def __init_logger(self):
        logger.level(name="SYSTEM", no=38, color="<green>")
        logger.level(name="MONITOR", no=39, color="<blue>")
        logger.level(name="CAMERA", no=40, color="<red>")
        logger.level(name="RTSP_SERVER", no=40, color="<yellow>")
        logger.remove()
        logger.add(
            sink=sys.stdout,
            format="<green>[{time:HH:mm:ss}]</green> | <level>{level: <8}</level> | {message}",
            level="INFO",
            colorize=True,
            backtrace=False,
            diagnose=False
        )


    def __server_rtsp(self,port):
        with open('./RTSP/rtsp-simple-server.bak','r',encoding='utf-8')as f:
            config = f.read()

        config=config.replace('@RTSP_MAPTNH',port or '8554')
        with open('./rtsp-simple-server.yml','w',encoding='utf-8')as f:
            f.write(config)
        logger.log("RTSP_SERVER","Successfully configured RTSP server")
        try:
            logger.log("RTSP_SERVER",f"Successfully started RTSP server on port [{self.__local_ip()}:{port}]")
            subprocess.run('rtsp-simple-server.exe', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            logger.log("RTSP_SERVER",f"Failed to start RTSP server, possibly due to port [{self.__local_ip()}:{port}] being occupied!")
            return False
        finally:
            logger.log("RTSP_SERVER",f"Exit...")
            return True


    def __get_camera_name(self):
        camera_name = list()
        pattern = r'\[dshow @ \w+\]  "(.*)"'
        cmd = ['./RTSP/ffmpeg.exe', '-hide_banner', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
        result = subprocess.run(cmd, capture_output=True).stderr.decode()
        matches = re.findall(pattern, result)
        for match in matches:
            camera_name.append(match)
        return camera_name


    def __monitor_desktop(self,server_ip, server_port, path):
        cmd = [
            './RTSP/ffmpeg.exe',
            '-f', 'gdigrab',
            '-framerate', '30',
            '-i', 'desktop',
            '-f', 'rtsp',
            '-rtsp_transport', 'tcp',f'rtsp://{server_ip}:{server_port}/{path}'
            ]
        try:
            logger.log("MONITOR",f" [Desktop Screen] Successfully pushed stream to RTPS address [{cmd[-1]}]")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            logger.log("MONITOR"," [Desktop Screen] Failed to stream to RTPS address!")
            return False
        finally:
            logger.log("MONITOR",f" [Desktop Screen] Exit...")
            return True


    def __monitor_camera(self,camera_name,server_ip,server_port,path):
        cmd = [
        './RTSP/ffmpeg',
        '-f', 'dshow',
        '-i', f'video={camera_name}',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-rtsp_transport', 'tcp',
        '-f', 'rtsp',
        f'rtsp://{server_ip}:{server_port}/{path}'
    ]
        try:
            logger.log("CAMERA",f" [{camera_name}] Successfully pushed stream to RTPS address [{cmd[-1]}]")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            logger.log("CAMERA",f" [{camera_name}] Failed to stream to RTPS address!")
            return False
        finally:
            logger.log("CAMERA",f" [{camera_name}] Exit...")
            return True


    def __random_key(self):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(6))
        return random_string


    def __rtsp_play(self,rstp_server):
        cmd = [
        './RTSP/ffplay.exe',
        '-rtsp_transport',
        'tcp',
        rstp_server
        ]
        try:
            logger.log("SYSTEM",f"Playing RTSP stream ...")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            logger.log("SYSTEM",f"Playback of RTSP stream failed")
            return False
        finally:
            logger.log("SYSTEM",f"Exit...")
            return True


if __name__ == '__main__':
    print(LOGO)
    print(TITLE)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
            Example:
                author-Github==>https://github.com/MartinxMax
            Basic usage:
                python {J0ker} -get # sObtain the name of the local camera
                python {J0ker} -desktop -rhost 127.0.0.1 -rport 9999 # Monitor local screen push to specified RTSP server host
                python {J0ker} -rhost 127.0.0.1 -rport 9999  -camera "USB2.0 PC CAMERA" # Push the name "USB2.0 PC CAMERA" to the RTSP server at 127.0.0.1:9999
                python {J0ker} -play rtsp://192.168.0.101:9999/OdP5n1 # Play RTSP stream
                python {J0ker} -server <port> # Enable RTSP server
                '''.format(J0ker=sys.argv[0])))
    parser.add_argument('-rhost', '--RHOST',default='', help='Remote Host')
    parser.add_argument('-rport', '--RPORT',default='', help='Remote Port')
    parser.add_argument('-get', '--GET', action='store_true', help='Get camera name')
    parser.add_argument('-camera', '--CAMERA',default='', help='Camera name')
    parser.add_argument('-server', '--SERVER',default='', help='Establish RTSP server')
    parser.add_argument('-play', '--PLAY',default='', help='Play RTSP stream')
    parser.add_argument('-desktop', '--DESKTOP', action='store_true', help='Monitoring Desktop')
    args = parser.parse_args()
    server(args)
