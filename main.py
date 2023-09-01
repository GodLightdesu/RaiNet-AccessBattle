from rainet import Rainet
import sys

path = './output.txt'
sys.stdout = open(path, 'w')

# game init
# please note that only can place 4 virus and 4 link
human_init = ['L', 'L', 'V', 'V', 'V', 'V', 'L', 'L']
ai_init = ['l', 'l', 'v', 'v', 'v', 'v', 'l', 'l']
rainet = Rainet(human_init, ai_init)

# duel
# rainet.print_game_info()
rainet.play()