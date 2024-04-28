import rumps
import subprocess
import psutil


def check_battery_level(sender):
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        if percent < 40:
            rumps.alert("Battery Less than 40%",  f"Battery level is {percent}%", "Connect To Power")
        elif percent >= 100:
            rumps.alert("Battery Fully Charged",  "Battery is fully charged", "100%")
        else:
            print(f"Battery level {percent}%")


def check_internet_connection():
    v = ["osascript", "-e", 'try', '-e', 'do shell script "ping -c 1 google.com"', '-e', 'return true', '-e',
             'on error', '-e', 'return false', '-e', 'end try']
    print("1")
    try:
        print("coming start")
        subprocess.run("ls")
        print("coming end")
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False


def update_status(self):
    print("0")
    current_status = check_internet_connection()
    if current_status != self.last_status:
        self.last_status = current_status
        if current_status:
            # self.menu.clear()
            # self.menu.add("Internet is stable")
            print("stable")
        else:
            # self.menu.clear()
            # self.menu.add("Internet is not stable")
            print("not stable")
    else:
        if current_status:
            # self.menu.clear()
            # self.menu.add("Internet is stable")
            print("stable yes")

        else:
            # self.menu.clear()
            # self.menu.add("Internet is not stable")
            print("stable not stable")


class Sias(rumps.App):
    def __init__(self):
        super(Sias, self).__init__("", icon="playstore-icon.png")
        self.title = ""
        self.battery_check_interval = 60
        self.timer = rumps.Timer(check_battery_level, self.battery_check_interval)
        self.timer.start()
        self.last_status = None

    @rumps.clicked("Battery Level")
    def battery_level(self, sender):
        check_battery_level(sender)

    @rumps.clicked("Sleep Now")
    def sleep_now(self, _):
        subprocess.run(["osascript", "-e", "tell application \"System Events\" to sleep"])

    @rumps.clicked("Internet Status")
    def check_internet_connection(self):
        print("-1")
        update_status(self)

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.alert("Hello")


if __name__ == "__main__":
    app = Sias()
    app.run()
