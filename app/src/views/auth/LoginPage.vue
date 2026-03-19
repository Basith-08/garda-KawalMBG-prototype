<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { z } from 'zod'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const rememberMe = ref(true)
const error = ref('')

const loginSchema = z.object({
  email: z.string().email('Email tidak valid'),
  password: z.string().min(1, 'Password harus diisi'),
})

async function handleLogin() {
  error.value = ''
  const result = loginSchema.safeParse({ email: email.value, password: password.value })
  if (!result.success) {
    error.value = result.error.issues[0].message
    return
  }

  const success = await authStore.login(email.value, password.value)
  if (success) {
    if (authStore.user?.role === 'regulator') {
      router.push('/regulator/dashboard')
    } else {
      router.push('/vendor/dashboard')
    }
  } else {
    error.value = 'Email harus mengandung "vendor" atau "regulator"'
  }
}
</script>

<template>
  <div class="min-h-screen bg-navy-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg border border-navy-200 p-6 sm:p-10 animate-fade-in">
      <h1 class="text-2xl font-bold text-navy-900 text-center mb-2">Login to Account</h1>
      <p class="text-navy-500 text-sm text-center mb-8">Please enter your email and password to continue</p>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-navy-700 mb-2">Email address:</label>
          <input
            v-model="email"
            type="email"
            placeholder="example@gmail.com"
            class="w-full px-4 py-3 bg-navy-50 rounded-lg border border-navy-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent focus:border-transparent"
          />
        </div>

        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="text-sm font-medium text-navy-700">Password</label>
            <a href="#" class="text-sm text-navy-500 hover:text-brand-accent">Forget Password?</a>
          </div>
          <input
            v-model="password"
            type="password"
            placeholder="••••••"
            class="w-full px-4 py-3 bg-navy-50 rounded-lg border border-navy-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent focus:border-transparent"
          />
        </div>

        <label class="flex items-center gap-2 cursor-pointer">
          <input v-model="rememberMe" type="checkbox" class="w-4 h-4 rounded border-navy-300 text-brand-accent" />
          <span class="text-sm text-navy-600">Remember Password</span>
        </label>

        <p v-if="error" class="text-sm text-brand-danger">{{ error }}</p>

        <button
          type="submit"
          class="w-full py-3.5 bg-brand-accent hover:bg-brand-accent-hover text-white font-semibold rounded-lg transition-colors shadow-md"
        >
          Sign In
        </button>

        <p class="text-center text-sm text-navy-500">
          Don't have an account?
          <a href="#" class="text-brand-accent hover:underline font-medium">Create Account</a>
        </p>
      </form>

      <div class="mt-6 p-3 bg-blue-50 rounded-lg text-xs text-navy-600">
        <strong>Hint:</strong> Gunakan email dengan kata "regulator" (misal: regulator@test.com) untuk masuk sebagai Regulator, atau "vendor" (misal: vendor@test.com) untuk Vendor. Password bebas.
      </div>
    </div>
  </div>
</template>
