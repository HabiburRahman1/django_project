import pdfplumber
file = '/home/habib/Downloads/django_project/static/6.PDF'

pdf_type1 = {
    'table_start_text': 'Code Goods Value',
    'table_end_text': 'Sterling',
    'table_header': ['Code', 'Description', 'Commodity Code', 'Quantity', 'Price', 'Disc%', 'Net Goods Value', 'Vat'],
    'no_one_word_string_fl': 6,
    'no_one_word_string_ff': 1,
    'table_continues_without_header': False,
}
pdf_type2 = {
    'table_start_text': 'ACTIVITY VAT QTY RATE AMOUNT',
    'table_end_text': 'SUBTOTAL',
    'table_header': ['Activity', 'VAT', 'Qty', 'Rate', 'Amount'],
    'no_one_word_string_fl': 5,
    'no_one_word_string_ff': 0,
    'table_continues_without_header': True,
}
pdf_type3 = {
    'table_start_text': 'Count Price Total',
    'table_end_text': 'Parcel Surcharge',
    'table_header': ['SKU', 'Product', 'Unit Count', 'Quantity', 'Unit Price', 'Sub Total', 'VAT', 'Total'],
    'no_one_word_string_fl': 6,
    'no_one_word_string_ff': 1,
    'table_continues_without_header': False,
}

pdf_type4 = {
    'table_start_text': 'QTY DESCRIPTION CODE VAT UNIT COST DISCOUNT TOTAL COST',
    'table_end_text': 'VAT SUMMARY',
    'table_header': ['QTY', 'DESCRIPTION', 'CODE', 'VAT', 'UNIT', 'COST', 'TOTAL COST'],
    'no_one_word_string_fl': 4,
    'no_one_word_string_ff': 1,
    'table_continues_without_header': False,
}
pdf_type5 = {
    'table_start_text': 'Code Description Qty Price Disc % Disc Price Tax % Total',
    'table_end_text': 'Sub Total',
    'table_header': ['Code', 'Description', 'Qty', 'Price', 'Disc %', 'Disc Price', 'Tax %', 'Total'],
    'no_one_word_string_fl': 6,
    'no_one_word_string_ff': 1,
    'table_continues_without_header': True,
}

type_dict = {
    'type1': pdf_type1,
    'type2': pdf_type2,
    'type3': pdf_type3,
    'type4': pdf_type4,
    'type5': pdf_type5,
}
type_selecter = 'type5'

with pdfplumber.open(file) as pdf:

    for index, page in enumerate(pdf.pages):
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        
        text = page.extract_text()
        print(text)
        text = text.strip()
        text = text.split('\n')
        line_found = False
        table = list()

        
        for line in text:
            # print(line)
            table_list = list()
            extra_line_count = 0

            if line_found:
                # print('line found')
                # line = line.trim()
                if type_dict[type_selecter]['table_end_text'] in line or 'Special Instructions' in line:
                    print('table end found')
                    break

                table_row = line.split(' ')
                table_row = ' '.join(table_row).split()
                # print(table_row)
                row_length = len(table_row)
                if row_length >= len(type_dict[type_selecter]['table_header']):
                    if type_dict[type_selecter]['no_one_word_string_ff'] != 0:
                        table_list = table_list + table_row[0:type_dict[type_selecter]['no_one_word_string_ff']]

                    table_list.append(" ".join(table_row[-(row_length-type_dict[type_selecter]['no_one_word_string_ff']):-type_dict[type_selecter]['no_one_word_string_fl']]))
                    table_list = table_list + table_row[-type_dict[type_selecter]['no_one_word_string_fl']:]
                    table.append(table_list)
                #     # print(table)
                else:
                    if table:
                        extra_line_count = extra_line_count + 1
                        if extra_line_count <=2:
                            print(line)
                            if not ("%" in line or line.isdigit()):
                                try:
                                    number = float(line)
                                except:
                                    table[-1][type_dict[type_selecter]['no_one_word_string_ff']] = table[-1][type_dict[type_selecter]['no_one_word_string_ff']] + ' ' + line
                
                

                

            if type_dict[type_selecter]['table_start_text'] in line or (type_dict[type_selecter]['table_continues_without_header'] and index != 0):
                line_found = True
        print(table)
