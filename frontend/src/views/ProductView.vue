<template>
    <div>
        <button @click="active = 'deposits'">예금</button>
        <button @click="active = 'savings'">적금</button>
    </div>
    <ProductList v-if="active === 'deposits'" :items= store.deposits type="deposit"/>
    <ProductList v-else :items= store.savings type="saving"/>

</template>

<script setup>
    import { onMounted, ref } from 'vue';
    import { useProductStore } from '@/stores/products';
    import { RouterLink } from 'vue-router';
    import ProductList from '@/components/ProductList.vue';

    const store = useProductStore()
    const active = ref('deposits')

    onMounted(() => {
        store.getDeposits()
        store.getSavings()
    })

</script>

<style scoped>

</style>