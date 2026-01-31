# Smart To-Do DevOps Project 🚀

Nowatorski projekt indywidualny realizujący pełny cykl życia aplikacji (SDLC) przy użyciu narzędzi DevOps. Jest to prosta aplikacja zarządzania zadaniami (To-Do List).

## 🛠 Technologie

- **Backend:** Python (FastAPI + SQLAlchemy)
- **Baza danych:** PostgreSQL (Komponent stanowy)
- **Konteneryzacja:** Docker & Docker Compose (Multi-stage build)
- **CI/CD:** GitHub Actions (Reusable workflows, Custom Actions)
- **Rejestr:** GitHub Container Registry (GHCR)

## 📋 Funkcjonalności API

Aplikacja udostępnia pełny interfejs CRUD pod adresem `http://localhost:8000/docs`:

- `GET /tasks` - lista zadań
- `POST /tasks` - dodawanie nowego zadania
- `PUT /tasks/{id}` - edycja (tytuł, opis, status)
- `DELETE /tasks/{id}` - usuwanie zadania

## 🚀 Szybki start (Docker)

Aby uruchomić projekt lokalnie:

```bash
docker compose up --build
```

## Struktura CI/CD

Projekt wykorzystuje zaawansowany pipeline:

- **Linting & Test:** Sprawdzanie poprawności kodu.
- **Reusable Workflow:** Centralna logika budowania obrazów.
- **Registry Push:** Automatyczna publikacja obrazu na GHCR po merge do main.
- **Custom Reporting:** Własna akcja generująca raport z wdrożenia.

---

# Sprawozdanie: Nowatorski Projekt Indywidualny (DevOps)

**Student:** Arkadiusz Sroczyk
**Indeks:** 52793
**Ocena docelowa:** 5.0 :)

---

## 1. Architektura Systemu

Zaprojektowane środowisko składa się z dwóch głównych usług w `docker-compose.yml`:

1.  **Web:** Aplikacja API (FastAPI) zbudowana na bazie lekkiego obrazu `python:3.11-slim`.
2.  **DB:** Baza danych PostgreSQL 15 z trwałym magazynem danych w wolumenie `todo_data`.

## 2. Realizacja wymagań na ocenę 5.0

### Optymalizacja obrazów (Wymaganie 3.5)

Zastosowałem **Multi-stage build** w `Dockerfile`. W pierwszym etapie (`builder`) instalowane są zależności, a w drugim kopiowany jest tylko finalny runtime. Zmniejsza to powierzchnię ataku i rozmiar obrazu.

### Orkiestracja i Statefulness (Wymaganie 4.0)

Zdefiniowałem dwa kontenery komunikujące się wewnątrz sieci Dockera. Usługa `web` posiada zdefiniowany `healthcheck` na bazie danych, co daje stabilność startu systemu. Dane są przechowywane w naszym wolumenie `todo_data`.

### Automatyzacja Reusable Workflows (Wymaganie 4.5)

Logika budowania została abstracted (nie wiem jak to przetłumaczyć) do pliku `reusable-build.yml`. Pozwala to na zachowanie zasady DRY - ten sam kod buduje obraz dla testów oraz publikuje go do rejestru **GHCR**.

### Własna Akcja i Publikacja (Wymaganie 5.0)

W katalogu `.github/actions/report-action` zaimplementowałem własną akcję typu `composite`. Akcja ta integruje się z systemem GitHub Actions, generując podsumowanie builda w formacie Markdown (`$GITHUB_STEP_SUMMARY`).

```

```
