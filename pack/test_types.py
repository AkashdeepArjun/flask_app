
data = [True,1,"akash",3.15,set([1,2,3]),{1: "one", 2: "two"},(1,2,3),[1,2,3],None]

for d in data:
    print(f"Value: {d}, Type: {type(d)}")


print(type(1)!=int)