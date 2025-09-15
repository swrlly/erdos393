from typing import List, Any

def partition_list(items: List[Any]) -> List[List[Any]]:
    """
    Returns list of all possible partitions of an arbitrary list.
    Each partition is a list of sublists.
    
    Args:
        items (List[Any]): List of arbitrary items, can be numbers, strings, etc. Repeats allowed.
    
    Returns:
        all_partitions (List[List[Any]]): List of all possible partitions.  

    Examples: 

    >>> partition_list([])
    [[]]

    >>> partition_list([1, 1, "e", -3]) 
    [[1], [1], ['e'], [-3]]
    [[1, 1], ['e'], [-3]]
    [[1], [1, 'e'], [-3]]
    [[1], ['e'], [1, -3]]
    [[1], [1, 'e'], [-3]]
    [[1, 1, 'e'], [-3]]
    [[1, 'e'], [1, -3]]
    [[1], ['e'], [1, -3]]
    [[1, 'e'], [1, -3]]
    [['e'], [1, 1, -3]]
    [[1], [1], ['e', -3]]
    [[1, 1], ['e', -3]]
    [[1], [1, 'e', -3]]
    [[1], [1, 'e', -3]]
    [[1, 1, 'e', -3]]

    >>> partition_list([1, [2], {0: -1}])
    [[1], [[2]], [{0: -1}]]
    [[1, [2]], [{0: -1}]]
    [[[2]], [1, {0: -1}]]
    [[1], [[2], {0: -1}]]
    [[1, [2], {0: -1}]]
    """
    # base cases
    if not items:
        return [[]]
    if len(items) == 1:
        return [[[items[0]]]]
    
    # use first item to add/not add
    first_item = items[0]
    rest_items = items[1:]
    
    # get partitions without first_item
    rest_partitions = partition_list(rest_items)
    
    all_partitions = []
    
    # now add first_item to all possibilities
    for partition in rest_partitions:
        # case 1: put first_item in its own new group
        new_partition = [[first_item]] + partition
        all_partitions.append(new_partition)
        
        # case 2: add first_item to each existing group in the partition
        for i in range(len(partition) - 1):
            # create a new group. put in [[], []] form
            added = [[first_item] + partition[i]]
            # every slice of partition is of form [[]]
            all_partitions.append(partition[:i] + added + partition[i+1:])

        # account for last group in partition
        added = [[first_item] + partition[-1]]
        all_partitions.append(partition[:len(partition)-1] + added)

    return all_partitions

def partition_list_generator(items: List[Any]) -> List[List[Any]]:
    """
    Generator version of `partition_list`.
    Use this method to generate partitions on the fly without saving into memory. Useful for lists of length greater than 14.
    Each partition is a list of sublists.

    Caveat: If `items = []`, generator will yield none.
    
    Args:
        items (List[Any]): List of arbitrary items, can be numbers, strings, etc. Repeats allowed.
    
    yields:
        List[Any]: One partition of `items`

    Examples:
    >>> for i in partition_list_generator([2,3,4]): print(i)
    [[2], [3], [4]]
    [[2, 3], [4]]
    [[3], [2, 4]]
    [[2], [3, 4]]
    [[2, 3, 4]]

    >>> for i in partition_list_generator([1,2,2,"e"]): print(i)
    [[1], [2], [2], ['e']]
    [[1, 2], [2], ['e']]
    [[2], [1, 2], ['e']]
    [[2], [2], [1, 'e']]
    [[1], [2, 2], ['e']]
    [[1, 2, 2], ['e']]
    [[2, 2], [1, 'e']]
    [[1], [2], [2, 'e']]
    [[1, 2], [2, 'e']]
    [[2], [1, 2, 'e']]
    [[1], [2], [2, 'e']]
    [[1, 2], [2, 'e']]
    [[2], [1, 2, 'e']]
    [[1], [2, 2, 'e']]
    [[1, 2, 2, 'e']]
    """
    
    if items == []:
        # StopIteration condition
        return [[]]
    if len(items) == 1:
        yield [[items[0]]]
    
    # use first item to add/not add
    first_item = items[0]
    rest_items = items[1:]

    # now iterate over the generator. add first_item over all possibilities
    for partition in partition_list_generator(rest_items):

        # case 1: put first_item in its own new group
        new_partition = [[first_item]] + partition
        yield new_partition

        # case 2: add first_item to each existing group in the partition
        for i in range(len(partition) - 1):
            # create a new group. put in [[], []] form
            added = [[first_item] + partition[i]]
            # every slice of partition is of form [[]]
            yield partition[:i] + added + partition[i + 1:]

        # account for last group in partition
        added = [[first_item] + partition[-1]]
        yield partition[:len(partition) - 1] + added