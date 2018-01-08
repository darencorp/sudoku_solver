import axios from "axios"

export default {
  name: 'app',
  data() {
    return {
      sudoku: [],
      error: false,
      reset: function () {
        this.sudoku.forEach((x, index_x) => {
          x.forEach((i, index_y) => {
            this.$set(this.sudoku[index_x], index_y, null)
            this.error = false;
          })
        })
      },
      random: function () {
        axios.post('/sudoku', {}).then((data) => {
          data.data.forEach(function (x, index_x) {
            x.forEach(function (i, index_y) {
              if (i == 0) {
                data.data[index_x][index_y] = null
              }
            })
          });

          this.sudoku = data.data
          this.error = false
        })
      },
      resolve: function () {
        axios.post('/resolve', this.sudoku).then((data) => {
          if (!data.data) {
            this.error = true
          } else {
            this.sudoku = data.data
            this.error = false
          }
        })
      }
    }
  },
  created: function () {
    axios.post('/sudoku', {}).then((data) => {
      data.data.forEach(function (x, index_x) {
        x.forEach(function (i, index_y) {
          if (i == 0) {
            data.data[index_x][index_y] = null
          }
        })
      });

      this.sudoku = data.data
    })
  }
}
