import pandas as pd
from rich.progress import Progress
from data.clean_app_size import clean_app_size
from data.clean_date import clean_date
from data.clean_float import clean_float
from data.clean_numeric import clean_numeric
from data.clean_price import clean_price


def main():
    with Progress() as progress:
        clean_task = progress.add_task("[cyan]Data cleaning", total=6)
    
        df = pd.read_csv("source//googleplaystore.csv")

        if "Installs" in df.columns:
            df["Installs"] = df["Installs"].apply(clean_numeric)
            progress.update(clean_task, advance=1)

        if "Reviews" in df.columns:
            df["Reviews"] = df["Reviews"].apply(lambda x: int(x) if pd.notna(x) and str(x).isdigit() else 0)
            progress.update(clean_task, advance=1)

        if "Rating" in df.columns:
            df["Rating"] = df["Rating"].apply(clean_float)
            progress.update(clean_task, advance=1)

        if "Price" in df.columns:
            df["Price"] = df["Price"].apply(clean_price)
            progress.update(clean_task, advance=1)

        if "Size" in df.columns:
            df["Size"] = df["Size"].apply(clean_app_size)
            progress.update(clean_task, advance=1)

        if "Last Updated" in df.columns:
            df["Last Updated"] = df["Last Updated"].apply(clean_date)
            progress.update(clean_task, advance=1)

    with Progress() as progress:
        # Exportar para CSV
        export_csv_task = progress.add_task("[cyan]Exporting to CSV", total=1)
        df.to_csv("output/googleplaystore_cleaned.csv", index=False, encoding="utf-8")
        progress.update(export_csv_task, advance=1)

    with Progress() as progress:
        create_table_task = progress.add_task("[cyan]Create table STM", total=13)
        columns = {
            "App": "VARCHAR(255) NULL",
            "Category": "VARCHAR(100) NULL",
            "Rating": "FLOAT NULL",
            "Reviews": "INT NULL",
            "Size": "FLOAT NULL",
            "Installs": "INT NULL",
            "Type": "VARCHAR(20) NULL",
            "Price": "FLOAT NULL",
            "Content Rating": "VARCHAR(50) NULL",
            "Genres": "VARCHAR(100) NULL",
            "Last Updated": "DATE NULL",
            "Current Ver": "VARCHAR(50) NULL",
            "Android Ver": "VARCHAR(50) NULL"
        }

        create_table = "CREATE TABLE googleplaystore (\n"
        for col, sql_type in columns.items():
            create_table += f"    `{col}` {sql_type},\n"
            progress.update(create_table_task, advance=1)
        create_table = create_table.rstrip(",\n") + "\n);\n"
    
    with Progress() as progress:
        insert_task = progress.add_task("[cyan]Insert STM", total=len(df))
        insert_statements = f"INSERT INTO googleplaystore ({', '.join('`'+col+'`' for col in columns.keys())}) VALUES \n"
        
        for count, row in df.iterrows():
            values = []
            for col, sql_type in columns.items():
                value = row[col] if col in row else None
                if pd.isna(value):
                    values.append("NULL")
                elif "VARCHAR" in sql_type or "DATE" in sql_type:
                    val_str = str(value).replace("'", "''")
                    values.append(f"'{val_str}'")
                else:
                    values.append(str(value))
                
            if count > 0:
                insert_statements += ", \n"
            insert_statements +=  f"({', '.join(values)})"
            progress.update(insert_task, advance=1)
        insert_statements += ";"

    with Progress() as progress:
        write_document_task = progress.add_task("[cyan]Writing document", total=2)
        with open("output/googleplaystore.sql", "w", encoding="utf-8") as f:
            f.write("-- CREATE TABLE\n")
            f.write(create_table + "\n")
            f.write("-- INSERTS\n")
            progress.update(write_document_task, advance=1)
            f.write(insert_statements + "\n")
            progress.update(write_document_task, advance=1)
    print('Created output/googleplaystore_cleaned.csv and output/googleplaystore.sql')


if __name__ == '__main__':
    main()
