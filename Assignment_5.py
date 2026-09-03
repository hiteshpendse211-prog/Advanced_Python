result = []

while i > 0 and j > 0:

        if sequence1[i - 1] == sequence2[j - 1]:

            result.append(sequence1[i - 1])
            i -= 1
            j -= 1

        elif dp[i - 1][j] > dp[i][j - 1]:

            i -= 1

        else:

            j -= 1

    # Reverse the result
    result.reverse()

    return lcs_length, ''.join(result)


# Main Program

sequence1 = input("Enter first sequence: ")
sequence2 = input("Enter second sequence: ")

length, subsequence = lcs(sequence1, sequence2)

print("\nLongest Common Subsequence:", subsequence)
print("Length of LCS:", length)