def test(func, testfile, expected_test_result, test_parameters=()):
    test_result = func(testfile, *test_parameters)
    if test_result != expected_test_result:
        print(
            f"Result doesn't match test, expected: {expected_test_result}, actual {test_result}"
        )
        return False
    print("Test OK")
    return True
    

def test_and_run(func, testfile, expected_test_result, inputfile, test_parameters=(), main_paramenters=()):
    if test(func, testfile, expected_test_result, test_parameters):

        print("Result:", func(inputfile, *main_paramenters))
