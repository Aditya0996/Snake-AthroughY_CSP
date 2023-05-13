import copy


def backtrack(grid, constraintMatrix, domains, alphabetsRemaining):
    # find the cell with the minimum remaining values
    index, min_values = getMRV(grid, domains)
    # if there are no empty cells, we're done
    if min_values == float('inf'):
        return True
    # try each possible value for the cell with the minimum remaining values, in LCV order
    possible_values = getLCV(index[0], index[1], grid, constraintMatrix, domains, alphabetsRemaining)
    if not possible_values:
        return False
    for value in possible_values:
        grid[index[0]][index[1]] = value
        alphabetsRemainingCopy = copy.deepcopy(alphabetsRemaining)
        alphabetsRemainingCopy.remove(value)
        domains, alphabetsRemainingCopy = findDomain(alphabetsRemainingCopy, constraintMatrix, grid)
        # try to fill out the rest of the grid
        if backtrack(grid, constraintMatrix, domains, alphabetsRemainingCopy):
            return grid
        # if we couldn't fill out the rest of the grid, backtrack
        grid[index[0]][index[1]] = '-'
    return False


def getMRV(grid, domains):
    mrvList = []
    mrvIndex = (-1, -1)
    blankMin = float('inf')
    for i in range(5):
        row = []
        for j in range(5):
            if grid[i][j] == "-":
                blanks = 0
                if i < 4 and grid[i + 1][j] == "-":
                    blanks += 1
                if j < 4 and grid[i][j + 1] == "-":
                    blanks += 1
                if i > 0 and grid[i - 1][j] == "-":
                    blanks += 1
                if j > 0 and grid[i][j - 1] == "-":
                    blanks += 1
                if blanks < blankMin:
                    blankMin = blanks
                    mrvIndex = (i, j)
                row.append(blanks)
                if blankMin == float('inf'):
                    blankMin = 100
        mrvList.append(row)
    return mrvIndex, blankMin


def findDomain(alphabets, constraintsMatrix, grid):
    domains = {}
    for i in range(5):
        for j in range(5):
            domain = getDomain(i, j, grid, constraintsMatrix, alphabets)
            domains[(i, j)] = domain
    return domains, alphabets


def getDomain(i, j, grid, constraintsMatrix, alphabetsRemaining, recursive= True):
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y']
    domain = []
    neighbours = []
    adjacentAlphabet = False
    constraintDomain = []
    for constraints in constraintsMatrix[i][j]:
        if grid[constraints[0]][constraints[1]] != "-":
            # index = alphabets.index(grid[constraints[0]][constraints[1]])
            # if index < 24 and (alphabets[index + 1] in alphabetsRemaining):
            #     constraintDomain.append(alphabets[index + 1])
            # if index > 0 and (alphabets[index - 1] in alphabetsRemaining):
            #     constraintDomain.append(alphabets[index - 1])
            # for constrain in constraintsMatrix[constraints[0]][constraints[1]]:
            #     if grid[constrain[0]][constrain[1]] not in constraintDomain:
            #         adjacentAlphabet = True
            #         neighbours.append(grid[constraints[0]][constraints[1]])
            #         break
            adjacentAlphabet = True
            neighbours.append(grid[constraints[0]][constraints[1]])

    if adjacentAlphabet:
        for neighbour in neighbours:
            index = alphabets.index(neighbour)
            if index < 24 and (alphabets[index + 1] in alphabetsRemaining):
                domain.append(alphabets[index + 1])
            if index > 0 and (alphabets[index - 1] in alphabetsRemaining):
                domain.append(alphabets[index - 1])
    else:
        domain.append(alphabetsRemaining)
    return domain


def getLCV(i, j, grid, constraintMatrix, domains, alphabetsRemaining):
    gridCopy = copy.deepcopy(grid)
    domain = domains[(i, j)]
    value = []
    if grid[i][j] == "-" and len(domain) >= 1:
        for d in domain:
            gridCopy[i][j] = d
            tempValue = []
            for constraint in constraintMatrix[i][j]:
                newDomain = getDomain(constraint[0], constraint[1], gridCopy, constraintMatrix,
                                      alphabetsRemaining)
                tempValue.append(len(newDomain))
            value.append((d, min(tempValue)))
        value.sort(key=lambda k: k[1], reverse=True)
        return [t[0] for t in value]
    return False


def select_unassigned_variable(grid):
    for i in range(5):
        for j in range(5):
            if grid[i][j] == '-':
                return i, j


def main():
    grid = [['-', '-', '-', '-', 'Y'],
            ['R', 'A', '-', '-', '-'],
            ['-', '-', '-', '-', '-'],
            ['-', 'E', '-', '-', '-'],
            ['-', '-', '-', '-', 'K']]

    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y']
    # adjacency constraints
    constraintsList = []
    for i in range(5):
        for j in range(5):
            if grid[i][j] != "-":
                alphabets.remove(grid[i][j])
            constraints = []
            if i < 4:
                constraints.append([i + 1, j])
            if j < 4:
                constraints.append([i, j + 1])
            if i > 0:
                constraints.append([i - 1, j])
            if j > 0:
                constraints.append([i, j - 1])
            constraintsList.append(constraints)
    constraintsMatrix = []
    for i in range(0, len(constraintsList), 5):
        constraintsMatrix.append(constraintsList[i:i + 5])
    domains, alphabets = findDomain(alphabets, constraintsMatrix, grid)
    result = backtrack(grid, constraintsMatrix, domains, alphabets)
    if result:
        for row in result:
            print(row)
    else:
        print("No solution found")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
