import json

path_config_file = "config/config.json"
# Read file
f = open(path_config_file)

config_data = json.load(f)

f.close()

print(config_data['configLOLA']['extra'])

config_data['configLOLA']['extra'] = "huevos"




# Example with dumps
# Serializing json
json_object = json.dumps(config_data)

# Writing to config_new.json
with open("config/config_new.json", "w") as outfile:
    outfile.write(json_object)