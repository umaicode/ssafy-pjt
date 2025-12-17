<template>
    <div>
        <h1>금융상품</h1>
        <DepositList />
    </div>
</template>

<script setup>
    import { onMounted } from 'vue';
    import { useProductStore } from '@/stores/products';
    import { RouterLink } from 'vue-router';
    import DepositList from '@/components/DepositList.vue';

    const store = useProductStore()

    onMounted(() => {
        store.getProducts()
    })

</script>

<style scoped>

</style>