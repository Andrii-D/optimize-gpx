import sys
import srtm
import gpxpy
import numpy as np
from rdp import rdp
from geopy.distance import distance
from gpxpy.gpx import GPXTrackSegment, GPXTrack


DISTANCE_THRESHOLD = 500  # Split segment if distance between two points exceeds threshold
EPSILON = 0.00001

elevation_data = srtm.get_data()


def get_distance(p1, p2):
    """ Distance between two points in meters """
    return distance((p1.latitude, p1.longitude), (p2.latitude, p2.longitude)).meters


def optimize_segment(seg):
    """ RDP algorithm """
    result = GPXTrackSegment()
    arr = np.array(list(map(lambda p: [p.latitude, p.longitude], seg.points)))
    mask = rdp(arr, algo="iter", return_mask=True, epsilon=EPSILON)
    parr = np.array(list(seg.points))
    result.points = list(parr[mask])
    return result


def split_by_distance(seg, max_distance=DISTANCE_THRESHOLD):
    """ Split segment if distance between two points exceeds max_distance """
    result = []
    last_split = 0
    for i in range(len(seg.points) - 1):
        s = seg.points[i]
        f = seg.points[i+1]
        if get_distance(s, f) > max_distance:
            result.append(seg.points[last_split:i+1])
            last_split = i + 1
        if i == len(seg.points) - 5:
            result.append(seg.points[last_split:i+1])
    return list(
        map(lambda points: GPXTrackSegment(points=points), filter(lambda p: len(p) > 2, result))
    )


filename = sys.argv[1]
new_filename = filename.replace('.gpx', '') + '-optimized.gpx'

gpx_file = open(filename, 'r')
gpx = gpxpy.parse(gpx_file)

print('Tracks: ', len(gpx.tracks))
print('Routes: ', len(gpx.routes))
print('Waypoints: ', len(gpx.waypoints))

elevation_data.add_elevations(gpx, smooth=True)

total_segments = 0
points_before = 0
points_after = 0
for track in gpx.tracks:
    new_segments = []
    for segment in track.segments:
        total_segments += 1
        points_before += len(segment.points)
        new_segment = optimize_segment(segment)
        points_after += len(new_segment.points)
        new_segments += split_by_distance(new_segment)
    track.segments = new_segments
    
print('Total segments: ', total_segments)
print('Points before: ', points_before)
print('Points after: ', points_after)
print('Saved to ' + new_filename)

file = open(new_filename, 'w')
file.write(gpx.to_xml())
file.close()

