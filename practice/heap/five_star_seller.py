from heapq import heappush, heappop, heapify


class Rating:

    def __init__(self, num_five_stars, num_total):
        self.num_five_stars = num_five_stars
        self.num_total = num_total

        self.current_rating = num_five_stars / num_total
        self.potential_improvement = (
            (num_five_stars + 1) / (num_total + 1) 
            - self.current_rating
        )

    def __lt__(self, other):
        return self.potential_improvement > other.potential_improvement


class Solution:

    def fiveStarReviews(self, productRatings, ratingsThreshold):
        ratings_heap = []
        ratings_sum = 0
        ratings_len = 0
        for rating in productRatings:
            rating_obj = Rating(*rating)
            ratings_heap.append(rating_obj)
            ratings_sum += rating_obj.current_rating
            ratings_len += 1

        # ratings_heap = [Rating(*rating) for rating in productRatings]
        # ratings_sum = sum(map(lambda prod: prod.current_rating, ratings_heap))
        # ratings_len = len(ratings_heap)

        heapify(ratings_heap)
        result = 0
        while ratings_sum / ratings_len < ratingsThreshold / 100:
            best_prod = heappop(ratings_heap)
            ratings_sum -= best_prod.current_rating

            best_prod = Rating(best_prod.num_five_stars + 1, best_prod.num_total + 1)
            ratings_sum += best_prod.current_rating
            heappush(ratings_heap, best_prod)
            
            result += 1
        
        return result


if __name__ == "__main__":
    solution = Solution()
    print(solution.fiveStarReviews([[4,4], [1,2], [3, 6]], 77))