nums=[5,1,9,2]
result=sorted(nums,key=lambda x:x)
print(result)


nums=[5,1,9,2]
result=sorted(nums,key=lambda x:-x)
print(result)


words=["apple","kiwi","banana"]
result=sorted(words,key=lambda x:len(x))
print(result)


students=[{"name":"Ali","score":88},{"name":"Dana","score":95},{"name":"Max","score":70}]
result=sorted(students,key=lambda x:x["score"])
print(result)


pairs=[(1,3),(2,1),(4,2)]
result=sorted(pairs,key=lambda x:x[1])
print(result)
