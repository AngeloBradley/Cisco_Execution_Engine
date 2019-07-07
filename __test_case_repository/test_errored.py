def response():
    outputFile = open('__test_case_repository/__test_results/test_errored.txt', 'w')
    outputFile.write('exit(Error)')
    outputFile.close()

response()