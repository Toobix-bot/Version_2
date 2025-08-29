# 🔐 TOOBIX API KEY SICHERHEIT - ANLEITUNG

## 🎯 **SICHERE API KEY VERWALTUNG**

### ✅ **Option 1: .env Datei (EMPFOHLEN)**

#### **1. Erstelle .env Datei:**
```bash
# Im Toobix-Verzeichnis
copy .env.example .env
```

#### **2. Bearbeite .env mit deinen Keys:**
```bash
# Öffne .env in Notepad/Editor
notepad .env
```

#### **3. Füge echten API Key ein:**
```env
# In der .env Datei:
GROQ_API_KEY=gsk_your_real_groq_api_key_here_123456789
OLLAMA_MODEL=gemma3:4b
OLLAMA_URL=http://localhost:11434
```

#### **4. .env ist automatisch in .gitignore!**
```gitignore
# .env Dateien werden NIEMALS committed!
.env
.env.local
.env.production
```

---

### ✅ **Option 2: Windows Umgebungsvariablen**

#### **Permanent (System-weit):**
```powershell
# PowerShell als Administrator:
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", "your_key_here", "User")
```

#### **Temporär (nur aktuelle Session):**
```powershell
# PowerShell:
$env:GROQ_API_KEY = "your_key_here"
python main.py
```

#### **CMD Version:**
```cmd
# Temporär in CMD:
set GROQ_API_KEY=your_key_here
python main.py
```

---

### ✅ **Option 3: Sichere Key-Datei (Lokal)**

#### **1. Erstelle sichere key-Datei:**
```bash
# Erstelle Ordner außerhalb von Git
mkdir C:\ToobixKeys
```

#### **2. Sichere Datei erstellen:**
```json
# C:\ToobixKeys\api_keys.json
{
    "groq_api_key": "your_real_key_here",
    "openai_api_key": "optional_openai_key",
    "anthropic_api_key": "optional_claude_key"
}
```

#### **3. Toobix konfigurieren:**
```python
# In settings.py würde dann stehen:
import json
import os

key_file = "C:/ToobixKeys/api_keys.json"
if os.path.exists(key_file):
    with open(key_file) as f:
        keys = json.load(f)
    GROQ_API_KEY = keys.get("groq_api_key", "")
```

---

### ✅ **Option 4: Windows Credential Manager**

#### **1. Key im Credential Manager speichern:**
```powershell
# PowerShell:
cmdkey /add:"ToobixGroqAPI" /user:"toobix" /pass:"your_api_key_here"
```

#### **2. Key aus Credential Manager lesen:**
```python
import subprocess

def get_stored_key(target):
    try:
        result = subprocess.run([
            'cmdkey', '/list:' + target
        ], capture_output=True, text=True)
        # Parse gespeicherten Key...
        return parsed_key
    except:
        return None
```

---

## 🛡️ **SICHERHEITS-BEST-PRACTICES**

### ✅ **DO's:**
- ✅ .env Datei für lokale Entwicklung
- ✅ Umgebungsvariablen für Production
- ✅ Keys niemals in Git commiten
- ✅ .gitignore für .env konfiguriert
- ✅ Unterschiedliche Keys für Test/Production

### ❌ **DON'Ts:**
- ❌ API Keys direkt im Code
- ❌ Keys in Git-Repository
- ❌ Keys in Screenshots/Logs
- ❌ Keys in öffentlichen Issues
- ❌ Keys per E-Mail/Chat senden

---

## 🚀 **TOOBIX SETUP-ANLEITUNG**

### **Schritt 1: .env Datei erstellen**
```powershell
# Im Toobix-Verzeichnis
cd "C:\GPT\Version_2"
copy .env.example .env
notepad .env
```

### **Schritt 2: Groq API Key holen**
1. Gehe zu: https://console.groq.com/
2. Erstelle Account / Login
3. Gehe zu "API Keys"
4. Erstelle neuen Key
5. Kopiere Key (beginnt mit "gsk_...")

### **Schritt 3: Key in .env eintragen**
```env
# In .env Datei:
GROQ_API_KEY=gsk_your_copied_key_here
```

### **Schritt 4: Toobix starten**
```powershell
python main.py
```

### **Ergebnis:**
```
✅ Ollama verfügbar - Model: gemma3:4b
✅ Groq Cloud-Backup verfügbar
🌟 Hybrid AI System aktiv!
```

---

## 🔍 **KEY VALIDIERUNG TESTEN**

### **Test ohne Key:**
```powershell
python -c "import os; print('Key Status:', 'GESETZT' if os.environ.get('GROQ_API_KEY') else 'FEHLT')"
```

### **Test mit Toobix:**
```powershell
python -c "
from toobix.config.settings import Settings
s = Settings()
config = s.get_ai_config()
print('Groq verfügbar:', bool(config['groq_api_key']))
"
```

### **Live API Test:**
```powershell
python -c "
import os
from groq import Groq
try:
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
    response = client.chat.completions.create(
        messages=[{'role': 'user', 'content': 'Test OK?'}],
        model='llama-3.1-8b-instant',
        max_tokens=5
    )
    print('✅ API funktioniert:', response.choices[0].message.content)
except Exception as e:
    print('❌ API Fehler:', str(e))
"
```

---

## 🎯 **EMPFEHLUNG FÜR DICH**

**Für Toobix verwende die .env Methode:**

1. **Schnell & Sicher**: `.env` Datei
2. **Automatisch geschützt**: Bereits in `.gitignore`
3. **Einfach zu verwalten**: Ein File für alle Keys
4. **Lokal**: Keys bleiben auf deinem PC

**Commands:**
```powershell
cd "C:\GPT\Version_2"
copy .env.example .env
notepad .env
# Trage echten API Key ein
python main.py
```

**So bleiben deine API Keys sicher und privat! 🔐**
