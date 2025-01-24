<template>
  <section>
    <div @click="toggle" class="header">
      <span class="indicator">{{ isOpen ? '▼' : '▲' }}</span>
      <h3>{{ title }}</h3>
    </div>
    <div v-if="isOpen" class="content">
      <slot></slot>
    </div>
  </section>
</template>

<script>
export default {
  name: 'CollapsibleSection',
  props: {
    title: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isOpen: true
    };
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen;
    }
  }
};
</script>

<style scoped>

section {
    background-color: #333;
    border-radius: 10px;
    margin: 0 1rem 1rem 1rem;
}

.header {
  border-radius: 10px 10px 0 0;
  cursor: pointer;
  display: flex;
  justify-content: start;
  padding: 0 2rem;
}

.header:hover {
    background-color: #444;
    cursor: pointer;
}

.content {
  padding: 1rem 2rem;
  overflow-x: auto;
}

.indicator {
    padding: 1.25rem 1rem;
}
</style>