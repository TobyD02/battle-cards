# How to use

## TODO
- [x] Add in a database layer, so that character stats and images are only generated/fetched once
  - Improve the database layer. SQLITE might work longterm, but there is still the issue that the same character can have multiple entries.
  - Need to enforce unique wiki url constraint - and if a duplicate is found, add the search term to be linked to that row.
- [x] prep strings for queries, and better naming convention for images
  - e.g. lower, strip spaces, maybe some level of fuzzy matching??? hard to decide.
  - will have to play around
    - Also - store database page url, so same searches that reveal same page don't do same card
    - Also - gives synonyms for characters. if someone searches for a new character and it returns same url, then can add that to the db as another reference to the same character.
- [ ] I have an endpoint for opening packs - to make it fun:
  - Mark unqiue card ID's - these can be added to some counter for the player
    - If a player already has that card, then it is a duplicate and can be sold etc...
    - I think generating cards should be able to be done with any label - but api endpoints should use the card ID / base card ID?
    - Searching should be done by using the "Name" of the card (string similarity).
      - Shouldn't lean on the labels at all - but should limit to one card per wiki page?
  - **ESSENTIALLY** - add users - have them be able to collect, generate & search for cards.

### Prerequisites 
- Ollama running somwhere (ideally locally), using gemma3:4b
  - if not running locally, edit the docker-compose.yml file environment variable to point to the correct url
- Docker

### Run

```shell
# If running ollama locally: 
ollama run gemma3:4b

docker compose up --build
```