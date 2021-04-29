# print(clustering.labels_)
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