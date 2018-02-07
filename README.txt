Change data_type in algorithm to numpy ndarray. 90% of manipulating data is numpy.
That give better performance over than 75%. For example: averege time of resolving the hardest sudoku with using pyhton array ~ 85s when with numpy.ndarray that time reduces under 19.5s on my PC. In webapp that time may be longer. For the best performance run fucntion resolver.resolve() in console.

Clone this repository and then:

- npm run inst
- npm start
