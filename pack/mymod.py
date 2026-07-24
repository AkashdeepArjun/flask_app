
def linear_search(arr:list[int],index,key)->int:
    if arr[index] ==key:
        return index
    elif index == len(arr)-1:
        return -1
    else: 
        return linear_search(arr,index+1,key)