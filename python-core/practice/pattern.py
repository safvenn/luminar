#pyramid-----------------------------------------------------------

#
# for i in range(6):
#     for j in range(5-i):
#         print(" ",end=" ")
#     for k in range(2*i-1):
#         print("*",end=' ')
#     print()
# ----------------------------------------------------------------
#         *
#       * * *
#     * * * * *
#   * * * * * * *
# * * * * * * * * *


# sqaure pattern

# for i in range(4):
#     for j in range(4):
#         print("*",end=" ")
#     print()
#-----------------------------------------------------------------------------
#
#
# * * * *
# * * * *
# * * * *
# * * * *

#left triangle

# for i in range(1,5):
#     for j in range(i):
#         print("*",end=" ")
#     print()
#
#     *
#     * *
#     * * *
#     * * * *


#Inverted Left Triangle


# for i in range(4,0,-1):
#     for j in range(i):
#         print("*",end=' ')
#     print()
#
#     * * * *
#     * * *
#     * *
#     *


#Number Triangle

# for i in range(1,6):
#     for j in range(1,i):
#         print(j,end=' ')
#     print()
#--------------------------------------------------------------
# 1
# 1 2
# 1 2 3
# 1 2 3 4
#-------------------------------------------------------------------
#Repeated Number Triangle
# for i in range(1,5):
#      for j in range(i):
#          print(i,end=' ')
#      print()

# 1
# 2 2
# 3 3 3
# 4 4 4 4
#-------------------------------------------
#Alphabet Triangle
# for i in range(1,5):
#      for j in range(i):
#          print(chr(65+j),end=' ')
#      print()
#
# A
# A B
# A B C
# A B C D


#-------------------------------------------------------------
#Continuous Numbers
# n=0
# for i in range(1,5):
#      for j in range(i):
#          n+=1
#          print(n,end=' ')
#      print()
#
# 1
# 2 3
# 4 5 6
# 7 8 9 10

#----------------------------------------------------------------------
#Right Triangle

# for i in range(5):
#     for k in range(4-i):
#         print(" ",end=" ")
#     for j in range(i):
#         print("*",end=" ")
#     print()
#
#       *
#     * *
#   * * *
# * * * *
#----------------------------------------------------------------------------

#Inverted Right Triangle
# for i in range(4,0,-1):
#     for k in range(4-i):
#         print(" ",end=" ")
#     for j in range(i):
#         print("*",end=" ")
#     print()
#
# * * * *
#   * * *
#     * *
#       *
#--------------------------------------------------------------------------------
#Hollow Square
# n=4
# for i in range(n):
#     for j in range(n):
#        if i == 0 or i == n-1 or j == 0 or j == n-1:
#            print("*",end=" ")
#        else:
#            print(" ",end=" ")
#     print()
#
#
# * * * *
# *     *
# *     *
# * * * *


#Hollow Pyramid
#
# for i in range(5):
#     for j in range(4-i):
#         print(" ",end=" ")
#     for k in range(2*i-1):
#         if k == 0 or k == 2*i-2:
#             print("*",end=" ")
#         else:
#             print(" ",end=" ")
#     print()
#     if i == 4:
#         for k in range(2*i-1):
#             print("*",end=" ")
#         print()
#         continue
#
#     print()
#
#       *
#
#     *   *
#
#   *       *
#
# *           *
# * * * * * * *
