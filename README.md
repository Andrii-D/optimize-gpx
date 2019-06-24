# Optimize GPX file
Optimize GPX track by fixing altitude (SRTM), deleting bitten segments and reducing number of points using Ramer–Douglas–Peucker algorithm.

## Install
`pip install -r requirements.txt`

## Run
`python optimize-gpx.py myfile.gpx`

## Overview
1. Fix elevations using data from Shuttle Radar Topography Mission
2. Split segments into two parts if the distance between to points exceeds the threshold (500m)
3. Reduce number of points using Ramer–Douglas–Peucker algorithm
