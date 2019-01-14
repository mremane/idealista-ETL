# idealista-api-ETL
>Scrapping of idealista website for garage rentals in Barcelona.

JSON is processed from API and enhanced with Selenium to cover missing data fields.

The idealista API returns less information than the actual idealista website so after API extraction, all garage URLs are HTML scrapped to gather missing features (divs) and saved on MongoDB for later processing.

### Workflow
``` bash
JSON API -> CSV -> Selenium (CSV) -> Save Mongo DB (extra data fields) -> Mongo DB info merge with CSV
```
