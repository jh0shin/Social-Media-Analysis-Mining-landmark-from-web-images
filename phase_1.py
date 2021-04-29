import os
import shutil
import csv

# for clustering
import numpy as np
from sklearn.cluster import MeanShift

# for result visualization
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# =====================================================
#          Read geo-coordinates from Document
# =====================================================

geoDataFile = './Photo.csv'

# geo-coordinate
# [filename, flicker id, latitude, longitude, time, (buffer)]
picInfo = []
geoCoord = []

# get picture list which exists in photos
photo_list = os.listdir('./photos')

# Read file and parse data
f = open(geoDataFile, 'r', encoding='UTF8')
for line in csv.reader(f):
    # break if eof
    if not line: break

    if line[0] + '.jpg' in photo_list:
        picInfo.append(line)
        geoCoord.append([float(line[2]), float(line[3])])

f.close()

print("End reading csv file")

# =====================================================
#                MeanShift Clustering
# =====================================================

# meanshift clustering
clustering = MeanShift(bandwidth=0.001, n_jobs=-2).fit(geoCoord)

# # print(clustering.labels_)
# print("End clustering")

# # create directory for clustering picture
# os.mkdir('./cluster')

# # create file for save clustering result
# f = open('./clustering_result.csv', 'w', encoding='UTF8', newline='')
# reswriter = csv.writer(f)

# # if photo exists in photos, copy it to cluster/(cluster_num)
# for index in range(len(geoCoord)):
#     photoname = picInfo[index][0] + '.jpg'

#     # write result
#     reswriter.writerow([picInfo[index][0], clustering.labels_[index]])

#     # filecopy if exists
#     if photoname in photo_list:
#         os.makedirs(                                        \
#             './cluster/'+str(clustering.labels_[index]),    \
#             exist_ok=True                                   \
#         )

#         shutil.copyfile(                                                    \
#             './photos/' + photoname,                                        \
#             './cluster/'+str(clustering.labels_[index]) + '/' + photoname   \
#         )

# f.close()

# =====================================================
#                Result visualization
# =====================================================

font_name = fm.FontProperties(fname = 'C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family = font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

colors = cm.rainbow(np.linspace(0, 1, len(clustering.labels_)))

plt.figure(figsize=(30, 20))
plt.title('Geo-Coordinate', fontsize = 15)
for i, color in zip(range(len(geoCoord)), colors):
    if 47.60 < geoCoord[i][0] < 47.62 and -122.35 < geoCoord[i][1] < -122.33:
        plt.scatter(geoCoord[i][0], geoCoord[i][1], color=color, s=2)
# plt.show()
plt.savefig('fig.png')