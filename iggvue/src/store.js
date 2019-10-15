import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import VueAxios from 'vue-axios';

Vue.use(VueAxios, axios);
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    games: [],
    gameDetails: {},
    recentActivity: [],
    RecentActivityLoading: false,
  },
  mutations: {
    fetchGames(state) {
      axios.get('http://127.0.0.1:8000/games')
        .then((response) => {
          state.games = response.data;
        });
    },
    getDetails(state, payload) {
      state.RecentActivityLoading = true;
      axios.get(encodeURI(`http://127.0.0.1:8000${payload.data.href}`))
        .then((response) => {
          state.gameDetails[payload.data.href] = response.data;
        })
        .finally(() => {
          state.RecentActivityLoading = false;
        });
    },
    fetchActivity(state) {
      state.RecentActivityLoading = true;
      axios.get('http://127.0.0.1:8000/recent')
        .then((response) => {
          state.recentActivity = response.data;
        })
        .finally(() => {
          state.RecentActivityLoading = false;
        });
    },
  },
  actions: {
    fetchGames(context) {
      context.commit('fetchGames');
    },
    getDetails(context, data) {
      context.commit('getDetails', { data });
    },
    fetchActivity(context) {
      context.commit('fetchActivity');
    },
  },
});
