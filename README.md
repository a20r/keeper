Keeper
======

Using nonlinear regression methods for position prediction of moving objects

## About
Keeper is a library that uses model selection and curve fitting to help predict the movement of objects in space. Imagine a goal keeper tending the net. If a ball is kicked towards him, he is able to predict the position of the ball as it gets closer to him (i.e. as time since the kick increases). This is the ability we are trying to insert into this project. However, we are not only looking at cases in which the model of movement is predetermined, but we are trying to allow our system to learn the model to use given the incoming data.

## How it works
Keeper works by breaking the main regression problem (i.e. *x, y, z*) into three different regression problems, making the functions easier to interpolate. This is done by converting these cartesian coordinates into parametric coordinates indexed by time. This means that we are able to have separate regressions for each dimension. However, this does not factor into how the system is to be used. There is a function in the predictor called `push` which when given a new point, the system will automatically reduce the dimension. Also when predicting a new point, all that is needed is the time that you would like to prediction to be.

Programmatically, how Keeper works is observed data about a tracked object is reported to Keeper in real-time. Keeper then uses this data (in real-time) to create models of the movement for the tracked object. This is shown in the tests by a simulated ball being dropped from 100 meters and keeper has show that it is able to continuously predict the position of the ball. As time increases, the size of the training set increases and therefore the error rate decreases.

## Use case
Keeper is designed to work in real-time for mobile robotics. We are adding functionality to combine the Kinect with Keeper such that given a classifier, the Kinect will be able to track and report the observed positions of a tracked object to Keeper. This will allow keeper to learn and interpolate movement of the tracked object. Keeper will then be able to inform a planning algorithm about the future positions of objects in the environment allowing the algorithm to plan ahead and account for the movements of obstacles, other robots, etc.

## To Run

### Install

    sudo pip install -r requirements.txt

However if this does not work (since I have not tested it yet), please read through the requirements file and install things yourself. It shouldn't be too hard.

### Tests

	python tests/unittest_runner.py

This command will run my unit tests. A `matplotlib` window will appear, but it (for some freaking reason) does not feel like being the top window. So you are going to have to click on the damn icon in your start bar.

What the tests show are a series of functions that are being interpolated by this system. Meaning that there is nothing more than perceived data being entered into the predictor, and it is able to select a model and make predictions on the objects position based on the model.