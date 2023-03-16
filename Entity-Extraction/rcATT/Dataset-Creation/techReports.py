from attackcti import attack_client
from datetime import datetime
import trafilatura
import requests
import os

skipDuplicates = True

path = "./Entity-Extraction/rcATT/Dataset-Creation/URL_Content"

if not os.path.exists(path):
    os.mkdir(path)

lift = attack_client()
techniques = lift.get_techniques()

i = 1
for technique in techniques:

    technique_name = technique['name'].replace("/", "_")
    technique_dir = path + "/" + technique_name

    # Do only if not already extracted
    if not os.path.exists(technique_dir) and skipDuplicates:
        print('[🔎 TECHNIQUE {}/{}] {}'.format(i, len(techniques), technique['name']))
        i += 1

        try:
            os.mkdir(technique_dir)
            references = technique['external_references']
            urls = []
            for reference in references:
                # Omit mitre attack references cause they usually are links to the main technique or tactic
                if reference['source_name'] != "mitre-attack":
                    urls.append(reference['url'])

            data = {}
            j = 1
            try:
                if len(urls) != 0:
                    for url in urls:
                        dt = datetime.now()
                        ts = datetime.timestamp(dt)
                        print('    [🌐 URL {}/{}] [🕛 {}] {}'.format(j, len(urls), str(dt)[11:19], url))
                        j += 1
                        
                        resp = requests.get(url)
                        if resp.status_code == 200:
                            data[url] = resp.text
                        
                        downloaded_url = trafilatura.fetch_url(url)
                        try:
                            text = trafilatura.extract(downloaded_url)
                            text = text.replace("\n", " ")

                            filename = technique_dir + "/url_" + str(j - 1) + ".txt"

                            if text != "":
                                with open(filename, "w") as text_file:
                                    text_file.write(text)
                            else:
                                print('    [📂 EMPTY TEXT]')
                        except:
                            print('    [❌ URL FAILED]')
            except:
                print('    [❌ URL FAILED]')
        except:
            print('[❌ NO URLS FOUND]')
    elif skipDuplicates:
        print('[✅ TECHNIQUE DONE] {}'.format(technique['name']))
        i += 1
    else:
        print('[🔎 TECHNIQUE {}/{}] {}'.format(i, len(techniques), technique['name']))
        i += 1

        try:
            os.mkdir(technique_dir)
            references = technique['external_references']
            urls = []
            for reference in references:
                # Omit mitre attack references cause they usually are links to the main technique or tactic
                if reference['source_name'] != "mitre-attack":
                    urls.append(reference['url'])

            data = {}
            j = 1
            try:
                if len(urls) != 0:
                    for url in urls:
                        dt = datetime.now()
                        ts = datetime.timestamp(dt)
                        print('    [🌐 URL {}/{}] [🕛 {}] {}'.format(j, len(urls), str(dt)[11:19], url))
                        j += 1
                        
                        resp = requests.get(url)
                        if resp.status_code == 200:
                            data[url] = resp.text
                        
                        downloaded_url = trafilatura.fetch_url(url)
                        try:
                            text = trafilatura.extract(downloaded_url)
                            text = text.replace("\n", " ")

                            filename = technique_dir + "/url_" + str(j - 1) + ".txt"

                            if text != "":
                                with open(filename, "w") as text_file:
                                    text_file.write(text)
                            else:
                                print('    [📂 EMPTY TEXT]')
                        except:
                            print('    [❌ URL FAILED]')
            except:
                print('    [❌ URL FAILED]')
        except:
            print('[❌ NO URLS FOUND]')

# Removing Empty Folders
folders = list(os.walk(path))[1:]
num_empty = 0
for folder in folders:
    if not folder[2]:
        num_empty += 1
        os.rmdir(folder[0])

print('[📂 REMOVED {} EMPTY FOLDERS]'.format(num_empty))