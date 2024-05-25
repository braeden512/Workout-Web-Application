from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Exercise
from datetime import datetime
from . import db
import json

views = Blueprint('views', __name__)

@login_required
@views.route('/', methods=['GET', 'POST'])
def home():
    bench_data = []
    bench_labels = []
    inner_count=0
    count=0
    for exercise in current_user.exercises:
        if (current_user.exercises[count].type_of_exercise == 'Benchpress'):
            bench_data.append(current_user.exercises[count].weight / (1.0278 - (0.0278*current_user.exercises[count].reps)))
            bench_labels.append(inner_count+1)
            inner_count=inner_count+1
        count=count+1

    leg_press_data = []
    leg_press_labels = []
    count=0
    inner_count=0
    for exercise in current_user.exercises:
        if (current_user.exercises[count].type_of_exercise == 'Leg Press'):
            leg_press_data.append(current_user.exercises[count].weight / (1.0278 - (0.0278*current_user.exercises[count].reps)))
            leg_press_labels.append(inner_count+1)
            inner_count=inner_count+1
        count=count+1

    deadlift_data = []
    deadlift_labels = []
    count=0
    inner_count=0
    for exercise in current_user.exercises:
        if (current_user.exercises[count].type_of_exercise == 'Deadlift'):
            deadlift_data.append(current_user.exercises[count].weight / (1.0278 - (0.0278*current_user.exercises[count].reps)))
            deadlift_labels.append(inner_count+1)
            inner_count=inner_count+1
        count=count+1

    squat_data = []
    squat_labels = []
    count=0
    inner_count=0

    for exercise in current_user.exercises:
        if (current_user.exercises[count].type_of_exercise == 'Squat'):
            squat_data.append(current_user.exercises[count].weight / (1.0278 - (0.0278*current_user.exercises[count].reps)))
            squat_labels.append(inner_count+1)
            inner_count=inner_count+1
        count=count+1


    if request.method == 'POST':
        if request.form['btn_identifier'] == 'enter_exercise':
            return redirect(url_for('views.createExercise'))
        
        elif request.form['btn_identifier'] == 'filter_exercise':
            if (request.form.get('filter_exercise') == 'Empty'):
                return redirect(url_for('views.home'))
            elif (request.form.get('filter_exercise') == 'Benchpress'):
                return redirect(url_for('views.benchpress'))
            elif (request.form.get('filter_exercise') == 'Leg Press'):
                return redirect(url_for('views.leg_press'))
            elif (request.form.get('filter_exercise') == 'Deadlift'):
                return redirect(url_for('views.deadlift'))
            elif (request.form.get('filter_exercise') == 'Squat'):
                return redirect(url_for('views.squat'))

    return render_template("home.html", user=current_user
                           , bench_data=bench_data
                           , leg_press_data=leg_press_data
                           , deadlift_data=deadlift_data
                           , squat_data=squat_data
                           , labels=max(bench_labels,leg_press_labels,deadlift_labels,squat_labels))

@views.route('/create-exercise', methods=['GET', 'POST'])
@login_required
def createExercise():

    if request.method == 'POST':
        type_of_exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        reps = request.form.get('reps')
        notes = request.form.get('notes')

        date = str(datetime.now().strftime("%x"))
        time = str(datetime.now().strftime("%I")) + ":" + str(datetime.now().strftime("%M")) + " " + str(datetime.now().strftime("%p")) + " " + str(datetime.now().strftime("%Z"))
        onerepmax = round(float(weight)/ (1.0278 - (0.0278*float(reps))))

        new_exercise = Exercise(
            type_of_exercise=type_of_exercise,
            weight=weight, reps=reps,
            text=notes,
            user_id=current_user.id,
            date=date,
            time=time,
            onerepmax= onerepmax
        )

        db.session.add(new_exercise)
        db.session.commit()
        flash('Exercise added!', category='success')
        return redirect(url_for('views.home'))
    
    return render_template("create_exercise.html", user=current_user)
    
@views.route('/delete-exercise', methods=['POST'])
def delete_exercise():
    exercise = json.loads(request.data)
    exerciseId = exercise['exerciseId']
    exercise = Exercise.query.get(exerciseId)
    if exercise:
        if exercise.user_id == current_user.id:
            db.session.delete(exercise)
            db.session.commit()
    
    return jsonify({})

