old_list1 = [1, 2, 3, 4]
new_list1 = old_list1

print('Old List 1:', old_list1)
print('New List 1:', new_list1)

print('First item of New List 1 is changed to 9999');
new_list1[0] = 9999
print('The changes done to new_list1 is reflected in old_list1 => because new_list1 is the shallow copy of old_list1')
print('Old List 1:', old_list1)
print('New List 1:', new_list1)

old_list2 = [1, 2, 3, 4]
new_list2 = old_list2[:]

print('First item of New List 2 is changed to 9999');
new_list2[0] = 9999
print('The changes done to new_list2 is NOT reflected in old_list2 => because new_list2 is the deep copy of old_list2')
print('Old List 2:', old_list2)
print('New List 2:', new_list2)