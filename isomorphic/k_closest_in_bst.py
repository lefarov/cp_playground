#          4
#      2      5
#   1    3

# if len(queue) < k:
#   always append
# if len(queue) == k:
#   if abs(query - current) > abs(query - queue.head()):
#       pop head
#       append current
#   else:
#       return result
# [1, 2, 3]
#  *     *