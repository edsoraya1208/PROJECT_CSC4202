import os
from flask import Flask, render_template, request
import time

app = Flask(__name__)

# distances and travel_times matrices
distances = [
    [0, 6.7, 20.6, 15.4, 26.9, 27.4, 27.2, 24.3, 25.0, 24.7],
    [6.7, 0, 26.3, 10.2, 27.7, 28.1, 27.3, 25.5, 30.8, 27.3],
    [20.6, 26.3, 0, 28.2, 35.5, 35.9, 37.7, 33.3, 34.2, 37.7],
    [15.4, 10.2, 28.2, 0, 32.0, 32.5, 31.7, 29.9, 32.4, 31.7],
    [26.9, 27.7, 35.5, 32.0, 0, 0.45, 4.0, 7.2, 2.8, 2.4],
    [27.4, 28.1, 35.9, 32.5, 0.45, 0, 3.3, 6.8, 3.5, 3.1],
    [27.2, 27.3, 37.7, 31.7, 4.0, 3.3, 0, 10.7, 1.0, 0.021],
    [24.3, 25.5, 33.3, 29.9, 7.2, 6.8, 10.7, 0, 11.5, 10.9],
    [25.0, 30.8, 34.2, 32.4, 2.8, 3.5, 1.0, 11.5, 0, 2.3],
    [24.7, 27.3, 37.7, 31.7, 2.4, 3.1, 21, 10.9, 2.3, 0]
]

travel_times = [
    [0, 9, 24, 19, 28, 30, 32, 30, 24, 24],
    [9, 0, 27, 15, 29, 31, 31, 29, 31, 31],
    [24, 27, 0, 36, 38, 39, 40, 38, 39, 39],
    [19, 15, 36, 0, 32, 33, 30, 31, 32, 30],
    [28, 29, 38, 32, 0, 1, 8, 11, 7, 6],
    [30, 31, 39, 33, 1, 0, 7, 10, 9, 12],
    [32, 31, 40, 30, 8, 7, 0, 13, 2, 1],
    [30, 29, 38, 31, 11, 10, 13, 0, 12, 12],
    [24, 31, 39, 32, 7, 9, 2, 12, 0, 6],
    [24, 31, 39, 30, 6, 12, 1, 12, 6, 0]
]


def knapsack_activities(activities, budget, time_limit, distance_limit, min_rating):
    n = len(activities)
    budget = int(budget)
    time_limit = int(time_limit * 60)
    distance_limit = int(distance_limit)

    dp = [[(0, []) for _ in range(time_limit + 1)] for _ in range(budget + 1)]

    for i in range(n):
        for b in range(budget, activities[i][5] - 1, -1):
            for t in range(time_limit, activities[i][2] - 1, -1):
                if activities[i][4] >= min_rating:
                    new_rating, new_activities = dp[b - activities[i][5]][t - activities[i][2]]
                    new_rating += activities[i][4]
                    new_activities = new_activities + [activities[i]]

                    if len(new_activities) > 1:
                        prev_activity = new_activities[-2]
                        travel_time = travel_times[prev_activity[0]][activities[i][0]]
                        travel_distance = distances[prev_activity[0]][activities[i][0]]
                        if t >= travel_time and travel_distance <= distance_limit:
                            if new_rating > dp[b][t][0]:
                                dp[b][t] = (new_rating, new_activities)
                    else:
                        if new_rating > dp[b][t][0]:
                            dp[b][t] = (new_rating, new_activities)

    best_rating, best_activities = max((dp[b][t] for b in range(budget + 1) for t in range(time_limit + 1)), key=lambda x: x[0])

    total_cost = sum(activity[5] for activity in best_activities)
    total_time = 0
    total_distance = 0

    for i, activity in enumerate(best_activities):
        if i == 0:
            total_time += activity[2]  # Use duration for the first activity
            total_distance += activity[3]
        else:
            prev_activity = best_activities[i - 1]
            total_time += travel_times[prev_activity[0]][activity[0]]
            total_distance += distances[prev_activity[0]][activity[0]]

    avg_rating = sum(activity[4] for activity in best_activities) / len(best_activities) if best_activities else 0

    return best_activities, avg_rating, total_cost, total_time, total_distance


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        budget = float(request.form['budget'])
        time_limit = float(request.form['time_limit'])
        distance_limit = float(request.form['distance_limit'])
        min_rating = float(request.form['min_rating'])

        activities = [
            (0, "District 21, IOI City Mall", 9, 4.9, 4.2, 60),
            (1, "Taman Saujana Hijau Putrajaya", 12, 9.7, 4.7, 0),
            (2, "Bangi Wonderland", 25, 21.8, 4.1, 55),
            (3, "Taman Tasik Cyberjaya Lake Gardens", 22, 20, 4.5, 30),
            (4, "Berjaya Time Square Theme Park", 26, 24.4, 4.3, 57),
            (5, "Partybox360, Lalaport BBCC", 28, 23.1, 4.9, 38),
            (6, "VAR Live MyTown", 27, 23.2, 4.8, 104),
            (7, "Supreme Bowl, Midvalley", 26, 22.3, 3.4, 60),
            (8, "Xction Xtreme Park, Sunway Velocity", 26, 23.3, 3.5, 65),
            (9, "EnerG X Park, MyTown", 28, 23.3, 4.1, 63)
        ]

        start_time = time.time()
        best_activities, avg_rating, total_cost, total_time, total_distance = knapsack_activities(activities, budget, time_limit, distance_limit, min_rating)
        end_time = time.time()
        runtime = end_time - start_time

        if not best_activities:
            result = "No valid itinerary found. Please adjust your constraints."
        else:
            result = "Optimal Itinerary:\n\n"
            for i, activity in enumerate(best_activities):
                result += f"{activity[1]}\n"
                result += f"Duration: {activity[2]} min, Rating: {activity[4]}, Cost: ${activity[5]}\n"
                if i == 0:
                    result += f"Distance: {activity[3]:.2f} km\n"
                if i > 0:
                    prev_activity = best_activities[i-1]
                    travel_distance = distances[prev_activity[0]][activity[0]]
                    travel_time = travel_times[prev_activity[0]][activity[0]]
                    result += f"Travel from previous: Distance: {travel_distance:.2f} km, Time: {travel_time} min\n"
                result += "\n"

            result += f"\nTotal Cost: ${total_cost:.2f}"
            result += f"\nTotal Travel Time: {total_time} minutes"
            result += f"\nTotal Travelling Distance: {total_distance:.2f} km"
            result += f"\nAverage Rating: {avg_rating:.2f}"
            result += f"\nAlgorithm Runtime: {runtime:.4f} seconds"

        return render_template('result.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)