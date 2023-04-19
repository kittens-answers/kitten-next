// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    head: {bodyAttrs: {class : 'bg-gray-800'}},
    css: ['~/assets/css/main.css'],
    postcss: {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        },
    },
})
