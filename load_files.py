import sys

user_based = {}
item_based = {}
item_sim = {}

def load_files(files):
    for file_name in files:
        load_file(file_name)
        
def load_file(file_name):
    for line in open(file_name):
        user, game, rating = line.split(";")
        game = game.split("/")[-2:]
        game = "/".join(game)
        rating = float(rating)
        
        user_based.setdefault(user, {})
        item_based.setdefault(game, {})
        
        user_based[user][game] = rating
        item_based[game][user] = rating
        
def create_game_list():
    gamelist = open("gamelist.txt", "w")
    for game in item_based.keys():
        gamelist.write(game + "\n")
    gamelist.flush()
    gamelist.close();
    
def load_item_sim_table(files):
    for file_name in files:
        for line in open(file_name):
            line = line.replace("\n", "")
            game, sim_game, sim = line.split(";")
            
            item_sim.setdefault(game, [])
            
            if sim:
                sim = float(sim)                
                item_sim[game].append((sim, sim_game))

if __name__ == "__main__":
    files = ["notas_parcial" + str(x) + ".txt" for x in range(1, int(sys.argv[1])+1)]
    
    load_files(files)
    create_game_list()
    print user_based["jfjohnny5"]
