def response():
    outputFile = open('__test_case_repository/__test_results/test_abort.txt', 'w')
    outputFile.write('exit(ABORT)')
    outputFile.close()

response()