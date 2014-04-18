import sys
import rec
import load_files

if __name__ == "__main__":
    gamelist = sys.argv[1]
    out_file = open(sys.argv[2], "w")
    files = ["notas_parcial" + str(x) + ".txt" for x in range(1, int(sys.argv[3])+1)]
    load_files.load_files(files)
    items_to_calc = {}
    
    for item in open(gamelist):
        items_to_calc[item.replace("\n", "")] = 1
    
    rec.create_item_sim_table_save(load_files.item_based, items_to_calc, out_file)
    #print rec.recommend_item(load_files.user_based, item_sim_table, "jfjohnny5")
