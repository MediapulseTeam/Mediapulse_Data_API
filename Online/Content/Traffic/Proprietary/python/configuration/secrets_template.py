from dataclasses import dataclass

# Adapt the needed information, so it can be used by the script
# Read the README.MD file for further instructions on how to obtain the token
# Rename the template file to "secrets.py"
credentials = {
    'tableau_online':
        {
            "server" : "https://tableau.mediapulse.ch",
            "api_version" : '3.13',
            "personal_access_token_name" : "[Name of your token here]",
            "personal_access_token_secret" : "[Token of your account settings page on tableau server]",
            'site_name': "",
            'site_url': ""
        }
}

# Adapt the needed information, so it can be used by the script
# Rename the template file to "secrets.py"
@dataclass(frozen=True)
class Config():
    server = "https://tableau.mediapulse.ch"
    username = "[your username here]"
    password = "[your password here]"
    site_id = ""

