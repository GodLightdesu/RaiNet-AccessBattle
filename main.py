from rainet import Rainet

# game init
blue_init = ['L', 'L', 'V', 'V', 'V', 'V', 'L', 'L']
yellow_init = ['l', 'l', 'v', 'v', 'v', 'v', 'l', 'l']
rainet = Rainet(blue_init, yellow_init)

# duel
rainet.play()