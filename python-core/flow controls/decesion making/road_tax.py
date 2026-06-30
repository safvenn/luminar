#bike tax calculation


price = float(input("Enter price of bike: "))


if price > 100000:
    tax = price*15 / 100
elif price >= 50000:
    tax = price*10 /100
else:
    tax = price*5 / 100

print(f"your road tax is {tax}")
