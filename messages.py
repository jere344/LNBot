import config


class BaseMessage(str):
    """Calling a class inheritting from BaseMessage return a string corressponding to the language selected in config.py"""

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls)

    def __str__(self):
        return self.__getattribute__(config.language)

    def __init__(self) -> str:
        return super().__init__()


class SendingEbook(BaseMessage):
    FR = "Ebook en cour d'envoi ..."
    EN = "Sending Ebook ..."


class ChapterDownloaded(BaseMessage):
    def __init__(self, chap_number, max_chap) -> str:
        self.EN = f"{chap_number}/{max_chap} chapters dowloaded"
        self.FR = f"{chap_number}/{max_chap} chapitres téléchargés"


class SummaryDownloaded(BaseMessage):
    FR = "Sommaire téléchargé"
    EN = "Summary downloaded"


class CoverDownloaded(BaseMessage):
    FR = "Couverture téléchargé"
    EN = "Cover downloaded"


class ChapterlistDownloaded(BaseMessage):
    FR = "Liste de chapitre téléchagé"
    EN = "Chapter list downloaded"


class NoNovelFound(BaseMessage):
    FR = "Aucun novel trouvé"
    EN = "No novel found"


class DownloadingNovel(BaseMessage):
    def __init__(self, novel):
        self.EN = f"Downloading {novel} ..."
        self.FR = f"{novel} en cour de telechargement ..."


class NovelDownloaded(BaseMessage):
    def __init__(self, novel):
        self.EN = f"{novel} downloaded, sending ..."
        self.FR = f"{novel} téléchargé, enovoi en cours ..."


class GeneratingEbook(BaseMessage):
    EN = "Generating ebook ..."
    FR = "Création de l'ebook ..."


class AldreadyDownloaded(BaseMessage):
    EN = "Novel aldready downloaded, checking for update ..."
    FR = "Novel déjà téléchargé, recherche de mise à jour ..."


class UpdateDetected(BaseMessage):
    EN = "New chapter found, downloading update ..."
    FR = "Nouveaux chapitres détectés, telechargement en cours ..."


class TooManyFound(BaseMessage):
    EN = "Too many novel found, please try again with a more precize search"
    FR = "Trop de novel trouvé, réessayez avec des thermes plus précis"


class MetadataDownloaded(BaseMessage):
    EN = "Metadata downloaded"
    FR = "Metadonnées téléchargés"
