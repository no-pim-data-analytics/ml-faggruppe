# 🤖 Session 4: Embedding - Q&A 

### 📝 Intro

Denne notebooken fokuserer på å jobbe med tekstdata on-prem, uten eksterne API-kall. Her er stegene:

- **Splitte et dokument til paragrafer:** Del et lengre dokument inn i mindre paragrafer for enklere håndtering.
- **Konvertere til embeddings:** Bruk teknikker som BERT eller FastText for å konvertere paragrafene til numeriske vektorer (embeddings).
- **Flytte til en vektor-database:** Lagre embeddings i en database som FAISS eller Annoy, som tillater raskt oppslag og sammenligning.
- **Finn dokumenter basert på spørsmålet:** Gjennomfør en søkeoperasjo🤖n i databasen for å finne de mest relevante paragrafene eller dokumentene basert på spørsmålets embedding.
- **Finn svaret i dokumentet:**  Bruk Language Model for å identifisere det mest relevante svaret i valgte paragrafer basert på inngående spørsmål.

Vi benytter denne metoden for å håndtere konfidensiell eller intern data uten å måtte dele den med tredjeparter.

Selv om OpenAI sin modell er state-of-the-art, er det viktig å merke seg at det er en "black-box" i forhold til databehandling.

Til slutt vil vi demonstrere hvordan alt dette kan implementeres i et UI ved bruk av Chainlit, inkludert henvisninger til relevante kilder.
