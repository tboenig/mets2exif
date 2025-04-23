# METS2EXIF – Automatische Metadaten-Extraktion und Einbettung

Dieses Python-Skript lädt METS-Dateien, extrahiert relevante Metadaten und fügt sie mithilfe von ExifTool in heruntergeladene Bilder ein.
Im Skript wird das Angebot der Digitalen Sammlungen der Staatsbibliothek zu Berlin genutzt.

## 📜 Funktionen
- **Lädt METS-Dateien** von der Staatsbibliothek Berlin mit Nutzung der PPN.
- **Extrahiert relevante Metadaten** basierend auf einer JSON-Konfiguration.
- **Lädt Bilder** von der Staatsbibliothek Berlin mit Nutzung der PPN.
- **Setzt EXIF/XMP-Metadaten** mithilfe von `ExifTool`.

## 🔧 Voraussetzungen
- Python 3.x
- `exiftool` (muss installiert sein)
- `requests` und `xml.etree.ElementTree` für das XML-Parsing

## 🚀 Installation
1. **Clone das Repository**:
   ```bash
   git clone https://github.com/tboenig/mets2exif.git
   cd mets2exif
   ```
2. **Installiere benötigte Python-Abhängigkeiten** (falls erforderlich):
   ```bash
   pip install requests
   ```
3. **Installiere ExifTool**:
   - **Linux/macOS**:
     ```bash
     sudo apt install libimage-exiftool-perl
     ```
   - **Windows**:
     Lade ExifTool von [Phil Harvey's Webseite](https://exiftool.org/) herunter und füge es dem PATH hinzu.

## 📄 Konfiguration (`config.json`)
Die Metadaten werden über eine JSON-Datei gesteuert. Beispiel:

```json
[
    {"element": ".//mods:language/mods:languageTerm", "metadata": "XMP:Language"},
    {"element": ".//mods:accessCondition[@type='use and reproduction']", "attribut": "xlink:href", "metadata": "XMP-cc:License"}
]
```

## 📄 Nutzung der Exif:Tags
Die Metadaten werden in Form von Exif:Tags angegeben. In den meisten Fällen sind das XMP Tags.
Siehe dazu: https://exiftool.org/TagNames/XMP.html


## ⚙️ Nutzung
1. **Starte das Skript** und gib die PPN (Pica Production Number) sowie die Bildnummern, die bearbeitet werden sollen an:
   ```bash
   python mets2exif.py
   ```
   **Beispiel Eingabe**
   ```
   Geben Sie die PPN ein: 192083222X
   Startbildnummer eingeben: 1
   Endbildnummer eingeben: 2
   ```

2. **Das Skript lädt Metadaten und Bilder** und bettet sie mit ExifTool ein.

## 📌 Beispiel-Workflow
- Das Skript lädt die METS-Datei anhand der angegebenen `PPN`.
- Es extrahiert Metadaten aus XML-Elementen und deren Attributen.
- Die heruntergeladenen Bilder erhalten die Metadaten als `XMP-dc, XMP-cc`-Tags.

## ❓ Fehlerbehebung
Falls das Skript nicht funktioniert:
- **Prüfe die XML-Datei** mit `ET.dump(root)`.
- **Teste ExifTool separat**:
  ```bash
  exiftool -XMP:all image.tif
  ```
- **Überprüfe die JSON-Konfiguration**, ob alle XPath-Ausdrücke korrekt sind.

## 💡 Weiterentwicklung
Falls du das Projekt erweitern willst:
- **Neue Metadaten-Felder** zur `config.json` hinzufügen.
- **Support für weitere XML-Formate** integrieren.
- **ExifTool-Befehle verbessern** (z. B. weitere XMP-Tags).

## 🏆 Lizenz
Dieses Projekt steht unter der CC-Lizenz – feel free to use and contribute!

---
🚀 Viel Erfolg mit der Metadaten-Extraktion!
```

### **Was wurde hinzugefügt?**
✅ **Beschreibung des Projekts**  
✅ **Installation & Setup für Python und ExifTool**  
✅ **Konfigurationsdetails für `config.json`**  
✅ **Schritt-für-Schritt Nutzung und Fehlerbehebung**  
✅ **Weiterentwicklungsmöglichkeiten**  

Falls du noch Anpassungen möchtest, lass es mich wissen! 🚀
