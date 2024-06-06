import display
import time
import socket
import struct
import machine

import secrets
import network
import urequests

# make a loading animation where it goes ....0.1.2.3.4
loadingAnimation = ["0000", "0001", "0012", "0123", "1234"]

# Connect to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(secrets.SSID, secrets.PASSWORD)

# Wait until the connection is established
itemCounter = 0
while not wifi.isconnected():
    display.displayLED(loadingAnimation[itemCounter], 0.25)
    itemCounter = (itemCounter + 1) % len(loadingAnimation)

# Display the IP address scrolling
print(wifi.ifconfig()[0])

display.displayLED("C00D", 0.5)


def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo("pool.ntp.org", 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - 2208988800
    tm = time.gmtime(t)
    machine.RTC().datetime(
        (tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))


def getHackHourTime():
    hackHourTime = urequests.get(
        url="http://hackhour.hackclub.com/api/clock/U062UG485EE")

    return hackHourTime.text


# start listening for the hack hour
# sync the time with the server
print("Syncing time with server")
# print local time
print(time.localtime())
set_time()
# print synced time
print(time.localtime())
minutesLeft = 0
while True:
    # get the hack hour from the server
    # find the minutes left as hack hour gives the end time in unix timestamp
    minutesLeft = getHackHourTime()
    print(minutesLeft)
    display.displayLED(minutesLeft, 3)
