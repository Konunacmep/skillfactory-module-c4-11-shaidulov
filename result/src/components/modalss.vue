<template>
    <b-modal ref="addUpdateTodoModal"
      id="modals"
      :title="taskTitle"
      hide-footer
      show>
      <b-form  @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-description-group"
          label="Описание:"
          label-for="form-description-input">
          <b-form-input id="form-description-input"
            type="text"
            v-model="todoForm.description"
            required
            :placeholder="taskPlaceholder">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-complete-group">
          <b-form-checkbox
            v-model="todoForm.is_completed"
            value="1"
            unchecked-value="0">
            Задача выполнена?
          </b-form-checkbox>
        </b-form-group>
        <b-button type="submit" variant="primary">Добавить</b-button>
        <b-button type="reset" variant="danger">Сброс</b-button>
      </b-form>
    </b-modal>
</template>

<script>
export default {
  name: 'modals',
  props: {
    todo: {
      uid: Number,
      description: String,
      is_completed: Number,
    },
  },
  data() {
    return {
      taskPlaceholder: 'Новая задача',
      taskTitle: 'Создать задачу',
      todoForm: this.todo,
    };
  },
  methods: {
    // обнуляем форму
    resetForm() {
      this.description = '';
      this.is_completed = 0;
    },
    // посылаем данные с формы
    onSubmit(event) {
      event.preventDefault();
      this.$refs.addUpdateTodoModal.hide();
      const newTask = {
        uid: this.todoForm.uid,
        description: this.todoForm.description,
        is_completed: this.todoForm.is_completed * 1,
      };
      this.$emit('addUpdateTask', newTask);
      this.$emit('addMessage', `Задача "${newTask.description}" ${newTask.uid === null ? 'добавлена' : 'обновлена'}`);
      this.resetForm();
    },
    // если нажали сброс
    onReset(event) {
      event.preventDefault();
      this.$refs.addUpdateTodoModal.hide();
      this.resetForm();
    },
  },
};
</script>
