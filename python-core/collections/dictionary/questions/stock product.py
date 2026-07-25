products={'Laptop':10,'Mouse':25,'Keyboard':15}
# Tasks:
# - Add Monitor:8
products['monitor']=8
# - Increase Mouse by 10
products['Mouse']=10
# - Print products with stock >10
for i in products:
    if products[i] > 10:
        print(i,':',products[i])