from greenery import parse
#parse("^[^e]*$").difference(
for s in parse("~(.*e.*)")).strings():
    print(s)