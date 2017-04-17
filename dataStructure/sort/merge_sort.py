#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataStructure.basic.single_link_list import Node
from dataStructure.common.test_data import rand


def merge1(array, start, mid, end):
    left = array[start:mid + 1]
    right = array[mid + 1:end + 1]
    i = 0
    j = 0
    k = start
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            array[k] = left[i]
            i += 1
        else:
            array[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        array[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        array[k] = right[j]
        j += 1
        k += 1


def msort1(array, start=0, end=-1):
    if end == -1:
        end = len(array) - 1
    if start < end:
        mid = (start + end) / 2
        msort1(array, start, mid)
        msort1(array, mid + 1, end)
        merge1(array, start, mid, end)


def merge2(array, left, right):
    # 简洁版
    i = 0
    while left != [] and right != []:
        array[i] = left.pop(0) if left[0] < right[0] else right.pop(0)
        i += 1
    array[i:] = left if left != [] else right


def msort2(array):
    # 简洁版
    n = len(array)
    if n > 1:
        left = [x for x in array[:n / 2]]
        right = [x for x in array[n / 2:]]
        left = msort2(left)
        right = msort2(right)
        merge2(array, left, right)
    return array


def merge3(array, left, mid, right):
    # 原地归并, 空间left\mid\right 为边界指针
    pass


def msort4(xs):
    # 链表的归并,空间复杂度O(1),不用另申请内存,时间复杂度O(nlogn)
    if isinstance(xs, list):  # 统一参数输入格式,方便测试和性能比较
        head = tx = Node(xs[0])
        for i in xs[1:]:
            tx.next = Node(i)
            tx = tx.next
        xs = head

    if xs is None or xs.next is None:
        return xs
    ax = None
    bx = None
    while xs:
        p = xs
        xs = xs.next
        p.next = ax  # 把pop(lklist) 加入到ax 的头部
        ax = p
        ax, bx = bx, ax
    ax = msort4(ax)
    bx = msort4(bx)
    return merge4(ax, bx)


def merge4(ax, bx):
    s = p = Node()
    while (ax and bx):
        if ax.key < bx.key:
            p.next = ax
            ax = ax.next
        else:
            p.next = bx
            bx = bx.next
        p = p.next
    if ax:
        p.next = ax
    if bx:
        p.next = bx
    return s.next


def msort5(array):
    # 2017-04-01
    # 自然归并排序
    # 迭代合并
    # 从两头找最长有序子数列,归并到工作区数组,然后交换原数组和工作区
    if len(array) <= 1:
        return array
    n = len(array)
    array_b = [None] * n
    while True:
        a = 0  # 0-a 已扫描
        b = 0  # a-b 正扫描
        c = n  # b-c 下轮
        d = n  # c-d 正扫描, d-n 已扫描
        f = 0  # 0-f 已归并
        r = n - 1  # f-r 未使用, r-n 已归并
        t = True  # 从front 归并还是从 rear归并
        while b < c:
            b += 1
            while b < c and array[b] >= array[b - 1]:
                b += 1
            c -= 1
            while c > b and array[c - 1] >= array[c]:
                c -= 1
            if c < b:
                c = b
            if b - a >= n:
                return array
            if t:
                f = merge5(array, a, b, c, d, array_b, f, 1)
            else:
                r = merge5(array, a, b, c, d, array_b, r, -1)
            a = b
            d = c
            t = False if t else True
        array, array_b = array_b, array
    return array


def merge5(array, a, b, c, d, array_b, w, delta):
    while a < b and c < d:
        if array[a] < array[d - 1]:  # 从两边往中间归并
            array_b[w] = array[a]
            a += 1
        else:
            array_b[w] = array[d - 1]
            d -= 1
        w += delta
    while a < b:
        array_b[w] = array[a]
        a += 1
        w += delta
    while d > c:
        array_b[w] = array[d - 1]
        d -= 1
        w += delta
    return w


def msort6(array):
    # 2017-04-05
    # 自底向上排序,每次从头部取出一对子列表,排序后追加到尾部
    # 迭代合并
    array = [[x] for x in array]
    while len(array) > 1:
        array.append(merge6(array.pop(0), array.pop(0)))
    return [] if array == [] else array.pop()


def merge6(xs, ys):
    zs = []
    while xs != [] and ys != []:
        zs.append(xs.pop(0) if xs[0] < ys[0] else ys.pop(0))
    return zs + (xs if xs != [] else ys)


def test(randlist=rand):
    array1 = list(randlist)
    array2 = list(randlist)
    array5 = list(randlist)
    array6 = list(randlist)
    print 'rand:    ', randlist
    msort1(array1)
    print 'array1:  ', array1
    array2 = msort2(array2)
    print 'array2:  ', array2

    head = tx = Node(None)
    for i in rand:
        tx.next = Node(i)
        tx = tx.next
    tx = msort4(head)
    array4 = []
    while tx.next:
        array4.append(tx.next.key)
        tx = tx.next
    print 'array4:  ', array4

    array5 = msort2(array5)
    print 'array5:  ', array5

    array6 = msort2(array6)
    print 'array5:  ', array6

    print 'sorted:  ', sorted(randlist)
    assert array1 == array2 == array4 == array5 == array6 == sorted(randlist)


if __name__ == '__main__':
    test(rand)
