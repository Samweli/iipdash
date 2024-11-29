module.exports = {
    env: {
        browser: true,
        es2021: true,
    },
    extends: [
        'standard',
        'plugin:prettier/recommended',
        'plugin:vue/essential',
    ],
    parserOptions: {
        ecmaVersion: 15,
        sourceType: 'module',
    },
    plugins: ['vue'],
    rules: {
        'prettier/prettier': 'error',
        'no-console': 'warn',
    },
};
