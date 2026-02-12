"""Hard code all expected variables for testing here."""
from datetime import datetime

from models.newsticker import Newsticker
from models.newstickers_website import NewstickersWebsite

EXPECTED_NEWSTICKER_STRINGS_BY_WEBSITE: dict[str, list[str]] = {
    "Newsticker (1).html": [
        "+++ Faules Pack: Fast 300.000 Deutsche in Kurzarbeit +++",
        "+++ Özdemir fordert Kopftuchverbot für attraktive Türkinnen +++",
        "+++ Papst erwartet Entschuldigung von Merkel und Zentralrat der Juden +++",
        "+++ Höhere Gewinne: Der Postillon dünnt Redaktionen aus +++",
    ],
    "Newsticker (2).html": [
        "+++ Schluss mit lustig: Gewerkschaft der Clowns will endlich ernstgenommen werden. +++",
        "+++ Gartentipps: Maulwürfe nachhaltig mit Lemmingselbstmordattentätern bekämpfen +++",
        "+++ Wahlschweizer Michael Schumacher fühlt sich vom Konjunkturprogramm übergangen +++",
        "+++ Hüftschaden: Kanzlerin Merkel leidet unter Spagat zwischen Interessengruppen +++",
    ],
    "Newsticker (500) - XXL-Edition (10+6).html": [
        "+++ Always Ultra: Weiblicher Fussballfan in der Regel bei jedem Spiel ihres Clubs dabei +++",
        "+++ Komplizierter Bruch: Ärzte kommen bei Visite auf keinen gemeinsamen Nenner +++",
        "+++ Lider wurden schwer: Musiker trat total übermüdet auf +++",
        "+++ Gut ausgegangen: Waldbrand konnte schnell gelöscht werden +++",
        "+++ Stehen unter Strom: Autofahrer gestresst von Stau in Elbtunnel +++",
        "+++ Scheißt auf den Boulevard: Pariser Fäkalkünstler trotzt unsachlicher Pressekritik +++",
        "+++ Rentner versteht die Welt nicht mehr: Neues Hörgerät nicht bewilligt +++",
        "+++ Mit spitzer Feder: Kritiker erledigt Romanautor +++",
        "+++ Wagenknecht: Linke Politikerin beutet Chauffeur schamlos aus +++",
        "+++ Hat den Bogen überspannt: Mann muss Verein nach Beschädigung des Trainingsgerätes verlassen +++",
        "+++ WHO cares: Nobody interested in work of World Health Organisation +++",
        '+++ "I\'m Sorry": Man apologizes for stupid name +++',
        "+++ It's about time: Einstein's last book finally published +++",
        "+++ Iran: Winner of Teheran Marathon reveals how he won +++",
        "+++ Well done: Engineer praised for new water supply +++",
        "+++ Stoned: Muslim woman gets punished after smoking weed +++",
    ],
    "Newsticker (1652).html": [
        "+++ Tödliche Ajvarsucht: Kroate erschlägt Nebenbuhler an Hochzeitsbuffet +++",
        "+++ Luftaufnahme: Ängstlicher Fotograf atmet vorm Start erst mal tief durch +++",
        "+++ Fetisch: Hesse schmiert sich mit Butter ein +++",
        "+++ Traumtor: Stürmer nickt ein +++",
        "+++ Andrej: Russe erläutert, wievielen Personen er Einladung geschickt hat +++",
        "+++ Wird hier nicht alt: Gerste will Düsseldorfer Brauerei sofort verlassen +++",
        "+++ Verdreht er: Schmerzsalben-Verkäufer kugelt Arzt zu Demonstrationszwecken den Arm aus +++",
    ],
    "Newsticker (2358).html": [
        "+++ Kein Inder Hesse: Einbürgerung in Frankfurt wird von Südasiaten nicht in Anspruch genommen +++",
        "+++ Tausende Pendler betroffen: Öffis-Streik zwingt Spiritualisten zu Homeoffice +++",
        "+++ Holzbein!: Pirat lässt Hund Prothese bringen +++",
        '+++ Notstromo: "Alien"-Raumschiff schaltet auf Dieselaggregat +++',
        "+++ Teilgenom: Biologe hat CRISPR-Kurs besucht +++",
        "+++ Der Bastian: Schweinsteiger jobbt in fränkischer Brillenwerkstatt +++",
        "+++ Hamsterkäufe nehmen zu: Zoohandlung beschränkt Abgabe auf haushaltsübliche Mengen +++",
    ],
}

EXPECTED_IMAGE_PATH_BY_WEBSITE: dict[str, str | None] = {
    "Newsticker (1).html": "Newsticker (1)_files/faulespack.webp",
    "Newsticker (2).html": "Newsticker (2)_files/clowns.webp",
    "Newsticker (500) - XXL-Edition (10+6).html": None,  # No Image on newsticker's website
    "Newsticker (1652).html": "Newsticker (1652)_files/tickerhibär_orig.webp",
    "Newsticker (2358).html": "Newsticker (2358)_files/tickerkeininder2.webp",
}



def get_expected_newsticker_by_website(website: str) -> Newsticker:
    match website:
        case "Newsticker (1).html":
            return Newsticker(
                text="+++ Faules Pack: Fast 300.000 Deutsche in Kurzarbeit +++",
                newstickers_website=NewstickersWebsite(
                    number=1,
                    title="Newsticker (1)",
                    date=datetime.date(2009, 2, 4),
                    url=website,
                ),
                extracted_from_image=True,
                image_extraction_invalid=False,
    ),



    "Newsticker (2).html": "Newsticker (2)_files/clowns.webp",
    "Newsticker (1652).html": "Newsticker (1652)_files/tickerhibär_orig.webp",
    "Newsticker (2358).html": "Newsticker (2358)_files/tickerkeininder2.webp",
}