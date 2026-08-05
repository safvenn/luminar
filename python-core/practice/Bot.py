# 🟡 Subarray Sum Equals K (Difficulty: Medium | Category: Sliding Window / Hashing)
#
# Problem:
# Given an array of integers nums and an integer k, return the total number of continuous subarrays whose sum equals to k.
#
# Input:
# A list of integers nums and an integer k.
#
# Output:
# An integer representing the count of subarrays that sum to k.
#
# Constraints:
# - 1 <= nums.length <= 2 * 10^4
# - -1000 <= nums[i] <= 1000
# - -10^7 <= k <= 10^7
#
# Example:
# Input: nums = [1, 1, 1], k = 2
# Output: 2
#
# Input: nums = [1, 2, 3], k = 3
# Output: 2
#
#
# This message was sent automatically with n8n


def subarraySum(nums, k):
    count = 0
    current_sum = 0
    # Map to store prefix_sum: frequency
    prefix_sums = {0: 1}

    for num in nums:
        current_sum += num

        # Check if (current_sum - k) exists in map
        diff = current_sum - k
        if diff in prefix_sums:
            count += prefix_sums[diff]

        # Add current_sum to map or update its count
        prefix_sums[current_sum] = prefix_sums.get(current_sum, 0) + 1

    return count
