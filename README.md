# 🎿 Ski Balance Board

Ovládej lyžařskou hru fyzickým nakláněním na balanční desce.  
Telefon na desce snímá náklon → PC simuluje šipky ← → → hra reaguje.

---

## Co potřebuješ

- Windows PC se hrou (např. [Ski Challenge 14](https://ski-challenge.en.uptodown.com/windows))
- Android telefon na stejné WiFi jako PC
- [Python 3](https://www.python.org/downloads/) nainstalovaný na PC

---

## Instalace

```bash
git clone https://github.com/sallynka/ski-balance-board.git
cd ski-balance-board
```

Nebo stáhni ZIP z GitHubu → rozbal na PC.

---

## Spuštění

1. Pravým tlačítkem na **`start.bat`** → **Spustit jako správce**
2. Server vypíše přesné adresy, např.:
   ```
   1. Na telefonu otevři Chrome a jdi na:
      http://192.168.1.54:8080/phone_gyro.html
   2. Do pole zadej a klikni Připojit:
      ws://192.168.1.54:8765
   ```
3. Na telefonu otevři Chrome, jdi na první adresu
4. Zadej druhou adresu (ws://...) a klikni **Připojit**
5. Polož telefon na desku a klikni **Kalibrovat**
6. Otevři hru, klikni do okna hry
7. Klikni **▶ Start hry** na telefonu a hraj!

---

## Ovládání

- Náklon doleva → šipka ←
- Náklon doprava → šipka →
- **▶ Start hry** → začne se držet šipka ↑ (lyžař jede)
- **■ Stop** → pustí šipku ↑
- Střed (±20 %) → žádná klávesa

---

## Jak to funguje

```
📱 Telefon (gyro HTML)
    ↓ WebSocket přes WiFi
🐍 server.py na PC
    ↓ simulace kláves
🎿 Ski hra
```

Žádné drivery — stačí Python.

---

## Firewall (Avast)

Avast může blokovat připojení. Přidej pravidlo:  
**Avast → Ochrana → Firewall → Aplikace → Python → přidat pravidlo**
- Protokol: TCP
- Směr: Příchozí
- Porty: 8080, 8765
- Akce: Povolit

---

## Nastavení

**Citlivost** — slider v aplikaci na telefonu.

**Práh náklonu** — v `server.py`:
```python
THRESHOLD = 0.20   # zmenšit = citlivější, doporučujeme 0.10
DEAD_ZONE = 0.05   # oblast kolem středu kde se nic neděje
```

**Jiné klávesy** — v `server.py`:
```python
keyboard.press(Key.left)   # změň na jinou klávesu
keyboard.press(Key.right)
```
