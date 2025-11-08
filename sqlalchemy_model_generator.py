import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

def generate_sqlalchemy_models(db_url: str, tables=None, output_file="models.py"):
    """
    Auto-generate SQLAlchemy declarative models from an existing database
    without using third-party libraries like sqlacodegen.

    :param db_url: SQLAlchemy database URL
    :param tables: List of table names to generate (None = all tables)
    :param output_file: Output .py file path
    """
    engine = create_engine(db_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    Base = declarative_base()

    # If no specific tables are provided, generate all
    selected_tables = tables or metadata.tables.keys()

    lines = []
    lines.append("from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, Text, ForeignKey\n")
    lines.append("from sqlalchemy.ext.declarative import declarative_base\n\n")
    lines.append("Base = declarative_base()\n\n")

    for table_name in selected_tables:
        if table_name not in metadata.tables:
            print(f"⚠️ Table '{table_name}' not found, skipping...")
            continue

        table = metadata.tables[table_name]
        lines.append(f"class {table_name.capitalize()}(Base):\n")
        lines.append(f"    __tablename__ = '{table_name}'\n\n")

        for column in table.columns:
            col_type = type(column.type).__name__
            type_mapping = {
                "INTEGER": "Integer",
                "SMALLINT": "Integer",
                "BIGINT": "Integer",
                "VARCHAR": "String",
                "TEXT": "Text",
                "DATETIME": "DateTime",
                "DATE": "Date",
                "BOOLEAN": "Boolean",
                "FLOAT": "Float",
                "NUMERIC": "Float",
                "DECIMAL": "Float",
                "CHAR": "String",
            }
            sa_type = type_mapping.get(col_type.upper(), "String")

            args = []
            if column.primary_key:
                args.append("primary_key=True")
            if not column.nullable:
                args.append("nullable=False")
            if column.default is not None:
                args.append(f"default={column.default.arg!r}")

            line = f"    {column.name} = Column({sa_type}"
            if args:
                line += ", " + ", ".join(args)
            line += ")\n"
            lines.append(line)

        lines.append("\n\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Models generated and saved in {output_file}")


if __name__ == "__main__":
    # Example configuration
    db_url = "mysql+pymysql://yaju:yaju@localhost:3306/yaju"
    tables_to_generate = ["customers", "loans"]  # set None to generate all tables

    os.makedirs("models", exist_ok=True)
    generate_sqlalchemy_models(
        db_url=db_url,
        tables=tables_to_generate,
        output_file="models/models.py"
    )
