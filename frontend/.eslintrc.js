module.exports= {
    parser: '@typescript-eslint/parser',
    extends: [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:react-hooks/recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:prettier/recommended',
        'plugin:jsx-a11y/recommended'
    ],
    plugins: [
        'react',
        'react-hooks',
        'jsx-a11y',
        'prettier',
        '@typescript-eslint'
    ],
    settings: {
        react: {
            version: 'detect'
        }
    },
    rules: {
        'react/react-in-jsx-scope': 'off',
        'prettier/prettier': 'warn'
    }
}