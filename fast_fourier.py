#THIS DOES NOT RUN IN FFT EFFICIENCY
#This is only used to create output of a matrix during FFT!

#creating in n^2 to demonstrate
def create_starting_matrix(a, n, z):
    return [[(a**(i*e))% z for e in range(n)]for i in range(n)]

def new_rearrange_matrix(matrix):
    re_matrix = []
    width = len(matrix[0])
    
    #get rearranged TL - half rows and hopping cols
    for row in range(len(matrix)//2):
        for hop in range(0, len(width), 2):
            re_matrix.append(matrix[row][hop])

    #get z/y - first odd row
    zy = [row[1] for row in matrix]

    return

def rearrange_matrix(matrix):
    return [rearrange_c(row) for row in matrix]

def rearrange_c(c):
    i = len(c) - 1
    odd = []
    for e in c[::-1]:
        if i % 2 != 0:
            odd.append(e)
            c.pop(i)
        i -= 1
    c.extend(odd[::-1])
    return c

def multMatrixCol(matrix, col, mod):
    product = []
    for r in matrix:
        total = 0
        for i, c in enumerate(r):
            total += r[i] * col[i]
        product.append(total % mod)
    return product

def multColCol(a, b, mod):
    return [(a[i] * b[i]) % mod for i in range(len(a))]

def addColCol(a, b, mod):
    return [(a[i] + b[i]) % mod for i in range(len(a))]

def recursive_fft(n_width, matrix, c, mod):

    if len(matrix) <= n_width:#base case - n width reached
        print('base case matrix:')
        for i in matrix: print(i)
        print('\nbase case c: ', c, '\n')
        return multMatrixCol(matrix, c, mod)
    else:
        #rearrange matrix  / c
        matrix = rearrange_matrix(matrix)
        c = rearrange_c(c)
        print('rearranged matrix')
        for i in matrix: print(i)
        print('\nc: ', c, '\n')
    
        #split and send down
        mid = len(matrix) // 2
        split_matrix = [[n for n in row[:mid]]for row in matrix[:mid]]
        split_c = c[:mid]
        tl_v = recursive_fft(n_width, split_matrix, split_c, mod)
    

    topLeftQuadrant = [[n for n in row[:mid]]for row in matrix[:mid]]

    z = [row[mid] for row in matrix[:mid]]
    y = [row[mid] for row in matrix[mid:]]
    v = c[:mid]
    w = c[mid:]

    tl_w = multMatrixCol(topLeftQuadrant, w, mod)   #multiply


    tl_w_z = multColCol(tl_w, z, mod)               #multiply
    tl_w_z__tl_v = addColCol(tl_w_z, tl_v, mod)

    tl_w_y = multColCol(tl_w, y, mod)               #multiply
    tl_w_y__tl_v = addColCol(tl_w_y, tl_v, mod)

    return tl_w_z__tl_v + tl_w_y__tl_v


a, n, z = 6, 12, 13
starting_matrix = create_starting_matrix(a, n, z)
c = [4, 3, 7, 8, 2, 9, 5, 11, 6, 10, 1, 12]

for i in starting_matrix: print(i)

print('\nc: ', c, '\n')
print(recursive_fft(3, starting_matrix, c, z))

