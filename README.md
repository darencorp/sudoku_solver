# Sudoku solver

App is used 'Stochastic search / optimization methods' algorithm. Changed data_type in algorithm to numpy ndarray. 90% of manipulating data is numpy.


That give better performance over than 87%. For example: average time of resolving the hardest sudoku with using pyhton array ~ 85s when with numpy.ndarray that time reduces under 11.3s on my PC. In webapp that time may be longer. For the best performance run fucntion resolver.resolve() in console.

Screen of main page:

![alt text](https://i.pinimg.com/originals/f5/53/e9/f553e906f58863f069ad8015f816f4e8.png)

Clone this repository and then:

- npm run inst
- npm start
