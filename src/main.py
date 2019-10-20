print("Pyrogue : la commutativité de l’anneau")

from Character import Character

jeanEude = Character()

jeanEude.print()
jeanEude.gain_xp(101)
jeanEude.print()

for i in range(10):
    jeanEude.take_damage(2)
    jeanEude.print()









