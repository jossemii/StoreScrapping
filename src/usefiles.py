import scraping
import json

with open('input.json', 'r') as file:
    input = json.load(file)

output = scraping.main(input['keywords'])

with open('output.json', 'w') as file:
    json.dump(
        scraping.main(input['keywords']),
        file
    )