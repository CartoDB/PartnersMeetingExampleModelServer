# An experimental API to add analysis to Sales Force

For now target analysis aim to include :

1) Balance Sales Teritories
2) Vehicle Routing

### Installation

```bash
git clone https://github.com/CartoDB/sales_quest_research_api.git
```

### Build & Launch

```bash
docker-compose up -d --build
```

To add more workers:

To add more workers:
```bash
docker-compose up -d --scale worker=5 --no-recreate
```

To shut down:

```bash
docker-compose down
```

---

adapted from [https://github.com/itsrifat/flask-celery-docker-scale](https://github.com/itsrifat/flask-celery-docker-scale)
