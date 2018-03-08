import axios from "axios"

export default {
  name: 'app',
  data() {
    return {
      sudoku: [],
      error: false,
      pending: false,
      type: 'constraint',
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
        this.pending = true
        axios.post('/resolve', {'sudoku': this.sudoku, 'type': this.type}).then((data) => {
          if (!data.data) {
            this.error = true
          } else {
            this.sudoku = data.data
            this.error = false
          }

          this.pending = false
        })
      },
      changeType: function (type) {
        this.type = type
        console.log(this.type)
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
