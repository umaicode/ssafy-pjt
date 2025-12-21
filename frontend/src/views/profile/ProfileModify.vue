<template>
  <div>
    <section class="card">
      <h4>닉네임 변경</h4>
      <form @submit.prevent="onUpdateNickname">
        <input v-model.trim="newNickname" placeholder="새 닉네임" />
        <button type="submit" :disabled="!newNickname">저장</button>
      </form>
    </section>

    <section class="card">
      <h4>비밀번호 변경</h4>
      <form @submit.prevent="onChangePassword">
        <input v-model="oldPassword" type="password" placeholder="현재 비밀번호" />
        <input v-model="newPassword1" type="password" placeholder="새 비밀번호" />
        <input v-model="newPassword2" type="password" placeholder="새 비밀번호 확인" />
        <button type="submit" :disabled="!canSubmitPw">변경</button>
      </form>
      <p class="hint">변경 후 보안을 위해 다시 로그인하게 됩니다.</p>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

const newNickname = ref('')

const oldPassword = ref('')
const newPassword1 = ref('')
const newPassword2 = ref('')

// 비밀번호 입력 완료 여부
const canSubmitPw = computed(() => {
  return oldPassword.value && newPassword1.value && newPassword2.value
})

// 닉네임 변경
const onUpdateNickname = () => {
  accountStore.updateNickname(newNickname.value)
    .then(() => {
      newNickname.value = '' // 입력값 초기화
    })
    .catch(() => {
      // updateNickname 내부에서 alert 처리 중이므로 여기선 생략 가능
    })
}

// 비밀번호 변경
const onChangePassword = () => {
  if (newPassword1.value !== newPassword2.value) {
    alert('새 비밀번호가 서로 일치하지 않습니다.')
    return
  }

  accountStore.changePassword({
    old_password: oldPassword.value,
    new_password1: newPassword1.value,
    new_password2: newPassword2.value,
  })
  .then(() => {
    // changePassword 내부에서 로그아웃 + 이동 처리
  })
  .catch(() => {
    // 에러 메시지도 store에서 처리 중
  })
}
</script>

<style scoped>
.card {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 16px;
  margin: 12px 0;
}
form {
  display: grid;
  gap: 10px;
  max-width: 360px;
}
input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
}
button {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #333;
  background: #fff;
  cursor: pointer;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.hint {
  color: #777;
  margin-top: 8px;
}
</style>
