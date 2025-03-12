

### Secuencia para ejecutar

``` bash
# activate env
pip install -r requeriments

# alembic 
alembic init alembic

```

En alembic.ini, busca la línea:
```
sqlalchemy.url = postgresql://user:password@localhost/certificates_db

#Asegúrate de que coincida con la configuración en config/db.py.
```

Edita alembic/env.py:

```python
from app.config.db import Base
target_metadata = Base.metadata
```

 Crear y aplicar migración
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

ejecutar 
```py
python main.py
```

**ir a http://127.0.0.1:8000/docs**