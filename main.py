from Code import channel_stats

channel_stats.dict_to_excel('Krish naik', channel_stats.required_stats)

for i, j in channel_stats.video_stats.items():
    print(i, "----->", j)
    print(len(j))

