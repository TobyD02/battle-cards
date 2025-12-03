# How to use

## TODO
- [x] Add in a database layer, so that character stats and images are only generated/fetched once
  - Improve the database layer. SQLITE might work longterm, but there is still the issue that the same character can have multiple entries.
  - Need to enforce unique wiki url constraint - and if a duplicate is found, add the search term to be linked to that row.
- [ ] prep strings for queries, and better naming convention for images
  - e.g. lower, strip spaces, maybe some level of fuzzy matching??? hard to decide.
  - will have to play around
    - Also - store database page url, so same searches that reveal same page don't do same card
    - Also - gives synonyms for characters. if someone searches for a new character and it returns same url, then can add that to the db as another reference to the same character.
- [ ] Work out which order CSS classes must be applied in, in order for them to be compatible
  - Subsequently, come up with a way of determining when a card should be holo, negative, gold, etc...
- [ ] On searching, check string similarity between search term and resultant page
  - Should only result in a card if there is similarity

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