import globals from 'globals';
import prettier from 'eslint-plugin-prettier';

export default [
	{ ignores: ['dist'] },
	{
		files: ['**/*.{js,jsx}'],
		languageOptions: {
			ecmaVersion: 2020,
			globals: globals.browser,
			parserOptions: {
				ecmaVersion: 'latest',
				ecmaFeatures: { jsx: true },
				sourceType: 'module'
			}
		},
		plugins: {
			prettier
		},
		rules: {
			
			'prettier/prettier': [
				'error',
				{
					useTabs: true,
					tabWidth: 2,
					singleQuote: false,
					semi: true,
					trailingComma: 'none',
					printWidth: 160
				}
			]
		}
	}
];