"""Need input table and distance table for inputs"""

"""import calc_total_ratio"""

def calc_likelihood_ratios:
    likelihood_ratios = []
    for i in distances:
        for j in table:
            if i[2] == j[0]:
                nz = float(j[1])
                mz = float(j[4]) * outside_total_ratio
                bigN = totalpop_total
                hyp_test = "Accept Null"
                if nz > mz:
                    hyp_test = "Reject Null"
                likeratio = ((nz/mz)**nz)*(((bigN-nz)/(bigN-mz))**(bigN-nz))
                likelihood_ratios.append([i[0], i[2], likeratio, hyp_test ])

for i in likelihood_ratios:
    print i
