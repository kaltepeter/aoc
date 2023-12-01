from scipy.stats import linregress

point1 = (-1, 7)
point2 = (8, -2)

x1, y1 = point1
x2, y2 = point2

slope, intercept, r_value, p_value, std_err = linregress([x1, x2], [y1, y2])
print(slope, intercept)
