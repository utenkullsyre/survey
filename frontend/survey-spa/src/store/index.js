// src/store/index.js

import Vue from 'vue';
import Vuex from 'vuex';

import { fetchSurveys, fetchSurvey } from '@/api';

Vue.use(Vuex);

const state = {
  // single source of data
  surveys: [],
  currentSurvey: {}
}

const actions = {
  // asynchronous operations
  loadSurveys(context) {
    return fetchSurveys()
      .then((response) => context.commit('setSurveys', { surveys: response }
    ));
  },

  loadSurvey(context, { id }) {
    return fetchSurvey(id)
      .then((response) => context.commit('setSurvey', { survey: response }))
  }
};

const mutations = {
  // isolated data mutations
  setSurveys(state, payload) {
    state.surveys = payload.surveys;
  },

  setSurvey(state, payload) {
    state.currentSurvey = payload.survey
    // const nQuestions = payload.survey.questions.length
    // for (let i = 0; i < nQuestions; i++) {
    //   payload.survey.questions[i].choice = null
    // }
    // state.currentSurvey = payload.survey
  }
}

const getters = {
  // reusable data accessors
}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
});

export default store;
