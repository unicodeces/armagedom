import requests
import os
import time
import base64
from pystyle import Colors, Write, Center

class d:
    def __init__(self, t):
        self.t = t
        self.u = "https://discord.com/api/v10"
        self.h = {"Authorization": t}
        self.s = None
        self.g = None
        self.sd = None
        self.gd = None
        self.w = 0.3

    def c(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def b(self):
        a = """
  /$$$$$$  /$$$$$$$  /$$      /$$  /$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$      /$$
 /$$__  $$| $$__  $$| $$$    /$$$ /$$__  $$ /$$__  $$| $$_____/| $$__  $$ /$$__  $$| $$$    /$$$
| $$  \ $$| $$  \ $$| $$$$  /$$$$| $$  \ $$| $$  \__/| $$      | $$  \ $$| $$  \ $$| $$$$  /$$$$
| $$$$$$$$| $$$$$$$/| $$ $$/$$ $$| $$$$$$$$| $$ /$$$$| $$$$$   | $$  | $$| $$  | $$| $$ $$/$$ $$
| $$__  $$| $$__  $$| $$  $$$| $$| $$__  $$| $$|_  $$| $$__/   | $$  | $$| $$  | $$| $$  $$$| $$
| $$  | $$| $$  \ $$| $$\  $ | $$| $$  | $$| $$  \ $$| $$      | $$  | $$| $$  | $$| $$\  $ | $$
| $$  | $$| $$  | $$| $$ \/  | $$| $$  | $$|  $$$$$$/| $$$$$$$$| $$$$$$$/|  $$$$$$/| $$ \/  | $$
|__/  |__/|__/  |__/|__/     |__/|__/  |__/ \______/ |________/|_______/  \______/ |__/     |__/
        """
        Write.Print(Center.XCenter(a), Colors.red_to_blue, interval=0.00001)

    def p(self, m, c=Colors.red_to_blue):
        Write.Print(m, c, interval=0.00001)

    def ls(self, i):
        try:
            r = requests.get(f"{self.u}/guilds/{i}?with_counts=true", headers=self.h)
            if r.status_code != 200:
                self.p(f"\n✗ Unable to access source server\n")
                return False
            self.sd = r.json()
            self.s = i
            return True
        except:
            self.p(f"\n✗ Connection error\n")
            return False

    def n(self):
        try:
            d = {"name": "My Server", "icon": None, "channels": [], "system_channel_id": None, "afk_channel_id": None}
            r = requests.post(f"{self.u}/guilds", headers=self.h, json=d)
            if r.status_code in [200, 201]:
                self.gd = r.json()
                self.g = self.gd.get('id')
                self.p(f"\n✓ Server created successfully\n")
                self.p(f"            ID: {self.g}\n")
                return True
            else:
                e = r.json() if r.text else {}
                self.p(f"\n✗ Creation failed\n")
                if e.get('message'):
                    self.p(f"    {e['message']}\n")
                return False
        except:
            self.p(f"\n✗ Server creation error\n")
            return False

    def lt(self, i):
        try:
            r = requests.get(f"{self.u}/guilds/{i}?with_counts=true", headers=self.h)
            if r.status_code != 200:
                self.p(f"\n✗ Unable to access target server\n")
                return False
            self.gd = r.json()
            self.g = i
            ur = requests.get(f"{self.u}/users/@me", headers=self.h)
            if ur.status_code != 200:
                self.p("\n✗ Authentication error\n")
                return False
            ud = ur.json()
            ui = ud.get('id')
            if self.gd.get('owner_id') == ui:
                return True
            gr = requests.get(f"{self.u}/users/@me/guilds", headers=self.h)
            if gr.status_code == 200:
                gs = gr.json()
                gi = next((g for g in gs if g.get('id') == i), None)
                if gi:
                    p = gi.get('permissions', 0)
                    ia = bool(int(p) & 0x8) if p else False
                    if ia:
                        return True
                    else:
                        self.p("\n✗ Insufficient permissions\n")
                        return False
            self.p("\n✗ Permission verification failed\n")
            return False
        except:
            self.p(f"\n✗ Connection error\n")
            return False

    def cl(self):
        self.p("\n╔════════════════════════════════════════════════════════════════╗\n")
        self.p("║                    PREPARING TARGET SERVER                     ║\n")
        self.p("╚════════════════════════════════════════════════════════════════╝\n")
        try:
            r = requests.get(f"{self.u}/guilds/{self.g}/channels", headers=self.h)
            if r.status_code == 200:
                ch = r.json()
                self.p(f"\n    Processing {len(ch)} channels...\n")
                for c in ch:
                    try:
                        requests.delete(f"{self.u}/channels/{c['id']}", headers=self.h)
                        time.sleep(self.w)
                    except:
                        pass
        except:
            self.p("    ✗ Channel cleanup error\n")
        try:
            r = requests.get(f"{self.u}/guilds/{self.g}/roles", headers=self.h)
            if r.status_code == 200:
                ro = [x for x in r.json() if x['name'] != '@everyone']
                self.p(f"    Processing {len(ro)} roles...\n")
                for x in ro:
                    try:
                        requests.delete(f"{self.u}/guilds/{self.g}/roles/{x['id']}", headers=self.h)
                        time.sleep(self.w)
                    except:
                        pass
        except:
            self.p("    ✗ Role cleanup error\n")
        try:
            r = requests.get(f"{self.u}/guilds/{self.g}/emojis", headers=self.h)
            if r.status_code == 200:
                em = r.json()
                if em:
                    self.p(f"    Processing {len(em)} emojis...\n")
                    for e in em:
                        try:
                            requests.delete(f"{self.u}/guilds/{self.g}/emojis/{e['id']}", headers=self.h)
                            time.sleep(self.w)
                        except:
                            pass
        except:
            self.p("    ✗ Emoji cleanup error\n")
        self.p("\n    ✓ Server prepared\n")

    def si(self):
        self.p("\n╔════════════════════════════════════════════════════════════════╗\n")
        self.p("║                    TRANSFERRING SETTINGS                       ║\n")
        self.p("╚════════════════════════════════════════════════════════════════╝\n")
        try:
            ud = {}
            if self.sd.get('name'):
                ud['name'] = self.sd['name']
            if self.sd.get('icon'):
                iu = f"https://cdn.discordapp.com/icons/{self.s}/{self.sd['icon']}.png"
                try:
                    ir = requests.get(iu)
                    if ir.status_code == 200:
                        im = base64.b64encode(ir.content).decode('utf-8')
                        ud['icon'] = f"data:image/png;base64,{im}"
                        self.p("    ✓ Icon transferred\n")
                except:
                    self.p("    ✗ Icon transfer failed\n")
            if self.sd.get('banner'):
                bu = f"https://cdn.discordapp.com/banners/{self.s}/{self.sd['banner']}.png"
                try:
                    br = requests.get(bu)
                    if br.status_code == 200:
                        bm = base64.b64encode(br.content).decode('utf-8')
                        ud['banner'] = f"data:image/png;base64,{bm}"
                        self.p("    ✓ Banner transferred\n")
                except:
                    pass
            if self.sd.get('splash'):
                su = f"https://cdn.discordapp.com/splashes/{self.s}/{self.sd['splash']}.png"
                try:
                    sr = requests.get(su)
                    if sr.status_code == 200:
                        sm = base64.b64encode(sr.content).decode('utf-8')
                        ud['splash'] = f"data:image/png;base64,{sm}"
                        self.p("    ✓ Splash transferred\n")
                except:
                    pass
            if self.sd.get('verification_level') is not None:
                ud['verification_level'] = self.sd['verification_level']
            if self.sd.get('default_message_notifications') is not None:
                ud['default_message_notifications'] = self.sd['default_message_notifications']
            if self.sd.get('explicit_content_filter') is not None:
                ud['explicit_content_filter'] = self.sd['explicit_content_filter']
            if ud:
                r = requests.patch(f"{self.u}/guilds/{self.g}", headers=self.h, json=ud)
                if r.status_code == 200:
                    self.p(f"\n    ✓ Server name: {ud.get('name', 'N/A')}\n")
                    if 'verification_level' in ud:
                        self.p(f"    ✓ Verification settings applied\n")
                    if 'default_message_notifications' in ud:
                        self.p(f"    ✓ Notification settings applied\n")
                else:
                    self.p("    ✗ Settings update failed\n")
        except:
            self.p("    ✗ Transfer error\n")

    def ro(self):
        self.p("\n╔════════════════════════════════════════════════════════════════╗\n")
        self.p("║                    CREATING ROLES                              ║\n")
        self.p("╚════════════════════════════════════════════════════════════════╝\n")
        try:
            r = requests.get(f"{self.u}/guilds/{self.s}/roles", headers=self.h)
            if r.status_code != 200:
                self.p("\n    ✗ Unable to retrieve roles\n")
                return {}
            sr = r.json()
            ev = next((x for x in sr if x['name'] == '@everyone'), None)
            sr = sorted([x for x in sr if x['name'] != '@everyone'], key=lambda x: x.get('position', 0))
            rm = {}
            ct = 0
            tr = requests.get(f"{self.u}/guilds/{self.g}/roles", headers=self.h)
            if tr.status_code == 200:
                te = next((x for x in tr.json() if x['name'] == '@everyone'), None)
                if te and ev:
                    rm[ev['id']] = te['id']
            for x in sr:
                try:
                    rd = {
                        "name": x.get('name', 'new-role'),
                        "permissions": str(x.get('permissions', '0')),
                        "color": x.get('color', 0),
                        "hoist": x.get('hoist', False),
                        "mentionable": x.get('mentionable', False)
                    }
                    if x.get('unicode_emoji'):
                        rd['unicode_emoji'] = x['unicode_emoji']
                    elif x.get('icon'):
                        rd['icon'] = x['icon']
                    cr = requests.post(f"{self.u}/guilds/{self.g}/roles", headers=self.h, json=rd)
                    if cr.status_code in [200, 201]:
                        nr = cr.json()
                        rm[x['id']] = nr['id']
                        ct += 1
                        self.p(f"\n    ✓ {x.get('name', 'Unknown')}\n")
                    time.sleep(self.w)
                except:
                    pass
            self.p(f"\n    ✓ Created {ct}/{len(sr)} roles\n")
            return rm
        except:
            self.p("\n    ✗ Role creation error\n")
            return {}

    def ch(self, rm):
        self.p("\n╔════════════════════════════════════════════════════════════════╗\n")
        self.p("║                    CREATING CHANNELS                           ║\n")
        self.p("╚════════════════════════════════════════════════════════════════╝\n")
        try:
            r = requests.get(f"{self.u}/guilds/{self.s}/channels", headers=self.h)
            if r.status_code != 200:
                self.p("\n    ✗ Unable to retrieve channels\n")
                return
            sc = r.json()
            ca = sorted([x for x in sc if x.get('type') == 4], key=lambda x: x.get('position', 0))
            oc = sorted([x for x in sc if x.get('type') != 4], key=lambda x: x.get('position', 0))
            cm = {}
            ct = 0
            for x in ca:
                try:
                    cd = {"name": x.get('name', 'new-category'), "type": 4, "position": x.get('position', 0)}
                    if x.get('permission_overwrites'):
                        ow = []
                        for o in x['permission_overwrites']:
                            no = {'type': o.get('type', 0), 'allow': str(o.get('allow', '0')), 'deny': str(o.get('deny', '0'))}
                            if o.get('type') == 0:
                                if o['id'] in rm:
                                    no['id'] = rm[o['id']]
                                    ow.append(no)
                            elif o.get('type') == 1:
                                no['id'] = o['id']
                                ow.append(no)
                        if ow:
                            cd['permission_overwrites'] = ow
                    cr = requests.post(f"{self.u}/guilds/{self.g}/channels", headers=self.h, json=cd)
                    if cr.status_code in [200, 201]:
                        nc = cr.json()
                        cm[x['id']] = nc['id']
                        ct += 1
                        pc = len(x.get('permission_overwrites', []))
                        pt = f" ({pc} permissions)" if pc > 0 else ""
                        self.p(f"\n    ✓ Category: {x.get('name', 'Unknown')}{pt}\n")
                    time.sleep(self.w)
                except:
                    pass
            for x in oc:
                try:
                    cd = {"name": x.get('name', 'new-channel'), "type": x.get('type', 0), "position": x.get('position', 0)}
                    if x.get('topic'):
                        cd['topic'] = x['topic']
                    if x.get('nsfw') is not None:
                        cd['nsfw'] = x['nsfw']
                    if x.get('rate_limit_per_user'):
                        cd['rate_limit_per_user'] = x['rate_limit_per_user']
                    if x.get('bitrate'):
                        cd['bitrate'] = x['bitrate']
                    if x.get('user_limit'):
                        cd['user_limit'] = x['user_limit']
                    if x.get('parent_id') and x['parent_id'] in cm:
                        cd['parent_id'] = cm[x['parent_id']]
                    if x.get('permission_overwrites'):
                        ow = []
                        for o in x['permission_overwrites']:
                            no = {'type': o.get('type', 0), 'allow': str(o.get('allow', '0')), 'deny': str(o.get('deny', '0'))}
                            if o.get('type') == 0:
                                if o['id'] in rm:
                                    no['id'] = rm[o['id']]
                                    ow.append(no)
                            elif o.get('type') == 1:
                                no['id'] = o['id']
                                ow.append(no)
                        if ow:
                            cd['permission_overwrites'] = ow
                    cr = requests.post(f"{self.u}/guilds/{self.g}/channels", headers=self.h, json=cd)
                    if cr.status_code in [200, 201]:
                        ct += 1
                        cty = {0: "text", 2: "voice", 5: "announcement", 13: "stage", 15: "forum"}.get(x.get('type'), "channel")
                        pc = len(x.get('permission_overwrites', []))
                        pt = f" ({pc} permissions)" if pc > 0 else ""
                        self.p(f"    ✓ {cty.capitalize()}: {x.get('name', 'Unknown')}{pt}\n")
                    time.sleep(self.w)
                except:
                    pass
            tt = len(ca) + len(oc)
            self.p(f"\n    ✓ Created {ct}/{tt} channels\n")
        except:
            self.p("\n    ✗ Channel creation error\n")

    def em(self):
        self.p("\n╔════════════════════════════════════════════════════════════════╗\n")
        self.p("║                    TRANSFERRING EMOJIS                         ║\n")
        self.p("╚════════════════════════════════════════════════════════════════╝\n")
        try:
            r = requests.get(f"{self.u}/guilds/{self.s}/emojis", headers=self.h)
            if r.status_code != 200:
                self.p("\n    ✗ Unable to retrieve emojis\n")
                return
            se = r.json()
            if not se:
                self.p("\n    ✓ No emojis to transfer\n")
                return
            ct = 0
            fl = 0
            for x in se:
                try:
                    eu = f"https://cdn.discordapp.com/emojis/{x['id']}.{'gif' if x.get('animated') else 'png'}"
                    ir = requests.get(eu)
                    if ir.status_code == 200:
                        im = base64.b64encode(ir.content).decode('utf-8')
                        fm = 'gif' if x.get('animated') else 'png'
                        id = f"data:image/{fm};base64,{im}"
                        ed = {"name": x.get('name', 'emoji'), "image": id}
                        if x.get('roles'):
                            ed['roles'] = x['roles']
                        cr = requests.post(f"{self.u}/guilds/{self.g}/emojis", headers=self.h, json=ed)
                        if cr.status_code in [200, 201]:
                            ct += 1
                            et = "animated" if x.get('animated') else "static"
                            self.p(f"    ✓ {et.capitalize()}: {x.get('name', 'Unknown')}\n")
                        else:
                            fl += 1
                    else:
                        fl += 1
                    time.sleep(self.w)
                except:
                    fl += 1
            self.p(f"\n    ✓ Transferred {ct}/{len(se)} emojis\n")
            if fl > 0:
                self.p(f"    ✗ {fl} failed\n")
        except:
            self.p("\n    ✗ Emoji transfer error\n")

    def sm(self):
        self.p("\n╔════════════════════════════════════════════════════════════════╗\n")
        self.p("║                    TRANSFER SUMMARY                            ║\n")
        self.p("╚════════════════════════════════════════════════════════════════╝\n")
        if self.sd:
            self.p(f"\n            Source Server:\n")
            self.p(f"    {self.sd.get('name', 'N/A')}\n")
            self.p(f"    ID: {self.s}\n")
        if self.gd:
            self.p(f"\n    Target Server:\n")
            self.p(f"    {self.gd.get('name', 'N/A')}\n")
            self.p(f"    ID: {self.g}\n")

    def r(self):
        self.c()
        self.b()
        self.p("\n")
        si = input("            Source Server ID: ").strip()
        if not si:
            self.p("\n✗ Source ID required\n")
            return
        self.p("\n✓ Connecting to source...\n")
        if not self.ls(si):
            return
        self.p(f"✓ Connected: {self.sd.get('name', 'Unknown')}\n\n")
        gi = input("            Target Server ID (ENTER for new): ").strip()
        if gi:
            self.p("\n✓ Connecting to target...\n")
            if not self.lt(gi):
                return
            self.p(f"✓ Connected: {self.gd.get('name', 'Unknown')}\n")
        else:
            self.p("\n✓ Creating new server...\n")
            if not self.n():
                return
            time.sleep(2)
            if not self.lt(self.g):
                self.p("\n✗ Unable to verify new server\n")
                return
        self.p("\n╔════════════════════════════════════════════════════════════════╗\n")
        self.p("║                    TRANSFER CONFIGURATION                      ║\n")
        self.p("╚════════════════════════════════════════════════════════════════╝\n")
        self.p(f"\n    Source: {self.sd.get('name', 'Unknown')} ({self.s})\n")
        self.p(f"    Target: {self.gd.get('name', 'Unknown')} ({self.g})\n\n")
        cf = input("    Proceed with transfer? (yes/no): ").strip().lower()
        if cf != "yes":
            self.p("\n✗ Transfer cancelled\n")
            return
        self.p("\n✓ Starting transfer process...\n")
        self.cl()
        time.sleep(1)
        self.si()
        time.sleep(1)
        rm = self.ro()
        time.sleep(1)
        self.ch(rm)
        time.sleep(1)
        self.em()
        self.sm()
        self.p("\n✓ Transfer completed successfully!\n")

def main(t):
    x = d(t)
    x.r()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        t = input("Token: ").strip()
        main(t)