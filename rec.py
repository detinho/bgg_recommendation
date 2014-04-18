from math import sqrt

prefs = {
    'u1': {'A': 5.0, 'B': 4.0, 'C': 3.0},
    'u2': {'B': 5.0, 'C': 4.0, 'D': 3.0},
    'u3': {'C': 5.0, 'D': 4.0, 'E': 3.0},
    'u4': {'A': 3.5, 'B': 3.5, 'C': 3.5},
    'u5': {'A': 5.0, 'B': 4.0, 'C': 3.0, 'F': 5.0},
    'u6': {'A': 5.0, 'G': 3}
}

def revert_prefs(prefs):
    ret = {}
    for user, ratings in prefs.items():
        for item, rate in ratings.items():
            ret.setdefault(item, {})
            ret[item][user] = rate
    return ret

def sim_euclidean(vet1, vet2):
    ret = sqrt(sum([pow(v1-v2,2) for v1, v2 in zip(vet1, vet2)]))
    return 1 / (1+ret)
    
def sim_cosine(v1, v2):
    """ cosO =     A.B
              ---------------
              ||A|| . ||B||
    """
    sumAB = sum([ai * bi for ai, bi in zip(v1, v2)])
    euclideanA = sqrt(sum([ai*ai for ai in v1]))
    euclideanB = sqrt(sum([bi*bi for bi in v2]))
    return sumAB / (euclideanA * euclideanB)

def top_matches(prefs, user, top=10, threshold=5, sim=sim_euclidean):
    matches = []
    user_prefs = prefs[user]
    for other, ratings in prefs.items():
        if user == other: continue

        ruser = []
        rother = []

        for item in ratings:
            if item in user_prefs:
                ruser.append(prefs[user][item])
                rother.append(prefs[other][item])
    
        if len(ruser) > threshold:
            similarity = sim(ruser, rother)
            matches.append((similarity, other))
    
    matches.sort(reverse=True)
    return matches[:top]
    
def create_item_sim_table(prefs):
    ret = {}
    reverted = revert_prefs(prefs)
    for item in reverted:
        ret[item] = top_matches(reverted, item, 10)
    
    return ret
    
def create_item_sim_table2(item_table):
    ret = {}
    total = len(item_table)
    current = 1
    for item in item_table:
        print "Building item sim table -> %d of %d: %s" % (current, total, item)
        ret[item] = top_matches(item_table, item, 10)
        current += 1
    
    return ret
    
def create_item_sim_table_save(item_table, items_to_calc, out_file):
    ret = {}
    total = len(item_table)
    current = 1
    for item in item_table:
        if item in items_to_calc:
            print "Building item sim table -> %d of %d: %s" % (current, total, item)
            ret[item] = top_matches(item_table, item, 50, 10, sim_cosine)
        else:
            print "Skiping %s" % item
        
        current += 1
    
    print "Saving..."
    for item, item_sim in ret.items():
        if item_sim:
            for sim, sim_item in item_sim:
                out_file.write("%s;%s;%f\n" % (item, sim_item, sim))
        else:
            out_file.write("%s;;\n" % item)
        out_file.flush()
    
    out_file.flush()
    out_file.close()

def get_top_items(prefs, user, k=5):
    def cmp_game(x, y):
        if x[1] > y[1]:
            return 1
        elif x[1] < y[1]:
            return -1
        else:
            return 0;
    
    items = prefs[user].items()
    items.sort(cmp=cmp_game, reverse=True)
    return items[:k]
    
def recommend_item(prefs, item_table, user):
    total_rates = {}
    total_sims = {}
        
    #for item, rate in prefs[user].items():
    for item, rate in get_top_items(prefs, user):
        sim_itens = item_table[item]

        for sim_rate, sim_item in sim_itens:
            if sim_item in prefs[user]:
                continue
            
            total_rates.setdefault(sim_item, 0.0)
            total_sims.setdefault(sim_item, 0.0)
            
            total_rates[sim_item] += rate * sim_rate
            total_sims[sim_item] += sim_rate
    
    ret = [(total_rate / total_sims[item], item) for item, total_rate in total_rates.items()]
    ret.sort(reverse=True)
    return ret

if __name__ == "__main__":
    #print top_matches(prefs, 'u1')
    #print revert_prefs(prefs)
    #print top_matches(revert_prefs(prefs), 'A')
    #print top_matches(revert_prefs(prefs), 'B')
    #print top_matches(revert_prefs(prefs), 'C')
    print create_item_sim_table(prefs)

    print top_matches(prefs, 'u1')
    print recommend_item(prefs, create_item_sim_table(prefs), 'u1')
