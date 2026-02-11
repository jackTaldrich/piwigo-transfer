import csv


def get_description(reader, image_id, column):
    for row in reader:
        if row[column] == image_id:
            alt_text = row[5]
            deposit_url = row[2]
            title = row[3]
            author = row[4]

            print(f'\nTitle:\n{title}')

            print(f"""
Alt Text: {alt_text}
Source URL: {deposit_url}
Publisher: DepositPhotos
Attribution: {author}/DepositPhotos
                            """)

            break


def main():
    image_id = ''
    piwigo = False
    while image_id != 'exit':
        print('Type exit to exit')
        image_id = str(input('Deposit/Piwigo ID: '))

        s = image_id.strip()

        if s.startswith("Depositphotos_"):
            s = s.removeprefix("Depositphotos_")

        if s.endswith("_XL.jpg"):
            s = s.removesuffix("_XL.jpg")
        elif s.endswith("_XL"):
            s = s.removesuffix("_XL")

        if 4 <= len(s) <= 5:
            piwigo = True

        image_id = s

        with open('completed.tsv', 'r', newline='', encoding='utf-8') as completed_tsv:
            reader = csv.reader(completed_tsv, delimiter='\t')
            next(reader)

            if piwigo:
                get_description(reader, image_id, 7)
            else:
                get_description(reader, image_id, 1)

if __name__ == '__main__':
    main()