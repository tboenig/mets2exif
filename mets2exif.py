import requests
from lxml import etree
import subprocess
import json

# Lade die Konfigurationsdatei
def load_config(config_file="config.json"):
    """Lädt die Konfigurationsdatei aus einer JSON-Datei."""
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Fehler: Die Konfigurationsdatei '{config_file}' wurde nicht gefunden.")
        return {}

CONFIG = load_config()

def download_mets(ppn):
    """Lädt die METS-Datei basierend auf der PPN und der URL aus der Konfiguration herunter."""
    base_url = CONFIG.get("mets_url", "")
    if not base_url:
        print("Fehler: Basis-URL für METS ist in der Konfigurationsdatei nicht definiert.")
        return None

    url = base_url.replace("{ppn}", ppn)
    response = requests.get(url)

    if response.status_code == 200:
        mets_file = f"{ppn}.mets.xml"
        with open(mets_file, "wb") as file:
            file.write(response.content)
        return mets_file
    else:
        print(f"Fehler beim Herunterladen der METS-Datei ({response.status_code}).")
        return None

def download_images(ppn, start, end):
    """Lädt Bilddateien herunter, basierend auf der URL aus der Konfiguration."""
    base_url = CONFIG.get("image_url", "")
    if not base_url:
        print("Fehler: Basis-URL für Bilder ist in der Konfigurationsdatei nicht definiert.")
        return []

    images = []
    for seite in range(start, end + 1):
        seite_str = str(seite).zfill(8)
        url = base_url.replace("{ppn}", ppn).replace("{seite}", seite_str)
        response = requests.get(url)

        if response.status_code == 200:
            filename = f"{ppn}_{seite_str}.tif"
            with open(filename, "wb") as file:
                file.write(response.content)
            images.append((filename, url))
        else:
            print(f"Fehler beim Herunterladen von {url}. Status-Code: {response.status_code}")

    return images

def extract_metadata(mets_file):
    """Extrahiert Metadaten basierend auf der Konfiguration."""
    try:
        tree = etree.parse(mets_file)

        # Namespace-Definitionen
        namespaces = {
            "OAI-PMH": "http://www.openarchives.org/OAI/2.0/",
            "dv": "http://dfg-viewer.de/",
            "mods": "http://www.loc.gov/mods/v3",
            "mets": "http://www.loc.gov/METS/",
            "xlink": "http://www.w3.org/1999/xlink"
        }

        metadata = {}
        for config_entry in CONFIG.get("metadata_config", []):
            xpath = config_entry["element"]
            elements = tree.xpath(xpath, namespaces=namespaces)
            values = []

            for elem in elements:
                if elem is not None:
                    if "attribut" in config_entry:
                        attrib_name = config_entry["attribut"]
                        attr_value = elem.get(f"{{{namespaces['xlink']}}}href") if attrib_name == "xlink:href" else elem.get(attrib_name)
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

    except Exception as e:
        print(f"Fehler beim Extrahieren der Metadaten: {e}")
        return {}

def apply_exif_metadata(images, metadata, config=None):
    """Fügt Metadaten mit ExifTool in einem einzigen Befehl in die Bilddateien ein."""
    for image, url in images:
        cmd = ["exiftool"]

        # Falls eine Konfigurationsdatei angegeben ist
        if config:
            cmd.append(f"-config .{config}")

        # Alle Metadaten in einem einzigen Aufruf hinzufügen
        for tag, value in metadata.items():
            cmd.append(f'-{tag}="{value}"')

        # Datei hinzufügen
        cmd.append(image)

        # ExifTool ausführen
        #print(f'Executing: {" ".join(cmd)}')
        subprocess.run(" ".join(cmd), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


        print(f"Metadaten erfolgreich in {image} eingefügt.")            

def main():
    """Hauptprogramm: Nutzerabfragen und Verarbeitung."""
    ppn = input("Geben Sie die PPN ein: ")
    startbild = int(input("Startbildnummer eingeben: "))
    endbild = int(input("Endbildnummer eingeben: "))
    config_file = input("Geben Sie optional die Konfigurationsdatei für ExifTool ein (oder drücken Sie Enter für keine): ")

    mets_file = download_mets(ppn)
    if mets_file:
        metadata = extract_metadata(mets_file)
        images = download_images(ppn, startbild, endbild)
        apply_exif_metadata(images, metadata, config_file if config_file else None)
        print("Metadaten erfolgreich hinzugefügt.")

if __name__ == "__main__":
    main()
