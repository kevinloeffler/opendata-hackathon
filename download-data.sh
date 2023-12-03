#!/bin/bash

url_w='https://www.daten.stadt.sg.ch/api/explore/v2.1/catalog/datasets/fuellstandsensoren-glassammelstellen-weissglas/exports/csv?lang=de&timezone=Europe%2FZurich&use_labels=true&delimiter=%3B'
output_file_w='data/data_w.csv'

curl -Lo "$output_file_w" "$url_w"

echo "Download (w) complete. File saved to $output_file_w."

url_b='https://www.daten.stadt.sg.ch/api/explore/v2.1/catalog/datasets/fuellstandsensoren-glassammelstellen-braunglas/exports/csv?lang=de&timezone=Europe%2FZurich&use_labels=true&delimiter=%3B'
output_file_b='data/data_b.csv'

curl -Lo "$output_file_b" "$url_b"

echo "Download (w) complete. File saved to $output_file_b."

url_g='https://www.daten.stadt.sg.ch/api/explore/v2.1/catalog/datasets/fuellstandsensoren-glassammelstellen-gruenglas/exports/csv?lang=de&timezone=Europe%2FZurich&use_labels=true&delimiter=%3B'
output_file_g='data/data_g.csv'

curl -Lo "$output_file_g" "$url_g"

echo "Download (w) complete. File saved to $output_file_g."
