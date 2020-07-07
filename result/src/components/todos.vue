<template>
  <div class="container">
    <div class="col-sm-10">
      <h1>Задачи</h1>
      <h2>Всего задач {{existingTodos}}, выполнено задач {{doneTodos}}</h2>
      <confirmation
        :message="message"
        :variant="variant"
        :showAlert="showAlert"
        @dismissedAlert="updateAlert">
      </confirmation>
      <button type="button"
        id="task-add"
        class="btn btn-success btn-sm align-left d-block"
        v-b-modal.modals
        @click="addTodo()">
        Добавить задачу
      </button>

      <table  v-if="existingTodos" class="table table-dark table-stripped table-hover">
        <thead class="thead-light">
          <tr>
            <th>Uid</th>
            <th>Описание</th>
            <th>Выполнена?</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="[index, todo] of todos.entries()" :key="index">
            <td class="todo-uid">{{ index + 1}}</td>
            <td>{{ todo.description }}</td>
            <td>
              <span v-if="todo.is_completed">Выполнено</span>
              <span v-else>Не выполнено</span>
            </td>
            <td>
              <div class="btn-group" role="group">
                <button type="button"
                  class="btn btn-secondary btn-sm"
                  v-b-modal.modals
                  @click="updateTodo(index, todo)">
                  Обновить
                </button>
                &nbsp;
                <button type="button"
                  class="btn btn-danger btn-sm"
                  @click="deleteTodo(index, todo)">
                  X
                  </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <h3 v-else>
        Похоже, что у вас пока нет дел
      </h3>
    </div>
    <modalss id="modals" ref="modalwindow"
      @addUpdateTask="receiveFromModal($event)"
      @addMessage="alertFromModal($event)"
      :todo="addUpdateTodoForm">
    </modalss>
  </div>
</template>

<style>
button#task-add {
  margin-top: 20px;
  margin-bottom: 20px;
}
h1, td {
  text-align: left;
}
.todo-uid {
  text-align: right;
}
</style>

<script>
import axios from 'axios';
import Confirmation from './confirmation.vue';
import Modalss from './modalss.vue';

const todoListURL = 'http://localhost:5000/api/tasks/';
let storage = 1;

export default {
  name: 'Todo',
  data() {
    return {
      todos: [],
      addUpdateTodoForm: {
        uid: 0,
        description: '',
        is_completed: 0,
      },
      oldDataforDB: {
        description: '',
        is_completed: 0,
      },
      showAlert: true,
      message: 'соединение с сервером',
      variant: 'info',
    };
  },
  components: {
    confirmation: Confirmation,
    modalss: Modalss,
  },
  methods: {
    // не показывать алерт
    updateAlert() {
      this.showAlert = false;
    },
    // подгружаем задачи из локал стораж
    getTodos() {
      try {
        const localTodos = JSON.parse(localStorage.getItem('todos'));
        if (localTodos) {
          this.todos = localTodos.map((x) => ({
            description: x.description, is_completed: x.is_completed * 1,
          }));
        }
      } catch {
        this.showAlert = true;
        this.message = 'Что-то пошло не так при загрузке дел';
      }
    },
    // записываем задачи в локал стораж
    setTodos() {
      localStorage.setItem('todos', JSON.stringify(this.todos));
    },
    // добавить задачу, инициализация формы
    addTodo() {
      this.addUpdateTodoForm.uid = null;
      this.addUpdateTodoForm.description = '';
      this.addUpdateTodoForm.is_completed = 0;
    },
    // изменение текущей задачи
    updateTodo(index, todo) {
      this.addUpdateTodoForm.is_completed = 0;
      this.addUpdateTodoForm.uid = index;
      this.addUpdateTodoForm.description = todo.description;
      if (todo.is_completed) {
        this.addUpdateTodoForm.is_completed = 1;
      }
      if (!storage) {
        // запись в бд, если используем бэкэнд
        this.oldDataforDB = todo;
      }
    },
    // удалияем задачу
    deleteTodo(index, todo) {
      this.todos.splice(index, 1);
      if (storage) {
        this.setTodos();
        this.getTodos();
      } else {
        // удаляем из базы
        const todoURL = `${todoListURL}desc=${todo.description}&iscompl=${todo.is_completed}`;
        axios.delete(todoURL);
      }
      this.showAlert = true;
      this.message = `Задача "${todo.description}" удалена из списка`;
    },
    // принимаем данные с формы и записываем либо в бд либо в локал
    receiveFromModal(eventdata) {
      this.variant = 'success';
      const data = {
        description: eventdata.description,
        is_completed: eventdata.is_completed,
      };
      if (eventdata.uid == null) {
        this.todos.push(data);
        if (!storage) {
          axios.post(todoListURL, data);
        }
      } else {
        this.todos[eventdata.uid] = data;
        if (!storage) {
          const todoURL = `${todoListURL}descold=${this.oldDataforDB.description}&iscomplold=${this.oldDataforDB.is_completed}&desc=${data.description}&iscompl=${data.is_completed}`;
          axios.put(todoURL);
        }
      }
      if (storage) {
        this.setTodos();
        this.getTodos();
      }
    },
    // сообщение о результате работы с формы
    alertFromModal(eventmessage) {
      this.showAlert = true;
      this.message = eventmessage;
    },
  },
  // первоначальная инициализация задач, стучимся в бэкэнд, если не вышло, то берем с локал
  created() {
    axios.get(todoListURL)
      .then((response) => {
        if (response.data) {
          this.todos.push(...response.data);
        }
        storage = 0;
        this.variant = 'success';
        this.showAlert = true;
        this.message = 'работаем с базой';
      }).catch(() => {
        this.variant = 'warning';
        this.showAlert = true;
        this.message = 'Соедидение не установлено, работаем с localStorage';
      }).finally(() => {
        if (storage) {
          this.getTodos();
        }
      });
  },
  // вычисляем, сколько всего и выполненных задач
  computed: {
    existingTodos() {
      return this.todos.length;
    },
    doneTodos() {
      return this.todos.filter((x) => x.is_completed).length;
    },
  },
};
</script>
