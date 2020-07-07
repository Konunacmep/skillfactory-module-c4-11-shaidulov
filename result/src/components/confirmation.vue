<template>
  <div>
    <b-alert
      :variant="variant"
      dismissible
      :show="showAlert"
      @dismissed="dismEmit">
      {{ message }}
    </b-alert>
  </div>
</template>

<script>
export default {
  props: ['message', 'variant', 'showAlert'],
  methods: {
    // сообщение, что алерт закрыт
    dismEmit() {
      this.$emit('dismissedAlert');
    },
  },
};
</script>
