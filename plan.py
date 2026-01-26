# objective of this model:
# takes students previous_marks ,exam_scores as inputs and group the class into high achievers ,mediocre achievers and low scorers
# so K=3
# features=2


# model1: groups students into persona
# model2:groups students into high,medium or low achievers
# model3:helps you predict how much he will score ,so you can simulate future

# so what are the options on our dashboard
# analyse the whole class:
    # upload the table containing 20 attributes about each student in the class
    # model2 runs : groups students into categories
        # we are able to say things like 60% of the class is in mediocre range (there is something more to consider here)
        # 30% of the class is struggling for grades
        # you can compare the results of two courses (i will explain)
    # you can understand who are the students in a particular marks range by passing the records of those students to model1
        # you are able to say things like:
        # 80% of your low scorers belong to low resource category---> so this implies the problem is not with effort its with the lack of resources--->targeted help--->provide more notes
    # upload just 19 columns and you get predictions on how much each student will score
        # this prediction+the 19 columns passed to model2 and you know how much your class is gonna struggle
# analyse one student
    # if we pass record of 1 student to model1 you get to know how good or bad he is in compared to the entire class
    # if you pass the record to model2 you can get which persona they are in
    # model 3 gives you how much he is predicted to score (risk detection and preventive help)
     