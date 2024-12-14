def test_and_run(func, testfile, expected_test_result, inputfile, test_parameters=(), main_paramenters=()):
    test_result = func(testfile, *test_parameters)
    if test_result != expected_test_result:
        print(
            f"Result doesn't match test, expected: {expected_test_result}, actual {test_result}"
        )
    else:
        print("Test OK")
        print("Result:", func(inputfile, *main_paramenters))
