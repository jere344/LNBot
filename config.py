language = "EN"  # FR / EN / DE / ES / IT
command_prefix = "%"  # Any

# These are the default argument passed when executing download
verbose = v = True  # Download status messages on discord
console = False  # Download status in console
pdf = False  # Automatically send pdf when download is finished #! not ready yet
epub = True  # Automatically send epub when download is finished
raw = False  # Automatically send raw when download is finished
download_lang = "all"  # same as language
source = "all"  # only sources with this word in url


# Sharing methods
# discord : send directly via discord, 8mb max for non-nitro users
# local : send via local server, won't use network when sending links, but will use it when downloading for each person
sharing_small = "discord"  # For files smaller than 8mb
sharing_large = "local"  # For file larger than 8mb


# Required for "local" sharing method
# Defaults are 127.0.0.1 and 127.0.0.1
# You will need to use port forwarding for it to work outside your network
host = "127.0.0.1"
port = "5000"
