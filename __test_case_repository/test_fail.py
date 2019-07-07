def response():
    outputFile = open('__test_case_repository/__test_results/test_fail.txt', 'w')
    outputFile.write('exit(FAIL)')
    outputFile.close()

response()

