# How to use

## TODO
- [ ] Add in a database layer, so that character stats and images are only generated/fetched once
- [ ] prep strings for queries, and better naming convention for images
  - e.g. lower, strip spaces, maybe some level of fuzzy matching??? hard to decide.
  - will have to play around
    - Also - store database page url, so same searches that reveal same page don't do same card
    - Also - gives synonyms for characters. if someone searches for a new character and it returns same url, then can add that to the db as another reference to the same character.
- [ ] Built better UI - probably dont want jinja templates - but it could work.
- [ ] init git repo, and push

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