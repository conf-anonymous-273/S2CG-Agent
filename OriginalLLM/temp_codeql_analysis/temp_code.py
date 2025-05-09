def count_upper(s):
    vowels = {'A', 'E', 'I', 'O', 'U'}
    count = 0
    for i, char in enumerate(s):
        if i % 2 == 0 and char.isupper() and char in vowels:
            count += 1
    return count