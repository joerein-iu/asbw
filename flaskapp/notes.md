use teams runs per game and runs against per game
create runs per inning
home team has a 3% advantage
make a score based of the rpi/avg_rpi and rapi/avg_rapi

then take team att * team def * average runs  * sqrt(1 + 3%) for home

away is att * def * average runs * (1/sqrt(1 +  3%))

prob dist

simulate box score


https://www.youtube.com/watch?v=a8uloqcqjso

has the whole formula

need m n p b
m = -0.01219
n = -1.813
p = -0.3865
b = -1.042

yeah i have no idea just convert it to code
