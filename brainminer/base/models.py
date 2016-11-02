from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable

Base = declarative_base()


# ----------------------------------------------------------------------------------------------------------------------
# http://stackoverflow.com/questions/38678336/sqlalchemy-how-to-implement-drop-table-cascade
@compiles(DropTable)
def compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + ' CASCADE'
