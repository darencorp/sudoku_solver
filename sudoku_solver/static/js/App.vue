<template>
  <div id="sudoku" class="uk-width-1-1 uk-margin-large-top">
    <div class="title uk-text-large uk-margin-small-right">Sudoku solver</div>
    <div v-if="error"
         class="uk-position-absolute uk-position-top-center uk-margin-xlarge-top uk-margin-right uk-text-danger">Sudoku
      is corrupt
    </div>
    <div class="uk-flex uk-flex-center uk-width-1-1">
      <div class="uk-margin-large-left uk-margin-large-top uk-width-1-3">
        <div v-for="(row, index_x) in sudoku" class="uk-flex uk-margin-large-left">
        <span v-for="(i, index_y) in row" class="uk-flex">
          <div class="cell" :class="{'uk-margin-left': index_y % 3 == 0, 'uk-margin-bottom': (index_x + 1) % 3 == 0}">
            <input v-model.number="sudoku[index_x][index_y]" class="uk-input cell"
                   v-bind:class="{'uk-form-danger': error}"/>
          </div>
        </span>
        </div>
      </div>
      <div class="uk-margin-medium-left uk-margin-large-top">
        <div>
          <button class="uk-button uk-button-default uk-width-1-1 uk-margin-top" v-on:click="reset()">Reset</button>
        </div>
        <div>
          <button class="uk-button uk-button-default uk-width-1-1 uk-margin-top" v-on:click="random()">Random</button>
        </div>
        <div>
          <button class="uk-button uk-button-primary uk-width-1-1 uk-margin-top">
            <div v-if="!pending" v-on:click="resolve()">Resolve</div>
            <div v-else uk-spinner="" class="uk-spinner uk-icon">
              <svg width="30" height="30" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg" ratio="1">
                <circle fill="none" stroke="#000" cx="15" cy="15" r="14"></circle>
              </svg>
            </div>
          </button>
        </div>
        <div>
          <div class="uk-width-1-1 uk-flex uk-margin-top">
            <div v-on:click="changeType('constraint')">
              <input id="constranit" type="radio" name="type" checked/>
              <label for="constranit">Constraint</label>
            </div>
            &nbsp;
            <div v-on:click="changeType('stochastic')">
              <input id="stochastic" type="radio" name="type"/>
              <label for="stochastic">Stochastic</label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script src="./app.js"></script>
<style src="./style.css"></style>
