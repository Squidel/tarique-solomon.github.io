def generateRefNum(lastRefNum):
    prefix = 'PSP'
    suffix = lastRefNum.split(prefix)[1]
    suffix = int(suffix) + 1
    suffix_padded = str(suffix).zfill(6)
    newRefNum = prefix + suffix_padded
    return newRefNum

