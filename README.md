# Sudoku solver

## Info

The app is using 'Stochastic search / optimization methods' algorithm. Arrays are defined using numpy.ndarray for greater perfomance.

This gives better performance over than 87%. For example: average time of resolving the hardest sudoku with using pyhton array ~ 85s when with numpy.ndarray that time reduces under 11.3s on my PC. In webapp that time may be longer. For the best performance run fucntion resolver.resolve() in console.

03.08.18 Update: Implement the Constraint programming algorithm. This has reduced the time of resolving any sudoku to a few milliseconds. The app is using *python_constraint* library.

## Resolving

![alt text](https://i.pinimg.com/originals/ab/e2/13/abe213d8b7136bdc148129a792b813ce.gif)

## Install

Clone this repository and then:

- npm run install
- npm start