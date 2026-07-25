# 5. . Country Capitals
countries={'India':'New Delhi','Japan':'Tokyo','USA':'Washington','France':'Paris'}
# Tasks:
# - Add Germany:Berlin
countries['Germany']="Berlin"
# - Update USA capital
countries['USA']="Washington DC"
# - Delete France
countries.pop('France')
# - Print alphabetically
for i in sorted(countries):
    print(i,":",countries[i])    