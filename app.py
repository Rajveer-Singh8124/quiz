from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


def load_questions(file_path):
    return pd.read_excel(file_path)

def check_answers(selected_options, correct_answers):
    score = 0
    for i, selected in enumerate(selected_options):
        if selected == correct_answers[i]:
            score += 1
    percentage = (score / len(correct_answers)) * 100

    if percentage == 100:
        feedback = "Excellent! You got all the answers correct!"
    elif 80 <= percentage < 100:
        feedback = "Great job! You have a strong understanding of thermodynamics."
    elif 50 <= percentage < 80:
        feedback = "Good effort! You may want to review some concepts to improve."
    else:
        feedback = "Keep practicing! With more study, you can improve your score."

    return score, feedback

file_path = 'thermodynamics_quiz.xlsx'
questions_df = load_questions(file_path)

@app.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        selected_options = []
        for i in range(len(questions_df)):
            selected_options.append(request.form.get(f'question_{i}'))

        correct_answers = questions_df['Answer'].tolist()
        score, feedback = check_answers(selected_options, correct_answers)
        return render_template('result.html', score=score, total=len(questions_df), feedback=feedback)

    return render_template('quiz.html', questions=questions_df)

if __name__ == '__main__':
    app.run(debug=True)
