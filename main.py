import pandas as pd
from data import clean_app_size, clean_date, clean_float, clean_numeric, clean_price

def main():
    df = pd.read_csv("source\\googleplaystore.csv")

    if "Installs" in df.columns:
        df["Installs"] = df["Installs"].apply(clean_numeric)

    if "Reviews" in df.columns:
        df["Reviews"] = df["Reviews"].apply(lambda x: int(x) if pd.notna(x) and str(x).isdigit() else None)

    if "Rating" in df.columns:
        df["Rating"] = df["Rating"].apply(clean_float)

    if "Price" in df.columns:
        df["Price"] = df["Price"].apply(clean_price)

    if "Size" in df.columns:
        df["Size"] = df["Size"].apply(clean_app_size)

    if "Last Updated" in df.columns:
        df["Last Updated"] = df["Last Updated"].apply(clean_date)
    
    columns = {
        "App": "VARCHAR(255)",
        "Category": "VARCHAR(100)",
        "Rating": "FLOAT",
        "Reviews": "INT",
        "Size": "FLOAT",
        "Installs": "INT",
        "Type": "VARCHAR(20)",
        "Price": "FLOAT",
        "Content Rating": "VARCHAR(50)",
        "Genres": "VARCHAR(100)",
        "Last Updated": "DATE",
        "Current Ver": "VARCHAR(50)",
        "Android Ver": "VARCHAR(50)"
    }

    create_table = "CREATE TABLE googleplaystore (\n"
    for col, sql_type in columns.items():
        create_table += f"    `{col}` {sql_type},\n"
    create_table = create_table.rstrip(",\n") + "\n);\n"

    insert_statements = []
    for _, row in df.iterrows():
        values = []
        for col, sql_type in columns.items():
            val = row[col] if col in row else None
            if pd.isna(val):
                values.append("NULL")
            elif "VARCHAR" in sql_type or "DATE" in sql_type:
                val_str = str(val).replace("'", "''")
                values.append(f"'{val_str}'")
            else:
                values.append(str(val))
            insert = f"INSERT INTO googleplaystore ({', '.join('`'+col+'`' for col in columns.keys())}) VALUES ({', '.join(values)});"
            insert_statements.append(insert)

            with open("output\\googleplaystore.sql", "w", encoding="utf-8") as f:
                f.write("-- Criação da tabela\n")
                f.write(create_table + "\n")
                f.write("-- Inserções dos registros\n")
                for stmt in insert_statements:
                    f.write(stmt + "\n")

if __name__ == '__main__':
    main()
