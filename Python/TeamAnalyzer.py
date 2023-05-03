import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

    conn = sqlite3.connect('../pokemon.sqlite')
    c = conn.cursor()

    #Here i am getting the name of the pokemon from its pokedex_number
    c.execute("SELECT name FROM pokemon WHERE pokedex_number = ?", (arg,))
    pokemon_name = c.fetchone()

    #Then the code will use the name to get the pokemon's types 
    c.execute("SELECT type1, type2 FROM pokemon_types_view WHERE name = ?", pokemon_name)
    results = c.fetchone()
    type1 = results[0]
    type2 = results[1]
    
   #Creating empty arrays that will hold pokemon's strengths and weaknesses 
    strengths = []
    weakness = []


    #Then it loops through all the types and finds pokemon's attack value
    for x in types:
        c.execute("SELECT against_" + x + " FROM battle WHERE type1name = ? AND type2name = ?", (type1, type2))
        against = c.fetchone()[0]
        
        #checks if it is a strength or weakness
        if against >  1.0:
            strengths.append(x)
        elif against <  1.0:
            weakness.append(x)


    #put it all together
    print(str(pokemon_name) + "(" + str(type1) + " " + str(type2) + ") is strong against " + str(strengths) + " but weak against " + str(weakness))

    c.close()
    conn.close()

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

