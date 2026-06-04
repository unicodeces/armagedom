import requests
import os
import random
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class ServerSettings:
    def __init__(self, t, u):
        self.t = t
        self.u = u
        self.h = {"Authorization": t}
        self.bt = ""
        self.bh = None
        self.sid = None
        self.sd = None
        self.md = None
        self.r = None
        self.ts = 0.1
        self.bid = None
        self.bis = False

    def c(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def b(self):
        from pystyle import Colors, Write, Center
        art = """
  /$$$$$$  /$$$$$$$  /$$      /$$  /$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$      /$$
 /$$__  $$| $$__  $$| $$$    /$$$ /$$__  $$ /$$__  $$| $$_____/| $$__  $$ /$$__  $$| $$$    /$$$
| $$  \ $$| $$  \ $$| $$$$  /$$$$| $$  \ $$| $$  \__/| $$      | $$  \ $$| $$  \ $$| $$$$  /$$$$
| $$$$$$$$| $$$$$$$/| $$ $$/$$ $$| $$$$$$$$| $$ /$$$$| $$$$$   | $$  | $$| $$  | $$| $$ $$/$$ $$
| $$__  $$| $$__  $$| $$  $$$| $$| $$__  $$| $$|_  $$| $$__/   | $$  | $$| $$  | $$| $$  $$$| $$
| $$  | $$| $$  \ $$| $$\  $ | $$| $$  | $$| $$  \ $$| $$      | $$  | $$| $$  | $$| $$\  $ | $$
| $$  | $$| $$  | $$| $$ \/  | $$| $$  | $$|  $$$$$$/| $$$$$$$$| $$$$$$$/|  $$$$$$/| $$ \/  | $$
|__/  |__/|__/  |__/|__/     |__/|__/  |__/ \______/ |________/|_______/  \______/ |__/     |__/
        """
        Write.Print(Center.XCenter(art), Colors.red_to_blue, interval=0.00001)

    def sb(self):
        if not self.bt:
            return False
        
        try:
            self.bh = {"Authorization": f"Bot {self.bt}"}
            r = requests.get(f"{self.u}/users/@me", headers=self.bh)
            if r.status_code == 200:
                d = r.json()
                self.bid = d.get('id')
                if d.get('bot') == True:
                    return True
            return False
        except:
            return False

    def cbs(self):
        if not self.bh or not self.sid:
            return False
        
        try:
            r = requests.get(f"{self.u}/users/@me/guilds", headers=self.bh)
            if r.status_code == 200:
                g = r.json()
                return any(x.get('id') == self.sid for x in g)
        except:
            return False

    def iba(self):
        if not self.bh or not self.bid:
            return False
        
        if self.cbs():
            return True
        
        try:
            rc = requests.get(f"{self.u}/guilds/{self.sid}/channels", headers=self.h)
            
            if rc.status_code == 200:
                ch = [c for c in rc.json() if c.get('type') == 0]
                if ch:
                    cid = ch[0]['id']
                    
                    wp = {"name": "sys"}
                    rw = requests.post(f"{self.u}/channels/{cid}/webhooks", headers=self.bh, json=wp)
                    
                    if rw.status_code in [200, 201]:
                        time.sleep(1)
                        if self.cbs():
                            from pystyle import Colors, Write
                            Write.Print("\n    ✓ Conexão estabelecida\n", Colors.red_to_blue, interval=0.0001)
                            return True
            
            from pystyle import Colors, Write
            Write.Print("\n    ✗ Falha na conexão automática\n", Colors.red_to_blue, interval=0.0001)
            return False
            
        except Exception as e:
            from pystyle import Colors, Write
            Write.Print(f"\n    ✗ Erro de conexão: {e}\n", Colors.red_to_blue, interval=0.0001)
            return False

    def rb(self):
        if not self.bis or not self.bid:
            return
        
        try:
            r = requests.delete(f"{self.u}/guilds/{self.sid}", headers=self.bh)
            if r.status_code in [200, 204]:
                from pystyle import Colors, Write
                Write.Print("\n    ✓ Desconectado\n", Colors.red_to_blue, interval=0.0001)
                self.bis = False
        except:
            pass

    def ls(self):
        from pystyle import Colors, Write
        
        sid = input("\n            ID do Servidor: ").strip()

        if not sid:
            Write.Print("\n    ✗ ID obrigatório\n", Colors.red_to_blue, interval=0.0001)
            return False

        try:
            r = requests.get(f"{self.u}/guilds/{sid}?with_counts=true", headers=self.h)
            if r.status_code != 200:
                Write.Print(f"\n    ✗ Falha ao carregar (Status: {r.status_code})\n", Colors.red_to_blue, interval=0.0001)
                return False

            self.sd = r.json()
            self.sid = sid

            ru = requests.get(f"{self.u}/users/@me", headers=self.h)
            if ru.status_code != 200:
                Write.Print("\n    ✗ Falha ao obter informações do usuário\n", Colors.red_to_blue, interval=0.0001)
                return False

            ud = ru.json()
            uid = ud.get('id')

            if self.sd.get('owner_id') == uid:
                self.r = "OWNER"
                self.md = {'user': ud, 'roles': []}
                return True

            rm = requests.get(f"{self.u}/users/@me/guilds/{sid}/member", headers=self.h)

            if rm.status_code != 200:
                rm = requests.get(f"{self.u}/guilds/{sid}/members/@me", headers=self.h)

            if rm.status_code == 200:
                self.md = rm.json()
            else:
                rg = requests.get(f"{self.u}/users/@me/guilds", headers=self.h)
                if rg.status_code == 200:
                    gs = rg.json()
                    gi = next((g for g in gs if g.get('id') == sid), None)

                    if gi:
                        self.md = {'user': ud, 'roles': []}
                        p = gi.get('permissions', 0)
                        ia = bool(int(p) & 0x8) if p else False
                        self.r = "ADMIN" if ia else "MEMBER"
                        return True

                Write.Print("\n    ✗ Falha ao obter informações de membro\n", Colors.red_to_blue, interval=0.0001)
                return False

            rl = self.md.get('roles', [])
            rr = requests.get(f"{self.u}/guilds/{self.sid}/roles", headers=self.h)

            if rr.status_code == 200:
                gr = rr.json()
                ia = False

                for rid in rl:
                    for gr_item in gr:
                        if gr_item['id'] == rid:
                            p = int(gr_item.get('permissions', 0))
                            if p & 0x8:
                                ia = True
                                break
                    if ia:
                        break

                self.r = "ADMIN" if ia else "MEMBER"
            else:
                self.r = "MEMBER"

            return True

        except Exception as e:
            Write.Print(f"\n    ✗ Erro ao carregar servidor: {e}\n", Colors.red_to_blue, interval=0.0001)
            return False

    def si(self):
        if not self.sd:
            return

        from pystyle import Colors, Write
        
        d = self.sd

        try:
            rc = requests.get(f"{self.u}/guilds/{self.sid}/channels", headers=self.h)
            tc = len(rc.json()) if rc.status_code == 200 else "N/A"
        except:
            tc = "N/A"

        iid = d.get('icon')
        au = f"https://cdn.discordapp.com/icons/{self.sid}/{iid}.png" if iid else "Sem ícone"

        try:
            ct = (int(self.sid) >> 22) + 1420070400000
            cd = datetime.fromtimestamp(ct / 1000).strftime('%d/%m/%Y %H:%M:%S UTC')
        except:
            cd = "N/A"

        mc = d.get('approximate_member_count') or d.get('member_count', 'N/A')

        bs = "INATIVO"
        if self.bt and self.bh:
            if self.cbs():
                bs = "PRONTO"
                self.bis = True
            else:
                bs = "DISPONÍVEL"

        Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("║                  INFORMAÇÕES DO SERVIDOR                       ║\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
        
        print(f"\n    Nome: {d.get('name')}")
        print(f"    ID: {self.sid}")
        print(f"    Função: {self.r}")
        print(f"    Bot: {bs}")
        print(f"    Membros: {mc}")
        print(f"    Canais: {tc}")
        print(f"    Criado: {cd}")
        print(f"    Ícone: {au}")

    def bfm(self):
        if not self.bis:
            return []
        
        try:
            m = []
            mi = set()
            a = "0"
            
            for _ in range(100):
                r = requests.get(f"{self.u}/guilds/{self.sid}/members?limit=1000&after={a}", headers=self.bh)
                
                if r.status_code != 200:
                    break
                
                ba = r.json()
                if not ba:
                    break
                
                for mb in ba:
                    mid = mb['user']['id']
                    if mid not in mi:
                        m.append(mb)
                        mi.add(mid)
                
                a = ba[-1]['user']['id']
                
                if len(ba) < 1000:
                    break
                
                time.sleep(0.5)
            
            return m
            
        except Exception as e:
            return []

    def bbm(self, m):
        if not self.bis:
            return 0, 0
        
        from pystyle import Colors, Write
        
        s = 0
        f = 0
        cui = self.md.get('user', {}).get('id')
        oi = self.sd.get('owner_id')
        
        for mb in m:
            uid = mb['user']['id']
            un = mb['user'].get('username', 'Desconhecido')
            
            if uid == cui or uid == oi or uid == self.bid:
                continue
            
            try:
                r = requests.put(
                    f"{self.u}/guilds/{self.sid}/bans/{uid}",
                    headers=self.bh,
                    json={"delete_message_days": 0}
                )
                
                if r.status_code in [200, 204]:
                    s += 1
                    Write.Print(f"    ✓ Banido: {un}\n", Colors.red_to_blue, interval=0.0001)
                else:
                    f += 1
                
                time.sleep(self.ts)
            except Exception as e:
                f += 1
        
        return s, f

    def bkm(self, m):
        if not self.bis:
            return 0, 0
        
        from pystyle import Colors, Write
        
        s = 0
        f = 0
        cui = self.md.get('user', {}).get('id')
        oi = self.sd.get('owner_id')
        
        for mb in m:
            uid = mb['user']['id']
            un = mb['user'].get('username', 'Desconhecido')
            
            if uid == cui or uid == oi or uid == self.bid:
                continue
            
            try:
                r = requests.delete(f"{self.u}/guilds/{self.sid}/members/{uid}", headers=self.bh)
                
                if r.status_code in [200, 204]:
                    s += 1
                    Write.Print(f"    ✓ Expulso: {un}\n", Colors.red_to_blue, interval=0.0001)
                else:
                    f += 1
                
                time.sleep(self.ts)
            except Exception as e:
                f += 1
        
        return s, f

    def dac(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        c = input("\n    Deletar TODOS os canais? Isso não pode ser desfeito! (sim/não): ").strip().lower()
        if c != "sim":
            Write.Print("\n    ✗ Cancelado\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/channels", headers=self.h)

            if r.status_code != 200:
                Write.Print("\n    ✗ Falha ao obter canais\n", Colors.red_to_blue, interval=0.0001)
                return

            ch = r.json()
            d = 0
            f = 0

            Write.Print(f"\n    Deletando {len(ch)} canais...\n\n", Colors.red_to_blue, interval=0.0001)

            for c in ch:
                try:
                    rd = requests.delete(f"{self.u}/channels/{c['id']}", headers=self.h)

                    if rd.status_code in [200, 204]:
                        d += 1
                        Write.Print(f"    ✓ Deletado: {c.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)
                    else:
                        f += 1
                        Write.Print(f"    ✗ Falha: {c.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)

                    time.sleep(self.ts)
                except Exception as e:
                    f += 1

            Write.Print(f"\n    Completo: {d} deletados, {f} falhas\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def dar(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        c = input("\n    Deletar todos os cargos? Isso não pode ser desfeito! (sim/não): ").strip().lower()
        if c != "sim":
            Write.Print("\n    ✗ Cancelado\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/roles", headers=self.h)

            if r.status_code != 200:
                Write.Print("\n    ✗ Falha ao obter cargos\n", Colors.red_to_blue, interval=0.0001)
                return

            ro = r.json()

            hp = -1

            if self.r != "OWNER":
                mr = self.md.get('roles', [])

                for rid in mr:
                    for rl in ro:
                        if rl['id'] == rid:
                            if rl.get('position', 0) > hp:
                                hp = rl.get('position', 0)

            d = 0
            sk = 0

            Write.Print("\n    Deletando cargos...\n\n", Colors.red_to_blue, interval=0.0001)

            for rl in ro:
                if rl['name'] == '@everyone':
                    sk += 1
                    continue

                if self.r != "OWNER" and rl.get('position', 0) >= hp:
                    sk += 1
                    continue

                try:
                    rd = requests.delete(f"{self.u}/guilds/{self.sid}/roles/{rl['id']}", headers=self.h)

                    if rd.status_code in [200, 204]:
                        d += 1
                        Write.Print(f"    ✓ Deletado: {rl.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)
                    else:
                        Write.Print(f"    ✗ Falha: {rl.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)

                    time.sleep(self.ts)
                except Exception as e:
                    pass

            Write.Print(f"\n    Completo: {d} deletados, {sk} ignorados\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def kam(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        c = input("\n    Expulsar TODOS os membros? Isso não pode ser desfeito! (sim/não): ").strip().lower()
        if c != "sim":
            Write.Print("\n    ✗ Cancelado\n", Colors.red_to_blue, interval=0.0001)
            return

        ub = False
        if self.bt and self.bh:
            if not self.bis:
                Write.Print("\n    Bot disponível mas não conectado\n", Colors.red_to_blue, interval=0.0001)
                ubi = input("    Conectar bot para melhores resultados? (sim/não): ").strip().lower()
                if ubi == "sim":
                    if self.iba():
                        self.bis = True
                        ub = True
            else:
                ub = True

        if ub and self.bis:
            Write.Print("\n    Usando método bot...\n", Colors.red_to_blue, interval=0.0001)
            m = self.bfm()
            
            if m:
                Write.Print(f"    Bot encontrou {len(m)} membros\n\n", Colors.red_to_blue, interval=0.0001)
                s, f = self.bkm(m)
                Write.Print(f"\n    Completo: {s} expulsos, {f} falhas\n", Colors.red_to_blue, interval=0.0001)
                return
            else:
                Write.Print("\n    Falha na busca do bot, usando método alternativo...\n", Colors.red_to_blue, interval=0.0001)

        Write.Print("\n    Usando método de token de usuário...\n", Colors.red_to_blue, interval=0.0001)
        self._mam("kick")

    def bam(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        c = input("\n    Banir TODOS os membros? Isso não pode ser desfeito! (sim/não): ").strip().lower()
        if c != "sim":
            Write.Print("\n    ✗ Cancelado\n", Colors.red_to_blue, interval=0.0001)
            return

        ub = False
        if self.bt and self.bh:
            if not self.bis:
                Write.Print("\n    Bot disponível mas não conectado\n", Colors.red_to_blue, interval=0.0001)
                ubi = input("    Conectar bot para melhores resultados? (sim/não): ").strip().lower()
                if ubi == "sim":
                    if self.iba():
                        self.bis = True
                        ub = True
            else:
                ub = True

        if ub and self.bis:
            Write.Print("\n    Usando método bot...\n", Colors.red_to_blue, interval=0.0001)
            m = self.bfm()
            
            if m:
                Write.Print(f"    Bot encontrou {len(m)} membros\n\n", Colors.red_to_blue, interval=0.0001)
                s, f = self.bbm(m)
                Write.Print(f"\n    Completo: {s} banidos, {f} falhas\n", Colors.red_to_blue, interval=0.0001)
                return
            else:
                Write.Print("\n    Falha na busca do bot, usando método alternativo...\n", Colors.red_to_blue, interval=0.0001)

        Write.Print("\n    Usando método de token de usuário...\n", Colors.red_to_blue, interval=0.0001)
        self._mam("ban")

    def _mam(self, a):
        from pystyle import Colors, Write
        
        try:
            m = []
            mi = set()

            Write.Print("\n    Tentando buscar membros via pesquisa...\n", Colors.red_to_blue, interval=0.0001)
            sr = requests.get(f"{self.u}/guilds/{self.sid}/members/search?query=&limit=1000", headers=self.h)

            if sr.status_code == 200:
                sm = sr.json()
                for mb in sm:
                    mid = mb['user']['id']
                    if mid not in mi:
                        m.append(mb)
                        mi.add(mid)
                Write.Print(f"    Encontrados {len(m)} membros via pesquisa\n", Colors.red_to_blue, interval=0.0001)

            if len(m) < 100:
                Write.Print("\n    Tentando buscar membros dos canais...\n", Colors.red_to_blue, interval=0.0001)
                
                cr = requests.get(f"{self.u}/guilds/{self.sid}/channels", headers=self.h)
                
                if cr.status_code == 200:
                    ch = cr.json()
                    tc = [c for c in ch if c.get('type') in [0, 5]][:10]
                    
                    for c in tc:
                        cid = c['id']
                        try:
                            mr = requests.get(f"{self.u}/channels/{cid}/messages?limit=100", headers=self.h)
                            
                            if mr.status_code == 200:
                                ms = mr.json()
                                for msg in ms:
                                    if 'author' in msg:
                                        uid = msg['author']['id']
                                        if uid not in mi:
                                            m.append({
                                                'user': {
                                                    'id': uid,
                                                    'username': msg['author'].get('username', 'Desconhecido')
                                                }
                                            })
                                            mi.add(uid)
                                
                                time.sleep(self.ts)
                        except:
                            continue
                    
                    Write.Print(f"    Total de membros encontrados: {len(m)}\n", Colors.red_to_blue, interval=0.0001)

            if len(m) == 0:
                Write.Print("\n    Impossível buscar lista de membros com token de usuário\n", Colors.red_to_blue, interval=0.0001)
                Write.Print(f"\n    Você pode inserir IDs de membros manualmente para {a} (um por linha, vazio para finalizar):\n\n", Colors.red_to_blue, interval=0.0001)

                mm = []
                while True:
                    uid = input("    ID do Membro: ").strip()
                    if not uid:
                        break
                    mm.append({'user': {'id': uid, 'username': 'Entrada Manual'}})

                if mm:
                    m = mm
                else:
                    return

            cui = self.md.get('user', {}).get('id')
            oi = self.sd.get('owner_id')

            s = 0
            f = 0
            sk = 0

            Write.Print(f"\n    Processando {len(m)} membros...\n\n", Colors.red_to_blue, interval=0.0001)

            for mb in m:
                uid = mb['user']['id']
                un = mb['user'].get('username', 'Desconhecido')

                if uid == cui or uid == oi:
                    sk += 1
                    continue

                try:
                    if a == "kick":
                        rp = requests.delete(f"{self.u}/guilds/{self.sid}/members/{uid}", headers=self.h)
                    else:
                        rp = requests.put(f"{self.u}/guilds/{self.sid}/bans/{uid}", headers=self.h)

                    if rp.status_code in [200, 204]:
                        s += 1
                        act = "Expulso" if a == "kick" else "Banido"
                        Write.Print(f"    ✓ {act}: {un}\n", Colors.red_to_blue, interval=0.0001)
                    else:
                        f += 1
                        Write.Print(f"    ✗ Falha: {un} (Status: {rp.status_code})\n", Colors.red_to_blue, interval=0.0001)

                    time.sleep(self.ts)
                except Exception as e:
                    f += 1

            act = "expulsos" if a == "kick" else "banidos"
            Write.Print(f"\n    Completo: {s} {act}, {f} falhas, {sk} ignorados\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def csn(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        nn = input("\n    Novo nome do servidor: ").strip()
        if not nn:
            Write.Print("\n    ✗ Nome não pode estar vazio\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            r = requests.patch(f"{self.u}/guilds/{self.sid}", headers=self.h, json={"name": nn})

            if r.status_code == 200:
                Write.Print(f"\n    ✓ Nome do servidor alterado para: {nn}\n", Colors.red_to_blue, interval=0.0001)
                self.sd['name'] = nn
            else:
                Write.Print(f"\n    ✗ Falha ao alterar nome (Status: {r.status_code})\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def csi(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        iu = input("\n    URL do ícone (link direto da imagem): ").strip()
        if not iu:
            Write.Print("\n    ✗ URL não pode estar vazia\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            ir = requests.get(iu)
            if ir.status_code != 200:
                Write.Print("\n    ✗ Falha ao baixar imagem\n", Colors.red_to_blue, interval=0.0001)
                return

            import base64
            idata = base64.b64encode(ir.content).decode('utf-8')

            ct = ir.headers.get('content-type', '')
            if 'png' in ct:
                fmt = 'png'
            elif 'jpeg' in ct or 'jpg' in ct:
                fmt = 'jpeg'
            elif 'gif' in ct:
                fmt = 'gif'
            else:
                Write.Print("\n    ✗ Formato de imagem não suportado\n", Colors.red_to_blue, interval=0.0001)
                return

            icond = f"data:image/{fmt};base64,{idata}"

            r = requests.patch(f"{self.u}/guilds/{self.sid}", headers=self.h, json={"icon": icond})

            if r.status_code == 200:
                Write.Print("\n    ✓ Ícone do servidor alterado com sucesso\n", Colors.red_to_blue, interval=0.0001)
            else:
                Write.Print(f"\n    ✗ Falha ao alterar ícone (Status: {r.status_code})\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def daw(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        c = input("\n    Deletar todos os webhooks? (sim/não): ").strip().lower()
        if c != "sim":
            Write.Print("\n    ✗ Cancelado\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/webhooks", headers=self.h)

            if r.status_code != 200:
                Write.Print("\n    ✗ Falha ao obter webhooks\n", Colors.red_to_blue, interval=0.0001)
                return

            wh = r.json()
            d = 0

            Write.Print(f"\n    Deletando {len(wh)} webhooks...\n\n", Colors.red_to_blue, interval=0.0001)

            for w in wh:
                try:
                    rd = requests.delete(f"{self.u}/webhooks/{w['id']}", headers=self.h)

                    if rd.status_code in [200, 204]:
                        d += 1
                        Write.Print(f"    ✓ Deletado webhook: {w.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)

                    time.sleep(self.ts)
                except:
                    pass

            Write.Print(f"\n    Deletados {d} webhooks\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def cc(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        cn = input("\n    Nome do canal: ").strip()
        if not cn:
            Write.Print("\n    ✗ Nome não pode estar vazio\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            ct = int(input("    Número de canais: ").strip())
            if ct < 1 or ct > 500:
                Write.Print("\n    ✗ Número deve estar entre 1 e 500\n", Colors.red_to_blue, interval=0.0001)
                return
        except:
            Write.Print("\n    ✗ Número inválido\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            cr = 0
            Write.Print(f"\n    Criando {ct} canais...\n\n", Colors.red_to_blue, interval=0.0001)

            for i in range(ct):
                n = f"{cn}-{random.randint(1000, 9999)}" if ct > 1 else cn

                try:
                    r = requests.post(f"{self.u}/guilds/{self.sid}/channels", headers=self.h, json={"name": n, "type": 0})

                    if r.status_code in [200, 201]:
                        cr += 1
                        Write.Print(f"    ✓ Criado: {n}\n", Colors.red_to_blue, interval=0.0001)
                    else:
                        Write.Print(f"    ✗ Falha: {n}\n", Colors.red_to_blue, interval=0.0001)

                    time.sleep(self.ts)
                except Exception as e:
                    pass

            Write.Print(f"\n    Criados {cr}/{ct} canais\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def cr(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        rn = input("\n    Nome do cargo: ").strip()
        if not rn:
            Write.Print("\n    ✗ Nome não pode estar vazio\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            ct = int(input("    Número de cargos: ").strip())
            if ct < 1 or ct > 250:
                Write.Print("\n    ✗ Número deve estar entre 1 e 250\n", Colors.red_to_blue, interval=0.0001)
                return
        except:
            Write.Print("\n    ✗ Número inválido\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            cr = 0
            Write.Print(f"\n    Criando {ct} cargos...\n\n", Colors.red_to_blue, interval=0.0001)

            for i in range(ct):
                n = f"{rn}-{random.randint(1000, 9999)}" if ct > 1 else rn

                try:
                    r = requests.post(f"{self.u}/guilds/{self.sid}/roles", headers=self.h, json={"name": n})

                    if r.status_code in [200, 201]:
                        cr += 1
                        Write.Print(f"    ✓ Criado: {n}\n", Colors.red_to_blue, interval=0.0001)
                    else:
                        Write.Print(f"    ✗ Falha: {n}\n", Colors.red_to_blue, interval=0.0001)

                    time.sleep(self.ts)
                except Exception as e:
                    pass

            Write.Print(f"\n    Criados {cr}/{ct} cargos\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def to(self):
        from pystyle import Colors, Write
        
        if self.r != "OWNER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║   ✗ APENAS O DONO DO SERVIDOR PODE TRANSFERIR PROPRIEDADE ✗  ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("║           LIMITAÇÃO DE TRANSFERÊNCIA DE PROPRIEDADE           ║\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
        
        print("\n    Embora o endpoint da API do Discord exista (PATCH /guilds/{id} com owner_id),")
        print("    o Discord bloqueia esta operação para tokens de conta de usuário para prevenir")
        print("    abuso de self-bots.")
        print("\n    Esta restrição é intencional - transferência de propriedade via API só funciona para:")
        print("    • Contas de bot que criaram o servidor elas mesmas")
        print("    • Não para contas de usuário, mesmo se você for o dono atual")
        print("\n    O Discord requer que você transfira a propriedade manualmente através do cliente:")
        print("    1. Clique com botão direito no ícone do servidor (ou clique no nome no mobile)")
        print("    2. Vá em: Configurações do Servidor > Membros")
        print("    3. Encontre o usuário para quem deseja transferir a propriedade")
        print("    4. Clique nos 3 pontos (...) ao lado do nome dele")
        print("    5. Selecione 'Transferir Propriedade'")
        print("    6. Confirme com sua senha e código 2FA se habilitado")
        print("\n    Esta é uma medida de segurança do Discord para prevenir transferências não autorizadas.")

    def ds(self):
        from pystyle import Colors, Write
        
        if self.r != "OWNER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║      ✗ APENAS O DONO DO SERVIDOR PODE DELETÁ-LO ✗            ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        c = input("\n    DELETAR SERVIDOR INTEIRO? Isso NÃO pode ser desfeito! Digite o nome do servidor para confirmar: ").strip()
        if c != self.sd.get('name'):
            Write.Print("\n    ✗ Confirmação falhou\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            r = requests.delete(f"{self.u}/guilds/{self.sid}", headers=self.h)

            if r.status_code in [200, 204]:
                Write.Print("\n    ✓ Servidor deletado com sucesso\n", Colors.red_to_blue, interval=0.0001)
                self.sid = None
                self.sd = None
                time.sleep(2)
            else:
                Write.Print(f"\n    ✗ Falha ao deletar servidor (Status: {r.status_code})\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def sac(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        msg = input("\n    Mensagem para enviar: ").strip()
        if not msg:
            Write.Print("\n    ✗ Mensagem não pode estar vazia\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            ct = int(input("    Número de vezes por canal: ").strip())
            if ct < 1 or ct > 100:
                Write.Print("\n    ✗ Número deve estar entre 1 e 100\n", Colors.red_to_blue, interval=0.0001)
                return
        except:
            Write.Print("\n    ✗ Número inválido\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/channels", headers=self.h)

            if r.status_code != 200:
                Write.Print("\n    ✗ Falha ao obter canais\n", Colors.red_to_blue, interval=0.0001)
                return

            ch = [c for c in r.json() if c.get('type') == 0]

            Write.Print(f"\n    Enviando para {len(ch)} canais...\n\n", Colors.red_to_blue, interval=0.0001)

            for c in ch:
                cid = c['id']
                cname = c.get('name', 'Desconhecido')
                sent = 0

                for i in range(ct):
                    try:
                        mr = requests.post(f"{self.u}/channels/{cid}/messages", headers=self.h, json={"content": msg})

                        if mr.status_code in [200, 201]:
                            sent += 1

                        time.sleep(self.ts)
                    except:
                        break

                Write.Print(f"    {cname}: {sent}/{ct} enviadas\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def dae(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        c = input("\n    Deletar todos os emojis? (sim/não): ").strip().lower()
        if c != "sim":
            Write.Print("\n    ✗ Cancelado\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/emojis", headers=self.h)

            if r.status_code != 200:
                Write.Print("\n    ✗ Falha ao obter emojis\n", Colors.red_to_blue, interval=0.0001)
                return

            em = r.json()
            d = 0

            Write.Print(f"\n    Deletando {len(em)} emojis...\n\n", Colors.red_to_blue, interval=0.0001)

            for e in em:
                try:
                    rd = requests.delete(f"{self.u}/guilds/{self.sid}/emojis/{e['id']}", headers=self.h)

                    if rd.status_code in [200, 204]:
                        d += 1
                        Write.Print(f"    ✓ Deletado: {e.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)

                    time.sleep(self.ts)
                except:
                    pass

            Write.Print(f"\n    Deletados {d} emojis\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"\n    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

    def j(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            return

        Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("║                      JULGAMENTO FINAL                          ║\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("\n    Isso executará múltiplas operações destrutivas\n", Colors.red_to_blue, interval=0.0001)

        tsi = input(f"\n    Tempo de espera (padrão {self.ts}): ").strip()
        if tsi:
            try:
                tsv = float(tsi)
                if tsv < 0:
                    Write.Print("\n    Tempo deve ser positivo, usando padrão\n", Colors.red_to_blue, interval=0.0001)
                    self.ts = 0.1
                else:
                    self.ts = tsv
                    Write.Print(f"\n    ✓ Tempo de espera definido para {self.ts}s\n", Colors.red_to_blue, interval=0.0001)
            except:
                Write.Print("\n    Número inválido, usando padrão\n", Colors.red_to_blue, interval=0.0001)
                self.ts = 0.1
        else:
            Write.Print(f"\n    Usando tempo de espera padrão: {self.ts}s\n", Colors.red_to_blue, interval=0.0001)

        sn = input("\n    Nome do servidor (pressione ENTER para pular): ").strip()
        if not sn:
            sn = None
            Write.Print("    ✓ Pulando alteração de nome do servidor\n", Colors.red_to_blue, interval=0.0001)

        iu = input("    URL do ícone (pressione ENTER para pular): ").strip()
        if not iu:
            iu = None
            Write.Print("    ✓ Pulando alteração de ícone\n", Colors.red_to_blue, interval=0.0001)

        cn = input("    Nome do canal: ").strip()
        if not cn:
            Write.Print("\n    ✗ Nome do canal obrigatório\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            cc = int(input("    Número de canais: ").strip())
            if cc < 1 or cc > 500:
                Write.Print("\n    ✗ Número deve estar entre 1 e 500\n", Colors.red_to_blue, interval=0.0001)
                return
        except:
            Write.Print("\n    ✗ Número inválido\n", Colors.red_to_blue, interval=0.0001)
            return

        rn = input("    Nome do cargo: ").strip()
        if not rn:
            Write.Print("\n    ✗ Nome do cargo obrigatório\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            rc = int(input("    Número de cargos: ").strip())
            if rc < 1 or rc > 250:
                Write.Print("\n    ✗ Número deve estar entre 1 e 250\n", Colors.red_to_blue, interval=0.0001)
                return
        except:
            Write.Print("\n    ✗ Número inválido\n", Colors.red_to_blue, interval=0.0001)
            return

        sm = input("    Mensagem de spam: ").strip()
        if not sm:
            Write.Print("\n    ✗ Mensagem de spam obrigatória\n", Colors.red_to_blue, interval=0.0001)
            return

        try:
            sc = int(input("    Número de mensagens por canal: ").strip())
            if sc < 1 or sc > 100:
                Write.Print("\n    ✗ Número deve estar entre 1 e 100\n", Colors.red_to_blue, interval=0.0001)
                return
        except:
            Write.Print("\n    ✗ Número inválido\n", Colors.red_to_blue, interval=0.0001)
            return

        Write.Print("\n    [1] Banir Membros\n", Colors.red_to_blue, interval=0.0001)
        Write.Print("    [2] Expulsar Membros\n", Colors.red_to_blue, interval=0.0001)
        Write.Print("    [3] Pular\n", Colors.red_to_blue, interval=0.0001)
        ma = input("\n    Selecione ação: ").strip()
        
        if ma not in ["1", "2", "3"]:
            Write.Print("\n    Opção inválida, pulando ações de membros\n", Colors.red_to_blue, interval=0.0001)
            ma = "3"

        Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("║                   CONFIRMAÇÃO FINAL                            ║\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
        
        print(f"\n    Nome do servidor: {sn if sn else 'Sem alteração'}")
        print(f"    Ícone: {iu if iu else 'Sem alteração'}")
        print(f"    Canais: {cc}x '{cn}'")
        print(f"    Cargos: {rc}x '{rn}'")
        print(f"    Spam: '{sm}' x{sc} por canal")
        print(f"    Membros: {'Banir' if ma == '1' else 'Expulsar' if ma == '2' else 'Pular'}")

        input("\n    Pressione ENTER para iniciar Julgamento...")

        Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("║                  INICIANDO JULGAMENTO...                       ║\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)

        Write.Print("\n[ETAPA 1/10] Deletando todos os canais...\n", Colors.red_to_blue, interval=0.0001)
        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/channels", headers=self.h)
            if r.status_code == 200:
                ch = r.json()
                for c in ch:
                    try:
                        requests.delete(f"{self.u}/channels/{c['id']}", headers=self.h)
                        Write.Print(f"    ✓ Deletado: {c.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)
                        time.sleep(self.ts)
                    except:
                        pass
        except Exception as e:
            Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

        Write.Print("\n[ETAPA 2/10] Deletando todos os cargos...\n", Colors.red_to_blue, interval=0.0001)
        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/roles", headers=self.h)
            if r.status_code == 200:
                ro = r.json()
                hp = -1

                if self.r != "OWNER":
                    mr = self.md.get('roles', [])
                    for rid in mr:
                        for rl in ro:
                            if rl['id'] == rid:
                                if rl.get('position', 0) > hp:
                                    hp = rl.get('position', 0)

                for rl in ro:
                    if rl['name'] == '@everyone':
                        continue
                    if self.r != "OWNER" and rl.get('position', 0) >= hp:
                        continue
                    try:
                        requests.delete(f"{self.u}/guilds/{self.sid}/roles/{rl['id']}", headers=self.h)
                        Write.Print(f"    ✓ Deletado: {rl.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)
                        time.sleep(self.ts)
                    except:
                        pass
        except Exception as e:
            Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

        Write.Print("\n[ETAPA 3/10] Deletando todos os emojis...\n", Colors.red_to_blue, interval=0.0001)
        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/emojis", headers=self.h)
            if r.status_code == 200:
                em = r.json()
                for e in em:
                    try:
                        requests.delete(f"{self.u}/guilds/{self.sid}/emojis/{e['id']}", headers=self.h)
                        Write.Print(f"    ✓ Deletado: {e.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)
                        time.sleep(self.ts)
                    except:
                        pass
        except Exception as e:
            Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

        Write.Print("\n[ETAPA 4/10] Deletando todos os webhooks...\n", Colors.red_to_blue, interval=0.0001)
        try:
            r = requests.get(f"{self.u}/guilds/{self.sid}/webhooks", headers=self.h)
            if r.status_code == 200:
                wh = r.json()
                for w in wh:
                    try:
                        requests.delete(f"{self.u}/webhooks/{w['id']}", headers=self.h)
                        Write.Print(f"    ✓ Deletado: {w.get('name', 'Desconhecido')}\n", Colors.red_to_blue, interval=0.0001)
                        time.sleep(self.ts)
                    except:
                        pass
        except Exception as e:
            Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

        if sn:
            Write.Print(f"\n[ETAPA 5/10] Alterando nome do servidor para '{sn}'...\n", Colors.red_to_blue, interval=0.0001)
            try:
                r = requests.patch(f"{self.u}/guilds/{self.sid}", headers=self.h, json={"name": sn})
                if r.status_code == 200:
                    Write.Print("    ✓ Nome do servidor alterado\n", Colors.red_to_blue, interval=0.0001)
                    self.sd['name'] = sn
                else:
                    Write.Print("    ✗ Falha ao alterar nome\n", Colors.red_to_blue, interval=0.0001)
            except Exception as e:
                Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)
        else:
            Write.Print("\n[ETAPA 5/10] Pulando alteração de nome do servidor...\n", Colors.red_to_blue, interval=0.0001)

        if iu:
            Write.Print("\n[ETAPA 6/10] Alterando ícone do servidor...\n", Colors.red_to_blue, interval=0.0001)
            try:
                import base64
                ir = requests.get(iu)
                if ir.status_code == 200:
                    idata = base64.b64encode(ir.content).decode('utf-8')
                    ct = ir.headers.get('content-type', '')
                    if 'png' in ct:
                        fmt = 'png'
                    elif 'jpeg' in ct or 'jpg' in ct:
                        fmt = 'jpeg'
                    elif 'gif' in ct:
                        fmt = 'gif'
                    else:
                        fmt = 'png'

                    icond = f"data:image/{fmt};base64,{idata}"
                    r = requests.patch(f"{self.u}/guilds/{self.sid}", headers=self.h, json={"icon": icond})
                    if r.status_code == 200:
                        Write.Print("    ✓ Ícone do servidor alterado\n", Colors.red_to_blue, interval=0.0001)
                    else:
                        Write.Print("    ✗ Falha ao alterar ícone\n", Colors.red_to_blue, interval=0.0001)
                else:
                    Write.Print("    ✗ Falha ao baixar imagem\n", Colors.red_to_blue, interval=0.0001)
            except Exception as e:
                Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)
        else:
            Write.Print("\n[ETAPA 6/10] Pulando alteração de ícone do servidor...\n", Colors.red_to_blue, interval=0.0001)

        Write.Print(f"\n[ETAPA 7/10] Criando {rc} cargos...\n", Colors.red_to_blue, interval=0.0001)
        try:
            for i in range(rc):
                n = f"{rn}-{random.randint(1000, 9999)}" if rc > 1 else rn
                try:
                    r = requests.post(f"{self.u}/guilds/{self.sid}/roles", headers=self.h, json={"name": n})
                    if r.status_code in [200, 201]:
                        Write.Print(f"    ✓ Criado: {n}\n", Colors.red_to_blue, interval=0.0001)
                    time.sleep(self.ts)
                except:
                    pass
        except Exception as e:
            Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

        Write.Print(f"\n[ETAPA 8/10] Criando {cc} canais...\n", Colors.red_to_blue, interval=0.0001)
        cch = []
        try:
            for i in range(cc):
                n = f"{cn}-{random.randint(1000, 9999)}" if cc > 1 else cn
                try:
                    r = requests.post(f"{self.u}/guilds/{self.sid}/channels", headers=self.h, json={"name": n, "type": 0})
                    if r.status_code in [200, 201]:
                        cd = r.json()
                        cch.append(cd)
                        Write.Print(f"    ✓ Criado: {n}\n", Colors.red_to_blue, interval=0.0001)
                    time.sleep(self.ts)
                except:
                    pass
        except Exception as e:
            Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

        Write.Print(f"\n[ETAPA 9/10] Enviando spam em {len(cch)} canais...\n", Colors.red_to_blue, interval=0.0001)
        try:
            for c in cch:
                cid = c['id']
                cnd = c.get('name', 'Desconhecido')
                sent = 0
                for i in range(sc):
                    try:
                        mr = requests.post(f"{self.u}/channels/{cid}/messages", headers=self.h, json={"content": sm})
                        if mr.status_code in [200, 201]:
                            sent += 1
                        time.sleep(self.ts)
                    except:
                        break
                Write.Print(f"    {cnd}: {sent}/{sc} enviadas\n", Colors.red_to_blue, interval=0.0001)
        except Exception as e:
            Write.Print(f"    ✗ Erro: {e}\n", Colors.red_to_blue, interval=0.0001)

        if ma in ["1", "2"]:
            an = "Banindo" if ma == "1" else "Expulsando"
            Write.Print(f"\n[ETAPA 10/10] {an} membros...\n", Colors.red_to_blue, interval=0.0001)
            
            ub = False
            if self.bt and self.bh:
                if not self.bis:
                    Write.Print("    Bot disponível, tentando conectar...\n", Colors.red_to_blue, interval=0.0001)
                    if self.iba():
                        self.bis = True
                        ub = True
                else:
                    ub = True

            if ub and self.bis:
                Write.Print("    Usando método bot...\n", Colors.red_to_blue, interval=0.0001)
                m = self.bfm()
                
                if m:
                    Write.Print(f"    Bot encontrou {len(m)} membros\n", Colors.red_to_blue, interval=0.0001)
                    if ma == "1":
                        s, f = self.bbm(m)
                        Write.Print(f"\n    Bot baniu {s} membros, {f} falhas\n", Colors.red_to_blue, interval=0.0001)
                    else:
                        s, f = self.bkm(m)
                        Write.Print(f"\n    Bot expulsou {s} membros, {f} falhas\n", Colors.red_to_blue, interval=0.0001)
                else:
                    Write.Print("    Falha na busca do bot, usando alternativo...\n", Colors.red_to_blue, interval=0.0001)
                    self._mam("ban" if ma == "1" else "kick")
            else:
                Write.Print("    Usando método de token de usuário...\n", Colors.red_to_blue, interval=0.0001)
                self._mam("ban" if ma == "1" else "kick")
                
            if self.bis:
                self.rb()
        else:
            Write.Print("\n[ETAPA 10/10] Pulando ações de membros...\n", Colors.red_to_blue, interval=0.0001)

        Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("║                   JULGAMENTO COMPLETO                          ║\n", Colors.red_to_blue, interval=0.00001)
        Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)

    def sm(self):
        from pystyle import Colors, Write
        
        if self.r == "MEMBER":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║           ✗ PERMISSÕES INSUFICIENTES ✗                        ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            
            Write.Print("\n    [0] Voltar ao menu principal\n\n", Colors.red_to_blue, interval=0.0001)
        elif self.r == "ADMIN":
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║                     MENU DE CONFIGURAÇÕES                      ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            
            Write.Print("\n    [1] Deletar Canais          [2] Deletar Cargos\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [3] Expulsar Membros        [4] Banir Membros\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [5] Alterar Nome            [6] Alterar Ícone\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [7] Deletar Webhooks        [8] Criar Canais\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [9] Criar Cargos            [10] Enviar Spam\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [11] Deletar Emojis         [14] JULGAMENTO\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [0] Voltar\n\n", Colors.red_to_blue, interval=0.0001)
        else:
            Write.Print("\n╔════════════════════════════════════════════════════════════════╗\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("║                     MENU DE CONFIGURAÇÕES                      ║\n", Colors.red_to_blue, interval=0.00001)
            Write.Print("╚════════════════════════════════════════════════════════════════╝\n", Colors.red_to_blue, interval=0.00001)
            
            Write.Print("\n    [1] Deletar Canais          [2] Deletar Cargos\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [3] Expulsar Membros        [4] Banir Membros\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [5] Alterar Nome            [6] Alterar Ícone\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [7] Deletar Webhooks        [8] Criar Canais\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [9] Criar Cargos            [10] Enviar Spam\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [11] Deletar Emojis         [12] Transferir Dono\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [13] DELETAR SERVIDOR       [14] JULGAMENTO\n", Colors.red_to_blue, interval=0.0001)
            Write.Print("    [0] Voltar\n\n", Colors.red_to_blue, interval=0.0001)

    def run(self):
        self.c()
        self.b()
        
        if self.bt:
            self.sb()

        if not self.ls():
            return

        self.si()

        while True:
            if not self.sd:
                break

            self.sm()
            ch = input("    Selecione: ").strip()

            if ch == "0":
                if self.bis:
                    self.rb()
                break
            elif self.r == "MEMBER":
                from pystyle import Colors, Write
                Write.Print("    ✗ Opção inválida\n", Colors.red_to_blue, interval=0.0001)
            elif ch == "1":
                self.dac()
            elif ch == "2":
                self.dar()
            elif ch == "3":
                self.kam()
            elif ch == "4":
                self.bam()
            elif ch == "5":
                self.csn()
            elif ch == "6":
                self.csi()
            elif ch == "7":
                self.daw()
            elif ch == "8":
                self.cc()
            elif ch == "9":
                self.cr()
            elif ch == "10":
                self.sac()
            elif ch == "11":
                self.dae()
            elif ch == "12" and self.r == "OWNER":
                self.to()
            elif ch == "13" and self.r == "OWNER":
                self.ds()
            elif ch == "14":
                self.j()
            else:
                from pystyle import Colors, Write
                Write.Print("    ✗ Opção inválida\n", Colors.red_to_blue, interval=0.0001)

            if self.sd:
                input("\n    Pressione ENTER para continuar...")
                self.c()
                self.b()
                self.si()

if __name__ == "__main__":
    TOKEN = ""
    BASE_URL = "https://discord.com/api/v9"
    
    settings = ServerSettings(TOKEN, BASE_URL)
    settings.run()