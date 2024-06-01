# HTMX Tutorial by BugBytes

## Intro

This is a demo project in order to get a sense of capabilities of HTMX.
Most of the functionality is implemented following the tutorial on [BugBytes](https://youtube.com/playlist?list=PL-2EBeDYMIbRByZ8GXhcnQSuv2dog4JxY&si=tdDkAjA1yyWSBNEN).

## Requirements

- **pip-tools** - package manager to manage Django dependencies locally

## Installation

Install dev environment dependencies:
```bash
pip install pip-tools
```
```bash
pip-compile requirements/requirements.dev.in
```
```bash
pip-sync requirements/requirements.dev.txt
```


Apply migrations:
```bash
make migrate
```

Run the server:
```bash
make run
```
## Useful commands
### Create and apply migrations
```bash
make migrations
```
```bash
make migrate
```

### Migrate to a specific migration
`make migrate <app_name> <migration_number>`
e.g.:
`make migrate anagram 0001`

### Run tests
Minimal test coverage is set to 80%. But it's 100% at the moment. To run tests:
```bash
make test
```

### Check and fix code style
`ruff` is the new cool kid on the block. It's replacing `black`, `isort` and `flake8`. It's used to check and fix code style unbelievably fast.
```bash
make check
```

### Makefile
There are more useful commands in the `Makefile`. Check it out.

## Roadmap / TODOs / Development ideas
- Add tests
- Add more features
- Add more HTMX examples
- Infinite scroll with disappearing top elements to keep the page size constant and not to slow down the page


## License

[MIT](https://choosealicense.com/licenses/mit/)