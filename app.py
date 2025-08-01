from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def load_quiz_data():
    with open("quiz.json", "r") as f:
        return json.load(f)

def save_results(result):
    results_file = "results.json"
    data = []
    if os.path.exists(results_file):
        try:
            with open(results_file, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    data.append(result)
    with open(results_file, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def quiz():
    quiz_data = load_quiz_data()
    if request.method == "POST":
        user_answers = request.form
        score = 0
        wrong_questions = []

        for i, question in enumerate(quiz_data):
            key = f"q{i}"
            user_answer = user_answers.get(key)
            if user_answer == question["answer"]:
                score += 1
            else:
                wrong_questions.append({
                    "question": question["question"],
                    "your_answer": user_answer,
                    "correct_answer": question["answer"]
                })

        result = {
            "score": score,
            "total": len(quiz_data),
            "wrong_questions": wrong_questions
        }
        save_results(result)

        return render_template("quiz.html", quiz_data=quiz_data, submitted=True, score=score, wrong=wrong_questions)

    return render_template("quiz.html", quiz_data=quiz_data, submitted=False)

if __name__ == "__main__":
    app.run(debug=True)
