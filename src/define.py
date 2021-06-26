class Define:
    default = "default"


class Crossover(Define):
    name = "crossover"
    pmx = "pmx"
    ox = "ox"


class Mutation(Define):
    name = "mutation"
    tpe = "tpe"
    insert = "insert"
    sub_reverse = "sub_reverse"


class Selection(Define):
    name = "selection"
    roulette = "roulette"
    champion2 = "champion2"
