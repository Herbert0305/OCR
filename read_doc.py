from docx import Document


def extract_table_as_dict(table):
    table_dict = {}
    for row in table.rows:
        cells = row.cells
        if len(cells) >= 4:  # 至少有四个单元格才处理
            outer_key = (cells[0].text.strip(), cells[1].text.strip())
            inner_key = cells[2].text.strip()
            inner_value = cells[3].text.strip()
            if outer_key not in table_dict:
                table_dict[outer_key] = {}
            if inner_key not in table_dict[outer_key]:
                table_dict[outer_key][inner_key] = []
            table_dict[outer_key][inner_key].append(inner_value)
        elif len(cells) >= 3:  # 至少有三个单元格才处理
            outer_key = cells[0].text.strip()
            inner_key = cells[1].text.strip()
            inner_value = cells[2].text.strip()
            if outer_key not in table_dict:
                table_dict[outer_key] = {}
            if inner_key not in table_dict[outer_key]:
                table_dict[outer_key][inner_key] = []
            table_dict[outer_key][inner_key].append(inner_value)
        elif len(cells) >= 2:  # 至少有两个单元格才处理
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            table_dict[key] = value

    return table_dict


def extract_all_tables_as_dicts(doc_path):
    doc = Document(doc_path)
    tables_dicts = []

    for table in doc.tables:
        table_dict = extract_table_as_dict(table)
        tables_dicts.append(table_dict)

    return tables_dicts


doc_path = 'shouce.docx'
tables_dicts = extract_all_tables_as_dicts(doc_path)

for table_dict in tables_dicts:
    for outer_key, inner_dict in table_dict.items():
        print(f"{outer_key}: {inner_dict}")
    print("------")

