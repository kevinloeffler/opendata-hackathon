#!/bin/bash

url='https://www.daten.stadt.sg.ch/api/explore/v2.1/catalog/datasets/fullstandssensoren-sammelstellen-stadt-stgallen/exports/csv?lang=en&timezone=Europe%2FZurich&use_labels=true&delimiter=%3B'
output_file='data/fill-levels-2.csv'

curl -Lo "$output_file" "$url"

echo "Download complete. File saved to $output_file."
