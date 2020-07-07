import Vue from 'vue';
import Router from 'vue-router';
import todos from '../components/todos.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    { path: '/', redirect: '/todos' },
    {
      path: '/todos',
      name: 'todos',
      component: todos,
    },
  ],
});
