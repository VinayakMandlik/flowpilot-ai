class ConfidenceService:

    @staticmethod
    def calculate(results):

        if not results:
            return 0.0

        scores = [point.score for point in results]

        average = sum(scores) / len(scores)

        if len(scores) >= 3:
            average *= 1.05

        return min(round(average, 3), 1.0)