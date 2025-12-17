<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="signUp">
      <label for="username">아이디 : </label>
      <input type="text" id="username" v-model.trim="username" /> <br>
      
      <label for="nickname">닉네임 : </label>
      <input type="text" id="nickname" v-model.trim="nickname" /> <br>
      
      <label for="password1">비밀번호 : </label>
      <input type="password" id="password1" v-model.trim="password1" /> <br>
      
      <label for="password2">비밀번호 확인 : </label>
      <input type="password" id="password2" v-model.trim="password2" /> <br>

      <input type="submit" value="회원가입">
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
  import { useAccountStore } from '@/stores/accounts';

  const username = ref(null)
  const nickname = ref(null)
  const password1 = ref(null)
  const password2 = ref(null)

  const accountStore = useAccountStore()

  const signUp = function () {
    const payload = {
      username: username.value,
      nickname: nickname.value,
      password1: password1.value,
      password2: password2.value,
    }
    
    accountStore.signUp(payload)
  }

</script>

<style scoped>

</style>