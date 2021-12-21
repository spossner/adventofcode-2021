if __name__ == '__main__':
    arr = list(range(1, 22))
    print(arr)
    n = 2
    for r in range(1,10):
        new_arr = []
        for i, v in enumerate(arr):
            if (i+1) % n != 0:
                new_arr.append(v)
        arr = new_arr
        print(f"{n}: {arr}")
        n = arr[r]
        if len(arr) <= 8:
            break
