from rainet import Rainet

# game init
# please note that only can place 4 virus and 4 link
blue_init = ['L', 'L', 'V', 'V', 'V', 'V', 'L', 'L']
yellow_init = ['l', 'l', 'v', 'v', 'v', 'v', 'l', 'l']
rainet = Rainet(blue_init, yellow_init)

# duel
# rainet.print_game_info()
rainet.play()