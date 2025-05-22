# METS2EXIF – Automatische METS-Metadaten-Extraktion und Einbettung in die Bild-Datei

Dieses Python-Skript lädt METS-Dateien, extrahiert relevante Metadaten und fügt sie mithilfe von ExifTool in heruntergeladene Bilder ein.
Im Skript wird das Angebot der Digitalen Sammlungen der Staatsbibliothek zu Berlin genutzt.

## 📜 Funktionen
- **Lädt die METS-Datei** vom digitalisierten Bestand mit Nutzung der PPN.
- **Extrahiert relevante Metadaten** basierend auf einer JSON-Konfiguration.
- **Lädt Bilder** vom digitalisierten Bestand mit Nutzung der PPN.
- **Lädt XMP-Tag Erweiterung** optional
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
Die Nutzung der Metadaten und der Download der TIFF-Bild-Dateien werden über eine JSON-Datei gesteuert. 

Beispiel aus dem Bestand der Digitalen Sammlungen der Staatsbibliothek zu Berlin:

```json
{
  "mets_url": "https://content.staatsbibliothek-berlin.de/dc/{ppn}.mets.xml",
  "image_url": "https://content.staatsbibliothek-berlin.de/dms/{ppn}/8000/0/{seite}.tif?original=true",
  "metadata_config": [
  {"element": ".//dv:owner", "metadata": "XMP:Contributor"},
  {"element": ".//mets:dmdSec[1]//mods:mods/mods:titleInfo/mods:title", "metadata": "XMP:Title"},
  {"element": ".//mods:name/mods:displayForm", "metadata": "XMP:Creator"},
  {"element": ".//mods:originInfo[@eventType='publication']/mods:publisher", "metadata": "XMP:Publisher"},
  {"element": ".//mods:accessCondition", "metadata": "XMP:Copyright"},
  {"element": ".//mods:classification", "metadata": "XMP:Subject"},
  {"element": ".//mods:identifier[@type='doi']", "metadata": "XMP:Identifier"},
  {"element": ".//mods:relatedItem[@type='original']/mods:recordInfo/mods:recordIdentifier", "metadata": "XMP:Relation"},
  {"element": ".//mods:language/mods:languageTerm", "metadata": "XMP:Language"},
  {"element": ".//mods:accessCondition[@type='use and reproduction']", "attribut": "xlink:href", "metadata": "XMP-cc:License"}
]
}
```
Möchten Sie den Bestand einer anderen Digitalen Sammlung nutzen?
1. Analysieren Sie die Metadaten.
2. Ermitteln Sie den Zugang zur Metadatendatei.
3. Ermitteln Sie den Zugang zu den Bilddateien.
4. Passen Sie die config JSON-Datei an.

Beispiel aus dem Bestand der Digitalen Sammlungen der Niedersächsische Staats- und Universitätsbibliothek Göttingen:

```json
{
  "mets_url": "https://gdz.sub.uni-goettingen.de/mets/PPN{ppn}.mets.xml",
  "image_url": "http://gdz.sub.uni-goettingen.de/tiff/PPN{ppn}/{seite}.tif",
  "metadata_config": [
  {"element": ".//dv:owner", "metadata": "XMP:Contributor"},
  {"element": ".//mets:dmdSec[1]//mods:mods/mods:titleInfo/mods:title", "metadata": "XMP:Title"},
  {"element": ".//mods:role[mods:roleTerm[text()='aut']]/following-sibling::mods:namePart", "metadata": "XMP:Creator"},
  {"element": ".//mods:publisher", "metadata": "XMP:Publisher"},
  {"element": ".//mods:classification", "metadata": "XMP:Subject"},
  {"element": ".//mods:identifier[@type='gbv-ppn']", "metadata": "XMP:Identifier"},
  {"element": ".//mods:identifier[@type='PPNanalog']", "metadata": "XMP:Relation"},
  {"element": ".//mets:dmdSec[1]//mods:language/mods:languageTerm", "metadata": "XMP:Language"}
]
}
```

## 📄 Nutzung der Exif:Tags
Die Metadaten werden in Form von Exif:Tags angegeben. In den meisten Fällen sind das XMP Tags.
Siehe dazu: https://exiftool.org/TagNames/XMP.html


## 📄 Nutzung der Exif:Tags Erweiterung

Mit der **.ExifTool_config**-Datei kann eine Erweiterung von Exif-Tags vorgenommen werden, um die Dokumentation von Rechten oder Lizenzen zu ermöglichen.

Diese Konfiguration definiert vorerst nur einen Tag, der mit **LibRML** korrespondiert und zur Speicherung von Lizenzinformationen dient.

### 🛠 Konfigurationsdatei

Die folgende Perl-Konfiguration ermöglicht die Nutzung des benutzerdefinierten XMP-Namespace [**LibRML**](https://librml.org):

Informationen zur Exiftool-Tag-Konfigurationsdatei siehe: https://exiftool.org/config.html
```perl
%Image::ExifTool::UserDefined = (
    'Image::ExifTool::XMP::Main' => {
        LibRML => {
            SubDirectory => { TagTable => 'Image::ExifTool::UserDefined::LibRML' },
        },
    },
);

%Image::ExifTool::UserDefined::LibRML = (
    GROUPS => { 0 => 'XMP', 1 => 'XMP-LibRML', 2 => 'Image' },
    NAMESPACE => { 'LibRML' => 'https://librml.org/LibRML/0.0.1/' },
    WRITABLE => 'string',
    AttributionURL => { Writable => 'string' },
);

require Image::ExifTool::XMP;
Image::ExifTool::XMP::RegisterNamespace(\%Image::ExifTool::UserDefined::LibRML);
```

### 📌 Hinweise zur Nutzung

1. **Einbindung in ExifTool:**  
   Die `.ExifTool_config`-Datei muss im ExifTool-Verzeichnis hinterlegt werden, damit die Erweiterung erkannt und verarbeitet wird.

2. **Tag-Nutzung:**  
   Der Tag `LibRML:AttributionURL` kann verwendet werden, um eine URL zur Attributionsdokumentation innerhalb der Metadaten zu speichern.

    Beispiel Konfiguration der **config.json**

    ```json

    {
        "mets_url": "https://content.staatsbibliothek-berlin.de/dc/{ppn}.mets.xml",
        "image_url": "https://content.staatsbibliothek-berlin.de/dms/{ppn}/8000/0/{seite}.tif?original=true",
        "metadata_config": [
        {"element": ".//mods:accessCondition[@type='use and reproduction']", "attribut": "xlink:href", "metadata": "XMP-LibRML:AttributionURL"},
    }
    ```    


3. **Kompatibilität:**  
   Diese Erweiterung nutzt das XMP-Format, wodurch eine breite Unterstützung in Bildbearbeitungssoftware und Archivierungssystemen gewährleistet wird.

---

Falls du noch Änderungen oder Ergänzungen möchtest, sag einfach Bescheid! 😊


## ⚙️ Nutzung
1. **Starte das Skript** und gib die PPN (Pica Production Number) sowie die Bildnummern, die bearbeitet werden sollen an:
   ```bash
   python mets2exif.py
   ```
   **Beispiel Eingabe**
   ```
   Geben Sie die PPN ein: 1872312616
   Startbildnummer eingeben: 6
   Endbildnummer eingeben: 7
   Geben Sie optional die Konfigurationsdatei für ExifTool ein (oder drücken Sie Enter für keine): ExifTool_config
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
