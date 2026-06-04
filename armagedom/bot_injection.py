import os
import sys
import time
import platform
import subprocess
from urllib.parse import urlparse, parse_qs, urlencode
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
    WDM_AVAILABLE = True
except ImportError:
    WDM_AVAILABLE = False

class I:
    @staticmethod
    def log(msg, color=Colors.red_to_blue):
        Write.Print(msg, color, interval=0.00001)

class DiscordBotInjection:
    def __init__(self, token, bot_url):
        self.token = token
        self.bot_url = bot_url
        self.driver = None
        self.system = platform.system()

    def parse_bot_url(self):
        try:
            if "discord.com/oauth2/authorize" in self.bot_url:
                parsed = urlparse(self.bot_url)
                params = parse_qs(parsed.query)

                client_id = params.get('client_id', [''])[0]
                permissions = params.get('permissions', ['8'])[0]
                integration_type = params.get('integration_type', ['0'])[0]
                scope = params.get('scope', ['applications.commands bot'])[0]

                oauth_params = {
                    'client_id': client_id,
                    'permissions': permissions,
                    'integration_type': integration_type,
                    'scope': scope
                }

                return f"/oauth2/authorize?{urlencode(oauth_params, doseq=True)}"
            else:
                I.log("\n✗ URL inválida. Use: https://discord.com/oauth2/authorize?client_id=...\n")
                return None
        except Exception as e:
            I.log(f"\n✗ Erro ao processar URL: {e}\n")
            return None

    def get_default_browser(self):
        try:
            if self.system == "Windows":
                import winreg
                try:
                    key = winreg.OpenKey(
                        winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER),
                        r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice"
                    )
                    prog_id, _ = winreg.QueryValueEx(key, "ProgId")

                    browser_map = {
                        'ChromeHTML': 'chrome',
                        'FirefoxURL': 'firefox',
                        'MSEdgeHTM': 'edge',
                        'BraveHTML': 'brave',
                        'OperaStable': 'opera'
                    }

                    for key_name, browser in browser_map.items():
                        if key_name in prog_id:
                            return browser
                except:
                    pass

            elif self.system == "Linux":
                try:
                    result = subprocess.run(
                        ['xdg-settings', 'get', 'default-web-browser'],
                        capture_output=True,
                        text=True
                    )
                    browser_desktop = result.stdout.strip().lower()

                    if 'chrome' in browser_desktop:
                        return 'chrome'
                    elif 'firefox' in browser_desktop:
                        return 'firefox'
                    elif 'edge' in browser_desktop:
                        return 'edge'
                    elif 'brave' in browser_desktop:
                        return 'brave'
                    elif 'opera' in browser_desktop:
                        return 'opera'
                except:
                    pass
        except:
            pass

        return 'chrome'

    def detect_browser_path(self, browser_name):
        paths = {
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

        for path in paths.get(browser_name, []):
            if os.path.exists(path):
                return path
        return None

    def init_chrome(self):
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-component-extensions-with-background-pages")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-breakpad")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        browser_path = self.detect_browser_path('chrome')
        if browser_path:
            options.binary_location = browser_path

        try:
            if WDM_AVAILABLE:
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
            else:
                return webdriver.Chrome(options=options)
        except:
            return None

    def init_firefox(self):
        options = FirefoxOptions()

        browser_path = self.detect_browser_path('firefox')
        if browser_path:
            options.binary_location = browser_path

        try:
            if WDM_AVAILABLE:
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=options)
            else:
                return webdriver.Firefox(options=options)
        except:
            return None

    def init_edge(self):
        options = EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")

        browser_path = self.detect_browser_path('edge')
        if browser_path:
            options.binary_location = browser_path

        try:
            if WDM_AVAILABLE:
                service = EdgeService(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=service, options=options)
            else:
                return webdriver.Edge(options=options)
        except:
            return None

    def init_driver(self, browser=None):
        if browser is None:
            browser = self.get_default_browser()

        if browser == 'chrome':
            self.driver = self.init_chrome()
        elif browser == 'firefox':
            self.driver = self.init_firefox()
        elif browser == 'edge':
            self.driver = self.init_edge()
        elif browser in ['brave', 'opera']:
            self.driver = self.init_chrome()

        if self.driver is None:
            for fallback in ['chrome', 'firefox', 'edge']:
                if fallback != browser:
                    if fallback == 'chrome':
                        self.driver = self.init_chrome()
                    elif fallback == 'firefox':
                        self.driver = self.init_firefox()
                    elif fallback == 'edge':
                        self.driver = self.init_edge()

                    if self.driver:
                        break

        return self.driver is not None

    def inject_token_and_redirect(self, redirect_path):
        script = f"""
        const token = "{self.token}";
        const redirectPath = "{redirect_path}";

        setInterval(() => {{
            let iframe = document.createElement('iframe');
            document.body.appendChild(iframe);
            iframe.contentWindow.localStorage.token = `"${{token}}"`;
        }}, 50);

        setTimeout(() => {{
            window.location.href = "https://discord.com" + redirectPath;
        }}, 2500);
        """

        try:
            self.driver.execute_script(script)
            return True
        except:
            return False

    def inject_bot(self):
        try:
            redirect_path = self.parse_bot_url()
            if not redirect_path:
                return False

            if not self.init_driver():
                I.log("\n✗ Falha ao inicializar navegador\n")
                return False

            I.log("\n✓ Navegador iniciado\n")

            self.driver.get("https://discord.com/login")
            time.sleep(3)

            if self.inject_token_and_redirect(redirect_path):
                I.log("✓ Token injetado\n")
                I.log("✓ Redirecionando...\n\n")

                time.sleep(6)

                I.log("\n✓ Autorização carregada\n")
                I.log("Selecione seu servidor e autorize o bot\n")
                I.log("Pressione Ctrl+C para sair\n\n")

                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    I.log("\n\n✓ Encerrando...\n")
                    self.driver.quit()

                return True
            else:
                I.log("\n✗ Falha ao injetar token\n")
                self.driver.quit()
                return False

        except KeyboardInterrupt:
            I.log("\n\n✓ Operação cancelada\n")
            if self.driver:
                self.driver.quit()
            return False
        except Exception as e:
            I.log(f"\n✗ Erro: {str(e)}\n")
            if self.driver:
                self.driver.quit()
            return False

def main(token=None, bot_url=None):
    if token is None:
        token = input("    Token: ").strip()

    if not token:
        I.log("\n✗ Token não fornecido\n")
        return

    if bot_url is None:
        bot_url = input("    URL do Bot: ").strip()

    if not bot_url:
        I.log("\n✗ URL não fornecida\n")
        return

    injection = DiscordBotInjection(token, bot_url)
    injection.inject_bot()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()