import time
from generate_partitions import partition_list, partition_list_generator

def test_partition(std_out):
    std_out("Starting test for in-memory partition creator.")
    start = time.time()
    # Test 5 items. Bell number 5, 52
    test = [1, -1, 2, 2, 3]
    p = partition_list(test)
    assert len(p) == 52
    std_out("Passed test for 5 items.")
    # Test 9 items. Bell number 9, 21147
    test = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    p = partition_list(test)
    assert len(p) == 21147
    std_out("Passed test for 9 items.")
    # Test 12 items. Bell number 12, 4213597
    test = [1,1,1,1,2,2,2,2,3,3,3,3]
    p = partition_list(test)
    assert len(p) == 4213597
    std_out("Passed test for 12 items.")
    end = time.time()
    std_out(f"Tests passed (non-generator): {round(end - start, 5)} seconds")

def test_partition_generator(std_out):
    std_out("Starting test for generator partition creator.")
    start = time.time()
    # Test 5 items. Bell number 5, 52
    test = [1, -1, 2, 2, 3]
    ctr = 0
    for _ in partition_list_generator(test): ctr += 1
    assert ctr == 52
    std_out("Passed test for 5 items.")
    # Test 9 items. Bell number 9, 21147
    test = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    ctr = 0
    for _ in partition_list_generator(test): ctr += 1
    assert ctr == 21147
    std_out("Passed test for 9 items.")
    # Test 12 items. Bell number 12, 4213597
    test = [1,1,1,1,2,2,2,2,3,3,3,3]
    ctr = 0
    for _ in partition_list_generator(test): ctr += 1
    assert ctr == 4213597
    std_out("Passed test for 12 items.")
    end = time.time()
    std_out(f"Tests passed (generator): {round(end - start, 5)} seconds")

def test_equality_of_generators(std_out):
    """
    Test if non-generator method vs. generator method return the same partitions, in order.
    """
    std_out("Starting equality test of non-generator vs. generator.")
    test = [1,"hello world",1,1,2,2,2,2,3,3,3,3]
    non_generated = partition_list(test)
    generated = []
    for i in partition_list_generator(test):
        generated.append(i)

    std_out("Testing equality of number of partitions.")
    assert len(non_generated) == len(generated)

    std_out("Testing equality of each partition.")
    for i in zip(non_generated, generated):
        assert i[0] == i[1]
    std_out("Equality of individual partitions passed.")
    
def final_test(std_out):
    """
    Method to test partition non-generator method vs. generator
    """
    std_out("Starting tests.")
    test_partition(std_out)
    test_partition_generator(std_out)
    test_equality_of_generators(std_out)
    std_out("Tests passed.")

def main():
    final_test(print)

if __name__ == "__main__":
    main()