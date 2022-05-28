def solution(minterm):
    answer = []
    var = [[] for i in range(minterm[0] + 1)]
    mintermList = []
    for i in range(minterm[1]):  # minterm[0] : variable 개수 minterm[1] : minterm 개수
        minterm[i + 2] = format(minterm[i + 2], "b")
        while (len(minterm[i + 2]) < minterm[0]):
            minterm[i + 2] = "0" + minterm[i + 2]
        if (minterm[i + 2].count("1") == 0):
            var[0].append(minterm[i + 2])
        elif (minterm[i + 2].count("1") == 1):
            var[1].append(minterm[i + 2])
        elif (minterm[i + 2].count("1") == 2):
            var[2].append(minterm[i + 2])
        elif (minterm[i + 2].count("1") == 3):
            var[3].append(minterm[i + 2])
        elif (minterm[i + 2].count("1") == 4):
            var[4].append(minterm[i + 2])
        elif (minterm[i + 2].count("1") == 5):
            var[5].append(minterm[i + 2])
        elif (minterm[i + 2].count("1") == 6):
            var[6].append(minterm[i + 2])
        i += 1
    mintermList = sum(var, [])
    # print(mintermList)
    # print(var)
    resPi = []
    res, pi = find_combine(var)
    resPi += pi
    while (True):
        res, pi = find_combine(res)
        resPi += pi
        if not res:
            break
    resPi = set(resPi)
    resPi = list(resPi)
    cnt = 1
    while True:
        print("case", cnt)
        epi, remove_min = findEPI(resPi, mintermList)
        answer += epi
        print("pi, minterm :", resPi, mintermList)
        for i in epi:
            if i in resPi:
                resPi.remove(i)
        for i in remove_min:
            if i in mintermList:
                mintermList.remove(i)
        print("epi, minterm :", epi, mintermList)
        dominanced_PI = row_dominance(resPi, mintermList)
        for i in dominanced_PI:
            if i in resPi:
                resPi.remove(i)
        dominanced_min = column_dominance(resPi, mintermList)
        for i in dominanced_min:
            if i in mintermList:
                mintermList.remove(i)
        if not dominanced_min and not dominanced_PI:
            break
        cnt += 1
    if mintermList:
        print("Petrick's Method needed!!!")
        print("EPI and Secondary EPI:", answer)
    else:
        print("All Minterm Covered!!!")
        print("EPI and Secondary EPI:", answer)
    # answer = sortPi(resPi)
    # answer.append("EPI")
    # answer += epi
    # print("answer = ", answer)
    return answer


def find_combine(it):  # it는 variable들의 list
    list = it
    checkedList = sum(it, [])

    piList = []
    # print(list)
    for i in range(len(list)):
        for j in list[i]:
            if (i == len(list) - 1):  # 마지막 리스트는 더하면 index out of range
                continue
            else:
                for k in list[i + 1]:
                    if k.find("-") != j.find("-"):
                        continue
                    if k.find("-") == j.find("-"):
                        c = "-"
                        comp1 = []
                        comp2 = []
                        for pos, char in enumerate(j):
                            if (char == c):
                                comp1.append(pos)
                        for pos, char in enumerate(k):
                            if (char == c):
                                comp2.append(pos)
                        # print(comp1,comp2)
                        if (comp1 != comp2):
                            continue
                    comp_min = [ord(a) ^ ord(b) for a, b in zip(j, k)]  # 문자열 비트단위로 XOR 계산
                    # print(comp_min,j,k)
                    if (comp_min.count(1) == 1):  # HD가 1일때 위치도 같을때 추가해야함!!!!
                        if j in checkedList:
                            checkedList.remove(j)
                            # checkedList.remove(k)
                        if k in checkedList:
                            checkedList.remove(k)
                        # print(comp_min, j, k, i)
                        # print(checkedList)
                        idx = comp_min.index(1)  # 그 인덱스 찾아서 -로 바꿔주기
                        k = k[:idx] + "-" + k[idx + 1:]
                        if k not in piList:
                            piList.append(k)

    # print(checkedList)
    newVar = [[] for i in range(len(list) - 1)]
    for i in range(len(piList)):
        if (piList[i].count("1") == 0):
            newVar[0].append(piList[i])
        elif (piList[i].count("1") == 1):
            newVar[1].append(piList[i])
        elif (piList[i].count("1") == 2):
            newVar[2].append(piList[i])
        elif (piList[i].count("1") == 3):
            newVar[3].append(piList[i])
        elif (piList[i].count("1") == 4):
            newVar[4].append(piList[i])
        elif (piList[i].count("1") == 5):
            newVar[5].append(piList[i])
        elif (piList[6].count("1") == 6):
            newVar[6].append(piList[i])
        i += 1

    # print("newVar : ",newVar)
    # print("checkedList : "  ,checkedList)
    # print("piList: ",piList)
    # print("list : ",list)
    return newVar, checkedList


