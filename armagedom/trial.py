import os
import sys
import time
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from pystyle import Colors, Write

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    a = True
except ImportError:
    a = False

class b:
    @staticmethod
    def c(d, e=Colors.red_to_blue, f=0.00001):
        Write.Print(d, e, interval=f)

class DiscordBrowserLogin:
    def __init__(self, g):
        self.g = g
        self.h = None
        self.i = platform.system()

    def j(self):
        try:
            if self.i == "Windows":
                import winreg
                try:
                    k = winreg.OpenKey(
                        winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER),
                        r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice"
                    )
                    l, _ = winreg.QueryValueEx(k, "ProgId")
                    m = {
                        'ChromeHTML': 'chrome',
                        'FirefoxURL': 'firefox',
                        'MSEdgeHTM': 'edge',
                        'BraveHTML': 'brave',
                        'OperaStable': 'opera'
                    }
                    for n, o in m.items():
                        if n in l:
                            return o
                except:
                    pass
            elif self.i == "Linux":
                try:
                    p = subprocess.run(
                        ['xdg-settings', 'get', 'default-web-browser'],
                        capture_output=True,
                        text=True
                    )
                    q = p.stdout.strip().lower()
                    if 'chrome' in q:
                        return 'chrome'
                    elif 'firefox' in q:
                        return 'firefox'
                    elif 'edge' in q:
                        return 'edge'
                    elif 'brave' in q:
                        return 'brave'
                    elif 'opera' in q:
                        return 'opera'
                except:
                    pass
        except:
            pass
        return 'chrome'

    def r(self, s):
        t = {
            'chrome': [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium"
            ],
            'firefox': [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                "/usr/bin/firefox",
                "/usr/bin/firefox-esr"
            ],
            'edge': [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                "/usr/bin/microsoft-edge"
            ],
            'brave': [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
                "/usr/bin/brave-browser",
                "/usr/bin/brave"
            ],
            'opera': [
                r"C:\Program Files\Opera\launcher.exe",
                r"C:\Program Files (x86)\Opera\launcher.exe",
                "/usr/bin/opera"
            ]
        }
        for u in t.get(s, []):
            if os.path.exists(u):
                return u
        return None

    def v(self):
        w = ChromeOptions()
        w.add_argument("--disable-blink-features=AutomationControlled")
        w.add_experimental_option("excludeSwitches", ["enable-automation"])
        w.add_experimental_option('useAutomationExtension', False)
        w.add_argument("--log-level=3")
        w.add_experimental_option('excludeSwitches', ['enable-logging'])
        x = self.r('chrome')
        if x:
            w.binary_location = x
        try:
            if a:
                y = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=y, options=w)
            else:
                return webdriver.Chrome(options=w)
        except:
            return None

    def z(self):
        aa = FirefoxOptions()
        aa.add_argument("--log-level=3")
        ab = self.r('firefox')
        if ab:
            aa.binary_location = ab
        try:
            if a:
                ac = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=ac, options=aa)
            else:
                return webdriver.Firefox(options=aa)
        except:
            return None

    def ad(self):
        ae = EdgeOptions()
        ae.add_argument("--disable-blink-features=AutomationControlled")
        ae.add_argument("--log-level=3")
        ae.add_experimental_option('excludeSwitches', ['enable-logging'])
        af = self.r('edge')
        if af:
            ae.binary_location = af
        try:
            if a:
                ag = EdgeService(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=ag, options=ae)
            else:
                return webdriver.Edge(options=ae)
        except:
            return None

    def ah(self, ai=None):
        if ai is None:
            ai = self.j()
        if ai == 'chrome':
            self.h = self.v()
        elif ai == 'firefox':
            self.h = self.z()
        elif ai == 'edge':
            self.h = self.ad()
        elif ai in ['brave', 'opera']:
            self.h = self.v()
        if self.h is None:
            for aj in ['chrome', 'firefox', 'edge']:
                if aj != ai:
                    if aj == 'chrome':
                        self.h = self.v()
                    elif aj == 'firefox':
                        self.h = self.z()
                    elif aj == 'edge':
                        self.h = self.ad()
                    if self.h:
                        break
        return self.h is not None

    def ak(self):
        al = f"""
        const token = "{self.g}";
        setInterval(() => {{
            let iframe = document.createElement('iframe');
            document.body.appendChild(iframe);
            iframe.contentWindow.localStorage.token = `"${{token}}"`;
        }}, 50);
        setTimeout(() => {{
            location.reload();
        }}, 2500);
        """
        try:
            self.h.execute_script(al)
            return True
        except:
            return False

    def login(self):
        try:
            b.c("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue)
            b.c("║                    BROWSER AUTO-LOGIN                          ║\n", Colors.red_to_blue)
            b.c("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue)
            
            if not self.ah():
                b.c("\n✗ Browser initialization failed\n", Colors.red_to_blue)
                return False

            b.c("\n✓ Browser launched\n", Colors.red_to_blue)
            self.h.get("https://discord.com/login")
            time.sleep(3)
            
            if self.ak():
                b.c("✓ Token injected\n", Colors.red_to_blue)
                time.sleep(5)
                b.c("✓ Login successful\n\n", Colors.red_to_blue)
                b.c("    Press CTRL+C to close browser...\n", Colors.red_to_blue)
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    self.h.quit()
                    b.c("\n✓ Browser closed\n", Colors.red_to_blue)
                return True
            else:
                b.c("\n✗ Token injection failed\n", Colors.red_to_blue)
                self.h.quit()
                return False
        except KeyboardInterrupt:
            if self.h:
                self.h.quit()
            b.c("\n✗ Operation cancelled\n", Colors.red_to_blue)
            return False
        except:
            if self.h:
                self.h.quit()
            return False

def main(am=None):
    if am is None:
        b.c("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue)
        b.c("║                    BROWSER AUTO-LOGIN                          ║\n", Colors.red_to_blue)
        b.c("╚════════════════════════════════════════════════════════════════╝\n\n", Colors.red_to_blue)
        am = input("    Token: ").strip()
    if not am:
        b.c("\n✗ No token provided\n", Colors.red_to_blue)
        return
    an = DiscordBrowserLogin(am)
    an.login()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()