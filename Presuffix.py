import re

def prefix_suffix(url):
    pattern = "-"
    m = re.search(pattern, url)
    if m:
        return 1
    else:
        return -1


"""def main():
    url1 = "www.test-test.com"
    url2 = "www.test.com"
    x = prefix_suffix(url1)
    z = prefix_suffix(url2)

    print(x)
    print(z)


if __name__ == "__main__":
    main()"""