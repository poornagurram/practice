a = "fa4chabc"
suba = "abc"

i=0
strt = 0
end = 0
count=0
subas = len(suba)
while end-1 != len(a):
    if a[strt:end] == suba[:count]:
        end = end+1
        count = count+1
    else:
        strt = strt+1
        end = strt
        count = 0

print(a[strt:end])
