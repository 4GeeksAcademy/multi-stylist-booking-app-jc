from sqlalchemy import create_engine, MetaData
from sqlalchemy_schemadisplay import create_schema_graph

# Conexión a la base de datos
engine = create_engine("postgresql://gitpod@localhost/example")

# Reflejar todas las tablas existentes
metadata = MetaData()
metadata.reflect(bind=engine)

# Crear el gráfico (IMPORTANTE: pasar engine también)
graph = create_schema_graph(
    metadata=metadata,
    engine=engine,
    show_datatypes=True,
    show_indexes=False,
    rankdir='LR',  # Left to Right
)

# Guardar imagen
graph.write_png("database_schema.png")