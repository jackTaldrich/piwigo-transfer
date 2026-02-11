# note that you can also set copyright in the batch manager in piwigo
# that is much faster and more accurate, but this will pair with the main script
# use this if you can't find the batch manager

import csv
import os
from tqdm import tqdm

from dotenv import load_dotenv
from pathlib import Path
from playwright.sync_api import sync_playwright


# user/pass for piwigo
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')


def main():
    with (open('completed.tsv', 'r', newline='', encoding='utf-8') as completed_tsv,
          open('copyrighted.tsv', 'r', newline='', encoding='utf-8') as copyright_tsv):
        image_ids = set()

        # add all completed ids to the set
        completed_reader = csv.reader(completed_tsv, delimiter='\t')
        next(completed_reader) # skip header

        for row in completed_reader:
            image_ids.add(row[7]) # piwigo id column

        # remove all already copyrighted ids from the set
        copyrighted_reader = csv.reader(copyright_tsv, delimiter='\t')
        next(copyrighted_reader) # skip header

        # skip if already set
        for row in copyrighted_reader:
            if not row:
                continue
            image_ids.discard(row[0].strip())

    if not image_ids:
        print('Already completed all ids.')
        return

    path = Path('copyrighted.tsv')
    if not path.exists() or path.stat().st_size == 0:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow('PiwigoID')

    with open('copyrighted.tsv', 'a') as copyrighted_tsv:
        copyrighted = csv.writer(copyrighted_tsv, delimiter='\t')

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto('https://mines.piwigo.com/identification.php')

            page.get_by_label('username').fill(USERNAME)
            page.get_by_label('password').fill(PASSWORD)
            with page.expect_navigation():
                page.get_by_role('button', name='Sign in').click()

            sorted_ids = sorted(image_ids, key=int)

            for image_id in tqdm(sorted_ids, desc='Updating Copyright', unit='img'):
                url = 'https://mines.piwigo.com/picture?/' + image_id + '/category/3-images'
                page.goto(url)
                page.get_by_role('link', name='Modify information').click()
                page.locator("#copyrightID").select_option(value="8")
                page.get_by_role('button', name='Save Settings').click()

                copyrighted.writerow([image_id])


if __name__ == '__main__':
    main()
