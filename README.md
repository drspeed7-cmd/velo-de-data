# VELO DE – Offline-Daten

Offline-Datenpakete für [VELO DE](https://github.com/drspeed7-cmd/velo-de), das Offline-Fahrrad-Navi für Deutschland.

## Enthaltene Daten

| Datei | Beschreibung | Quelle |
|-------|-------------|--------|
| `nrw.mbtiles` | Vektor-Tiles für NRW (Zoom 0–14) | OpenStreetMap via Planetiler |
| `nrw.db` | Suchdatenbank (SQLite/FTS5) | OpenStreetMap via osmium |
| `routing-nrw.tar.gz` | BRouter-Segmentdateien (.rd5) | brouter.de |
| `fonts.tar.gz` | Noto Sans Glyphs (PBF) | Google Noto Fonts |
| `sprites.tar.gz` | Kartensymbole | Generiert |
| `checksums.txt` | SHA256-Prüfsummen | Generiert |

## Download

Die Daten stehen als [GitHub Release](https://github.com/drspeed7-cmd/velo-de-data/releases/tag/offline-data) bereit.

Die App lädt sie automatisch aus dem Kartenmanager herunter.

## Daten aktualisieren

Die GitHub Actions Pipeline kann jederzeit manuell gestartet werden:
1. Gehe zu [Actions](https://github.com/drspeed7-cmd/velo-de-data/actions)
2. Wähle "Build Offline Data (NRW)"
3. Klicke "Run workflow"

Die Pipeline lädt aktuelle OSM-Daten von Geofabrik und generiert alle Pakete neu.

## Lizenz

- Kartendaten: [OpenStreetMap](https://www.openstreetmap.org/copyright) (ODbL)
- BRouter-Segmente: [brouter.de](https://brouter.de) (MIT)
- Schriften: [Noto Sans](https://fonts.google.com/noto/specimen/Noto+Sans) (OFL)
