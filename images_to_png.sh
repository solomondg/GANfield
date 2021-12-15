#!/bin/bash

NUM_IMAGES = $(find "images" -type f -name "*.png")
for img in `find "images" -type f`; do echo $img; convert $img ${img%.*}.png; done 
