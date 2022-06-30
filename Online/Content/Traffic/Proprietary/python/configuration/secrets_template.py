from dataclasses import dataclass

# Adapt the needed information, so it can be used by the script
# Rename the template file to "secrets.py"
@dataclass(frozen=True)
class Config():
    server = "https://tableau.mediapulse.ch"
    username = "[your username here]"
    password = "[your password here]"
    site_id = ""
    group_name = ""
    workbook = "[ID of workbook]"
    view = "[ID of view]"