def sortPi(resPi):
    sortRes = []
    for i in resPi:
        i = i.replace("-", "2")
        sortRes.append(i)
    resPi = []
    sortRes.sort()
    for i in sortRes:
        i = i.replace("2", "-")
        resPi.append(i)

    return resPi


def comparePI(r, m):
    numList = []
    combineList = []
    for i in m:
        for j in range(len(r)):
            a = r[j]
            for k in range(len(r[j])):
                if r[j][k] == "-":
                    # print(r[j],i)
                    a = a.replace("-", i[k], 1)
                    #print("i:",i,"r[j]:", r[j], a)
            if (a == i):
                #print("a:",a,"r[j]:", r[j])
                numList.append(a)
                combineList.append(r[j])
    # print("numList: ",numList)
    # print("combineList: ", combineList)
    return numList, combineList


def findEPI(resPi, mintermList):
    r = resPi[:]
    m = mintermList[:]
    epiList = []
    numList, combineList = comparePI(r, m)
    usedMinterm = []
    for i in numList:
        if numList.count(i) == 1:
            epiValue = combineList[numList.index(i)]
            if combineList[numList.index(i)] not in epiList:
                epiList.append(epiValue)
    for i in epiList:
        for j in range(len(combineList)):
            if i == combineList[j]:
                usedMinterm.append(numList[j])
    # print("epiList:", epiList)
    # print("usedMinterm:", usedMinterm)
    return epiList, usedMinterm


def row_dominance(resPi, mintermList):
    print("rd check...")
    n, c = comparePI(resPi, mintermList)
    rowList = [[] for i in range(len(resPi))]
    for i in range(len(resPi)):
        rowList[i].append(resPi[i])
    #print("rowList:",rowList)
    for i in resPi:
        for j in range(len(c)):
            if i == c[j]:
                for k in rowList:
                    if i in k:
                        k.append(n[j])
    #print("rowList:",rowList)
    row_eraseList = []
    for i in rowList:
        for j in range(len(rowList)):
            if i[0] != rowList[j][0]:
                row_intersection = list(set(i) & set(rowList[j]))
                #print("row_intersection:",row_intersection)
                if sorted(row_intersection) == sorted(i[1:]):
                    if rowList[j][0] in row_eraseList:          #interchangable 제외 위함
                        continue
                    print(i[0], "dominated by", rowList[j][0])
                    if i[0] in row_eraseList:                   #rd가 여러번 일어나는 것을 방지하기 위함
                        continue
                    row_eraseList.append(i[0])
    print("rd:", row_eraseList, "will be erased")
    return row_eraseList


def column_dominance(resPi, mintermList):
    print("cd check...")
    n, c = comparePI(resPi, mintermList)
    #print(n, c)
    columnList = [[] for i in range(len(mintermList))]
    for i in range(len(mintermList)):
        columnList[i].append(mintermList[i])
    for i in mintermList:
        for j in range(len(n)):
            if i == n[j]:
                for k in columnList:
                    if i in k:
                        k.append(c[j])
    #print("columnList:",columnList)
    column_eraseList = []
    for i in columnList:
        for j in range(len(columnList)):
            if i[0] != columnList[j][0]:
                column_intersection = list(set(i) & set(columnList[j]))
                # print(i, columnList[j], column_intersection)
                if sortPi(column_intersection) == sortPi(i[1:]):
                    if i[0] in column_eraseList:
                        continue
                    print(i[0], "dominated by", columnList[j][0])
                    if columnList[j][0] in column_eraseList:
                        continue
                    column_eraseList.append(columnList[j][0])
    print("cd:", column_eraseList, "will be erased")
    return column_eraseList


solution([4, 13, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
print("finished")
solution([4, 8, 0, 4, 8, 10, 11, 12, 13, 15])
print("finished")
solution([4, 11, 0, 2, 5, 6, 7, 8, 10, 12, 13, 14, 15])
print("finished")