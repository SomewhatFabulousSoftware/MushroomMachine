# This is the file access code, which we will need to use for making 
# a config file, or a web interface
# write to file
with open("Measurements.txt", "w") as f:
    f.write("temp: " + str(temp_dirt) + "\nHumidity: " + str(relative_humidity))


with open("Measurements.txt", "r") as f:
    for line in f:
        split = line.split(": ")
        measurements.append(split[1].replace("\n", ""))
f.close()

