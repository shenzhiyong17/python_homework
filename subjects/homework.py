#!/usr/bin/python

def san1(num=9):
    print 'san1:'
    for i in range(num):
        print '*' * (i + 1)


def san2(num=9):
    print 'san2:'
    for i in range(num):
        print ' ' * (num - i) + '*' * (i + 1)


def san3(num=9):
    print 'san3:'
    for i in range(num):
        j = num - i
        print '*' * j


def san4(num=9):
    print('san4:')
    for i in range(num):
        print(' ' * i + '*' * (num - i))


def san5(num=10):
    print('san5:')
    for i in range(1, num + 1):
        print(' ' * (num - i) + '*' * (2 * i - 1))


def san6(num=9):
    print('san6:')
    print(' ' * (num - 1) + '*')
    for i in range(2, num):
        front = (num - i)
        middle = (i * 2) - 3
        print(' ' * front + '*' + ' ' * middle + '*')
    print('* ' * (num))


def ling(num=10):
    san6(num)
    for i in range(1, num + 1):
        print(' ' * i + '*' * (2 * (num - i) - 1))


def su(num):
    if not isinstance(num, int):
        return str(num) + ' is not a int'
    elif num <= 1:
        return 'number must > 1'
    for i in range(2, int(num / 2 + 1)):
        if (num % i) == 0:
            print ' is not sushu'
    print str(num), " is sushu"
    return num


def psu(num):
    su = []
    for n in range(2, num + 1):
        for i in range(2, n):
            if (n % i) == 0:
                break
        su.append(n)
    print(su)


import math


def sphere(R):
    times = 2
    for l in range(R):
        h = R - l
        #        r=int(((R*R)-(h*h))**0.5*times)
        r = int(math.sqrt((R * R) - (h * h)) * times)
        s = times * R - r
        print(' ' * int(s) + '*' * 2 * r)
    for h in range(R):
        l = R - h
        r = int(((R * R) - (h * h)) ** 0.5 * times)
        s = times * R - r
        print(' ' * int(s) + '*' * 2 * r)


def circle(R):
    times = 2
    for l in range(R):
        h = R - l
        #        r=int(((R*R)-(h*h))**0.5*times)
        r = int(math.sqrt((R * R) - (h * h)) * times)
        s = times * R - r
        #        space=str(' '*r+'$'*(r-2))
        space = str(' ' * (2 * r - 2))
        print(' ' * int(s) + '*' + space + '*')
    for h in range(R):
        l = R - h
        #        r=int(((R*R)-(h*h))**0.5*times)
        r = int(math.sqrt((R * R) - (h * h)) * times)
        s = times * R - r
        print(' ' * int(s) + '*' * 2 * r)


def quicksort(list, left, right):
    if left < right:
        i = left
        j = right
        p = list[left]
        while i < j:
            i += 1
            while list[i] < p and i < len(list) - 1:
                i += 1
            while list[j] > p:
                j -= 1
            if i < j:
                tmp = list[i]
                list[i] = list[j]
                list[j] = tmp
        list[left] = list[j]
        list[j] = p
        quicksort(list, left, j - 1)
        quicksort(list, j + 1, right)


def merge(list, start, mid, end):
    left = list[start:mid + 1]
    right = list[mid + 1:end + 1]
    i = 0
    j = 0
    k = start
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            list[k] = left[i]
            i += 1
            k += 1
        elif left[i] > right[j]:
            list[k] = right[j]
            j += 1
            k += 1
    while i < len(left):
        list[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        list[k] = right[j]
        j += 1
        k += 1


def mergesort(list, start, end):
    if start < end:
        mid = (start + end) / 2
        mergesort(list, start, mid)
        mergesort(list, mid + 1, end)
        merge(list, start, mid, end)


if __name__ == '__main__':
    san1()
    san2()
    san3()
    san4()
    san5()
    san6()
    ling()
    su(9)
    psu(10)
    sphere(20)
    circle(20)
    input()
    list = [9, 6, 5, 4, 3, 2, 1, 7]
    quicksort(list, 0, len(list) - 1)
    mergesort(list, 0, len(list))
    print list
