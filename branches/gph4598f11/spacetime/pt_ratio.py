def point_ratio:
   p_ratio = []
   for i in table:
        w = float(i[3])
        t = float(i[4])
        pt_ratio = w/t
        p_ratio.append([i[0], pt_ratio ])

