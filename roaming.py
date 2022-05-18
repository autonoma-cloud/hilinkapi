"""
Roaming can be queried with:

curl -s http://192.168.8.1/api/dialup/connection 2>/dev/null |
    xml2 |
    grep Roam
/response/RoamAutoConnectEnable=1

curl -X POST http://192.168.8.1/api/dialup/connection should be possible too
with other, smaller libraries, but this works:
"""
from HiLinkAPI import webui
import logging
from time import sleep

logging.basicConfig(
    filename="hilinkapitest.log",
    format="%(name)s::%(levelname)s  {%(pathname)s:%(lineno)d} -- %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %I:%M:%S %p:%Z",
)

try:
    webUIArray = [
        # webui("E3372h-153", "192.168.18.1", "admin", "adm", logger=logging),
        webui("E3372h-320", "192.168.8.1", "", "", logger=logging),
    ]

    for webUI in webUIArray:
        try:
            webUI.start()
            while not webUI.getValidSession():
                if webUI.getActiveError() is not None:
                    error = webUI.getActiveError()
                    print(error)
                    sleep(5)
                if webUI.getLoginWaitTime() > 0:
                    print(
                        f"Login wait time = {webUI.getLoginWaitTime()} minutes"
                    )
                    sleep(5)
            # Enable data roaming and no idle timeout
            webUI.configureDataConnection(True, 0)
            webUI.queryDataConnection()
            print(f"devicename = {webUI.getDeviceName()}")
            print(f"login required = {webUI.getLoginRequired()}")
            print(f"Data roaming = {webUI.getDataRoaming()}")
            print(f"Max idle time = {webUI.getMaxIdleTime()}")
            webUI.stop()
            while not webUI.isStopped():
                webUI.stop()
                print(f"Waiting for stop")
                sleep(1)
        except Exception as e:
            print(e)
except Exception as e:
    print(e)
