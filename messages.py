import config


class BaseMessage(str):
    """Calling a class inheritting from BaseMessage return a string corressponding to the language selected in config.py"""

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls)

    def __str__(self):
        return self.__getattribute__(config.language)

    def __init__(self) -> str:
        return super().__init__()


class ChapterDownloaded(BaseMessage):
    def __init__(self, chap_number, max_chap) -> str:
        self.EN = f"{chap_number}/{max_chap} chapters dowloaded"
        self.FR = f"{chap_number}/{max_chap} chapitres téléchargés"


class SummaryDownloaded(BaseMessage):
    FR = "Sommaire téléchargé"
    EN = "Summary downloaded"
    ES = "Resumen descargado"
    DE = "Zusammenfassung heruntergeladen"


class CoverDownloaded(BaseMessage):
    FR = "Couverture téléchargé"
    EN = "Cover downloaded"
    ES = "Portada descargada"
    DE = "Cover heruntergeladen"


class ChapterlistDownloaded(BaseMessage):
    FR = "Liste de chapitre téléchagé"
    EN = "Chapter list downloaded"
    ES = "Lista de capítulos descargada"
    DE = "Kapitel-Liste heruntergeladen"


class NoNovelFound(BaseMessage):
    FR = "Aucun novel trouvé"
    EN = "No novel found"
    ES = "Ningún novel encontrado"
    DE = "Kein Novel gefunden"


class DownloadingNovel(BaseMessage):
    def __init__(self, novel):
        self.EN = f"Downloading {novel} ..."
        self.FR = f"{novel} en cour de telechargement ..."
        self.ES = f"Descargando {novel} ..."
        self.DE = f"{novel} wird heruntergeladen ..."


class NovelDownloaded(BaseMessage):
    def __init__(self, novel):
        self.EN = f"{novel} downloaded"
        self.FR = f"{novel} téléchargé"
        self.ES = f"{novel} descargado"
        self.DE = f"{novel} heruntergeladen"


class GeneratingEbook(BaseMessage):
    EN = "Generating ebook ..."
    FR = "Création de l'ebook ..."
    ES = "Generando ebook ..."
    DE = "Erstelle eBook ..."


class AldreadyDownloaded(BaseMessage):
    EN = "Novel aldready downloaded, checking for update ..."
    FR = "Novel déjà téléchargé, recherche de mise à jour ..."
    ES = "Novel ya descargado, comprobando actualizaciones ..."
    DE = "Novel bereits heruntergeladen, prüfe aktualisierung ..."


class UpdateDetected(BaseMessage):
    EN = "New chapter found, downloading update ..."
    FR = "Nouveaux chapitres détectés, telechargement en cours ..."
    ES = "Nuevos capítulos encontrados, descargando actualizaciones ..."
    DE = "Neue Kapitel gefunden, lade aktualisierung ..."


class TooManyFound(BaseMessage):
    EN = "Too many novel found, please try again with a more precize search"
    FR = "Trop de novel trouvé, réessayez avec des thermes plus précis"
    ES = "Demasiados novel encontrados, por favor intente de nuevo con una búsqueda más precisa"
    DE = "Zu viele Novel gefunden, bitte versuche es noch einmal mit einer genaueren Suche"


class MetadataDownloaded(BaseMessage):
    EN = "Metadata downloaded"
    FR = "Metadonnées téléchargés"
    ES = "Metadatos descargados"
    DE = "Metadaten heruntergeladen"


class SendingEbook(BaseMessage):
    def __init__(self, ebook_type):
        self.EN = f"Sending {ebook_type} ..."
        self.FR = f"{ebook_type} en cours d'envoi ..."
        self.ES = f"{ebook_type} enviando ..."
        self.DE = f"{ebook_type} wird gesendet ..."


class DownloadHelpMessage(BaseMessage):
    EN = f"""{config.command_prefix}download <*novel> [?*-options]

Search the novel in availible sources, ask the user which one to download and download it.

on/off options : (default value in brackets)
-v : send discord message with download status [{"on" if config.v else "off"}]
-console : print the status in console [{"on" if config.console else "off"}]
-pdf : send the pdf [{"on" if config.pdf else "off"}]
-epub : send the epub [{"on" if config.epub else "off"}]
-raw : send the raw [{"on" if config.raw else "off"}]

variables options with default value: ('all' to show everything) 

-lang:{config.download_lang} : only show novel of the selected language [ex : lang:EN] -> english language only
-source:{config.source} : only show novel witch match input [ex : source:world] -> source with 'world' in name"""

    FR = f"""{config.command_prefix}download <*novel> [?*-options]

Cherche le novel parmis les sources disponible, demande lequel télécharger, et le télécharge.

on/off options : (valeurs par default entre crochets)
-v : donne le status du téléchargement par messages discord [{"on" if config.v else "off"}]
-console : print le status dans la console [{"on" if config.console else "off"}]
-pdf : envoie le pdf [{"on" if config.pdf else "off"}]
-epub : envoie l'epub [{"on" if config.epub else "off"}]
-raw : envoie le fichier brut [{"on" if config.raw else "off"}]

Options variables avec leurs valeurs par default : ('all' pour tout afficher)

-lang:{config.download_lang} : Montre seulement le novel de la langue selectionnée [ex : lang:EN] -> langue anglaise seulement
-source:{config.source} : montre seulement les novels qui correspondent au nom de la source [ex : source:world] -> source avec 'world' dans le nom"""

    ES = f"""{config.command_prefix}download <*novel> [?*-options]

Busca el novel en las fuentes disponibles, pregunta al usuario que novel descargar y lo descarga.

on/off options : (valores por default entre corchetes)
-v : envia un mensaje de discord con el estado del descarga [{"on" if config.v else "off"}]
-console : imprime el estado en la consola [{"on" if config.console else "off"}]
-pdf : envia el pdf [{"on" if config.pdf else "off"}]
-epub : envia el epub [{"on" if config.epub else "off"}]
-raw : envia el fichero [{"on" if config.raw else "off"}]

variables options con valores por default: ('all' para mostrar todo)

-lang:{config.download_lang} : solo muestra novel de la seleccionada idioma [ex : lang:EN] -> idioma ingles solo
-source:{config.source} : solo muestra novel que coincidan con el nombre de la fuente [ex : source:world] -> fuente con 'world' en el nombre"""

    DE = f"""{config.command_prefix}download <*novel> [?*-options]
Sucht das Novel in den verfügbaren Quellen, fragt den Benutzer welches zu downloaden und lädt es.

on/off options : (Standardwerte in Klammern)
-v : sendet eine Discord Nachricht mit dem Download Status [{"on" if config.v else "off"}]
-console : gibt den Status in der Konsole aus [{"on" if config.console else "off"}]
-pdf : sendet das pdf [{"on" if config.pdf else "off"}]
-epub : sendet das epub [{"on" if config.epub else "off"}]
-raw : sendet das raw [{"on" if config.raw else "off"}]

Variablen Optionen mit Standardwerten: ('all' für alles anzeigen)

-lang:{config.download_lang} : zeigt nur Novel der ausgewählten Sprache an [ex : lang:EN] -> englische Sprache nur
-source:{config.source} : zeigt nur Novel die den Namen der Quelle entsprechen [ex : source:world] -> Quelle mit 'world' in Namen"""
