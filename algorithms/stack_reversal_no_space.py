st = [1,2,3,4]

def st_rev(st):
    if st==[]:
        return []
    else:
        return [st.pop()]+st_rev(st)