@login_required
@views.route('/benchpress', methods=['GET', 'POST'])
def benchpress():
    bench_data = []
    bench_labels = []
    inner_count=0
    count=0
    for exercise in current_user.exercises:
        if (current_user.exercises[count].type_of_exercise == 'Benchpress'):
            bench_data.append(current_user.exercises[count].weight / (1.0278 - (0.0278*current_user.exercises[count].reps)))
            bench_labels.append(inner_count+1)
            inner_count=inner_count+1
        count=count+1

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'enter_exercise':
            return redirect(url_for('views.createExercise'))
        
        elif request.form['btn_identifier'] == 'filter_exercise':
            if (request.form.get('filter_exercise') == 'Empty'):
                return redirect(url_for('views.home'))
            elif (request.form.get('filter_exercise') == 'Benchpress'):
                return redirect(url_for('views.benchpress'))
            elif (request.form.get('filter_exercise') == 'Leg Press'):
                return redirect(url_for('views.leg_press'))
            elif (request.form.get('filter_exercise') == 'Deadlift'):
                return redirect(url_for('views.deadlift'))
            elif (request.form.get('filter_exercise') == 'Squat'):
                return redirect(url_for('views.squat'))

        return redirect(url_for('views.createExercise'))
    return render_template("benchpress.html"
                           , user=current_user
                           , data=bench_data
                           , labels=bench_labels)

@login_required
@views.route('/leg-press', methods=['GET', 'POST'])
def leg_press():

    leg_press_data = []
    leg_press_labels = []
    count=0
    inner_count=0
    for exercise in current_user.exercises:
        if (current_user.exercises[count].type_of_exercise == 'Leg Press'):
            leg_press_data.append(current_user.exercises[count].weight / (1.0278 - (0.0278*current_user.exercises[count].reps)))
            leg_press_labels.append(inner_count+1)
            inner_count=inner_count+1
        count=count+1

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'enter_exercise':
            return redirect(url_for('views.createExercise'))
        
        elif request.form['btn_identifier'] == 'filter_exercise':
            if (request.form.get('filter_exercise') == 'Empty'):
                return redirect(url_for('views.home'))
            elif (request.form.get('filter_exercise') == 'Benchpress'):
                return redirect(url_for('views.benchpress'))
            elif (request.form.get('filter_exercise') == 'Leg Press'):
                return redirect(url_for('views.leg_press'))
            elif (request.form.get('filter_exercise') == 'Deadlift'):
                return redirect(url_for('views.deadlift'))
            elif (request.form.get('filter_exercise') == 'Squat'):
                return redirect(url_for('views.squat'))

        return redirect(url_for('views.createExercise'))

    return render_template("leg_press.html", user=current_user
                           , data=leg_press_data
                           , labels=leg_press_labels)

@login_required
@views.route('/deadlift', methods=['GET', 'POST'])
def deadlift():

    deadlift_data = []
    deadlift_labels = []
    count=0
    inner_count=0
    for exercise in current_user.exercises:
        if (current_user.exercises[count].type_of_exercise == 'Deadlift'):
            deadlift_data.append(current_user.exercises[count].weight / (1.0278 - (0.0278*current_user.exercises[count].reps)))
            deadlift_labels.append(inner_count+1)
            inner_count=inner_count+1
        count=count+1

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'enter_exercise':
            return redirect(url_for('views.createExercise'))
        
        elif request.form['btn_identifier'] == 'filter_exercise':
            if (request.form.get('filter_exercise') == 'Empty'):
                return redirect(url_for('views.home'))
            elif (request.form.get('filter_exercise') == 'Benchpress'):
                return redirect(url_for('views.benchpress'))
            elif (request.form.get('filter_exercise') == 'Leg Press'):
                return redirect(url_for('views.leg_press'))
            elif (request.form.get('filter_exercise') == 'Deadlift'):
                return redirect(url_for('views.deadlift'))
            elif (request.form.get('filter_exercise') == 'Squat'):
                return redirect(url_for('views.squat'))

        return redirect(url_for('views.createExercise'))

    return render_template("deadlift.html", user=current_user
                           , data=deadlift_data
                           , labels=deadlift_labels)

@login_required
@views.route('/squat', methods=['GET', 'POST'])
def squat():

    squat_data = []
    squat_labels = []
    count=0
    inner_count=0
    for exercise in current_user.exercises:
        if (current_user.exercises[count].type_of_exercise == 'Squat'):
            squat_data.append(current_user.exercises[count].weight / (1.0278 - (0.0278*current_user.exercises[count].reps)))
            squat_labels.append(inner_count+1)
            inner_count=inner_count+1
        count=count+1

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'enter_exercise':
            return redirect(url_for('views.createExercise'))
        
        elif request.form['btn_identifier'] == 'filter_exercise':
            if (request.form.get('filter_exercise') == 'Empty'):
                return redirect(url_for('views.home'))
            elif (request.form.get('filter_exercise') == 'Benchpress'):
                return redirect(url_for('views.benchpress'))
            elif (request.form.get('filter_exercise') == 'Leg Press'):
                return redirect(url_for('views.leg_press'))
            elif (request.form.get('filter_exercise') == 'Deadlift'):
                return redirect(url_for('views.deadlift'))
            elif (request.form.get('filter_exercise') == 'Squat'):
                return redirect(url_for('views.squat'))

        return redirect(url_for('views.createExercise'))

    return render_template("squat.html", user=current_user
                           , data=squat_data
                           , labels=squat_labels)