from basic_3 import basic

if __name__ == '__main__':

    s = "ACGT"
    t = "AGCT"
    result = basic(s, t)
    print("Alignment Cost:", result[0])
    print("Aligned s:", result[1])
    print("Aligned t:", result[2])
