def reverse(l, first=0, last=-1):
    if first >= len(l)/2: return
    l[first], l[last] = l[last], l[first]
    reverse(l, first+1, last-1)

mylist = list(range(20))
print(mylist)
reverse(mylist)
print(mylist)