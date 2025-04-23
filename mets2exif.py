import requests
import xml.etree.ElementTree as ET
import subprocess
import json

# Lade die Konfigurationsdatei
def load_config(config_file="config.json"):
    """Lädt die Metadaten-Konfiguration aus einer JSON-Datei."""
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Fehler: Die Konfigurationsdatei '{config_file}' wurde nicht gefunden.")
        return []

CONFIG = load_config()

def download_mets(ppn):
    """Lädt die METS-Datei basierend auf der PPN herunter."""
    url = f"https://content.staatsbibliothek-berlin.de/dc/{ppn}.mets.xml"
    response = requests.get(url)

    if response.status_code == 200:
        mets_file = f"{ppn}.mets.xml"
        with open(mets_file, "wb") as file:
            file.write(response.content)
        return mets_file
    else:
        print(f"Fehler beim Herunterladen der METS-Datei ({response.status_code}).")
        return None

def extract_metadata(mets_file):
    """Extrahiert Metadaten basierend auf der Konfiguration."""
    try:
        tree = ET.parse(mets_file)
    except ET.ParseError:
        print("Fehler: Die XML-Datei konnte nicht korrekt eingelesen werden.")
        return {}

    root = tree.getroot()

    # Namespace-Definitionen
    ns = {
        "OAI-PMH": "http://www.openarchives.org/OAI/2.0/",
        "dv": "http://dfg-viewer.de/",
        "mods": "http://www.loc.gov/mods/v3",
        "mets": "http://www.loc.gov/METS/",
        "xlink": "http://www.w3.org/1999/xlink"
    }

    metadata = {}

    for config_entry in CONFIG:
        xpath = config_entry["element"]
        elements = root.findall(xpath, ns)
        values = []

        for elem in elements:
            if elem is not None:
                if "attribut" in config_entry:
                    attrib_name = config_entry["attribut"]
                    attr_value = elem.get(f"{{{ns['xlink']}}}href") if attrib_name == "xlink:href" else elem.get(attrib_name)
                    if attr_value:
                        values.append(attr_value)
                else:
                    text_value = elem.text.strip() if elem.text else "True"
                    values.append(text_value)

        if values:
            metadata[config_entry["metadata"]] = ", ".join(filter(None, values))

    print("\nExtrahierte Metadaten:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    return metadata

def download_images(ppn, start, end):
    """Lädt Bilddateien herunter."""
    images = []

    for seite in range(start, end + 1):
        seite_str = str(seite).zfill(8)
        url = f"https://content.staatsbibliothek-berlin.de/dms/{ppn}/8000/0/{seite_str}.tif?original=true"
        response = requests.get(url)

        if response.status_code == 200:
            filename = f"{ppn}_{seite_str}.tif"
            with open(filename, "wb") as file:
                file.write(response.content)
            images.append((filename, url))
        else:
            print(f"Fehler beim Herunterladen von {url}. Status-Code: {response.status_code}")

    return images

def apply_exif_metadata(images, metadata):
    """Fügt Metadaten mit ExifTool in die Bilddateien ein."""
    for image, url in images:
        for tag, value in metadata.items():
            subprocess.run(["exiftool", f"-{tag}={value}", image], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["exiftool", f"-XMP-dc:Source={url}", image], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Metadaten erfolgreich in {image} eingefügt.")

def main():
    """Hauptprogramm: Nutzerabfragen und Verarbeitung."""
    ppn = input("Geben Sie die PPN ein: ")
    startbild = int(input("Startbildnummer eingeben: "))
    endbild = int(input("Endbildnummer eingeben: "))

    mets_file = download_mets(ppn)
    if mets_file:
        metadata = extract_metadata(mets_file)
        images = download_images(ppn, startbild, endbild)
        apply_exif_metadata(images, metadata)
        print("Metadaten erfolgreich hinzugefügt.")

if __name__ == "__main__":
    main()
