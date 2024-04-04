class Solution():
    def is_valid(self, array: list[int], side_length: int) -> bool:
        inversion = self.count_inversion(array, side_length)
        row_of_blank = side_length - array.index(side_length ** 2) // side_length

        if side_length % 2 == 1 and inversion % 2 == 0:
            return True
        if side_length % 2 == 0:
            if row_of_blank % 2 == 0 and inversion % 2 == 1:
                return True
            if row_of_blank % 2 == 1 and inversion % 2 == 0:
                return True
        return False     

    def count_inversion(self, array, side_length):
        result = 0
        len_array = len(array)
        for i in range(len_array - 1):
            for j in range(i + 1, len_array):
                if array[i] == side_length ** 2 or \
                array[j] == side_length ** 2:
                    continue
                if array[i] > array[j]:
                    result += 1
        return result

def main():
    array = [3,9,1,15,14,11,4,6,13,16,10,12,2,7,8,5]
    side_length = 4
    solution = Solution()

    ans = solution.is_valid(array, side_length)
    print(ans)

if __name__ == "__main__":
    main()