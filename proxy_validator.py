import re

# Expression régulière pour valider le format de la ligne (url:port) dans le fichier proxy
validation_pattern = re.compile(r'^\s*proxy\s*=\s*(?:(\w+):(\w+)@)?(https?://[a-zA-Z0-9.-]+):(\d+)\s*$', re.IGNORECASE)

# Expression régulière pour récupérer les éléments dans un dictionnaire Python
extraction_pattern = re.compile(r'^\s*proxy\s*=\s*(?:(\w+):(\w+)@)?(https?://[a-zA-Z0-9.-]+):(\d+)\s*$', re.IGNORECASE)

# Exemple d'utilisation
proxy_line = "    Proxy = :pass@http://example.com:8080    "

# Validation
validation_match = validation_pattern.match(proxy_line)
if validation_match:
    print(f"La ligne proxy est valide. URL: {validation_match.group(3)}, Port: {validation_match.group(4)}")

    # Réinitialisation de la position du curseur
    proxy_line = validation_match.group(0)

    # Afficher la ligne après validation
    print(f"Ligne après validation: {proxy_line}")

    # Extraction
    extraction_match = extraction_pattern.match(proxy_line)
    if extraction_match:
        proxy_dict = {
            "Username": extraction_match.group(1),
            "Password": extraction_match.group(2),
            "URL": extraction_match.group(3),
            "Port": extraction_match.group(4)
        }
        print("Éléments extraits dans un dictionnaire Python :", proxy_dict)
    else:
        print("Erreur lors de l'extraction. La ligne après validation ne correspond pas à l'expression d'extraction.")
else:
    print("La ligne proxy n'est pas valide.")
