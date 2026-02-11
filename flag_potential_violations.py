import csv

def main():
    error_code = 0

    seen = [dict() for _ in range(8)]
    column_names = [
        'LocalPath',
        'DepositID',
        'SourceURL',
        'Title',
        'Author',
        'AltText',
        'Keywords',
        'PiwigoID'
    ]

    with open('completed.tsv', 'r', newline='', encoding='utf-8') as completed_tsv:
        reader = csv.reader(completed_tsv, delimiter='\t')
        next(reader)

        row_number = 1
        for row in reader:
            row_number += 1

            if not row:
                print(f'Row {row_number} is empty')
                error_code = 1

            for col_idx, value in enumerate(row):
                if col_idx == 4:  # skip Author column
                    continue

                if value in seen[col_idx]:
                    first_row = seen[col_idx][value]
                    print(
                        f'Duplicate detected in column {col_idx + 1} ({column_names[col_idx]}): '
                        f'"{value}" (rows {first_row} and {row_number})'
                    )
                    error_code = 1
                else:
                    seen[col_idx][value] = row_number

            for i in range(0, 8):
                if not row[i]:
                    print(f'Row {row_number}, Column {i + 1} is empty')
                    error_code = 1

            if row[2] == 'about:blank':
                print(f'Row {row_number} has an incorrect source url (C3)')
                error_code = 1

            if len(row[3].split()) >= 20:
                print(f'Row {row_number} has a very long title')
                error_code = 1

            if len(row[6].split(';')) < 10:
                print(f'Row {row_number} has few keywords')
                error_code = 1

    if not error_code:
        print('All tests passed!')


if __name__ == '__main__':
    main()