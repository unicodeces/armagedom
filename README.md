# Armagedom

<div align="center">

![Banner](https://img.shields.io/badge/Discord-Advanced%20Account%20Manager-blueviolet?style=flat-square&logo=discord)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

**Ferramenta avançada para análise e gerenciamento de contas Discord**

[Recursos](#-recursos) • [Instalação](#-instalação) • [Uso](#-uso) • [Funcionalidades](#-funcionalidades) • [Créditos](#-créditos)

</div>

---

## 📋 Sobre

**Armagedom** é uma ferramenta poderosa e intuitiva desenvolvida em Python para análise, monitoramento e gerenciamento completo de contas Discord. Com uma interface visual sofisticada e suporte para múltiplas operações avançadas, oferece funcionalidades desde simples consultas até automações complexas.

### ✨ Destaques

- 🔐 Validação e autenticação de tokens Discord
- 📊 Análise detalhada de contas e dados de usuário
- 🖥️ Gerenciamento de servidores com clonagem avançada
- 🤖 Injeção e automação de bots
- 🌐 Login automático via navegador com Selenium
- 📁 Geração de relatórios completos exportáveis
- 🎨 Interface visual colorida e responsiva
- ⚡ Operações multi-thread para melhor performance

---

## 🚀 Recursos

### Consulta de Dados
- **Informações da Conta**: ID, username, email, status de verificação, MFA
- **Servidores**: Lista completa com roles, permissões, data de entrada
- **Conexões Externas**: Spotify, Twitch, YouTube e outras integrações
- **Métodos de Pagamento**: Cartões registrados (últimos dígitos)
- **Status Nitro**: Tipo de assinatura e detalhes premium
- **Lista de Amigos**: Contatos adicionados na conta
- **Sessões Ativas**: Dispositivos conectados e localizações
- **Informações de Segurança**: Autenticação, flags, status de conta

### Funcionalidades Avançadas
- **Geração de Relatórios**: Exportação completa em arquivo `.txt`
- **Clonagem de Servidores**: Duplica estrutura, canais e configurações
- **Browser Auto-Login**: Automação de login via navegador com injeção de token
- **Injeção de Bots**: Autorização automática de bots em servidores
- **Gerenciamento de Configurações**: Ajustes avançados de servidor
- **Múltiplos Tokens**: Troca rápida entre contas

---

## 💻 Requisitos

- **Python**: 3.8 ou superior
- **Sistema Operacional**: Windows, Linux ou macOS
- **Memória**: 512MB mínimo
- **Navegadores**: Chrome, Firefox, Edge ou Brave (para funcionalidades de browser)

---

## 📦 Instalação

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/unicodeces/armagedom.git
cd armagedom
```

### 2️⃣ Crie um Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Execute a Ferramenta

```bash
python main.py
```

---

## 🎯 Uso

### Inicialização Básica

```bash
python main.py
```

A ferramenta exibirá um banner e solicitará um token Discord válido. Após autenticação bem-sucedida, você terá acesso ao menu principal.

### Obtendo um Token Discord

**Aviso**: Tokens são credenciais sensíveis. Nunca compartilhe seu token.

1. Abra Discord no navegador
2. Pressione `F12` para abrir DevTools
3. Vá para a aba **Console**
4. Execute: `document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token`
5. Copie o valor exibido

### Menu Principal

```
[1]  Servidores            [2]  Conexões Externas
[3]  Métodos de Pagamento  [4]  Status Nitro
[5]  Lista de Amigos       [6]  Sessões Ativas
[7]  Informações de Seg.   [8]  Relatório Completo
[9]  Salvar em Arquivo     [10] Configurações
[11] Clonar Servidor       [12] Browser Login
[13] Alterar Token         [14] Adicionar Bot
[0]  Sair
```

### Exemplos de Uso

#### Visualizar Informações da Conta

```
>>> Token: seu_token_aqui
>>> Select: 1
```

#### Gerar Relatório Completo

```
>>> Select: 9
✓ Report saved to: report_2024_01_15_10_30_45.txt
```

#### Browser Auto-Login

```
>>> Select: 12
✓ Browser launched
✓ Token injected
✓ Login successful
```

#### Adicionar Bot a Servidor

```
>>> Select: 14
Enter the bot authorization URL
Example: https://discord.com/oauth2/authorize?client_id=...
>>> Bot URL: https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID
```

---

## 🔧 Funcionalidades Detalhadas

### 📊 Análise de Dados

A ferramenta extrai informações em tempo real via Discord API v10:

- Perfil completo do usuário
- Historialicidade de servidores e permissões
- Integração de contas externas
- Dados de faturamento e pagamento
- Status de premium/Nitro
- Log de atividades e sessões

### 🤖 Automação de Navegador

Utiliza Selenium para:

- Detectar navegador padrão automaticamente
- Injetar tokens via localStorage
- Navegar por URLs OAuth automaticamente
- Suportar Chrome, Firefox, Edge

### 📁 Geração de Relatórios

Relatórios incluem:

```
ACCOUNT INFORMATION
- ID, Username, Global Name
- Email, Verified Status, MFA
- Avatar URL, Account Flags

SERVERS
- Server name, ID, Role
- Permissions, Join Date

CONNECTIONS
- Type (Spotify, Twitch, etc)
- Connected username

PAYMENT METHODS
- Brand, Last 4 digits

[... e mais informações ...]
```

---

## 📂 Estrutura do Projeto

```
armagedom/
├── main.py              # Arquivo principal com lógica principal
├── config.py            # Gerenciador de configurações de servidor
├── features.py          # Funcionalidades avançadas (clonagem)
├── trial.py             # Browser auto-login com Selenium
├── bot_injection.py     # Injeção e automação de bots
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação
```

---

## 🔑 Dependências Principais

| Biblioteca | Versão | Descrição |
|-----------|--------|-----------|
| `requests` | 2.28.0+ | HTTP requests para Discord API |
| `pystyle` | 2.8.0+ | Renderização visual colorida |
| `selenium` | 4.0.0+ | Automação de navegador |
| `webdriver-manager` | 3.8.0+ | Gerenciamento de drivers |

**Instalação via requirements.txt**:

```bash
pip install requests>=2.28.0
pip install pystyle>=2.8.0
pip install selenium>=4.0.0
pip install webdriver-manager>=3.8.0
```

---

## ⚙️ Configuração Avançada

### Variáveis de Ambiente

Você pode configurar comportamentos padrão via variáveis de ambiente:

```bash
# Windows
set DISCORD_API_VERSION=v10
set ARMAGEDOM_TIMEOUT=30

# Linux/macOS
export DISCORD_API_VERSION=v10
export ARMAGEDOM_TIMEOUT=30
```

### Preferências de Navegador

O sistema detecta automaticamente o navegador padrão, mas você pode forçar:

```python
# No código, ao usar browser login:
from trial import DiscordBrowserLogin
login = DiscordBrowserLogin(token)
login.ah('firefox')  # Force Firefox
```

---

## 🛡️ Segurança

### ⚠️ Avisos Importantes

1. **Tokens Sensíveis**: Nunca compartilhe seu token Discord
2. **Uso Responsável**: Respeite os Termos de Serviço do Discord
3. **Consentimento**: Use apenas em contas que você possui
4. **Risco de Ban**: O Discord pode banir contas por uso inadequado
5. **Dados Pessoais**: A ferramenta pode acessar dados sensíveis

### Boas Práticas

```bash
# Nunca commite tokens
echo "*.token" >> .gitignore

# Use variáveis de ambiente para credenciais
set TOKEN=seu_token_seguro
python main.py
```

---

## 📊 Exemplos de Saída

### Informações da Conta

```
╔════════════════════════════════════════════════════════════════╗
║                    ACCOUNT INFORMATION                         ║
╚════════════════════════════════════════════════════════════════╝

    ID: 123456789012345678
    Username: usuario
    Global Name: Usuário Real
    Email: usuario@example.com
    Verified: True
    MFA: True
    Avatar: https://cdn.discordapp.com/avatars/...
```

### Lista de Servidores

```
╔════════════════════════════════════════════════════════════════╗
║                    SERVERS (45)                                ║
╚════════════════════════════════════════════════════════════════╝

    Servidor Principal
    ID: 987654321098765432 | Role: OWNER | Joined: 15/01/2023 10:30:45 UTC

    Servidor Dev
    ID: 876543210987654321 | Role: ADMIN | Joined: 20/06/2023 14:22:10 UTC
```

---

## 🐛 Troubleshooting

### Erro: "Invalid token"

- Verifique se o token está correto
- Tokens expiram após logout
- Gere um novo token do Discord

### Erro: "Browser initialization failed"

- Instale um navegador compatível (Chrome, Firefox, Edge)
- Execute: `pip install webdriver-manager --upgrade`
- No Linux, instale: `sudo apt-get install chromium-browser`

### Erro: "Failed to retrieve guilds"

- Verifique conexão com internet
- Confirme que o token está ativo
- Discord API pode estar indisponível

### Selenium/WebDriver Issues

```bash
# Limpe cache e reinstale drivers
pip uninstall webdriver-manager -y
pip install webdriver-manager --upgrade
```

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](./LICENSE) para detalhes completos.

```
MIT License © 2024 Unicodeces
```

---

## 👨‍💻 Créditos

**Desenvolvido por**: [Unicodeces](https://github.com/unicodeces)

**Repositório**: [github.com/unicodeces/armagedom](https://github.com/unicodeces/armagedom)

### Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

Encontrou um bug ou tem sugestões?

- **Issues**: [Abra uma issue](https://github.com/unicodeces/armagedom/issues)
- **Discussões**: [Participe das discussões](https://github.com/unicodeces/armagedom/discussions)

---

## ⚡ Changelog

### v1.0.0 (Atual)
- ✅ Análise completa de conta
- ✅ Gerenciamento de servidores
- ✅ Browser auto-login
- ✅ Injeção de bots
- ✅ Geração de relatórios

---

<div align="center">

**[⬆ Voltar ao topo](#armagedom)**

Feito com ❤️ por [Unicodeces](https://github.com/unicodeces)

</div>
