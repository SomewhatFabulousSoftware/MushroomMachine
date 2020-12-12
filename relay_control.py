import qwiic_relay
MAX_TEMP = 23
MAX_HUM = 80
MIN_TEMP = 18
MIN_HUM = 50

def main():

    measurements = []

    myRelay = qwiic_relay.QwiicRelay(0x6D)
    myRelay.begin()

    with open("Measurements.txt", "r") as f:
        for line in f:
            split = line.split(": ")
            measurements.append(split[1].replace("\n", ""))
    f.close()

    if (float(measurements[0]) < MIN_TEMP):
        myRelay.set_relay_on(1)
    if (float(measurements[1]) < MIN_HUM):
        myRelay.set_relay_on(2)
    if (float(measurements[0]) > MAX_TEMP):
        myRelay.set_relay_off(1)
    if (float(measurements[1]) > MAX_HUM):
        myRelay.set_relay_off(2)

if __name__ == "__main__":
    main()
