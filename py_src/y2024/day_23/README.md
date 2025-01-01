# approach

kh -> {'ta', 'tc', 'ub'}
tc -> {'td'}
qp -> {'kh', 'ub'}
de -> {'ta', 'cg', 'co'}
cg -> {'tb'}
ka -> {'de', 'co'}
co -> {'tc'}
yn -> {'aq', 'cg'}
aq -> {'cg'}
ub -> {'vc'}
tb -> {'vc', 'wq', 'ka'}
vc -> {'aq'}
wh -> {'qp', 'yn', 'tc', 'td'}
ta -> {'co', 'ka'}
td -> {'yn', 'qp'}
wq -> {'vc', 'aq', 'ub'}

aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq

python py_src/y2024/day_23/day.py 8.19s user 0.19s system 95% cpu 8.811 total max RSS 419200

cliques

----------------------------------------------------------------------------------------------------------------------------------- Captured stdout call -----------------------------------------------------------------------------------------------------------------------------------
['kh', 'tc']
x ['kh', 'ub', 'qp']
['kh', 'ta']
x ['wq', 'vc', 'ub']
x ['wq', 'vc', 'aq']
x ['wq', 'vc', 'tb']
x ['td', 'wh', 'tc']
x ['td', 'wh', 'yn']
x ['td', 'wh', 'qp']
x ['aq', 'cg', 'yn']
['ka', 'de', 'co', 'ta']
['ka', 'tb']
['cg', 'tb']
['cg', 'de']
['co', 'tc']

x aq,cg,yn
x aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
x kh,qp,ub
x qp,td,wh
x tb,vc,wq
x tc,td,wh
x td,wh,yn
x ub,vc,wq

python py_src/y2024/day_23/day.py 0.35s user 0.07s system 70% cpu 0.595 total max RSS 67664

triads: python py_src/y2024/day_23/day.py 11.43s user 0.16s system 97% cpu 11.886 total max RSS 284272
