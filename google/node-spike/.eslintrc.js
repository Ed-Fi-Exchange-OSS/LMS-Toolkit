module.exports = {
  parser: '@typescript-eslint/parser',
  'extends': [
    'airbnb-base',
    'prettier',
    'prettier/@typescript-eslint'
  ],
  plugins: ['@typescript-eslint', 'prettier'],
  settings: {
    'import/resolver': {
      node: {
        extensions: ['.mjs', '.js', '.json', '.ts'],
      },
    },
    'import/extensions': ['.js', '.mjs', '.jsx', '.ts', '.tsx'],
  },
  rules: {
    // TODO: setting no-unused-vars to off for now -- eslint-plugin-typescript 1.0.0-rc.2 is plagued with problems with this rule
    'no-unused-vars': 'off',
    'typescript/no-unused-vars': 'off',

    // originally required in the early days of monorepos -- consider revisiting
    'import/no-cycle': 'off',

    // prettier is handling this
    'max-len': 'off',

    // our loop iterations are rarely independent, and it's a more readable syntax
    'no-await-in-loop': 'off',

    // we almost never do default exports
    'import/prefer-default-export': 'off',

    // artifact of the Flow days, imports were indeed duplicated because types had to be separate
    'import/no-duplicates': 'off',

    // relax this to avoid unnecessary temp variables
    'no-param-reassign': [
      2,
      {
        props: false,
      },
    ],

    // prettier issues are warnings here
    'prettier/prettier': 'warn',
  },
};
