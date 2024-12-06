def test_and_run(func, testfile, expected_test_result, inputfile):
    test_result = func(testfile)
    if test_result != expected_test_result:
        print(
            f"Result doesn't match test, expected: {expected_test_result}, actual {test_result}"
        )
    else:
        print("Test OK")
        print("Result:", func(inputfile))
