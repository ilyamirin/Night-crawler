import googlesearch as gs

if __name__ == '__main__':
    query = input('Запрос:\n')

path = 'scraped_links/' + query

with open(path,'w') as file:
    num = 0
    for i in gs.search(query,num = 10, stop = 100):
        num += 1
        if num % 10 == 0:
            print(num)
        file.write(i)
        file.write('\n')
#1 opinion on technological progress
#2 advantages and disadvantages of living in the city
        
#3 advantages and disadvantages of social networks
#4 advantages and disadvantages of friendship
#5 advantages and disadvantages of reading books
#6 what you can and cannot do while raising a child

#7 safe childhood (bad)
#8 pros and cons of university education (bad)
#9 advantages and disadvantages of university educating (bad)
#10 advantages and disadvantages of gaming
#11 pros and cons of fashion trends
#12 pros and cons of listening to music
#13 importance of the museums
#14 pros and cons of being a teacher
#15 how sport can influence a persons life

#16 advantages of zoos?  ++
#17 how to choose future profession?
#18 importance of space exploration? -
#19 is it good to be rich?
#20 the impact of machines on humanity 
#21 reasons to love football-
#22 reasons to go to the cinema-
#23 reasons to become a vegetarian+
#24 harm caused by corruption+
#25 the most important thing in live 
#26 is manga better than anime
#27 pros and cons of watching anime
#28 money for happiness 
#29 advantages of being the teenager
#30 pros and cons of the internet
#31 modern art