import csv

def main():
    image_paths = []

    with open('failed.tsv', 'r', newline='', encoding='utf-8') as failed_tsv:
        reader = csv.reader(failed_tsv, delimiter='\t')

        for row in reader:
            if row[3] == 'File is too large to generate alt text. Shrink file and run again':
                image_paths.append(row[0])

    command = 'cp ' + ' '.join(image_paths) + ' .'
    print(command)
    print('https://compressjpeg.com/')

if __name__ == '__main__':
    main()