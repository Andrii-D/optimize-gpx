# Optimize GPX file
Optimize GPX track by fixing altitude (SRTM), deleting bitten segments and reducing number of points using Ramer–Douglas–Peucker algorithm.

## Install
`pip install -r requirements.txt`

## Run
`python optimize-gpx.py myfile.gpx`

## Overview
1. Fix elevations using data from Shuttle Radar Topography Mission
2. Split segments into two parts if the distance between two points exceeds the threshold (500m)
3. Reduce number of points using Ramer–Douglas–Peucker algorithm

## Examples

Fix elevations:
![65043524_385586968743450_1600004295627898880_n](https://user-images.githubusercontent.com/9039044/60018578-6d06d000-9694-11e9-8e9d-389611bcacca.png)

Delete segments with distance of 500m or more between points
![65027121_471196397017624_7341208610585706496_n](https://user-images.githubusercontent.com/9039044/60018646-90ca1600-9694-11e9-9218-9cbc236ef055.png)
